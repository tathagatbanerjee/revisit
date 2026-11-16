import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import os from 'node:os';import path from 'node:path';import {createHash} from 'node:crypto';
import {createShowcaseCache,showcaseSpec} from '../lib/showcase.mjs';
import {validateRun} from '../lib/contracts.mjs';
test('Guildhall descriptor retains all full-density states, source clock and cameras',async()=>{
 const s=await showcaseSpec(),r=validateRun(s.run);assert.equal(r.id,'guildhall');assert.equal(r.frames.length,305);assert.equal(r.frames[0].time,0);assert.equal(r.frames.at(-1).time,25.333333);assert.equal(r.inspectionViews.length,3);assert.equal(s.license,'CC-BY-SA-4.0');
 for(const name of [s.video,s.poster,...r.frames.map(f=>f.model)]){assert.match(name,/^[a-zA-Z0-9-]+\.(ply|mp4|jpg)$/);assert.ok(s.assets[name].bytes>0);assert.match(s.assets[name].sha256,/^[a-f0-9]{64}$/);}
});
test('showcase cache deduplicates requests, verifies bytes, works offline and rejects unknown assets',async()=>{
 const root=await mkdtemp(path.join(os.tmpdir(),'revisit-showcase-'));try{
 const b=Buffer.from('test model bytes'),spec={downloadBase:'https://example.invalid/',assets:{'state.ply':{bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')}}};let calls=0;
 const cached=createShowcaseCache(root,{spec,fetcher:async url=>{calls++;assert.equal(url,'https://example.invalid/state.ply');return new Response(b);}});
 const [a,c]=await Promise.all([cached('state.ply'),cached('state.ply')]);assert.equal(a,c);assert.equal(calls,1);assert.deepEqual(await readFile(a),b);await assert.rejects(()=>cached('../private.env'),/unavailable/);
 const offline=createShowcaseCache(root,{spec,fetcher:()=>{throw Error('No network');}});assert.equal(await offline('state.ply'),a);
 await writeFile(a,Buffer.from('corrupt'));const corrupt=createShowcaseCache(root,{spec,fetcher:async()=>new Response(Buffer.alloc(b.length))});await assert.rejects(()=>corrupt('state.ply'),/checksum mismatch/);assert.equal((await readFile(a)).toString(),'corrupt');
 }finally{await rm(root,{recursive:true,force:true});}
});
test('shared room and motion parts reconstruct original model bytes and hash',async()=>{
 const root=await mkdtemp(path.join(os.tmpdir(),'revisit-parts-'));try{
 const header='ply\n',parts={'room.bin':Buffer.from('static'),'motion.bin':Buffer.from('dynamic')},b=Buffer.concat([Buffer.from(header),...Object.values(parts)]),asset=bytes=>({bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex')});
 const spec={downloadBase:'https://example.invalid/',assets:{'state.ply':{...asset(b),header,parts:Object.keys(parts)},...Object.fromEntries(Object.entries(parts).map(([k,v])=>[k,asset(v)]))}};
 const cache=createShowcaseCache(root,{spec,fetcher:async url=>new Response(parts[url.split('/').at(-1)])});assert.deepEqual(await readFile(await cache('state.ply')),b);
 }finally{await rm(root,{recursive:true,force:true});}
});
