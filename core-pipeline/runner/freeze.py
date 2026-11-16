"""Build an isolated worker input bundle after reviewed source and passing mapping.
No paid resources are created; no credentials, source video or third-party source
are included. Setup must acquire upstream sources/weights separately.
"""
from pathlib import Path
import hashlib,json,shutil,sys,tarfile
ROOT=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main(project,output):
    p=Path(project).resolve();out=Path(output).resolve();meta=json.loads((p/'project.json').read_text());cfg=json.loads((p/'config.json').read_text());case=cfg['id']
    assert meta['sourceReview']['passed'] and cfg['mode']=='static'
    report=json.loads((p/'mapping/map-result.json').read_text());assert report['passed'] and report['minimumObserved']>=64
    out.mkdir(parents=True,exist_ok=False);ws=out/'input'/case;ws.mkdir(parents=True)
    shutil.copytree(p/'prepared/images',ws/'images')
    for name in ['map-cameras.json','map-tracks.npz']:shutil.copyfile(p/'mapping'/name,ws/name)
    write(ws/'config.json',cfg);write(ws/'source-reviewed.json',meta['sourceReview'])
    for source,target in [('static-fit.yaml','fit.yaml'),('prep.yaml','prep.yaml')]:shutil.copyfile(ROOT/'core-pipeline/configs'/source,ws/target)
    rows=json.loads((p/'prepared/frames.json').read_text());assert all(sha(ws/'images'/r['file'])==r['sha256'] for r in rows)
    write(out/'input/manifest.json',{case:dict(frames=rows,count=len(rows),clock='actual original presentation timestamps',sourceVideoSha256=meta['sha256'],sourceStartSeconds=rows[0]['sourceSeconds'],photoSteps=cfg['photoSteps'],staticOnly=True,diagnostics=False,fitProfileSha256=sha(ws/'fit.yaml'),prepProfileSha256=sha(ws/'prep.yaml'),config=cfg)})
    support=out/'input/support';support.mkdir()
    for source in (ROOT/'core-pipeline/worker').glob('*.py'):shutil.copyfile(source,support/source.name)
    # Native scripts expect these helper modules at the workspace root as well.
    for source in (ROOT/'core-pipeline/worker').glob('*.py'):shutil.copyfile(source,out/source.name)
    shutil.copyfile(out/'worker.py',out/'duration_reconstruct.py')
    (out/'weights').mkdir();shutil.copyfile(ROOT/'core-pipeline/configs/weights.json',out/'weights/manifest.json')
    correction=json.loads((ROOT/'core-pipeline/configs/depth-validity.json').read_text());correction.update({k:sha(out/n) for k,n in [('helperSha256','ba_depth_validity.py'),('patcherSha256','patch_depth_validity.py'),('cudaSmokeSha256','cuda_depth_smoke.py')]});correction['cases']={case:dict(baselinePolicy='freeze all-target camera-facing fractions before optimization')};write(out/'depth-correction.json',correction)
    write(out/'duration-manifest.json',dict(schemaVersion=1,status='FROZEN_NOT_ALLOCATED',freshFits=[dict(id=case,staticOnly=True)],preflightCase=case,upstreamRevision='02404d2841b4e0dc2d9074860950bce5da579656',qualification='GPU migration unvalidated in Revisit'))
    shutil.copyfile(ROOT/'core-pipeline/bootstrap.sh',out/'bootstrap.sh')
    files={str(f.relative_to(out)):sha(f) for f in out.rglob('*') if f.is_file()};write(out/'payload-manifest.json',files)
    with tarfile.open(out.with_suffix('.tar.gz'),'w:gz') as archive:
        for name in [*files,'payload-manifest.json']:archive.add(out/name,arcname=name,recursive=False)
    print(json.dumps(dict(case=case,files=len(files),archive=str(out.with_suffix('.tar.gz')),sha256=sha(out.with_suffix('.tar.gz')),credentialsIncluded=False,allocated=False)))
if __name__=='__main__':main(*sys.argv[1:])
