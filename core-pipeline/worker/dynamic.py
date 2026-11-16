"""Resume qualified geometry; lock every camera load and carry dense correction."""
from pathlib import Path
import os,sys,json,time
B=Path('/workspace/revisit');sys.path[:0]=[str(B/'mosca'),str(B)];os.environ.setdefault('GS_BACKEND','native_add3')
import numpy as np,torch
from PIL import Image,ImageDraw
from omegaconf import OmegaConf
from mosca_reconstruct import scaffold_reconstruct,photometric_reconstruct,photometric_warmup
from lib_moca.camera import MonocularCameras
from lib_prior.prior_loading import Saved2D
from lib_moca.bundle import prepare_track_homo_dep_rgb_buffers,get_world_points
from pytorch3d.ops import knn_points

def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n')

def main():
    torch.set_num_threads(4);stage,case=sys.argv[1:];ws=B/'input'/case;log=Path(json.loads((ws/'geometry-location.json').read_text())['log']);cfg=OmegaConf.load(ws/'fit.yaml');exploratory=False;config=json.loads((ws/'config.json').read_text());N=len(json.loads((B/'input/manifest.json').read_text())[case]['frames']);wanted=np.linspace(0,N-1,6).round().astype(int).tolist()
    reference=torch.load(log/'bundle/bundle_cams.pth',map_location='cpu');loaded=[];depth_calls=[]
    original_load=MonocularCameras.load_from_ckpt
    def locked_load(cls,state):
        assert all(torch.equal(state[k].cpu(),v.cpu()) for k,v in reference.items()),'Camera checkpoint differs from frozen reference'
        cams=original_load(state)
        for param in cams.parameters():param.requires_grad_(False)
        # Native photo code hardcodes nonzero camera rates: exclude optimizer groups.
        cams.get_optimizable_list=lambda **kw:[]
        loaded.append(cams);return cams
    MonocularCameras.load_from_ckpt=classmethod(locked_load)
    original_rescale=Saved2D.rescale_perframe_depth_from_bundle
    def corrected_depth(saved,bundle_pth_fn=None):
        original_rescale(saved,bundle_pth_fn)
        deltas=np.stack([np.load(ws/'background-corrections'/(name+'.npz'))['correction'] for name in saved.frame_names])
        saved.dep=saved.dep+torch.from_numpy(deltas).to(saved.dep)
        assert torch.isfinite(saved.dep).all() and bool((saved.dep[saved.dep_mask]>.001).all())
        saved.recompute_dep_mask(depth_boundary_th=float(cfg.depth_boundary_th))
        depth_calls.append({'frames':len(deltas),'minimumDepth':float(saved.dep.min()),'positiveValidDepth':True,'maximumAbsoluteCorrection':float(np.abs(deltas).max())})
        return saved
    Saved2D.rescale_perframe_depth_from_bundle=corrected_depth
    # Ensure camera optimizer learning rates are zero as well as excluding groups.
    solver=photometric_reconstruct.__globals__['DynReconstructionSolver'];original_fit=solver.photometric_fit
    @torch.no_grad()
    def anchored_foreground(self,saved,cams,viz_fname=None):
        data=torch.load(log/'bundle/bundle.pth');track=data['s_track'].to(saved.dep.device);mask=data['s_track_mask'].to(saved.dep.device)
        homo,depth,_=prepare_track_homo_dep_rgb_buffers(saved,track,mask,torch.arange(saved.T,device=saved.dep.device))
        world=get_world_points(homo,depth,cams);use=mask&(depth>.001);mean=torch.where(use[...,None],world,0).sum(0)/use.sum(0).clamp_min(1)[:,None]
        scf=torch.load(log/'mosca/mosca.pth');xyz=scf['_node_xyz'].to(saved.dep.device);certain=scf['_node_certain'].to(saved.dep.device).bool();masks=[];rows=[]
        sheet=Image.new('RGB',(1920,780),'#18212a');draw=ImageDraw.Draw(sheet);wanted=np.linspace(0,saved.T-1,6).round().astype(int).tolist()
        for i in range(saved.T):
            moving=xyz[i,certain[i]];anchors=torch.cat([mean,moving]);query=cams.trans_pts_to_world(i,cams.backproject(cams.get_homo_coordinate_map(),saved.dep[i]))
            _,idx,_=knn_points(query.reshape(1,-1,3),anchors[None],K=1);fg=(idx[0,:,0]>=len(mean)).reshape(saved.H,saved.W)&saved.dep_mask[i]
            raw_fraction=float(fg.float().mean())
            visitor=torch.from_numpy(np.asarray(Image.open(ws/'visitor-masks'/(saved.frame_names[i]+'.png'))).copy()==0).to(fg.device)
            fg=fg&visitor
            fraction=float(fg.float().mean());assert fraction<.6,'Foreground covers most of room; stop before fitting'
            rows.append({'frame':i,'foregroundFraction':fraction,'unclippedForegroundFraction':raw_fraction,'visibleScaffoldNodes':int(certain[i].sum())});masks.append(fg)
            if i in wanted:
                rgb=(saved.rgb[i].cpu().numpy()*255).astype(np.uint8);overlay=(rgb.astype(float)*.25).astype(np.uint8);overlay[fg.cpu().numpy()]=rgb[fg.cpu().numpy()];im=Image.fromarray(overlay);col=wanted.index(i);x=640*(col%3);y=390*(col//3);sheet.paste(im,(x,y+30));draw.text((x+4,y+5),f'Frame{i} / foreground {fraction:.1%} / fixed map + visible motion nodes',fill='white')
        fg=torch.stack(masks);saved.register_2d_identification(static_2d_mask=~fg,dynamic_2d_mask=fg)
        sheet.save(B/f'results/{case}-foreground-review.jpg');write(B/f'results/{case}-foreground-report.json',{'method':'Nearest qualified mean background anchor versus currently visible fitted scaffold nodes, intersected with existing visitor-box support; original static Boots means excluded. Detector boxes are not segmentation ground truth.','rows':rows,'maximumForegroundFraction':max(r['foregroundFraction'] for r in rows),'maximumUnclippedForegroundFraction':max(r['unclippedForegroundFraction'] for r in rows),'qualityPromotion':False})
        return fg
    solver.identify_fg_mask_by_nearest_curve=anchored_foreground
    def locked_fit(self,**kw):
        cams=kw['cams'];assert all(not p.requires_grad for p in cams.parameters())
        for key in ['lr_cam_q','lr_cam_t','lr_cam_f','lr_cam_q_final','lr_cam_t_final','lr_cam_f_final']:
            setattr(kw['optimizer_cfg'],key,0.)
        assert not cams.get_optimizable_list(lr_q=1.,lr_t=1.,lr_f=1.)
        if stage=='foreground':raise ForegroundReady()
        assert json.loads((ws/'foreground-reviewed.json').read_text())['gatePassed']
        return original_fit(self,**kw)
    class ForegroundReady(Exception):pass
    solver.photometric_fit=locked_fit
    try:
        if stage=='geometry':
            photometric_warmup(str(ws),str(log),cfg)
            namespace=scaffold_reconstruct.__globals__;curves=namespace['get_dynamic_curves']
            def checked_curves(s2d,cams,**kw):
                result=curves(s2d,cams,**kw);xyz,mask,rgb,selection=result;tids=kw['t_list'];uv=s2d.track[:,s2d.dynamic_track_mask][:,selection][tids,:,:2]
                assert len(xyz)==N and xyz.shape[1]>=32 and torch.isfinite(xyz).all()
                counts=mask.sum(1)
                times=np.array([r['eventSeconds'] for r in json.loads((B/'input/manifest.json').read_text())[case]['frames']]);required=np.zeros(N,bool)
                for a,b in config['motionRequiredSeconds']:required|=(times>=a)&(times<b)
                assert required.any()
                required_minimum=int(counts[torch.from_numpy(required).to(counts.device)].min())
                sheet=Image.new('RGB',(1920,780),'#18212a');draw=ImageDraw.Draw(sheet);wanted=np.linspace(0,N-1,6).round().astype(int).tolist()
                for col,i in enumerate(wanted):
                    im=Image.open(sorted((ws/'images').glob('*'))[i]).convert('RGB');d=ImageDraw.Draw(im)
                    for j in torch.where(mask[i])[0].cpu().tolist():
                        x,y=uv[i,j].cpu().tolist();d.ellipse((x-2,y-2,x+2,y+2),fill='#5ce8a3')
                    x=640*(col%3);y=390*(col//3);sheet.paste(im,(x,y+30));draw.text((x+4,y+5),f'Frame{i} / {int(counts[i])} retained dynamic observations',fill='white')
                sheet.save(B/f'results/{case}-motion-review.jpg')
                write(B/f'results/{case}-motion-input.json',{'retainedCurves':int(xyz.shape[1]),'minimumVisibleCurves':int(counts.min()),'perFrameVisible':counts.cpu().tolist(),'numericPassed':True,'originalBootsBanks':True,'originalFullMotionCoveragePassed':int(counts.min())>=8,'requiredMotionCoveragePassed':required_minimum>=8,'requiredMinimumVisibleCurves':required_minimum,'requiredMotionFrames':np.where(required)[0].tolist(),'requiredRangesDeclaredBeforeFit':config['motionRequiredSeconds'],'exploratoryDespiteSparseMotion':exploratory,'qualityPromotion':False})
                assert required_minimum>=8,'Insufficient support in predeclared visible-actor interval'
                return result
            namespace['get_dynamic_curves']=checked_curves
            scaffold_reconstruct(str(ws),str(log),cfg)
            scf=torch.load(log/'mosca/mosca.pth',map_location='cpu');nodes=int(scf['_node_xyz'].shape[1]);assert nodes>=32 and all(torch.isfinite(v).all() for v in scf.values() if torch.is_tensor(v) and v.is_floating_point())
            write(B/f'results/{case}-motion-report.json',{'numericGatePassed':True,'frames':N,'retainedScaffoldNodes':nodes,'motionSupport':json.loads((B/f'results/{case}-motion-input.json').read_text()),'staticBundleReused':True,'noCameraBa':True,'qualityPromotion':False})
        elif stage in ['foreground','photo']:
            assert json.loads((ws/'geometry-reviewed.json').read_text())['gatePassed']
            try:photometric_reconstruct(str(ws),str(log),cfg)
            except ForegroundReady:
                assert stage=='foreground';return
            fitted=torch.load(log/'photometric_cam.pth',map_location='cpu');assert all(torch.equal(fitted[k],v) for k,v in reference.items()),'Saved photo cameras moved'
        else:raise ValueError(stage)
    finally:
        checks=[all(torch.equal(c.state_dict()[k].cpu(),v.cpu()) for k,v in reference.items()) and all(not p.requires_grad for p in c.parameters()) for c in loaded]
        result={'stage':stage,'cameraLoads':len(loaded),'allCameraStateExactlyUnchanged':bool(checks and all(checks)),'allCameraOptimizersDisabled':True,'denseDepthApplications':depth_calls}
        write(B/f'results/{case}-{stage}-camera-invariance.json',result);assert result['allCameraStateExactlyUnchanged']

if __name__=='__main__':main()
