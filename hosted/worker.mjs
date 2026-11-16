// ASSETS and CATALOG are injected by build.mjs. Only pinned public files may proxy.
export function worker(ASSETS,CATALOG){
 return {async fetch(request){
  const url=new URL(request.url),p=url.pathname;
  const headers={'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Cross-Origin-Opener-Policy':'same-origin'};
  if(!['GET','HEAD'].includes(request.method))return new Response('This public viewer is read-only. Run Revisit locally to upload videos.',{status:405,headers});
  if(p.startsWith('/showcase/')){
   const name=p.slice(10),asset=CATALOG.showcase.assets[name];if(!Object.hasOwn(CATALOG.showcase.assets,name)||asset.parts)return new Response('Unknown public asset',{status:404,headers});
   const h=new Headers(),range=request.headers.get('Range');if(range&&/^bytes=\d*-\d*$/.test(range))h.set('Range',range);
   try{const upstream=await fetch(CATALOG.showcase.downloadBase+name,{method:request.method,headers:h,redirect:'follow'});if(!upstream.ok&&upstream.status!==416)return new Response('Sample download unavailable; retry shortly.',{status:502,headers});
    const out=new Headers(headers);for(const k of ['Content-Length','Content-Range','Accept-Ranges'])if(upstream.headers.has(k))out.set(k,upstream.headers.get(k));out.set('Content-Type',name.endsWith('.mp4')?'video/mp4':name.endsWith('.jpg')?'image/jpeg':'application/octet-stream');out.set('Cache-Control','public, max-age=86400');return new Response(upstream.body,{status:upstream.status,headers:out});
   }catch{return new Response('Sample download unavailable; retry shortly.',{status:502,headers});}
  }
  const file=ASSETS[p==='/'?'/index.html':p];if(!file)return new Response('Not found',{status:404,headers});return new Response(request.method==='HEAD'?null:file.body,{headers:{...headers,'Content-Type':file.type,'Cache-Control':'no-cache'}});
 }};
}
