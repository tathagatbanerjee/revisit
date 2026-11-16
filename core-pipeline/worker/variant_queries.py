"""Freeze exact V00 TAP queries, reuse their physical source positions in all arms.

No fresh sampler or mask changes enter the comparisons. Baseline is unmodified.
"""
from pathlib import Path
import hashlib,json,os
import numpy as np

def image_hashes(ws):
 return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((Path(ws)/'images').glob('*'))}
def freeze(ws,dest):
 ws,dest=Path(ws),Path(dest);dest.mkdir(parents=True,exist_ok=False);records={}
 for kind,n in [('uniform',512),('dynamic',2048)]:
  files=list(ws.glob(f'*{kind}*bootstapir_tap.npz'));assert len(files)==1,files
  x=np.load(files[0]);q=x['queries'];assert q.shape==(n,3) and np.isfinite(q).all()
  assert x['tracks'].shape[1]==n
  np.save(dest/f'{kind}.npy',q);records[kind]={'count':n,'order':'t,y,x','grid':[256,256],'sha256':hashlib.sha256((dest/f'{kind}.npy').read_bytes()).hexdigest()}
 (dest/'manifest.json').write_text(json.dumps({'images':image_hashes(ws),'queries':records},indent=2)+'\n')
def load(ws,name,total,source_size=None):
 bank=Path(os.environ['MOSCA_QUERY_BANK']);manifest=json.loads((bank/'manifest.json').read_text())
 assert image_hashes(ws)==manifest['images'],'Query bank is for another input'
 kind='uniform' if name.startswith('uniform') else 'dynamic' if name.startswith('dynamic') else None
 assert kind is not None,name
 p=bank/f'{kind}.npy';assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['queries'][kind]['sha256']
 q=np.load(p);assert q.shape==(total,3)
 if source_size is not None:
  width,height=source_size;q=q[:,[0,2,1]].astype(np.float32);q[:,1]*=width/256;q[:,2]*=height/256
 return q

def install(source):
 source=Path(source);p=source/'lib_prior/tracking/bootstapir_wrapper.py';s=p.read_text()
 start=s.index('    queries = get_uniform_random_queries(',s.index('def bootstapir_process_folder'));end=s.index('    queries = queries.to(device)',start)
 original=s[start:end]
 s=s[:start]+'''    if os.environ.get('MOSCA_QUERY_BANK'):
        from variant_queries import load
        queries=torch.from_numpy(load(working_dir,save_name,total_n_pts)).to(torch.int32)
    else:
'''+''.join('    '+line+'\n' for line in original.splitlines())+s[end:];p.write_text(s)
 p=source/'lib_prior/tracking/cotracker_wrapper.py';s=p.read_text()
 needle='    start_t = time.time()';assert needle in s
 s=s.replace(needle,'''    from variant_queries import load
    canonical=torch.from_numpy(load(working_dir,save_name,total_n_pts,(W,H)))[None]
'''+needle,1)
 old='''        queries = get_uniform_random_queries(
            video_pt, chunk_size, mask_list=sample_mask_list
        )'''
 assert old in s;s=s.replace(old,'''        queries = canonical[:, round*chunk_size:min((round+1)*chunk_size,total_n_pts)]''',1);p.write_text(s)
if __name__=='__main__':
 import sys
 if sys.argv[1]=='freeze':freeze(*sys.argv[2:])
 elif sys.argv[1]=='install':install(sys.argv[2])
