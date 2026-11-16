// Fixed, checksummed public research assets. No user-controlled download URLs.
import path from 'node:path';
import {readFile,mkdir,writeFile,rename,rm,readdir,stat} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
export async function showcaseSpec(){return JSON.parse(await readFile(new URL('../../examples/guildhall.json',import.meta.url),'utf8'));}
export function createShowcaseCache(root,{spec,fetcher=fetch}={}){
 const active=new Map(),verified=new Set(),progress=new Map();let controller=new AbortController(),job={state:'idle',completed:0,total:0},jobPromise=null,clearing=false;
 const descriptor=()=>spec?Promise.resolve(spec):showcaseSpec();
 async function ensure(name){
  if(clearing)throw Object.assign(Error('Cache is being cleared. Retry in a moment.'),{status:409});
  const d=await descriptor();if(!Object.hasOwn(d.assets,name))throw Object.assign(Error('Showcase asset unavailable'),{status:404});const asset=d.assets[name],file=path.join(root,'showcase',name);
  if(verified.has(name))return file;if(active.has(name))return active.get(name);
  const signal=controller.signal;
  const task=(async()=>{
   try{const b=await readFile(file);if(b.length===asset.bytes&&createHash('sha256').update(b).digest('hex')===asset.sha256){verified.add(name);return file;}}catch(e){if(e.code!=='ENOENT')throw e;}
   let b;
   if(asset.parts){const chunks=[Buffer.from(asset.header,'ascii')];for(const part of asset.parts)chunks.push(await readFile(await ensure(part)));b=Buffer.concat(chunks);}
   else{
    progress.set(name,{name,received:0,total:asset.bytes});let response;
    try{response=await fetcher(d.downloadBase+name,{signal:AbortSignal.any([signal,AbortSignal.timeout(180000)])});}catch{throw Object.assign(Error(signal.aborted?'Download cancelled.':'Guildhall download unavailable. Check your connection and retry.'),{status:502});}
    if(!response.ok)throw Object.assign(Error('Guildhall download unavailable. Check your connection and retry.'),{status:502});
    const chunks=[];let bytes=0;for await(const chunk of response.body){signal.throwIfAborted();bytes+=chunk.length;if(bytes>asset.bytes)throw Object.assign(Error('Guildhall asset exceeds expected size'),{status:502});chunks.push(chunk);progress.set(name,{name,received:bytes,total:asset.bytes});}b=Buffer.concat(chunks);
   }
   signal.throwIfAborted();if(b.length!==asset.bytes||createHash('sha256').update(b).digest('hex')!==asset.sha256)throw Object.assign(Error('Guildhall checksum mismatch; asset not installed'),{status:502});
   await mkdir(path.dirname(file),{recursive:true});const temp=file+'.'+randomUUID()+'.part';try{await writeFile(temp,b);signal.throwIfAborted();await rename(temp,file);}finally{await rm(temp,{force:true});}verified.add(name);return file;
  })();active.set(name,task);try{return await task;}finally{active.delete(name);progress.delete(name);}
 }
 ensure.info=async()=>{
  const d=await descriptor(),names=new Set();let bytes=0;
  try{for(const entry of await readdir(path.join(root,'showcase'),{withFileTypes:true})){if(!entry.isFile()||!Object.hasOwn(d.assets,entry.name))continue;const s=await stat(path.join(root,'showcase',entry.name));if(s.size===d.assets[entry.name].bytes){names.add(entry.name);bytes+=s.size;}}}catch(e){if(e.code!=='ENOENT')throw e;}
  const physical=Object.keys(d.assets).filter(n=>!d.assets[n].parts),referenced=new Set(Object.values(d.assets).flatMap(a=>a.parts??[])),needed=new Set(physical.filter(n=>!referenced.has(n)));for(const [name,asset] of Object.entries(d.assets))if(asset.parts&&!names.has(name))for(const part of asset.parts)needed.add(part);const missingFiles=[...needed].filter(n=>!names.has(n));return {location:'Local app sample cache',bytes,cachedFiles:names.size,downloadBytes:physical.reduce((n,k)=>n+d.assets[k].bytes,0),remainingBytes:missingFiles.reduce((n,k)=>n+d.assets[k].bytes,0),missingFiles,offlineReady:missingFiles.length===0,active:[...progress.values()],job:{...job}};
 };
 ensure.downloadAll=async()=>{
  if(clearing)throw Object.assign(Error('Cache is being cleared'),{status:409});if(job.state==='running')return ensure.info();
  const state=await ensure.info(),names=state.missingFiles;job={state:'running',completed:0,total:names.length};
  jobPromise=(async()=>{try{for(const n of names){if(job.state!=='running')break;await ensure(n);job.completed++;}if(job.state==='running')job.state='complete';}catch(e){if(job.state==='running'){job.state='failed';job.error=e.message;}}})();return ensure.info();
 };
 ensure.cancel=async()=>{if(job.state==='running')job.state='cancelled';controller.abort();await Promise.allSettled([...active.values(),jobPromise].filter(Boolean));controller=new AbortController();return ensure.info();};
 ensure.clear=async()=>{clearing=true;try{await ensure.cancel();await rm(path.join(root,'showcase'),{recursive:true,force:true});verified.clear();job={state:'idle',completed:0,total:0};}finally{clearing=false;}return ensure.info();};
 return ensure;
}
