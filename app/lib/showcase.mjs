// Fixed, checksummed public research assets. No user-controlled download URLs.
import path from 'node:path';
import {readFile,mkdir,writeFile,rename,rm} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
export async function showcaseSpec(){return JSON.parse(await readFile(new URL('../../examples/guildhall.json',import.meta.url),'utf8'));}
export function createShowcaseCache(root,{spec,fetcher=fetch}={}){
 const active=new Map(),verified=new Set();
 async function ensure(name){
  const descriptor=spec??await showcaseSpec(),asset=descriptor.assets[name];
  if(!Object.hasOwn(descriptor.assets,name))throw Object.assign(Error('Showcase asset unavailable'),{status:404});
  const file=path.join(root,'showcase',name);
  if(verified.has(name))return file;
  if(active.has(name))return active.get(name);
  const task=(async()=>{
   try{const b=await readFile(file);if(b.length===asset.bytes&&createHash('sha256').update(b).digest('hex')===asset.sha256){verified.add(name);return file;}}catch(e){if(e.code!=='ENOENT')throw e;}
   let b;
   if(asset.parts){
    const chunks=[Buffer.from(asset.header,'ascii')];for(const part of asset.parts)chunks.push(await readFile(await ensure(part)));b=Buffer.concat(chunks);
   }else{
    let response;try{response=await fetcher(descriptor.downloadBase+name,{signal:AbortSignal.timeout(180000)});}catch{throw Object.assign(Error('Guildhall download unavailable. Check your connection and retry.'),{status:502});}
    if(!response.ok)throw Object.assign(Error('Guildhall download unavailable. Check your connection and retry.'),{status:502});
    const chunks=[];let bytes=0;for await(const chunk of response.body){bytes+=chunk.length;if(bytes>asset.bytes)throw Object.assign(Error('Guildhall asset exceeds expected size'),{status:502});chunks.push(chunk);}b=Buffer.concat(chunks);
   }
   if(b.length!==asset.bytes||createHash('sha256').update(b).digest('hex')!==asset.sha256)throw Object.assign(Error('Guildhall checksum mismatch; asset not installed'),{status:502});
   await mkdir(path.dirname(file),{recursive:true});const temp=file+'.'+randomUUID()+'.part';try{await writeFile(temp,b);await rename(temp,file);}finally{await rm(temp,{force:true});}verified.add(name);return file;
  })();active.set(name,task);try{return await task;}finally{active.delete(name);}
 }
 return ensure;
}
