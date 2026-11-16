import path from 'node:path';
import { readFile,mkdir,writeFile,rename,rm } from 'node:fs/promises';
import { createHash,randomUUID } from 'node:crypto';
export const dataDir=path.resolve(process.env.REVISIT_DATA??new URL('../../data/',import.meta.url).pathname);
// Correct relative path from app/lib to repository examples.
export async function sampleSpec(){return JSON.parse(await readFile(new URL('../../examples/houseplant.json',import.meta.url),'utf8'));}
export async function ensureSample(root=dataDir){
  const spec=JSON.parse(await readFile(new URL('../../examples/houseplant.json',import.meta.url),'utf8'));
  const folder=path.join(root,'samples');await mkdir(folder,{recursive:true});const file=path.join(folder,'houseplant.splat');
  try{const b=await readFile(file);if(b.length===spec.bytes&&createHash('sha256').update(b).digest('hex')===spec.sha256)return spec;}catch(e){if(e.code!=='ENOENT')throw e;}
  let result;try{result=await fetch(spec.url,{signal:AbortSignal.timeout(90000),redirect:'error'});}catch{throw Object.assign(Error('Sample download unavailable. Check your network or choose the offline synthetic interaction test.'),{status:502});}if(!result.ok)throw Object.assign(Error('Sample download failed. Check your network and retry.'),{status:502});
  const chunks=[];let count=0;for await(const chunk of result.body){count+=chunk.length;if(count>spec.bytes)throw Error('Sample exceeds expected size');chunks.push(chunk);}const b=Buffer.concat(chunks);
  if(b.length!==spec.bytes||createHash('sha256').update(b).digest('hex')!==spec.sha256)throw Object.assign(Error('Sample checksum mismatch; nothing installed. Retry or use the synthetic test.'),{status:502});
  const temp=file+'.'+randomUUID()+'.part';try{await writeFile(temp,b);await rename(temp,file);}finally{await rm(temp,{force:true});}return spec;
}
export function syntheticSplat(time=0){
 const pts=[];for(let i=0;i<500;i++){const a=i*2.39996323,y=1-2*i/499,s=Math.sqrt(1-y*y);pts.push([Math.cos(a)*s*.55,y*.55,Math.sin(a)*s*.55,90,175,145]);}
 for(let i=0;i<150;i++){const a=i*2.39996323,y=1-2*i/149,s=Math.sqrt(1-y*y);pts.push([Math.cos(time*1.5)*1.05+Math.cos(a)*s*.22,y*.22,Math.sin(time*1.5)*1.05+Math.sin(a)*s*.22,235,159,92]);}
 const out=Buffer.alloc(pts.length*32);pts.forEach((p,i)=>{const o=i*32;for(let j=0;j<3;j++){out.writeFloatLE(p[j],o+j*4);out.writeFloatLE(.035,o+12+j*4);}out[o+24]=p[3];out[o+25]=p[4];out[o+26]=p[5];out[o+27]=240;out[o+28]=255;out[o+29]=128;out[o+30]=128;out[o+31]=128;});return out;
}
