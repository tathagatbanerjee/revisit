// Runpod REST v2. Account key remains in the local backend environment.
export class Runpod{
 constructor({key=process.env.RUNPOD_API_KEY,fetcher=fetch}={}){this.key=key;this.fetcher=fetcher;}
 async request(method,route,body){
  if(!this.key)throw Object.assign(Error('Set RUNPOD_API_KEY in the server environment and restart. Never put it in a video or run manifest.'),{status:400});
  let response;try{response=await this.fetcher('https://api.runpod.io/v2'+route,{method,headers:{Authorization:'Bearer '+this.key,'Content-Type':'application/json'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(20000)});}catch{throw Object.assign(Error('Runpod could not be reached. Resource status is unknown; check the provider console.'),{status:502});}
  if(!response.ok){if(response.status===404)return null;throw Object.assign(Error(response.status===401||response.status===403?'Runpod authentication failed. Check the local API key permissions.':'Runpod request failed; check the provider console. No automatic allocation retry.'),{status:502});}
  return response.status===204?null:response.json();
 }
 async verify(){const account=await this.request('GET','/account');if(!account?.id)throw Error('Runpod account response is invalid');return {verified:true,scope:'Read-only account access; no worker allocated'};}
 async offers(){const d=await this.request('GET','/catalog/gpus?include=AVAILABILITY&product=POD&cloud=SECURE&count=1');return (d?.gpus??[]).map(g=>({id:g.id,memory:g.memory,price:g.price,availability:g.availability}));}
 async get(id){if(!/^[a-zA-Z0-9_-]{1,80}$/.test(id))throw Error('Invalid pod ID');return this.request('GET','/pods/'+encodeURIComponent(id));}
 async terminateOwned(job){if(!job.podId||!job.name)throw Error('No owned worker receipt');const pod=await this.get(job.podId);if(pod&&pod.name!==job.name)throw Error('Ownership mismatch; refusing termination');if(pod)await this.request('DELETE','/pods/'+encodeURIComponent(job.podId));const remaining=await this.get(job.podId);return {verifiedAbsent:remaining===null,resourceState:remaining===null?'terminated':'unknown'};}
 async create(){throw Object.assign(Error('Paid allocation is disabled in this preview. Independent termination and end-to-end qualification are not complete. No worker was created.'),{status:409});}
}
