"""Export every freshly fitted Gaussian and every native observed state, no labels."""
import os,sys,json,hashlib
from pathlib import Path
os.environ.setdefault('GS_BACKEND','native_add3')
BASE=Path('/workspace/revisit');sys.path[:0]=[str(BASE/'mosca'),str(BASE)]
import numpy as np,torch,imageio.v2 as imageio
from pytorch3d.transforms import matrix_to_quaternion
from lib_mosca.static_gs import StaticGaussian
from lib_mosca.dynamic_gs import DynSCFGaussian
from lib_moca.camera import MonocularCameras
from lib_render.render_helper import render
from geometry import DTYPE,save_ply

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,gs):
    xyz,rot,scale,opacity,sh=gs;assert all(torch.isfinite(v).all() for v in gs);assert (scale>0).all();v=np.zeros(len(xyz),dtype=DTYPE);q=matrix_to_quaternion(rot).cpu().numpy()
    for j,k in enumerate(['x','y','z']):v[k]=xyz[:,j].cpu().numpy()
    for j in range(3):v[f'f_dc_{j}']=sh[:,j].cpu().numpy();v[f'scale_{j}']=scale[:,j].log().cpu().numpy()
    v['opacity']=torch.logit(opacity.clamp(1e-6,1-1e-6)).flatten().cpu().numpy()
    for j in range(4):v[f'rot_{j}']=q[:,j]
    save_ply(p,v)
def main():
    mode=sys.argv[1];torch.set_num_threads(4);ws=BASE/'input'/mode;static_only=json.loads((ws/'config.json').read_text())['mode']=='static';logs=sorted(ws.glob('logs/*/'+('static_warm_s_model_native_add3.pth' if static_only else 'photometric_d_model_native_add3.pth')));assert len(logs)==1,logs;log=logs[0].parent
    sfile=logs[0] if static_only else log/'photometric_s_model_native_add3.pth';dfile=None if static_only else logs[0];cfile=log/('static_warm_cam.pth' if static_only else 'photometric_cam.pth');static=StaticGaussian.load_from_ckpt(torch.load(sfile)).cuda().eval();dynamic=None if static_only else DynSCFGaussian.load_from_ckpt(torch.load(dfile)).cuda().eval();camera=MonocularCameras.load_from_ckpt(torch.load(cfile)).cuda().eval();out=BASE/'output/native'/mode;out.mkdir(parents=True,exist_ok=False);H=int(camera.default_H);W=int(camera.default_W);K=camera.K();T=int(camera.T) if static_only else int(dynamic.T);poses=[];frames=[];scores=[]
    with torch.no_grad():
        fixed=static();save(out/'static.ply',fixed)
        for i in range(T):
            moving=tuple(value[:0] for value in fixed) if static_only else dynamic(i);save(out/f'frames/{i:03d}.ply',moving);gs=tuple(torch.cat([fixed[j],moving[j]]) for j in range(5));pose=camera.T_cw(i);poses.append(camera.T_wc(i).cpu().numpy().tolist());frames.append(dict(nativeFrame=i,model=f'frames/{i:03d}.ply'))
            rendered=render(gs,H,W,K,pose);rgb=rendered['rgb'].permute(1,2,0).cpu().numpy();(out/'native-rgb').mkdir(exist_ok=True);imageio.imwrite(out/f'native-rgb/{i:03d}.png',np.uint8(np.clip(rgb,0,1)*255));source=imageio.imread(sorted((ws/'images').glob('*'))[i])/255.;scores.append(float(-10*np.log10(np.mean((np.clip(rgb,0,1)-source)**2)+1e-12)))
            if i in sorted(set([0,T//4,T//2,3*T//4,T-1])):
                (out/'native-buffers').mkdir(exist_ok=True)
                np.savez_compressed(out/f'native-buffers/{i:03d}.npz',dep=rendered['dep'].squeeze().cpu().numpy(),alpha=rendered['alpha'].squeeze().cpu().numpy())
            if i in [0,T//2,T-1]:
                shifted=pose.clone();shifted[0,3]+=.1;rr=render(gs,H,W,K,shifted)['rgb'].permute(1,2,0).cpu().numpy();imageio.imwrite(out/f'native-shift-{i:03d}.png',np.uint8(np.clip(rr,0,1)*255))
        report=dict(nativeFrames=T,staticGaussians=len(fixed[0]),dynamicGaussians=len(moving[0]),frames=frames,K=K.cpu().numpy().tolist(),width=W,height=H,cameraToWorld=poses,frameLayout='dynamic-only',appearance='PLY DC; native RGB full learned SH',nativePsnr=scores,checkpoints={p.name:sha(p) for p in ([sfile,cfile] if static_only else [sfile,dfile,cfile])},freshFit=mode!="reference",nativeBackground="white (upstream render default; viewer uses black)")
        import shutil
        (out/'checkpoints').mkdir()
        for checkpoint in [sfile,dfile,cfile]:
            if checkpoint is not None:shutil.copy2(checkpoint,out/'checkpoints'/checkpoint.name)
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(mode,T,len(fixed[0]),len(moving[0]),'median fitted PSNR',np.median(scores),flush=True)
if __name__=='__main__':main()
