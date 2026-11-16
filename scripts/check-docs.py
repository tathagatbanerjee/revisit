"""Validate public relative markdown links and Python/JSON syntax without imports."""
from pathlib import Path
import ast,json,re
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','node_modules','data','working','__pycache__'}
checked=0
for p in ROOT.rglob('*'):
    if not p.is_file() or any(part in EXCLUDED for part in p.relative_to(ROOT).parts):continue
    if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    if p.suffix=='.json':json.loads(p.read_text())
    if p.suffix=='.md':
        checked+=1
        text=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target or target.startswith(('mailto:','#')):continue
            target=target.split('#')[0]
            assert (p.parent/target).exists(),f'{p.relative_to(ROOT)}: missing {target}'
print(f'Checked {checked} markdown files; Python and JSON syntax valid.')
