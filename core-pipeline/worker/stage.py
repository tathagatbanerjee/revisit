"""Supervised static worker-stage wrapper; never allocates or controls a Pod.
Requires an externally provided runtime deadline. This is not independent cloud
termination and does not qualify the preview's disabled paid allocation path.
"""
from pathlib import Path
import fcntl,hashlib,json,os,signal,subprocess,sys,time
B=Path('/workspace/revisit')
STAGES=('prepare','bundle','dense','photo','export')
def read(p):return json.loads(p.read_text())
def main(stage,case):
    assert stage in STAGES and case in read(B/'input/manifest.json')
    cfg=read(B/'input'/case/'config.json');assert cfg['mode']=='static'
    bounds=read(B/'runtime-bounds.json');remaining=bounds['deadlineEpoch']-time.time()-1200
    assert remaining>=60,'External deadline leaves insufficient work/retrieval time'
    assert (B/'output/preflight-complete').is_file(),'Native/model preflight required'
    frozen=read(B/'input/manifest.json')[case];ws=B/'input'/case
    for row in frozen['frames']:
        with (ws/'images'/row['file']).open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==row['sha256']
    for name,key in [('fit.yaml','fitProfileSha256'),('prep.yaml','prepProfileSha256')]:assert hashlib.sha256((ws/name).read_bytes()).hexdigest()==frozen[key]
    out=B/'results'/f'{case}-{stage}.json';assert not out.exists(),'Completed/failed receipt is immutable; declare a new attempt'
    for prior in STAGES[:STAGES.index(stage)]:assert read(B/'results'/f'{case}-{prior}.json')['exitCode']==0
    if stage!='prepare':assert read(ws/'priors-reviewed.json')['gatePassed'],'Explicit priors review required'
    if stage in ('photo','export'):assert read(ws/'geometry-reviewed.json')['gatePassed'],'Explicit geometry review required'
    lock=(B/'output/gpu-stage.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    py=str(B/'mosca-env/bin/python');command=[py,str(B/('export-native.py' if stage=='export' else 'worker.py'))]
    command+=([case] if stage=='export' else [stage,case])
    env={**os.environ,'MOSCA_CASE':case,'CORE_STATIC':'1','CORE_DIAGNOSTICS':'0','GS_BACKEND':'native_add3','PYTHONPATH':str(B),'CUDA_HOME':'/usr/local/cuda-11.8','OMP_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','MPLBACKEND':'Agg'}
    code=1;start=time.time();reason=None
    with (B/'results'/f'{case}-{stage}.log').open('xb') as log:
        child=subprocess.Popen(command,cwd=B/'mosca',env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:code=child.wait(timeout=min(remaining,5400 if stage=='photo' else 1200))
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
            reason='stage deadline';code=1
        if code==0 and stage=='prepare':
            try:
                subprocess.run([py,str(B/'review-priors.py'),str(ws)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=min(120,max(1,bounds['deadlineEpoch']-time.time()-1200)))
                assert read(ws/'priors-report.json')['numericGatePassed']
            except (subprocess.SubprocessError,AssertionError):code=1;reason='prior validation'
    with out.open('x') as stream:json.dump(dict(stage=stage,case=case,exitCode=code,seconds=time.time()-start,reason=reason,cloudTerminationScope='Not controlled by this process'),stream,indent=2)
    if code:raise SystemExit(code)
if __name__=='__main__':main(*sys.argv[1:])
