"""Small pure contracts shared by the CLI, stage runner and tests."""
import re
STAGES=('prepare','bundle','dense','photo','export')
def validate_config(c):
    assert re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,80}',c['id'])
    assert c['width']==640 and c['height']==360 and c['fps']==12
    assert c['startSeconds']>=0 and 0<c['durationSeconds']<=30
    assert c['mode'] in ['static','dynamic']
    assert c['depthRefinement']=='scale-only'
    assert c['photoSteps']==30000 and c['seed']==12345
    assert isinstance(c['diagnostics'],bool)
    assert not c['source'].startswith('/') and '..' not in c['source'].split('/')
    if c['mode']=='dynamic':
        assert c['motionRequiredSeconds'] and all(0<=a<b<=c['durationSeconds'] for a,b in c['motionRequiredSeconds'])
    return c

def stages(mode):
    assert mode in ['static','dynamic']
    return STAGES if mode=='static' else ('prepare','bundle','dense','motion','foreground','photo','export')

def reservation_cost(seconds,rate,disk_gb=80):
    return seconds/3600*(rate+disk_gb*.2/720)

def check_stage(stage,receipts,priors_review=False,geometry_review=False,mode='static',motion_review=False,foreground_review=False):
    sequence=stages(mode)
    assert stage in sequence
    index=sequence.index(stage)
    for previous in sequence[:index]:assert receipts.get(previous,{}).get('exitCode')==0,previous+' not completed'
    if index>=1:assert priors_review,'Prior review required'
    if index>=3:assert geometry_review,'Geometry review required'

    if mode=='dynamic' and index>=4:assert motion_review,'Motion review required'
    if mode=='dynamic' and index>=5:assert foreground_review,'Foreground review required'
