import {classify,VERSION} from '../relay/worker/index.js';
let input=''; for await (const chunk of process.stdin) input+=chunk;
const records=JSON.parse(input);
console.log(JSON.stringify(records.map(p=>({id:p.id,...classify(p.title,p.html,p.category_id),classifier_version:VERSION}))));
