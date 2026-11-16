import path from 'node:path';
import { realpath, stat } from 'node:fs/promises';
import { createReadStream } from 'node:fs';
export const idOK = s => typeof s === 'string' && /^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$/.test(s);
export function relativeFile(s) {
  return typeof s === 'string' && s.length < 240 && !s.includes('\\') && !s.includes(':') && !s.includes('\0') && !path.isAbsolute(s) && s.split('/').every(p => p && p !== '.' && p !== '..') && /\.(ply|splat)$/i.test(s);
}
export async function confined(root, name) {
  const base = await realpath(root), file = await realpath(path.resolve(base, name));
  if (!file.startsWith(base + path.sep)) throw Object.assign(new Error('Path outside allowed folder'), { status: 403 });
  return file;
}
const types = { '.html':'text/html; charset=utf-8', '.css':'text/css', '.js':'text/javascript', '.mjs':'text/javascript', '.json':'application/json', '.png':'image/png', '.jpg':'image/jpeg', '.mp4':'video/mp4', '.webm':'video/webm', '.mov':'video/quicktime', '.md':'text/plain; charset=utf-8' };
export async function sendFile(req, res, root, name, allowed) {
  if (allowed && !allowed.includes(path.extname(name).toLowerCase())) throw Object.assign(new Error('Unsupported file'), {status:403});
  const file = await confined(root,name), info = await stat(file);
  if (!info.isFile()) throw Object.assign(new Error('Not a file'),{status:404});
  let start=0,end=info.size-1,code=200;
  const headers={'Content-Type':types[path.extname(file)]??'application/octet-stream','Accept-Ranges':'bytes','Cache-Control':'no-cache'};
  if(req.headers.range) {
    const m=/^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
    if(!m || (!m[1]&&!m[2])) {res.writeHead(416,{'Content-Range':`bytes */${info.size}`});res.end();return;}
    if(m[1]) {start=Number(m[1]);if(m[2])end=Number(m[2]);} else start=Math.max(0,info.size-Number(m[2]));
    end=Math.min(end,info.size-1);
    if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start>end||start>=info.size){res.writeHead(416,{'Content-Range':`bytes */${info.size}`});res.end();return;}
    headers['Content-Range']=`bytes ${start}-${end}/${info.size}`;code=206;
  }
  headers['Content-Length']=Math.max(0,end-start+1);res.writeHead(code,headers);
  if(req.method==='HEAD'||!info.size){res.end();return;}
  const stream=createReadStream(file,{start,end});stream.on('error',()=>res.destroy());res.on('close',()=>stream.destroy());stream.pipe(res);
}
export function json(res,status,value){res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(value));}
export async function readJSON(req,max=65536){let chunks=[],n=0;for await(const c of req){n+=c.length;if(n>max)throw Object.assign(new Error('Request too large'),{status:413});chunks.push(c);}try{return JSON.parse(Buffer.concat(chunks).toString());}catch{throw Object.assign(new Error('Invalid JSON'),{status:400});}}
