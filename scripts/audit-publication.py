"""Scan intended files and reachable history without printing matched secret values.
Pattern scanning complements review; it is not proof of the absence of all secrets.
"""
from pathlib import Path
import json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
RULES={
 'private-key':rb'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
 'github-token':rb'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
 'aws-key-id':rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
 'stripe-key':rb'\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b',
 'slack-token':rb'\bxox[baprs]-[A-Za-z0-9-]{20,}\b',
 'credential-url':rb'https?://[^\s/@:]+:[^\s/@]+@',
 'literal-secret':rb'''(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["'][A-Za-z0-9_./+=-]{24,}["']''',
}
FORBIDDEN={'.secrets','node_modules','.venv','__pycache__','data','working','output','outputs'}
MEDIA={'.splat','.ply','.mp4','.mov','.png','.jpg','.pt','.pth','.pem','.key','.zip','.tar','.gz'}
def scan(name,data):
 problems=[];p=Path(name)
 if any(part in FORBIDDEN for part in p.parts) or (p.name.startswith('.env') and p.name!='.env.example') or p.suffix.lower() in MEDIA or p.name.startswith(('id_rsa','id_ed25519')):problems.append('excluded-file-type-or-directory')
 if len(data)>3*1024**2:problems.append('unexpected-large-file')
 for rule,pattern in RULES.items():
  if re.search(pattern,data):problems.append(rule)
 return [dict(file=name,rule=rule) for rule in problems]
def main():
 names=git('ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0');names=sorted(set(n for n in names if n));findings=[]
 for name in names:
  p=ROOT/name
  if p.is_symlink():findings.append(dict(file=name,rule='unexpected-symlink'));continue
  if p.is_file():findings+=scan(name,p.read_bytes())
 blobs=0
 for row in git('rev-list','--objects','--all').decode().splitlines():
  oid,_,name=row.partition(' ')
  if git('cat-file','-t',oid).strip()!=b'blob':continue
  blobs+=1;findings+=scan(name,git('cat-file','blob',oid))
 report=dict(intendedFiles=len(names),historicalBlobs=blobs,findings=findings,scope='Pattern and filename scan of intended files and all reachable historical file blobs; no matched values printed. Does not replace provenance/content review.')
 print(json.dumps(report,indent=2));return bool(findings)
if __name__=='__main__':sys.exit(main())
