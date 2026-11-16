"""Actual worker CUDA regression of the opt-in correction before any fitting."""
import json,torch
from pathlib import Path
from ba_depth_validity import SupportGuard,safe_depth_inputs
cfg={'nearDepth':.001,'minimumGlobalPairFraction':.8,'minimumPositiveInputDepthPairFraction':.995,'maximumPerTargetSupportDrop':.2,'minimumIndependentTracks':2,'cases':{'test':{'initialPerTargetFrontFractions':[1.,1.,1.]}}}
def ratio(z,d):return .5*abs(d/z.clamp(min=1e-6)-1)+.5*abs(z/d.clamp(min=1e-6)-1)
z=torch.full((3,3,4),1.1,device='cuda',requires_grad=True);source=torch.ones(3,1,4,device='cuda');target=torch.ones(1,3,4,device='cuda',requires_grad=True);raw=torch.ones_like(z,dtype=torch.bool);weights=torch.ones_like(z);ids=torch.arange(3,device='cuda')
mask,good=SupportGuard(cfg,'test').mask(z,source,target,raw,weights,ids,0);a,b=safe_depth_inputs(z,target,good);old=(ratio(z,target)*weights).sum()/weights.sum();new=(ratio(a,b)*mask).sum()/mask.sum();assert torch.allclose(old,new,rtol=1e-6,atol=1e-7);g1=torch.autograd.grad(old,(z,target),retain_graph=True);g2=torch.autograd.grad(new,(z,target));assert all(torch.allclose(x,y,rtol=1e-6,atol=1e-7) for x,y in zip(g1,g2))
z=torch.ones_like(z);z[2,0,0]=-.02914123;z.requires_grad_();mask,good=SupportGuard(cfg,'test').mask(z,source,target,raw,weights,ids,0);a,b=safe_depth_inputs(z,target,good);loss=(ratio(a,b)*mask).sum()/mask.sum();loss.backward();assert torch.isfinite(z.grad).all() and target.grad.abs().max()==0 and loss==0
try:SupportGuard(cfg,'test').mask(-torch.ones_like(z),source,target,raw,weights,ids,0)
except RuntimeError:pass
else:raise AssertionError('Hidden observations accepted')
torch.cuda.synchronize();print(json.dumps({'gpu':torch.cuda.get_device_name(),'validLossAndGradientsUnchanged':True,'capturedInvalidDepthTermSuppressed':True,'supportEvasionRejected':True,'device':'cuda'}))
