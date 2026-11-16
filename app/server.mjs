import http from 'node:http';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {readFile,readdir,mkdir,stat} from 'node:fs/promises';
import {randomBytes,timingSafeEqual} from 'node:crypto';
import {sendFile,json,readJSON,confined,idOK} from './lib/files.mjs';
import {validateRun} from './lib/contracts.mjs';
import {ensureSample,sampleSpec,syntheticSplat} from './lib/sample.mjs';
import {Projects} from './lib/projects.mjs';
import {Runpod} from './lib/runpod.mjs';
import {setupReport} from './lib/setup.mjs';
import {showcaseSpec,createShowcaseCache} from './lib/showcase.mjs';
const appDir=path.dirname(fileURLToPath(import.meta.url));
export async function createApp({dataRoot=process.env.REVISIT_DATA??path.join(appDir,'../data'),provider=new Runpod()}={}){
 await mkdir(dataRoot,{recursive:true});const projects=new Projects(dataRoot);await projects.recover();
 const showcaseAsset=createShowcaseCache(dataRoot);
 const csrf=randomBytes(32).toString('hex');let downloading=null;
 function trusted(req){
  const host=req.headers.host;if(!host||!['localhost','127.0.0.1','[::1]'].includes(host.replace(/:\d+$/,'')))return false;
  if(req.headers.origin&&req.headers.origin!=='http://'+host)return false;
  if(req.headers['sec-fetch-site']==='cross-site')return false;
  return true;
 }
 async function runs(){const root=path.join(dataRoot,'runs');await mkdir(root,{recursive:true});const result=[];
  for(const d of await readdir(root,{withFileTypes:true})){if(!d.isDirectory()||!idOK(d.name))continue;try{const r=validateRun(JSON.parse(await readFile(await confined(root,d.name+'/run.json'),'utf8')));if(r.id!==d.name)continue;const files=r.representation==='static'?[r.model]:r.frames.map(f=>f.model);for(const f of files)await stat(await confined(root,d.name+'/'+f));result.push(r);}catch{}}
  return result;
 }
 const server=http.createServer(async(req,res)=>{
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');res.setHeader('Cross-Origin-Opener-Policy','same-origin');
  try{
   if(!trusted(req))throw Object.assign(Error('Only same-origin localhost requests are accepted'),{status:403});
   const url=new URL(req.url,'http://'+req.headers.host),p=decodeURIComponent(url.pathname);
   if(!['GET','HEAD','POST','PUT'].includes(req.method))throw Object.assign(Error('Method unavailable'),{status:405});
   if(['POST','PUT'].includes(req.method)){
    const token=req.headers['x-revisit-token']??'';if(!/^[a-f0-9]{64}$/.test(token)||!timingSafeEqual(Buffer.from(token),Buffer.from(csrf)))throw Object.assign(Error('Reload the local app before changing projects'),{status:403});
   }
   if(p==='/api/session'&&req.method==='GET')return json(res,200,{token:csrf});
   if(p==='/health')return json(res,200,{status:'ok',mode:'local-preview',paidAllocationEnabled:false});
   if(p==='/api/catalog'&&req.method==='GET'){
    const sample=await sampleSpec();let installed=false;try{const info=await stat(path.join(dataRoot,'samples/houseplant.splat'));installed=info.size===sample.bytes;}catch{}
    return json(res,200,{sample:{...sample,installed,model:'/samples/houseplant.splat'},showcase:await showcaseSpec(),runs:await runs()});
   }
   if(p==='/api/sample'&&req.method==='POST'){
    downloading??=ensureSample(dataRoot).finally(()=>{downloading=null;});await downloading;return json(res,200,{installed:true});
   }
   if(p==='/api/setup'&&req.method==='GET')return json(res,200,await setupReport(dataRoot));
   if(p==='/api/cache'&&req.method==='GET')return json(res,200,await showcaseAsset.info());
   if(p==='/api/cache/download'&&req.method==='POST')return json(res,202,await showcaseAsset.downloadAll());
   if(p==='/api/cache/cancel'&&req.method==='POST')return json(res,200,await showcaseAsset.cancel());
   if(p==='/api/cache/clear'&&req.method==='POST')return json(res,200,await showcaseAsset.clear());
   if(p==='/api/compute'&&req.method==='GET')return json(res,200,{configured:Boolean(provider.key),paidAllocationEnabled:false,reason:'Worker packaging and independent termination qualification are incomplete. This preview cannot allocate paid workers.'});
   if(p==='/api/compute/verify'&&req.method==='POST')return json(res,200,await provider.verify());
   if(p==='/api/compute/offers'&&req.method==='GET')return json(res,200,{gpus:await provider.offers(),scope:'Advisory GPU list rates; storage/setup additional. No worker allocated.'});
   if(p==='/api/compute/start'&&req.method==='POST')return json(res,200,await provider.create());
   if(p==='/api/projects'&&req.method==='GET')return json(res,200,{projects:await projects.list()});
   if(p==='/api/projects'&&req.method==='PUT')return json(res,201,await projects.upload(req,url.searchParams.get('name')));
   const project=p.match(/^\/api\/projects\/([a-zA-Z0-9_-]+)(?:\/(prepare|cancel|review|map|freeze))?$/);
   if(project){const [,id,action]=project;if(!action&&req.method==='GET')return json(res,200,await projects.get(id));if(req.method!=='POST')throw Object.assign(Error('Method unavailable'),{status:405});if(action==='prepare')return json(res,202,await projects.prepare(id,await readJSON(req)));if(action==='cancel')return json(res,202,await projects.cancel(id));if(action==='review')return json(res,200,await projects.review(id));if(action==='map')return json(res,202,await projects.map(id));if(action==='freeze')return json(res,202,await projects.freeze(id));}
   if(!['GET','HEAD'].includes(req.method))throw Object.assign(Error('Route unavailable'),{status:404});
   if(p.startsWith('/showcase/')){const name=p.slice(10);await showcaseAsset(name);return await sendFile(req,res,path.join(dataRoot,'showcase'),name,['.ply','.mp4','.jpg']);}
   if(p.startsWith('/samples/'))return await sendFile(req,res,path.join(dataRoot,'samples'),p.slice(9),['.splat']);
   if(p.startsWith('/synthetic/')){const match=/^\/synthetic\/(\d+)\.splat$/.exec(p);if(!match||Number(match[1])>39)throw Object.assign(Error('Observation unavailable'),{status:404});const b=syntheticSplat(Number(match[1])/10);res.writeHead(200,{'Content-Type':'application/octet-stream','Content-Length':b.length});res.end(req.method==='HEAD'?undefined:b);return;}
   if(p.startsWith('/artifacts/'))return await sendFile(req,res,path.join(dataRoot,'runs'),p.slice(11),['.ply','.splat']);
   const handoff=p.match(/^\/projects\/([a-zA-Z0-9_-]+)\/handoff$/);if(handoff)return await sendFile(req,res,projects.dir(handoff[1]),'handoff.tar.gz',['.gz']);
   const media=p.match(/^\/projects\/([a-zA-Z0-9_-]+)\/(source|preview\/(\d{5}\.png))$/);
   if(media){const root=projects.dir(media[1]);return await sendFile(req,res,root,media[2]==='source'?'source.video':'prepared/images/'+media[3],media[2]==='source'?null:['.png']);}
   if(p.startsWith('/vendor/three/'))return await sendFile(req,res,path.join(appDir,'node_modules/three'),p.slice(14));
   if(p.startsWith('/vendor/spark/'))return await sendFile(req,res,path.join(appDir,'node_modules/@sparkjsdev/spark/dist'),p.slice(14));
   if(p.startsWith('/docs/'))return await sendFile(req,res,path.join(appDir,'../docs'),p.slice(6),['.md','.json']);
   return await sendFile(req,res,path.join(appDir,'public'),p==='/'?'index.html':p.slice(1),['.html','.js','.css']);
  }catch(e){if(res.headersSent){res.destroy();return;}const status=e.status??(['ENOENT','ENOTDIR'].includes(e.code)?404:e instanceof URIError?400:500);json(res,status,{error:status===500?'Operation failed. Check the input, installed prerequisites and saved project report.':status===404?'File or project unavailable.':e.message});}
 });server.projects=projects;return server;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const server=await createApp(),port=Number(process.env.PORT??4320),host=process.env.HOST??'127.0.0.1';server.listen(port,host,()=>console.log(`Revisit: http://localhost:${port}`));
 const stop=()=>{for(const id of server.projects.active.keys())server.projects.cancel(id).catch(()=>{});server.close(()=>process.exit(0));};process.on('SIGINT',stop);process.on('SIGTERM',stop);
}
