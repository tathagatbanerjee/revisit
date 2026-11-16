import {readdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
async function visit(dir){for(const e of await readdir(dir,{withFileTypes:true})){if(['node_modules','.cache'].includes(e.name))continue;const p=path.join(dir,e.name);if(e.isDirectory())await visit(p);else if(/\.(mjs|js)$/.test(p)){const r=spawnSync(process.execPath,['--check',p],{stdio:'inherit'});if(r.status)process.exit(r.status);}}}
await visit(new URL('../',import.meta.url).pathname);
