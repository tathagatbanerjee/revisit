"""Replay native sparse depths against saved initialization, without dense RGB."""
from pathlib import Path
import json,time
import numpy as np
import torch
from PIL import Image,ImageDraw
B=Path('/workspace/revisit')
@torch.no_grad()
def inspect(ws,log,cfg,static_only):
    start=time.monotonic();case=ws.name
    p=json.loads((ws/'camera-package.json').read_text())
    b=torch.load(log/'bundle/bundle.pth',map_location='cpu')
    track=b['s_track'].detach();valid=b['s_track_mask'].bool()
    poses=torch.tensor(p['cameraToWorld'],dtype=torch.float32);K=torch.tensor(p['K'],dtype=torch.float32)
    uv=track.round().long();uv[...,0].clamp_(0,639);uv[...,1].clamp_(0,359)
    depth=[]
    for i in range(len(track)):
        raw=np.load(ws/'metric3d_depth'/f'{i:05d}.npz')['dep'].astype(np.float32)
        dep=(raw.clip(.001,1000)/p['normalizedRawDepthMedian']).clip(.001,1000)
        depth.append(dep[uv[i,:,1],uv[i,:,0]])
    raw=torch.from_numpy(np.array(depth));init=np.load(B/f'results/{case}-initialization.npz')
    initial_depth_difference=float((raw[valid]-torch.from_numpy(init['depth'])[valid]).abs().max())
    assert initial_depth_difference<1e-5
    def world(d):
        x=torch.linspace(-640/360,640/360,640)[uv[...,0]]/(K[0,0]/180)
        y=torch.linspace(-1,1,360)[uv[...,1]]/(K[1,1]/180)
        q=torch.stack([x*d,y*d,d],-1)
        return torch.einsum('tij,tnj->tni',poses[:,:3,:3],q)+poses[:,None,:3,3]
    initial_world_difference=float((world(raw)[valid]-torch.from_numpy(init['world'])[valid]).abs().max())
    assert initial_world_difference<1e-5
    d=raw*b['dep_scale'].detach()[:,None]+b['dep_correction'].detach();xyz=world(d)
    keep=valid&(d>.001)&torch.isfinite(xyz).all(-1)
    mean=torch.where(keep[...,None],xyz,0).sum(0)/keep.sum(0).clamp_min(1)[:,None]
    cp=torch.einsum('tji,tnj->tni',poses[:,:3,:3],mean[None]-poses[:,None,:3,3]);q=cp@K.T
    projection=q[...,:2]/q[...,2:].clamp_min(1e-6);use=keep&(cp[...,2]>.001);err=(projection-track).norm(dim=-1)
    rows=[dict(frame=i,observations=int(use[i].sum()),medianPx=float(np.median(err[i,use[i]].numpy())),p90Px=float(torch.quantile(err[i,use[i]],.9))) for i in range(len(track))]
    from lib_moca.camera import MonocularCameras
    cams=MonocularCameras.load_from_ckpt(torch.load(log/'bundle/bundle_cams.pth',map_location='cpu'))
    actual=torch.stack([cams.T_wc(i) for i in range(len(track))]).detach()
    same=bool(torch.allclose(actual,poses,rtol=0,atol=1e-5))
    sheet=Image.new('RGB',(1920,780),'#18212a');draw=ImageDraw.Draw(sheet)
    for j,i in enumerate(np.linspace(0,len(track)-1,6).round().astype(int)):
        im=Image.open(ws/'images'/f'{i:05d}.png').convert('RGB');di=ImageDraw.Draw(im)
        indices=torch.where(use[i])[0].numpy()[::max(1,int(use[i].sum())//80)]
        for n in indices:
            a=track[i,n].numpy();bb=projection[i,n].numpy()
            if np.abs(bb).max()<2000:di.line([tuple(a),tuple(bb)],fill='#f7b565',width=1);di.ellipse((a[0]-2,a[1]-2,a[0]+2,a[1]+2),fill='#8be6a3')
        x=640*(j%3);y=390*(j//3);sheet.paste(im,(x,y+30));draw.text((x+3,y+5),f"Frame{i}: {rows[i]['medianPx']:.3f}px, {rows[i]['observations']} anchors",fill='white')
    sheet.save(B/f'results/{case}-geometry-review.jpg')
    result=dict(numericGatePassed=same and all(np.isfinite(r['medianPx']) for r in rows),frames=len(track),K=K.tolist(),cameraToWorld=actual.tolist(),staticReprojection=rows,initialDepthReplayMaximumDifference=initial_depth_difference,initialWorldReplayMaximumDifference=initial_world_difference,inspectionSeconds=time.monotonic()-start,diagnosticLimit='Fitted sparse consistency, not held-out physical accuracy')
    (B/f'results/{case}-geometry-report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
