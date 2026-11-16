#!/usr/bin/env python3
"""Review artifacts from real depth and track inference; no automatic fit approval."""
import argparse,json
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw
p=argparse.ArgumentParser();p.add_argument('case',type=Path);a=p.parse_args();d=a.case;ws=d
depth=sorted((ws/'metric3d_depth').glob('*.npz'));tracks=sorted(ws.glob('*_tap.npz'));images=sorted(p for p in (ws/'images').glob('*') if p.suffix.lower() in ['.png','.jpg'])
result={'depthFrames':len(depth),'tracks':[],'depth':[]};grid=Image.new('RGB',(960,480))
for f in depth:
    v=np.load(f)['dep'];valid=np.isfinite(v)&(v>0);result['depth'].append({'file':f.name,'positiveFiniteFraction':float(valid.mean()),'median':float(np.median(v[valid])) if valid.any() else None})
for col,i in enumerate(np.linspace(0,len(depth)-1,min(3,len(depth))).round().astype(int)):
    im=Image.open(images[i]).convert('RGB');im.thumbnail((320,240));grid.paste(im,(320*col,0))
    v=np.load(depth[i])['dep'];lo,hi=np.nanpercentile(v,[2,98]);color=cv2.applyColorMap(np.clip((v-lo)/(hi-lo+1e-6)*255,0,255).astype('uint8'),cv2.COLORMAP_TURBO)[...,::-1];im=Image.fromarray(color);im.thumbnail((320,240));grid.paste(im,(320*col,240))
for f in tracks:
    x=np.load(f);t=x['tracks'];v=x['visibility'].astype(bool);q=x['queries'].reshape(-1,3);im=Image.open(images[0]);W,H=im.size
    inside=(t[...,0]>=0)&(t[...,0]<W)&(t[...,1]>=0)&(t[...,1]<H)
    expected=q[:,[2,1]]*[W/256,H/256] if 'bootstapir' in f.name else q[:,1:]
    errors=np.linalg.norm(t[q[:,0].astype(int),np.arange(len(q))]-expected,axis=1)
    result['tracks'].append({'file':f.name,'shape':list(t.shape),'finite':bool(np.isfinite(t).all()),'visibilityFraction':float(v.mean()),'tracksVisibleFourFrames':int(((v&inside).sum(0)>=4).sum()),'observationsMatchImages':bool(t.shape[0]==len(images) and v.shape==t.shape[:2]),'queryCountMatchesTracks':bool(len(q)==t.shape[1]),'querySourcePositionP90ErrorPx':float(np.percentile(errors,90))})
static_only=json.loads((ws/'config.json').read_text())['mode']=='static'
required=[r for r in result['tracks'] if (not static_only) or 'uniform_' in r['file']]
result['staticOnly']=static_only
result['numericGatePassed']=len(depth)==len(images) and all(x['positiveFiniteFraction']>.99 for x in result['depth']) and any('uniform_' in x['file'] for x in result['tracks']) and (static_only or any('dynamic_' in x['file'] for x in result['tracks'])) and all(x['finite'] and x['tracksVisibleFourFrames']>=64 and x['observationsMatchImages'] and x['queryCountMatchesTracks'] and x['querySourcePositionP90ErrorPx']<=4 for x in required)
(d/'priors-report.json').write_text(json.dumps(result,indent=2)+'\n');grid.save(d/'priors-review.jpg');print(d.name,result['numericGatePassed'],flush=True)
