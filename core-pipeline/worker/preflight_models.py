"""Real pinned pretrained inference for every proposed model, on the exact RGB."""
import os,sys,json,time
from pathlib import Path
os.environ['GS_BACKEND']='native_add3'
B=Path('/workspace/revisit');sys.path[:0]=[str(B/'mosca'),str(B)]
import torch,numpy as np,imageio.v2 as imageio
from lib_prior.depth_models.metric3d_wrapper import get_metric3dv2_model,__process_frame__
from lib_prior.tracking.bootstapir_wrapper import get_bootstapir_model,inference
from lib_prior.tracking.cotracker_wrapper import get_cotracker,online_track_point
case=json.loads((B/'duration-manifest.json').read_text()).get('preflightCase','guildhall-3s-large') if (B/'duration-manifest.json').exists() else 'guildhall'
im=imageio.imread(B/'input'/case/'images/00000.png');records={};torch.set_num_threads(4)
for version in ['small','large']:
 start=time.time();model=get_metric3dv2_model('cuda',version);dep=__process_frame__(im,str(B/f'output/preflight-{version}.npz'),model)
 assert dep.shape==im.shape[:2] and (np.isfinite(dep)&(dep>0)).mean()>.99
 records['metric3d-'+version]=dict(checkpointLoading=model.checkpoint_loading_receipt,seconds=time.time()-start,positiveFiniteFraction=float((np.isfinite(dep)&(dep>0)).mean()))
 del model;torch.cuda.empty_cache()
start=time.time();model=get_bootstapir_model(device='cuda');video=torch.from_numpy(np.stack([im]*3)).permute(0,3,1,2).float();video=torch.nn.functional.interpolate(video,(256,256)).permute(0,2,3,1).to('cuda');tracks,visible=inference(video,torch.tensor([[0,128,128]],device='cuda'),model)
assert tracks.shape==(1,3,2) and torch.isfinite(tracks).all();records['bootstapir']=dict(seconds=time.time()-start,shape=list(tracks.shape))
del model;torch.cuda.empty_cache();start=time.time();model=get_cotracker('cuda');video=torch.from_numpy(np.stack([im]*9)).permute(0,3,1,2).float()[None]
tracks,visible=online_track_point(video,torch.tensor([[[0.,320.,180.]]]),model,'cuda')
assert tracks.shape==(9,1,2) and torch.isfinite(tracks).all();records['cotracker3']=dict(seconds=time.time()-start,shape=list(tracks.shape))
(B/'output/model-preflight.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records),flush=True)
