"""Similarity transforms and observed interval composition; no Gaussian fitting."""
from bisect import bisect_right
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation
FIELDS=['x','y','z','nx','ny','nz','f_dc_0','f_dc_1','f_dc_2','opacity','scale_0','scale_1','scale_2','rot_0','rot_1','rot_2','rot_3']
DTYPE=np.dtype([(k,'<f4') for k in FIELDS])
def load_ply(path):
 with Path(path).open('rb') as f:
  assert f.readline().strip()==b'ply';fields=[];count=None;fmt=None
  while True:
   raw=f.readline()
   if not raw:raise ValueError('Truncated PLY header')
   line=raw.decode().strip()
   if line.startswith('format '):fmt=line.split()[1]
   elif line.startswith('element vertex '):count=int(line.split()[-1])
   elif line.startswith('property '):
    _,kind,key=line.split();assert kind=='float';fields.append(key)
   elif line=='end_header':break
  assert fields==FIELDS and fmt=='binary_little_endian' and count is not None
  v=np.fromfile(f,dtype=DTYPE,count=count);assert len(v)==count
 return v

def save_ply(path,v):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 h='ply\nformat binary_little_endian 1.0\nelement vertex '+str(len(v))+'\n'+''.join('property float '+k+'\n' for k in FIELDS)+'end_header\n'
 with p.open('wb') as f:f.write(h.encode());v.tofile(f)

def transform(v,scale,rotation,translation):
 assert scale>0 and np.linalg.det(rotation)>0
 out=v.copy();xyz=scale*np.column_stack([v[k] for k in ['x','y','z']])@rotation.T+translation
 for j,k in enumerate(['x','y','z']):out[k]=xyz[:,j]
 for j in range(3):out[f'scale_{j}']=v[f'scale_{j}']+np.log(scale)
 q=np.column_stack([v[f'rot_{j}'] for j in range(4)])
 q=(Rotation.from_matrix(rotation)*Rotation.from_quat(q[:,[1,2,3,0]])).as_quat()[:,[3,0,1,2]]
 for j in range(4):out[f'rot_{j}']=q[:,j]
 return out

def similarity(source,target):
 x=np.asarray(source,dtype=float);y=np.asarray(target,dtype=float)
 assert len(x)>=3 and x.shape==y.shape and x.shape[1]==3
 xc=x-x.mean(0);yc=y-y.mean(0);u,s,vt=np.linalg.svd(yc.T@xc/len(x));sign=np.ones(3);sign[-1]=np.linalg.det(u@vt)
 r=(u*sign)@vt;scale=float((s*sign).sum()/np.mean((xc*xc).sum(1)))
 if not np.isfinite(scale) or scale<=0:raise ValueError('Invalid scale')
 return scale,r,y.mean(0)-scale*r@x.mean(0)

def robust_similarity(source,target,threshold=.10,iterations=512):
 x=np.asarray(source);y=np.asarray(target);rng=np.random.default_rng(12345);best=None
 for _ in range(iterations):
  i=rng.choice(len(x),3,replace=False)
  if np.linalg.matrix_rank(x[i]-x[i].mean(0),tol=1e-5)<2:continue
  try:s,r,t=similarity(x[i],y[i])
  except (ValueError,np.linalg.LinAlgError):continue
  err=np.linalg.norm(s*x@r.T+t-y,axis=1);mask=err<threshold;score=(int(mask.sum()),-float(np.median(err)))
  if best is None or score>best[0]:best=(score,mask)
 if best is None or best[1].sum()<3:raise ValueError('No consistent similarity')
 mask=best[1]
 for _ in range(3):
  s,r,t=similarity(x[mask],y[mask]);err=np.linalg.norm(s*x@r.T+t-y,axis=1);new=err<threshold
  if new.sum()<3:break
  mask=new
 return s,r,t,mask,err

def active_frame(times,time):
 if not times or time<times[0] or time>times[-1]:return None
 return bisect_right(times,time)-1

def union_at(a,a_times,b,b_times,time):
 ia=active_frame(a_times,time);ib=active_frame(b_times,time);chunks=[]
 if ia is not None:chunks.append(a[ia])
 if ib is not None:chunks.append(b[ib])
 return np.concatenate(chunks) if chunks else np.empty(0,dtype=DTYPE)
