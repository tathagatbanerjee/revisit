import {spawn} from 'node:child_process';
export function run(command,args,{timeout=60000,onChild}={}){
 return new Promise((resolve,reject)=>{
  const child=spawn(command,args,{stdio:['ignore','pipe','pipe'],detached:process.platform!=='win32'});onChild?.(child);
  let out='',err='',done=false;
  const kill=()=>{try{if(process.platform==='win32')child.kill('SIGKILL');else process.kill(-child.pid,'SIGKILL');}catch{}};
  const timer=setTimeout(()=>{kill();finish(Error('Operation timed out. Try a shorter clip.'));},timeout);
  function finish(e){if(done)return;done=true;clearTimeout(timer);e?reject(e):resolve(out);}
  child.stdout.on('data',c=>{out+=c;if(out.length>16*1024*1024){kill();finish(Error('Diagnostic output exceeded limit'));}});
  child.stderr.on('data',c=>{err=(err+c).slice(-3000);});
  child.on('error',e=>finish(Error(e.code==='ENOENT'?`${command} is not installed. Run npm run doctor or use Docker.`:'Could not start preparation process')));
  child.on('exit',(code,signal)=>finish(code===0?null:Error(signal?'Preparation cancelled or interrupted':`${command} failed. Check the input format or select another clip. ${err.slice(-600)}`)));
 });
}
export function stop(child){if(!child)return;try{if(process.platform==='win32')child.kill('SIGKILL');else process.kill(-child.pid,'SIGKILL');}catch{}}
