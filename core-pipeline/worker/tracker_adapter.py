"""Explicit query geometry and CoTracker online state. Source coordinates [t,x,y]."""
import numpy as np

def canonical_queries(mask,n,seed=12345):
    """Uniform over eligible time/pixels on the shared 256-grid, with replacement."""
    eligible=np.argwhere(np.asarray(mask,dtype=bool))
    if not len(eligible):raise ValueError('Empty query support')
    rows=eligible[np.random.default_rng(seed).choice(len(eligible),n,replace=len(eligible)<n)]
    return rows[:,[0,2,1]].astype(np.float32)

def to_source(q,width,height):
    result=q.copy();result[:,1]*=width/256;result[:,2]*=height/256
    return result

def online_pass(video,queries,model,device,add_support_grid=True):
    """Initialize each pass, consume every step including the short final window."""
    import torch
    T=video.shape[1]
    if T<1:raise ValueError('Empty video')
    model(video[:,:min(2*model.step,T)].to(device),is_first_step=True,queries=queries.to(device),add_support_grid=add_support_grid)
    tracks=visibility=None
    for start in range(0,max(T-model.step,1),model.step):
        tracks,visibility=model(video[:,start:start+2*model.step].to(device),is_first_step=False,queries=queries.to(device),add_support_grid=add_support_grid)
    if tracks is None or tracks.shape[1]<T:raise RuntimeError('CoTracker omitted tail observations')
    return tracks[:,:T].cpu(),visibility[:,:T].cpu()
