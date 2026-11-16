"""Separate native geometry/photo phases to review geometry before appearance work."""
import os,sys,json,time
from pathlib import Path
B=Path('/workspace/revisit');sys.path[:0]=[str(B/'mosca'),str(B)]
os.environ.setdefault('GS_BACKEND','native_add3')
import torch,numpy as np
from PIL import Image,ImageDraw
from omegaconf import OmegaConf
from mosca_reconstruct import static_reconstruct,photometric_warmup,scaffold_reconstruct,photometric_reconstruct,setup_recon_ws
from lib_moca.camera import MonocularCameras
from lib_prior.prior_loading import Saved2D
from lib_moca.bundle import prepare_track_homo_dep_rgb_buffers,get_world_points

def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
from sparse_inspect import inspect

def capture_initialization(**kw):
 from ba_depth_validity import guard
 cams=kw['cams'];saved=kw['s2d'];case=os.environ['MOSCA_CASE'];g=guard()
 bank=np.load(B/'input'/case/'observed-static-tracks.npz');tracks=torch.from_numpy(bank['tracks']).to(saved.dep.device);valid=torch.from_numpy(bank['valid']).to(saved.dep.device)
 assert tracks.ndim==3 and tracks.shape[0]==saved.T and tracks.shape[2]==2 and valid.shape==tracks.shape[:2]
 kw.update(s_track=tracks,s_track_valid_mask=valid)
 # Only background BA inputs change. The cached BootsTAPIR banks remain intact.
 assert g.config['cases'][case]['baselinePolicy']=='freeze all-target camera-facing fractions before optimization'
 assert 'initialPerTargetFrontFractions' not in g.config['cases'][case]
 with torch.no_grad():
  homo,depth,_=prepare_track_homo_dep_rgb_buffers(saved,tracks,valid,torch.arange(saved.T,device='cuda'))
  world=get_world_points(homo,depth,cams);poses=cams.forward_T() if cams.delta_flag else torch.stack([cams.T_wc(i) for i in range(saved.T)]);R=poses[:,:3,:3];t=poses[:,:3,3]
  z=torch.einsum('tj,snj->stn',R[:,:,2],world)-(R[:,:,2]*t).sum(-1)[None,:,None]
  raw=valid[:,None]&valid[None];good=torch.isfinite(z)&(z>.001)&(depth[:,None]>.001)&(depth[None]>.001);baseline=((raw&good).sum((0,2))/raw.sum((0,2)).clamp_min(1)).cpu().tolist()
  mean=torch.where(valid[...,None],world,0).sum(0)/valid.sum(0).clamp_min(1)[:,None]
  cp=torch.einsum('tji,tnj->tni',R,mean[None]-t[:,None])
  usable=(valid&(cp[...,2]>.001)).sum(1)
  assert int(usable.min())>=64, 'Native initial mean-anchor coverage failed'
  write(B/f'results/{case}-initial-coverage.json',{'minimumUsableAnchors':int(usable.min()),'perFrame':usable.cpu().tolist(),'passed':True})
  g.config['cases'][case]['initialPerTargetFrontFractions']=baseline
  g.mask(z,depth[:,None],depth[None],raw,raw.float(),torch.arange(saved.T,device='cuda'),0)
  write(B/f'results/{case}-initial-support.json',{**g.pending,'baselinePolicy':g.config['cases'][case]['baselinePolicy'],'optimizationHasStarted':False})
  np.savez_compressed(B/f'results/{case}-initialization.npz',cameraToWorld=poses.cpu().numpy(),K=cams.K().cpu().numpy(),tracks=tracks.cpu().numpy(),valid=valid.cpu().numpy(),depth=depth.cpu().numpy(),world=world.cpu().numpy())
 return original_ba(**kw)

def main():
 global original_ba
 stage,case=sys.argv[1:];assert stage=='geometry';ws=B/'input'/case;cfg=OmegaConf.load(ws/'fit.yaml');package=json.loads((ws/'camera-package.json').read_text());expected=torch.tensor(package['cameraToWorld'],dtype=torch.float32)
 cams=MonocularCameras(n_time_steps=len(expected),default_H=360,default_W=640,fxfycxcy=[package['nativeFovDegrees']]*2+package['nativePrincipalPointRatio'],delta_flag=False,init_camera_pose=expected,iso_focal=True).cuda()
 for p in cams.parameters():p.requires_grad_(False)
 before={k:v.detach().clone() for k,v in cams.state_dict().items()};actual=torch.stack([cams.T_wc(i) for i in range(len(expected))]);K=torch.tensor(package['K'],device='cuda',dtype=torch.float32)
 assert torch.allclose(actual,expected.cuda(),rtol=0,atol=1e-5) and torch.allclose(cams.K(),K,rtol=0,atol=1e-4)
 # Native projection/backprojection and supplied pose convention control.
 homo=torch.tensor([[.1,.2],[-.2,.1]],device='cuda');depth=torch.tensor([1.2,2.1],device='cuda');xyz=cams.backproject(homo,depth);assert torch.allclose(cams.project(xyz),homo,atol=1e-6)
 write(B/'output/camera-lock-smoke.json',{'nativeCameraPackagePassed':True,'fixedAllParameters':all(not p.requires_grad for p in cams.parameters()),'frames':len(expected),'maximumPoseConversionDifference':float((actual-expected.cuda()).abs().max()),'maximumIntrinsicConversionDifference':float((cams.K()-K).abs().max()),'projectionRoundtripPassed':True})
 log=Path(setup_recon_ws(str(ws),fit_cfg=cfg));write(ws/'geometry-location.json',{'log':str(log)})
 static_namespace=static_reconstruct.__globals__;solve=static_namespace['moca_solve'];namespace=solve.__globals__;original_ba=namespace['compute_static_ba'];namespace['compute_static_ba']=capture_initialization
 def supplied_solve(**kw):
  assert kw['gt_cam'] is None
  kw.update(gt_cam=cams,ba_lr_cam_q=0.,ba_lr_cam_t=0.,ba_lr_cam_f=0.,rescale_gt_cam_transl=False)
  return solve(**kw)
 static_namespace['moca_solve']=supplied_solve
 try:
  static_reconstruct(str(ws),str(log),cfg)
  result=inspect(ws,log,cfg,True);result['scope']='All configured observations, supplied static-map cameras locked; observed background tracks; native depth BA only; no motion scaffold or appearance';write(B/f'results/{case}-geometry-report.json',result)
  assert result['numericGatePassed']
 finally:
  differences={k:float((v-before[k]).abs().max()) if v.is_floating_point() else int(not torch.equal(v,before[k])) for k,v in cams.state_dict().items()};unchanged=all(torch.equal(v,before[k]) for k,v in cams.state_dict().items());write(B/f'results/{case}-camera-invariance.json',{'allCameraStateExactlyUnchanged':unchanged,'differences':differences,'allParametersStillFrozen':all(not p.requires_grad for p in cams.parameters()),'cameraLockOnly':True});assert unchanged,'A supplied fixed camera changed during BA'
if __name__=='__main__':main()
