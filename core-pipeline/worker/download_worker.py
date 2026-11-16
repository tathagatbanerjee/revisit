"""Direct public downloads on the worker; verify the same local freeze before use."""
from pathlib import Path
import concurrent.futures,hashlib,json,shutil,tarfile,time,urllib.request
B=Path('/workspace/revisit')
def download(j):
 p=B/'weights'/j['file'];tmp=p.with_suffix('.part')
 with urllib.request.urlopen(j['url'],timeout=60) as r,tmp.open('wb') as f:shutil.copyfileobj(r,f)
 assert tmp.stat().st_size==j['bytes'] and hashlib.sha256(tmp.read_bytes()).hexdigest()==j['sha256'],p
 tmp.replace(p);print('Verified',p.name,flush=True)
rows=json.loads((B/'weights/manifest.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(download,rows))
(B/'sources').mkdir(exist_ok=True)
for repo,rev,name,expected in [('YvanYin/Metric3D','eb5b6fac0dc155e4e52f576e304fbf11655ff339','metric3d','6859f6024544916afe44adcbbcf7e5837032db732e406a5129df44240c2dc223'),('facebookresearch/co-tracker','82e02e8029753ad4ef13cf06be7f4fc5facdda4d','cotracker','45ccb696ddd27b89caffefe6b9c2f5c36f61357fd8419ae02da7ba7b8cc999d1')]:
 p=B/'sources'/f'{name}.tar.gz'
 with urllib.request.urlopen(f'https://codeload.github.com/{repo}/tar.gz/{rev}',timeout=60) as r,p.open('wb') as f:shutil.copyfileobj(r,f)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
 dest=B/'sources'/name;dest.mkdir(exist_ok=True)
 with tarfile.open(p) as t:
  for member in t.getmembers():
   member.name='/'.join(member.name.split('/')[1:])
   if member.name:t.extract(member,dest,filter='data')
 print('Verified source',name,flush=True)
