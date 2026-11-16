import { relativeFile,idOK } from './files.mjs';
const fail = message => {throw Object.assign(new Error(message),{status:400});};
export function validateRun(r) {
  if(!r||r.schemaVersion!==1||!idOK(r.id)||typeof r.title!=='string'||r.title.length>200)fail('Invalid run identity');
  if(!['static','sequence'].includes(r.representation))fail('Expected static scene or timestamped sequence');
  if(r.representation==='static'&&!relativeFile(r.model))fail('Invalid static model path');
  if(r.representation==='sequence'){
    if(!Array.isArray(r.frames)||!r.frames.length||r.frames.length>2000)fail('Sequence needs 1–2000 observations');
    r.frames.forEach((f,i)=>{if(!f||!relativeFile(f.model)||!Number.isFinite(f.time)||f.time<0||(i&&f.time<=r.frames[i-1].time))fail('Observation times must be finite and strictly increasing');});
    if(!Number.isFinite(r.durationSeconds)||r.durationSeconds<=0||r.durationSeconds<r.frames.at(-1).time)fail('Invalid sequence duration');
  }
  if(r.inspectionViews!==undefined&&(!Array.isArray(r.inspectionViews)||r.inspectionViews.length>16||r.inspectionViews.some(v=>!v||!idOK(v.id)||typeof v.label!=='string'||v.label.length>80||!v.camera)))fail('Invalid recorded camera list');
  for(const c of [r.inspectionCamera,...(r.inspectionViews??[]).map(v=>v.camera)].filter(Boolean)){
    if(!Array.isArray(c.position)||c.position.length!==3||!Array.isArray(c.quaternion)||c.quaternion.length!==4||![...c.position,...c.quaternion,c.fx,c.fy,c.cx,c.cy,c.width,c.height,c.near,c.far,c.targetDistance].every(Number.isFinite)||Math.abs(Math.hypot(...c.quaternion)-1)>.01||c.fx<=0||c.fy<=0||c.width<=0||c.height<=0||c.near<=0||c.far<=c.near||c.targetDistance<=0)fail('Invalid inspection camera');
  }
  if(r.coordinateSystem&&!['opencv','y-up'].includes(r.coordinateSystem))fail('Unsupported coordinates');
  if(r.backgroundColor!==undefined&&(!Number.isInteger(r.backgroundColor)||r.backgroundColor<0||r.backgroundColor>0xffffff))fail('Invalid background colour');
  return r;
}
export function observationAt(frames,t){let index=0;for(let i=1;i<frames.length&&frames[i].time<=t;i++)index=i;return index;}
export function interval(input,duration){
  const start=Number(input.startSeconds),seconds=Number(input.durationSeconds);
  if(!Number.isFinite(start)||!Number.isFinite(seconds)||start<0||seconds<1||seconds>30||start+seconds>duration+.01)fail('Choose a continuous interval of 1–30 seconds within the video');
  return {startSeconds:start,durationSeconds:seconds,fps:12,width:640,height:360,mode:'static',depthRefinement:'scale-only',photoSteps:30000,seed:12345,diagnostics:false};
}
