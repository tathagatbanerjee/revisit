// Browser cache contains only pinned public sample parts, never uploads or keys.
export class OfflineStore{
 constructor(spec,{storage=caches,fetcher=fetch,origin=location.origin,notify=()=>{}}={}){Object.assign(this,{spec,storage,fetcher,origin,notify});this.name='revisit-guildhall-v1';this.active=new Map();this.progress=new Map();this.job={state:'idle',completed:0,total:0};this.controller=new AbortController();this.clearing=false;}
 key(name){return this.origin+'/showcase/'+name;}
 async check(bytes,asset){if(bytes.length!==asset.bytes)throw Error('Unexpected download size');const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');if(digest!==asset.sha256)throw Error('Checksum mismatch; retry the download.');return bytes;}
 async ensure(name){
  if(this.clearing)throw Error('Cache is being cleared. Retry shortly.');if(!Object.hasOwn(this.spec.assets,name))throw Error('Unknown public sample asset');if(this.active.has(name))return this.active.get(name);
  const asset=this.spec.assets[name],signal=this.controller.signal;
  const task=(async()=>{
   const cache=await this.storage.open(this.name);
   if(asset.parts){const parts=[new TextEncoder().encode(asset.header)];for(const p of asset.parts)parts.push(await this.ensure(p));const bytes=new Uint8Array(parts.reduce((n,p)=>n+p.length,0));let offset=0;for(const p of parts){bytes.set(p,offset);offset+=p.length;}return this.check(bytes,asset);}
   const saved=await cache.match(this.key(name));if(saved){try{return await this.check(new Uint8Array(await saved.arrayBuffer()),asset);}catch{await cache.delete(this.key(name));}}
   const response=await this.fetcher.call(globalThis,this.key(name),{signal:AbortSignal.any([signal,AbortSignal.timeout(180000)])});if(!response.ok)throw Error('Download unavailable. Check your connection and retry.');
   const reader=response.body.getReader(),chunks=[];let size=0;this.progress.set(name,{name,received:0,total:asset.bytes});this.notify();
   try{while(true){const {done,value}=await reader.read();if(done)break;signal.throwIfAborted();size+=value.length;if(size>asset.bytes){await reader.cancel();throw Error('Unexpected download size');}chunks.push(value);this.progress.set(name,{name,received:size,total:asset.bytes});this.notify();}}finally{reader.releaseLock();}
   const bytes=new Uint8Array(size);let offset=0;for(const part of chunks){bytes.set(part,offset);offset+=part.length;}await this.check(bytes,asset);signal.throwIfAborted();
   try{await cache.put(this.key(name),new Response(bytes));}catch{throw Error('Browser storage is full. Clear the Guildhall cache or use the local app.');}return bytes;
  })();this.active.set(name,task);try{return await task;}finally{this.active.delete(name);this.progress.delete(name);this.notify();}
 }
 async info(){
  const cache=await this.storage.open(this.name),keys=await cache.keys(),names=new Set(keys.map(k=>new URL(k.url).pathname.split('/').at(-1))),physical=Object.keys(this.spec.assets).filter(n=>!this.spec.assets[n].parts);return {location:'This browser’s public sample cache',bytes:physical.filter(n=>names.has(n)).reduce((n,k)=>n+this.spec.assets[k].bytes,0),cachedFiles:names.size,downloadBytes:physical.reduce((n,k)=>n+this.spec.assets[k].bytes,0),remainingBytes:physical.filter(n=>!names.has(n)).reduce((n,k)=>n+this.spec.assets[k].bytes,0),offlineReady:physical.every(n=>names.has(n)),active:[...this.progress.values()],job:{...this.job}};
 }
 async downloadAll(){
  if(this.clearing)throw Error('Cache is being cleared');if(this.job.state==='running')return this.jobPromise;const names=Object.keys(this.spec.assets).filter(n=>!this.spec.assets[n].parts);this.job={state:'running',completed:0,total:names.length};this.notify();
  this.jobPromise=(async()=>{try{for(const n of names){if(this.job.state!=='running')break;await this.ensure(n);this.job.completed++;}if(this.job.state==='running')this.job.state='complete';}catch(e){if(this.job.state==='running'){this.job.state='failed';this.job.error=e.message;}}this.notify();})();return this.jobPromise;
 }
 async cancel(){if(this.job.state==='running')this.job.state='cancelled';this.controller.abort();await Promise.allSettled([...this.active.values(),this.jobPromise].filter(Boolean));this.controller=new AbortController();return this.info();}
 async clear(){this.clearing=true;try{await this.cancel();await this.storage.delete(this.name);this.job={state:'idle',completed:0,total:0};}finally{this.clearing=false;}return this.info();}
}
