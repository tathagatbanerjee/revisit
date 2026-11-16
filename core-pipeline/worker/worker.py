"""Fresh fixed-camera static control; no reuse of fitted scene inputs."""
from pathlib import Path
import os,sys,json,time,faulthandler,signal
faulthandler.enable()
faulthandler.register(signal.SIGUSR1,all_threads=True)
B=Path('/workspace/revisit');sys.path[:0]=[str(B/'mosca'),str(B),str(B/'input/support')]
os.environ.setdefault('GS_BACKEND','native_add3')
from patch_source import patch
patch()
import numpy as np,torch
from omegaconf import OmegaConf
from lib_prior.prior_loading import Saved2D
from lib_moca.camera import MonocularCameras
from scipy.spatial import cKDTree
from camera_contract import build_contract

def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')

def track(case):
    import hashlib
    import mosca_precompute as pre
    ws=B/'input'/case;cfg=OmegaConf.load(ws/'prep.yaml')
    paths=sorted((ws/'metric3d_depth').glob('*.npz'))+sorted((ws/'flow_raft').glob('*.npz'))+sorted((ws/'epi').rglob('*'))
    paths=[p for p in paths if p.is_file()]
    before={str(p.relative_to(ws)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert len(list((ws/'metric3d_depth').glob('*.npz')))==len(list((ws/'images').glob('*.png'))) and len(list((ws/'flow_raft').glob('*.npz')))==2*(len(list((ws/'images').glob('*.png')))-1)
    epi=list((ws/'epi/error').glob('*.npy'));assert len(epi)==len(list((ws/'images').glob('*.png'))) and all(np.isfinite(np.load(p)).all() for p in epi)
    assert not list(ws.glob('*_tap.npz'))
    processor=pre.get_moca_processor(cfg);images,names=pre.load_imgs_from_dir(str(ws));pre.seed_everything(int(cfg.seed));depth=processor.load_dep_list(str(ws),'metric3d_depth')
    processor.compute_tap(ws=str(ws),save_name='uniform_dep=metric3d',n_track=int(cfg.n_track_uniform),img_list=images,mask_list=np.ones_like(depth)>0,dep_list=depth,K=None,chunk_size=int(cfg.tap_chunk_size))
    same=all(hashlib.sha256((ws/p).read_bytes()).hexdigest()==h for p,h in before.items())
    write(B/f'results/{case}-resume-input-verification.json',dict(savedArrayFiles=len(before),allSavedDepthFlowEpiArraysUnchanged=same,hashes=before));assert same

def bundle(case):
    ws=B/'input'/case;cfg=OmegaConf.load(ws/'fit.yaml')
    saved=Saved2D(str(ws)).load_dep('metric3d_depth',float(cfg.depth_boundary_th)).normalize_depth(float(cfg.dep_median)).recompute_dep_mask(depth_boundary_th=float(cfg.depth_boundary_th)).to('cuda')
    bank=np.load(ws/'map-tracks.npz');tracks=bank['tracks'];valid=bank['valid'].copy();xyz=bank['mapWorld']
    package=json.loads((ws/'map-cameras.json').read_text());poses=np.array([np.vstack([r['cameraToWorld'],[0,0,0,1]]) for r in package['poses']]);ratios=[]
    for i in range(len(poses)):
        uv=np.rint(tracks[i]).astype(int);uv[:,0]=uv[:,0].clip(0,639);uv[:,1]=uv[:,1].clip(0,359)
        valid[i]&=saved.dep_mask[i,uv[:,1],uv[:,0]].cpu().numpy()
        z=((xyz-poses[i,:3,3])@poses[i,:3,:3])[:,2]
        use=valid[i]&(z>.001);dep=saved.dep[i,uv[use,1],uv[use,0]].cpu().numpy();ratios.append(float(np.median(dep/z[use])))
    assert valid.sum(1).min()>=64
    scale=float(np.median(ratios));rows=json.loads((B/'input/manifest.json').read_text())[case]['frames']
    contract=build_contract(rows,package['poses'],package['K'],scale);contract['normalizedRawDepthMedian']=1/float(saved.scale_nw)
    write(ws/'camera-package.json',contract)
    np.savez_compressed(ws/'observed-static-tracks.npz',tracks=tracks,valid=valid)
    del saved;torch.cuda.empty_cache()
    import anchor_geometry
    sys.argv=['anchor_geometry.py','geometry',case];anchor_geometry.main()
    report=json.loads((B/f'results/{case}-geometry-report.json').read_text());med=np.array([r['medianPx'] for r in report['staticReprojection']]);counts=np.array([r['observations'] for r in report['staticReprojection']]);bins=[float(np.median(x)) for x in np.array_split(med,5)]
    gate=dict(median=float(np.median(med)),worst=float(med.max()),binMedians=bins,minAnchors=int(counts.min()),passed=bool(np.median(med)<=5 and med.max()<=20 and max(bins)<=8 and counts.min()>=64))
    write(B/f'results/{case}-background-gate.json',gate);assert gate['passed'],gate

@torch.no_grad()
def dense(case):
    from lib_moca.bundle import prepare_track_homo_dep_rgb_buffers,get_world_points
    ws=B/'input'/case;cfg=OmegaConf.load(ws/'fit.yaml');log=Path(json.loads((ws/'geometry-location.json').read_text())['log']);b=torch.load(log/'bundle/bundle.pth',map_location='cpu')
    if not bool(torch.count_nonzero(b['dep_correction'])):
        # Interpolating an identically zero field cannot change a pixel. Check
        # dense positivity directly and avoid loading RGB or building KNN trees.
        package=json.loads((ws/'camera-package.json').read_text());out=ws/'background-corrections';out.mkdir();minimum=float('inf')
        for i in range(len(b['dep_scale'])):
            raw=np.load(ws/'metric3d_depth'/f'{i:05d}.npz')['dep'].astype(np.float32)
            dep=raw.clip(.001,1000)*np.float32(1/package['normalizedRawDepthMedian'])*float(b['dep_scale'][i])
            assert np.isfinite(dep).all() and (dep>.001).all()
            minimum=min(minimum,float(dep.min()));np.savez_compressed(out/f'{i:05d}.npz',correction=np.zeros_like(dep))
        gate=json.loads((B/f'results/{case}-background-gate.json').read_text())
        gate.update(frames=len(b['dep_scale']),minimumDenseDepth=minimum,allDensePixelsPositive=True,localCorrectionsExactlyZero=True,method='Exact zero-field shortcut; same native scaled depths, no RGB reload or RBF calculation')
        write(B/f'results/{case}-dense-gate.json',gate);assert gate['passed'];return
    saved=Saved2D(str(ws)).load_dep('metric3d_depth',float(cfg.depth_boundary_th)).normalize_depth(float(cfg.dep_median)).recompute_dep_mask(depth_boundary_th=float(cfg.depth_boundary_th))
    cams=MonocularCameras.load_from_ckpt(torch.load(log/'bundle/bundle_cams.pth',map_location='cpu'))
    rays=cams.backproject(cams.get_homo_coordinate_map(),torch.ones((saved.H,saved.W))).detach().numpy()
    valid=b['s_track_mask'].bool();tracks=b['s_track'];scale=b['dep_scale'].detach().numpy();corr=b['dep_correction'].detach().numpy()
    out=ws/'background-corrections';out.mkdir();rows=[];sampled=[]
    for i in range(saved.T):
        dep=saved.dep[i].numpy();allowed=saved.dep_mask[i].numpy();uv=np.rint(tracks[i].numpy()).astype(int);uv[:,0]=uv[:,0].clip(0,639);uv[:,1]=uv[:,1].clip(0,359);idx=uv[valid[i].numpy()];scaled=dep*scale[i]
        src=rays[idx[:,1],idx[:,0]]*scaled[idx[:,1],idx[:,0],None];tree=cKDTree(src);nearest=tree.query(src,k=2,workers=4)[0][:,1];sigma=np.maximum(nearest,1e-4)*.333
        query=rays[allowed]*scaled[allowed,None];dist,indices=tree.query(query,k=min(16,len(src)),workers=4);weights=np.exp(-dist**2/(2*sigma[indices]**2));weights/=weights.sum(1,keepdims=True).clip(1e-8)
        delta=np.zeros_like(dep);delta[allowed]=(weights*corr[i,valid[i].numpy()][indices]).sum(1);new=scaled+delta
        assert np.isfinite(new).all() and (new[allowed]>.001).all()
        np.savez_compressed(out/(saved.frame_names[i]+'.npz'),correction=delta);sampled.append(new[uv[:,1],uv[:,0]])
        rows.append(dict(frame=i,minimum=float(new[allowed].min())))
        if i%60==0:print('Dense correction',i,flush=True)
    # Dense propagation must preserve qualified sparse geometry before appearance.
    homo,_,_=prepare_track_homo_dep_rgb_buffers(saved,tracks,valid,torch.arange(saved.T));world=get_world_points(homo,torch.tensor(np.array(sampled)),cams);mean=torch.where(valid[...,None],world,0).sum(0)/valid.sum(0).clamp_min(1)[:,None];errors=[];counts=[]
    for i in range(saved.T):
        cp=cams.trans_pts_to_cam(i,mean);q=cp@cams.K().T;uv=q[:,:2]/q[:,2:].clamp_min(1e-6);use=valid[i]&(cp[:,2]>.001);errors.append(float((uv-tracks[i])[use].norm(dim=-1).median()));counts.append(int(use.sum()))
    gate=dict(frames=saved.T,median=float(np.median(errors)),worst=max(errors),minimumAnchors=min(counts),passed=np.median(errors)<=5 and max(errors)<=20 and min(counts)>=64)
    gate['passed']=bool(gate['passed']);write(B/f'results/{case}-dense-gate.json',gate);assert gate['passed'],gate

def photo(case):
    from mosca_reconstruct import photometric_warmup
    ws=B/'input'/case;cfg=OmegaConf.load(ws/'fit.yaml');log=Path(json.loads((ws/'geometry-location.json').read_text())['log'])
    assert json.loads((ws/'geometry-reviewed.json').read_text())['gatePassed']
    reference=torch.load(log/'bundle/bundle_cams.pth',map_location='cpu');loads=[];original=MonocularCameras.load_from_ckpt
    def load(cls,state):
        assert all(torch.equal(state[k].cpu(),v) for k,v in reference.items())
        cams=original(state)
        for p in cams.parameters():p.requires_grad_(False)
        cams.get_optimizable_list=lambda **kw:[];loads.append(cams);return cams
    MonocularCameras.load_from_ckpt=classmethod(load)
    rescale=Saved2D.rescale_perframe_depth_from_bundle
    def corrected(saved,bundle_pth_fn=None):
        rescale(saved,bundle_pth_fn)
        delta=torch.from_numpy(np.stack([np.load(ws/'background-corrections'/(name+'.npz'))['correction'] for name in saved.frame_names])).to(saved.dep)
        saved.dep+=delta;saved.recompute_dep_mask(depth_boundary_th=float(cfg.depth_boundary_th));return saved
    Saved2D.rescale_perframe_depth_from_bundle=corrected
    # Static control: all valid depth is eligible; moving people are not claimed.
    fn=photometric_warmup.__globals__['set_epi_mask_to_s2d_for_bg_render']
    def all_static(s,e,d):
        s=fn(s,e,d);s.register_2d_identification(static_2d_mask=s.dep_mask,dynamic_2d_mask=torch.zeros_like(s.dep_mask));return s
    photometric_warmup.__globals__['set_epi_mask_to_s2d_for_bg_render']=all_static
    photometric_warmup(str(ws),str(log),cfg)
    result=torch.load(log/'static_warm_cam.pth',map_location='cpu');same=all(torch.equal(result[k],v) for k,v in reference.items())
    write(B/f'results/{case}-photo-camera-invariance.json',dict(allCameraStateExactlyUnchanged=same,cameraLoads=len(loads),staticControl=True));assert same

def prepare(case):
    import mosca_precompute as pre
    ws=B/'input'/case;cfg=OmegaConf.load(ws/'prep.yaml')
    images,names=pre.load_imgs_from_dir(str(ws));processor=pre.get_moca_processor(cfg)
    pre.preprocess(images,names,str(ws),processor,cfg,resample_for_dynamic=json.loads((ws/'config.json').read_text())['mode']=='dynamic')

def instrument_fit(case):
    from mosca_reconstruct import DynReconstructionSolver
    original=DynReconstructionSolver.photometric_fit
    def timed(self,**kwargs):
        torch.cuda.synchronize();start=time.monotonic();ok=False
        try:
            result=original(self,**kwargs);ok=True;return result
        finally:
            torch.cuda.synchronize()
            write(B/f"results/{case}-fit-timing.json",dict(phase=kwargs['phase_name'],requestedSteps=kwargs['total_steps'],completedSteps=kwargs['total_steps'] if ok else None,returnedCleanly=ok,seconds=time.monotonic()-start,scope='Native photometric_fit including final checkpoint save; optional final diagnostics disabled'))
    DynReconstructionSolver.photometric_fit=timed

def verify_photo(case):
    ws=B/'input'/case;log=Path(json.loads((ws/'geometry-location.json').read_text())['log'])
    config=json.loads((ws/'config.json').read_text());phase='static_warm' if config['mode']=='static' else 'photometric'
    reference=torch.load(log/'bundle/bundle_cams.pth',map_location='cpu')
    actual=torch.load(log/(phase+'_cam.pth'),map_location='cpu')
    assert set(reference)==set(actual) and all(torch.equal(actual[k],v) for k,v in reference.items())
    files=[log/(phase+'_s_model_native_add3.pth')]
    if config['mode']=='dynamic':files.append(log/(phase+'_d_model_native_add3.pth'))
    for path in files:
        state=torch.load(path,map_location='cpu')
        assert all(torch.isfinite(v).all() for v in state.values() if torch.is_tensor(v) and v.is_floating_point())
    timing=json.loads((B/f'results/{case}-fit-timing.json').read_text())
    assert timing['returnedCleanly'] and timing['completedSteps']==config['photoSteps']
    write(B/f'results/{case}-checkpoint-verification.json',dict(allCameraStateExactlyUnchanged=True,allModelTensorsFinite=True,completedSteps=timing['completedSteps'],modelFiles=[p.name for p in files]))

if __name__=='__main__':
    torch.set_num_threads(4);stage,case=sys.argv[1:]
    cfg=json.loads((B/'input'/case/'config.json').read_text())
    if stage=='photo':instrument_fit(case)
    if cfg['mode']=='dynamic' and stage in ['motion','foreground','photo']:
        import dynamic
        sys.argv=[sys.argv[0],'geometry' if stage=='motion' else stage,case];dynamic.main()
    else:{'prepare':prepare,'track':track,'bundle':bundle,'dense':dense,'photo':photo}[stage](case)

    if stage=='photo':verify_photo(case)
