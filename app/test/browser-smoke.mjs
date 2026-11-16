// Real Chromium/WebGL smoke test using its DevTools protocol; no cloud credentials.
import {spawn} from 'node:child_process';import {mkdir,readFile,writeFile,rm} from 'node:fs/promises';import path from 'node:path';import {randomUUID} from 'node:crypto';
const root=new URL('../../',import.meta.url).pathname,work=path.join(root,'working/browser-'+randomUUID());await mkdir(work,{recursive:true});
const chrome=spawn(process.env.CHROME_PATH??'/opt/google/chrome/chrome',['--headless=new','--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader','--use-angle=swiftshader','--remote-debugging-port=0','--user-data-dir='+work,'about:blank'],{stdio:'ignore'});
let ws;let seq=0;const pending=new Map();
const delay=ms=>new Promise(r=>setTimeout(r,ms));
try{
 let port;for(let i=0;i<100;i++){try{port=Number((await readFile(path.join(work,'DevToolsActivePort'),'utf8')).split('\n')[0]);break;}catch{await delay(100);}}
 if(!port)throw Error('Chromium did not start');const target=await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);if(m.error)p.reject(Error(m.error.message));else p.resolve(m.result);}});
 function call(method,params={}){return new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});}
 async function js(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.text);return r.result.value;}
 async function until(expression,timeout=90000){const end=Date.now()+timeout;while(Date.now()<end){if(await js(expression))return;await delay(300);}throw Error('Timed out: '+expression);}
 await call('Page.enable');await call('Runtime.enable');await call('Emulation.setDeviceMetricsOverride',{width:1280,height:1000,deviceScaleFactor:1,mobile:false});await call('Page.navigate',{url:process.env.VIEWER_URL??'http://127.0.0.1:4320'});
 await until("Boolean(document.querySelector('#sample') && !document.querySelector('#sample').disabled && window.revisitInspection)");
 await js("document.querySelector('#sample').click()");await until("window.revisitInspection().points===113648 && !window.revisitInspection().loading && !document.querySelector('#sample').disabled");
 const real=await js('window.revisitInspection()');await js("document.querySelector('[data-move=right]').click()");const shifted=await js('window.revisitInspection()');if(JSON.stringify(real.position)===JSON.stringify(shifted.position))throw Error('Camera translation failed');
 await js("document.querySelector('#run').value='synthetic';document.querySelector('#run').dispatchEvent(new Event('change'))");await until('window.revisitInspection().points===650 && !window.revisitInspection().loading');
 await js("document.querySelector('[data-move=right]').click()");const before=await js('window.revisitInspection()');await js("document.querySelector('#time').value='1.2';document.querySelector('#time').dispatchEvent(new Event('input'))");await until('window.revisitInspection().loadedFrame===12 && !window.revisitInspection().loading');const after=await js('window.revisitInspection()');
 const delta=Math.max(...after.position.map((x,i)=>Math.abs(x-before.position[i])));if(delta>1e-6)throw Error('Time seek moved camera by '+delta);
 await js("document.querySelector('#play').click()");await until('window.revisitInspection().time>1.3',15000);await js("document.querySelector('#play').click()");
 await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});await delay(1000);if(await js('document.documentElement.scrollWidth>window.innerWidth+1'))throw Error('Mobile horizontal overflow');
 const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});const dest=path.join(root,'working/browser-mobile.png');await writeFile(dest,Buffer.from(shot.data,'base64'));
 const record={date:'2026-11-16',realSampleGaussians:real.points,syntheticGaussians:after.points,seekCameraMaxDelta:delta,translation:true,playback:true,mobileOverflow:false,renderer:'Chromium headless SwiftShader',scope:'Real sample loading, navigation, synthetic time/camera independence and mobile layout. No real reconstruction or paid allocation.'};await writeFile(path.join(root,'docs/testing/browser-smoke.json'),JSON.stringify(record,null,2)+'\n');console.log(JSON.stringify(record,null,2));
}finally{ws?.close();chrome.kill('SIGKILL');setTimeout(()=>rm(work,{recursive:true,force:true}).catch(()=>{}),500);}
