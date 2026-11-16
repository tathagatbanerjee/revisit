"""Require actual CUDA computation and native KNN, not just GPU enumeration."""
import json,torch
from simple_knn._C import distCUDA2
x=torch.randn(128,128,device='cuda',requires_grad=True);loss=(x@x.T).square().mean();loss.backward();torch.cuda.synchronize();assert torch.isfinite(x.grad).all()
p=torch.randn(128,3,device='cuda');distance=distCUDA2(p);torch.cuda.synchronize();assert torch.isfinite(distance).all()
import sys
sys.path.insert(0,'/workspace/revisit/mosca')
from lib_render.gauspl_renderer_native_add3 import render_cam_pcl
xyz=torch.tensor([[0.,0.,2.],[.1,.1,2.]],device='cuda',requires_grad=True)
frame=torch.eye(3,device='cuda')[None].repeat(2,1,1)
scale=torch.full((2,3),.08,device='cuda',requires_grad=True)
opacity=torch.full((2,1),.5,device='cuda',requires_grad=True)
sh=torch.zeros(2,3,device='cuda',requires_grad=True)
out=render_cam_pcl(xyz,frame,scale,opacity,sh,32,32,fx=32)
out['rgb'].square().mean().backward();torch.cuda.synchronize()
assert all(x.grad is not None and torch.isfinite(x.grad).all() for x in [xyz,scale,opacity,sh])
assert xyz.grad.abs().sum()>0
print(json.dumps(dict(gpu=torch.cuda.get_device_name(),torch=torch.__version__,cuda=torch.version.cuda,matrixForwardBackwardPassed=True,nativeKnnPassed=True,nativeRasterForwardBackwardPassed=True)))
