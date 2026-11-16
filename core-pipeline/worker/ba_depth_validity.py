"""Opt-in visible-positive-depth BA correction, with explicit support guards.

No loss weights, camera initialization or training schedules are changed.
"""
from pathlib import Path
import json,os
import torch

class SupportGuard:
 def __init__(self,config,case,log_path=None):
  self.config=config;self.case=case;self.log_path=Path(log_path) if log_path else None;self.pending={}
 def mask(self,projected,source_depth,target_depth,raw_pair,weighted_pair,target_indices,step):
  near=self.config['nearDepth'];target_depth=target_depth.expand_as(projected);source_depth=source_depth.expand_as(projected)
  good=torch.isfinite(projected)&torch.isfinite(target_depth)&torch.isfinite(source_depth)&(projected>near)&(target_depth>near)&(source_depth>near)
  output=weighted_pair*good.to(weighted_pair.dtype)
  if step%50==0:
   with torch.no_grad():
    raw=raw_pair.bool();kept=raw&good;count=raw.sum();retained=kept.sum();counts=raw.sum((0,2));per_target=kept.sum((0,2))/counts.clamp_min(1)
    positive_inputs=raw&torch.isfinite(source_depth)&torch.isfinite(target_depth)&(source_depth>near)&(target_depth>near)
    positive_input_fraction=float(positive_inputs.sum()/count.clamp_min(1))
    global_fraction=float(retained/count.clamp_min(1));case=self.config['cases'][self.case];baseline=case.get('initialPerTargetFrontFractions')
    minimum=torch.as_tensor([max(.4,baseline[int(t)]-self.config['maximumPerTargetSupportDrop']) if baseline else self.config['minimumGlobalPairFraction'] for t in target_indices],device=projected.device)
    # Exclude diagonal source=target observations when counting independent support.
    source_indices=torch.arange(projected.shape[0],device=projected.device)
    independent=kept&(source_indices[:,None,None]!=target_indices[None,:,None]);unique=independent.any(0).sum(-1)
    stats={'step':int(step),'rawPairs':int(count),'retainedPairs':int(retained),'retainedPairFraction':global_fraction,'positiveInputDepthPairFraction':positive_input_fraction,'minimumTargetRetainedFraction':float(per_target.min()),'minimumIndependentTracksPerTarget':int(unique.min()),'perTarget':[{'frame':int(t),'fraction':float(fr),'requiredFraction':float(m),'independentTracks':int(n)} for t,fr,m,n in zip(target_indices,per_target,minimum,unique)]}
    passed=bool(count>0 and positive_input_fraction>=self.config['minimumPositiveInputDepthPairFraction'] and global_fraction>=self.config['minimumGlobalPairFraction'] and (per_target>=minimum).all() and (unique>=self.config['minimumIndependentTracks']).all() and output.sum()>0)
    stats['supportPassed']=passed;self.pending=stats
    if not passed:
     self.write(stats);raise RuntimeError('Positive-depth BA support declined; stop rather than hide difficult observations: '+str({k:v for k,v in stats.items() if k!='perTarget'}))
  return output,good
 def write(self,record):
  if self.log_path:
   self.log_path.parent.mkdir(parents=True,exist_ok=True)
   with self.log_path.open('a') as f:f.write(json.dumps(record)+'\n')
 def losses(self,step,**components):
  if step%50==0:
   self.write({**self.pending,'losses':{k:float(v.detach()) for k,v in components.items()}})

def safe_depth_inputs(projected,target,valid):
 # Invalid pairs become1/1 BEFORE division; their weights are already zero.
 # This avoids enormous masked intermediates and preserves gradients on valid pairs.
 return torch.where(valid,projected,torch.ones_like(projected)),torch.where(valid,target,torch.ones_like(projected))

_guard=None
def guard():
 global _guard
 if _guard is None:
  base=Path('/workspace/revisit');config=json.loads((base/'depth-correction.json').read_text());case=os.environ['MOSCA_CASE'];_guard=SupportGuard(config,case,base/f'results/{case}-depth-validity.jsonl')
 return _guard
