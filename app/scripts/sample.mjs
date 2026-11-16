import {ensureSample} from '../lib/sample.mjs';
const s=await ensureSample();console.log(`Verified ${s.title}, ${s.bytes} bytes. ${s.attribution}`);
