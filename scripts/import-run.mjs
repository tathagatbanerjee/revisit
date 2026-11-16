// Import only a manifest and its referenced splat files. No parent folders/media.
import path from 'node:path';import {readFile,mkdir,copyFile,rename,rm,stat} from 'node:fs/promises';import {randomUUID,createHash} from 'node:crypto';import {fileURLToPath} from 'node:url';
import {validateRun} from '../app/lib/contracts.mjs';import {confined,idOK} from '../app/lib/files.mjs';
export async function importRun(source,destination,id){
 source=path.resolve(source);const raw=JSON.parse(await readFile(path.join(source,'run.json'),'utf8'));
 const run=validateRun({...raw,schemaVersion:1,id:id??raw.id??path.basename(source)});const base=path.resolve(destination);await mkdir(base,{recursive:true});const dest=path.join(base,run.id);
 try{await stat(dest);throw Error('Run already exists; use a new run ID');}catch(e){if(e.code!=='ENOENT')throw e;}
 const temp=path.join(base,'.import-'+randomUUID());await mkdir(temp);try{
 const names=run.representation==='static'?[run.model]:run.frames.map(f=>f.model),hashes={};
 for(const name of new Set(names)){const file=await confined(source,name);if(run.fileHashes?.[name]&&createHash('sha256').update(await readFile(file)).digest('hex')!==run.fileHashes[name])throw Error('Source model checksum mismatch: '+name);const target=path.join(temp,name);await mkdir(path.dirname(target),{recursive:true});await copyFile(file,target);hashes[name]=createHash('sha256').update(await readFile(target)).digest('hex');}
 run.fileHashes=hashes;await import('node:fs/promises').then(m=>m.writeFile(path.join(temp,'run.json'),JSON.stringify(run,null,2)+'\n'));await rename(temp,dest);return {id:run.id,files:Object.keys(hashes).length};
 }catch(e){await rm(temp,{recursive:true,force:true});throw e;}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const [source,id]=process.argv.slice(2);if(!source)throw Error('Usage: node scripts/import-run.mjs /path/to/run-folder [new-id]');
 const root=process.env.REVISIT_DATA??new URL('../data/',import.meta.url).pathname;console.log(await importRun(source,path.join(root,'runs'),id));
}
