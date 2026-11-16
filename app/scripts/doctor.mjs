import {spawnSync} from 'node:child_process';
for(const cmd of ['node','ffmpeg','ffprobe','python3','ssh']){const r=spawnSync(cmd,[cmd==='python3'?'--version':cmd==='ssh'?'-V':cmd==='node'?'--version':'-version'],{encoding:'utf8'});console.log(`${cmd}: ${r.error?'MISSING':r.status===0?'available':'check installation'}`);}
console.log('Runpod key: '+(process.env.RUNPOD_API_KEY?'configured in server environment (value hidden)':'not configured; local viewing/preparation still work'));
console.log('Paid reconstruction: not qualified; see docs/runbooks/operations/runpod.md');
