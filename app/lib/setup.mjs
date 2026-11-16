import {statfs} from 'node:fs/promises';
export async function setupReport(root){
 let freeBytes=null;try{const s=await statfs(root,{bigint:true});freeBytes=Number(s.bavail*s.bsize);}catch{}
 return {mode:process.env.REVISIT_DATA==='/data'?'Docker container':'Native Node',node:process.versions.node,freeBytes,checks:[{name:'Local service',ok:true,message:'The local service is reachable.'},{name:'Sample storage',ok:freeBytes===null?null:freeBytes>=128*1024**2,message:freeBytes===null?'Disk availability could not be measured. Check your data drive.':freeBytes<128*1024**2?'Free at least 128 MiB on the sample-cache drive before opening Guildhall.':'Enough free space for the first Guildhall state. Allow 12 GB for the complete expanded local cache.'}],paidAllocationEnabled:false};
}
