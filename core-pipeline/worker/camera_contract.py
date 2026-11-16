"""Geometry contract for future supplied-camera tests; no training or allocation."""
import hashlib
import numpy as np

def homogeneous(matrix):
 a=np.asarray(matrix,dtype=np.float64)
 if a.shape==(3,4):a=np.vstack([a,[0,0,0,1]])
 if a.shape!=(4,4) or not np.isfinite(a).all() or not np.allclose(a[3],[0,0,0,1]):raise ValueError('Invalid camera matrix')
 R=a[:3,:3]
 if not np.allclose(R.T@R,np.eye(3),atol=1e-5) or not np.isclose(np.linalg.det(R),1,atol=1e-5):raise ValueError('Camera rotation must be proper and orthonormal')
 return a

def build_contract(frames,poses,K,world_unit_scale=1.):
 K=np.asarray(K,dtype=np.float64)
 if K.shape!=(3,3) or not np.isfinite(K).all() or not np.allclose(K[2],[0,0,1]) or K[0,0]<=0 or K[1,1]<=0 or not np.isclose(K[0,0],K[1,1]) or K[0,1]!=0 or K[1,0]!=0:raise ValueError('Expected finite iso-focal pinhole calibration')
 if not np.isfinite(world_unit_scale) or world_unit_scale<=0:raise ValueError('World-unit scale must be positive')
 lookup={p['file']:p for p in poses}
 if len(lookup)!=len(poses) or len({r['file'] for r in frames})!=len(frames):raise ValueError('Duplicate frame identity')
 if set(lookup)!={r['file'] for r in frames}:raise ValueError('Every exact source frame needs one validated camera')
 matrices=[]
 for frame in frames:
  row=lookup[frame['file']]
  if row.get('localizationPassed') is False:raise ValueError('Unqualified localized camera')
  T=homogeneous(row['cameraToWorld']).copy();T[:3,3]*=world_unit_scale;matrices.append(T)
 matrices=np.asarray(matrices,dtype=np.float32)
 # Native MoSca normalizes using half the short image side (360/2).
 fov=float(np.rad2deg(2*np.arctan(180/K[1,1])))
 return {'cameraToWorld':matrices.tolist(),'K':K.tolist(),'nativeFovDegrees':fov,'nativePrincipalPointRatio':[float(K[0,2]/640),float(K[1,2]/360)],'worldUnitScale':float(world_unit_scale),'poseFloat32Sha256':hashlib.sha256(matrices.tobytes()).hexdigest(),'locksRequired':['BA rotation','BA translation','BA focal','static warmup cameras','appearance cameras'],'depthScaleMustUseSameWorldUnits':True}
