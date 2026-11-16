import {OfflineStore} from './offline-store.js';
const SHELL='revisit-shell-v1';let storePromise,lastNotice=0;
function notify(){if(Date.now()-lastNotice<200)return;lastNotice=Date.now();self.clients.matchAll().then(clients=>clients.forEach(c=>c.postMessage({type:'cache-progress'})));}
async function store(){return storePromise??=fetch('/api/catalog').then(r=>r.json()).then(c=>new OfflineStore(c.showcase,{notify}));}
self.addEventListener('install',e=>e.waitUntil((async()=>{const cache=await caches.open(SHELL),files=await (await fetch('/offline-files.json')).json();await cache.addAll(files);await self.skipWaiting();})()));
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const name of await caches.keys())if(name.startsWith('revisit-shell-')&&name!==SHELL)await caches.delete(name);await self.clients.claim();})()));
// Cache manifest survives offline startup; do not require a network call to use it.
async function cachedStore(){if(storePromise)return storePromise;const cache=await caches.open(SHELL),r=await cache.match('/api/catalog');if(r){const c=await r.json();storePromise=Promise.resolve(new OfflineStore(c.showcase,{notify}));return storePromise;}return store();}
async function media(request){
 const s=await cachedStore(),name=new URL(request.url).pathname.slice(10);if(!Object.hasOwn(s.spec.assets,name))return new Response('Unknown sample asset',{status:404});
 try{const bytes=await s.ensure(name),headers={'Content-Type':name.endsWith('.ply')?'application/octet-stream':name.endsWith('.mp4')?'video/mp4':name.endsWith('.jpg')?'image/jpeg':'application/octet-stream','Accept-Ranges':'bytes'};let start=0,end=bytes.length-1,code=200;
 if(request.headers.has('Range')){const m=/^bytes=(\d*)-(\d*)$/.exec(request.headers.get('Range'));if(!m||(!m[1]&&!m[2]))return new Response(null,{status:416,headers:{'Content-Range':'bytes */'+bytes.length}});if(m[1]){start=Number(m[1]);if(m[2])end=Number(m[2]);}else start=Math.max(0,bytes.length-Number(m[2]));end=Math.min(end,bytes.length-1);if(start>end||start>=bytes.length)return new Response(null,{status:416,headers:{'Content-Range':'bytes */'+bytes.length}});code=206;headers['Content-Range']=`bytes ${start}-${end}/${bytes.length}`;}
 headers['Content-Length']=String(end-start+1);return new Response(request.method==='HEAD'?null:bytes.slice(start,end+1),{status:code,headers});
 }catch(e){return new Response(e.message,{status:503});}
}
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==location.origin||!['GET','HEAD'].includes(e.request.method))return;if(u.pathname.startsWith('/showcase/')){e.respondWith(media(e.request));return;}e.respondWith((async()=>{const cache=await caches.open(SHELL),key=u.pathname==='/'?'/':u.pathname;const saved=await cache.match(key);return saved??fetch(e.request);})());});
self.addEventListener('message',e=>{e.waitUntil((async()=>{try{const s=await cachedStore();let result;if(e.data.action==='download'){e.waitUntil(s.downloadAll());result=await s.info();}else if(e.data.action==='clear')result=await s.clear();else if(e.data.action==='cancel')result=await s.cancel();else result=await s.info();e.ports[0]?.postMessage({ok:true,result});}catch(error){e.ports[0]?.postMessage({ok:false,error:error.message});}})());});
