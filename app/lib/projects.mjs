import path from 'node:path';
import {mkdir,readFile,writeFile,rename,readdir,rm} from 'node:fs/promises';
import {createWriteStream,createReadStream} from 'node:fs';
import {pipeline} from 'node:stream/promises';
import {Transform} from 'node:stream';
import {randomUUID,createHash} from 'node:crypto';
import {run,stop} from './process.mjs';
import {idOK} from './files.mjs';
import {interval} from './contracts.mjs';
export class Projects{
 constructor(root){this.root=path.join(root,'projects');this.active=new Map();this.cancelled=new Set();}
 dir(id){if(!idOK(id))throw Object.assign(Error('Invalid project'),{status:400});return path.join(this.root,id);}
 async save(p){const dir=this.dir(p.id);await mkdir(dir,{recursive:true});const temp=path.join(dir,randomUUID()+'.json.part');await writeFile(temp,JSON.stringify(p,null,2)+'\n');await rename(temp,path.join(dir,'project.json'));return p;}
 async get(id){return JSON.parse(await readFile(path.join(this.dir(id),'project.json'),'utf8'));}
 async list(){await mkdir(this.root,{recursive:true});const result=[];for(const e of await readdir(this.root,{withFileTypes:true})){if(e.isDirectory()&&idOK(e.name)){try{result.push(await this.get(e.name));}catch{}}}return result.sort((a,b)=>b.created.localeCompare(a.created));}
 async recover(){for(const p of await this.list())if(['UPLOADING','PROBING','PREPARING','MAPPING','PACKAGING'].includes(p.state)){p.state='INTERRUPTED';p.error='Local app stopped during preparation. Upload a new attempt; prior evidence is retained.';await this.save(p);}}
 async upload(req,name){
  const p={schemaVersion:1,id:randomUUID(),title:String(name??'My video').replace(/[\x00-\x1f]/g,'').slice(0,120),created:new Date().toISOString(),state:'UPLOADING',mode:'static',compute:'not allocated'};
  await this.save(p);const dest=path.join(this.dir(p.id),'source.video');let bytes=0;const hash=createHash('sha256');
  const limit=1024**3;const meter=new Transform({transform(chunk,enc,callback){bytes+=chunk.length;if(bytes>limit)return callback(Object.assign(Error('Video exceeds 1 GiB limit. Trim it before upload.'),{status:413}));hash.update(chunk);callback(null,chunk);}});
  try{await pipeline(req,meter,createWriteStream(dest+'.part',{flags:'wx'}));if(bytes===0)throw Error('Empty video');await rename(dest+'.part',dest);p.bytes=bytes;p.sha256=hash.digest('hex');p.state='PROBING';await this.save(p);this.probe(p);return p;}
  catch(e){p.state='FAILED';p.error='Upload failed: '+e.message;await this.save(p);await rm(dest+'.part',{force:true});throw e;}
 }
 async probe(p){try{
  const output=await run('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=width,height,codec_name:format=duration','-of','json',path.join(this.dir(p.id),'source.video')],{onChild:c=>this.active.set(p.id,c)});
  const d=JSON.parse(output),v=d.streams?.[0],duration=Number(d.format?.duration);if(!v||!Number.isFinite(duration)||duration<=0||duration>600)throw Error('Use a video with a readable duration of at most 10 minutes.');
  p.video={...v,durationSeconds:duration};p.state='INPUT_READY';p.error=null;
 }catch(e){p.state=this.cancelled.has(p.id)?'CANCELLED':'FAILED';p.error=this.cancelled.has(p.id)?'Local preparation cancelled; partial evidence is retained.':e.message;}finally{this.active.delete(p.id);await this.save(p);}}
 async prepare(id,body){const p=await this.get(id);if(this.active.has(id))throw Object.assign(Error('This project is busy'),{status:409});if(p.state!=='INPUT_READY')throw Object.assign(Error('Use a new upload for a new attempt; failed and completed attempts are retained.'),{status:409});
  p.config={id,source:'source.video',...interval(body,p.video.durationSeconds)};
  if(Math.abs(p.video.width/p.video.height-16/9)>.02)throw Object.assign(Error('The initial recipe requires a landscape 16:9 video. Crop a copy first; the original remains unchanged.'),{status:400});
  p.state='PREPARING';p.error=null;await this.save(p);
  this.extract(p);return p;
 }
 async extract(p){try{
  const dir=this.dir(p.id),cfg=path.join(dir,'config.json');await writeFile(cfg,JSON.stringify(p.config,null,2));
  const script=new URL('../../core-pipeline/runner/prepare_video.py',import.meta.url).pathname;
  const result=await run('python3',[script,dir],{timeout:300000,onChild:c=>this.active.set(p.id,c)});
  p.preparation=JSON.parse(result);p.state='SOURCE_REVIEW';p.nextAction='Inspect all six previews for cuts, blur and changing scenes. Confirm source continuity to prepare a reconstruction handoff. Camera mapping has not run yet.';
 }catch(e){p.state=this.cancelled.has(p.id)?'CANCELLED':'FAILED';p.error=this.cancelled.has(p.id)?'Local preparation cancelled; partial evidence is retained.':e.message;p.nextAction='Try a sharper continuous clip with overlapping stationary detail. Create a new upload to preserve this failed attempt.';}finally{this.active.delete(p.id);await this.save(p);}}
 async review(id){const p=await this.get(id);if(p.state!=='SOURCE_REVIEW')throw Object.assign(Error('Source is not ready for review'),{status:409});p.state='SOURCE_APPROVED';p.sourceReview={passed:true,time:new Date().toISOString(),scope:'User reviewed source continuity only; not camera geometry'};p.nextAction='Source approved. Run the advanced camera-mapping stage; paid reconstruction remains unavailable until lifecycle qualification.';await this.save(p);return p;}
 async map(id){const p=await this.get(id);if(p.state!=='SOURCE_APPROVED'||this.active.has(id))throw Object.assign(Error('Approve source continuity before camera recovery'),{status:409});p.state='MAPPING';await this.save(p);this.mapWorker(p);return p;}
 async mapWorker(p){try{const script=new URL('../../core-pipeline/runner/map_video.py',import.meta.url).pathname;await run(process.env.REVISIT_PREP_PYTHON??'python3',[script,this.dir(p.id)],{timeout:900000,onChild:c=>this.active.set(p.id,c)});p.mapping=JSON.parse(await readFile(path.join(this.dir(p.id),'mapping/map-result.json'),'utf8'));p.state='CAMERAS_READY';p.nextAction='Static cameras pass numeric checks. Geometry/priors still require native review. Export an isolated worker handoff for advanced use.';}catch(e){p.state=this.cancelled.has(p.id)?'CANCELLED':'FAILED';p.error=this.cancelled.has(p.id)?'Local preparation cancelled; partial evidence is retained.':e.message;p.nextAction='Check the saved mapping report and capture overlapping stationary detail. Use Docker for the pinned CPU dependencies. A new attempt preserves this failure.';}finally{this.active.delete(p.id);await this.save(p);}}
 async freeze(id){const p=await this.get(id);if(p.state!=='CAMERAS_READY'||this.active.has(id))throw Object.assign(Error('Passing static camera recovery is required'),{status:409});p.state='PACKAGING';await this.save(p);this.freezeWorker(p);return p;}
 async freezeWorker(p){try{await run('python3',[new URL('../../core-pipeline/runner/freeze.py',import.meta.url).pathname,this.dir(p.id),path.join(this.dir(p.id),'handoff')],{timeout:120000,onChild:c=>this.active.set(p.id,c)});p.state='HANDOFF_READY';p.handoff='/projects/'+p.id+'/handoff';p.nextAction='Worker input bundle is ready. It contains frames and configuration, not credentials or third-party weights. Native worker execution and paid lifecycle remain unqualified.';}catch(e){p.state=this.cancelled.has(p.id)?'CANCELLED':'FAILED';p.error=this.cancelled.has(p.id)?'Local preparation cancelled; partial evidence is retained.':e.message;}finally{this.active.delete(p.id);await this.save(p);}}
 async cancel(id){const p=await this.get(id);if(!this.active.has(id))throw Object.assign(Error('No local process is active'),{status:409});this.cancelled.add(id);stop(this.active.get(id));return {id,state:'CANCELLING',compute:'not allocated'};}
}
