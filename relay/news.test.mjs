import test from 'node:test';
import assert from 'node:assert/strict';
import worker,{classify,safeUrl,text,collect} from './worker/index.js';
const news='The servers open on Wednesday. Players can reserve their names and prepare their characters for the launch. Additional realm details are now available.';
test('dedicated Forever article can compare another game without becoming mixed',()=>{
 assert.equal(classify('WoW Forever launch',`<h2>What changed</h2><p>${news} Unlike Dragonflight, this uses Classic systems.</p>`,347).kind,'forever');
});
test('roundup identifies only the substantive Forever section',()=>{
 const d=classify('WoW Weekly',`<h2>WoW Forever</h2><p>${news}</p><h2>Midnight</h2><p>${news} New retail raid.</p>`,1);
 assert.equal(d.kind,'mixed');assert.equal(d.section,'WoW Forever');assert.ok(!d.excerpt.includes('retail'));
});
test('passing mention and related-story links are not relevant coverage',()=>{
 assert.equal(classify('Midnight launch',`<article><p>${news} Visit Forever too.</p></article><aside><h2>Forever</h2>${news}</aside>`,1).kind,'unverified');
 assert.equal(classify('News',`<article><p>${news}</p></article><aside>WoW Forever ${news}</aside>`,1).kind,'unrelated');
});
test('short text cannot be classified from a headline alone',()=>assert.equal(classify('Forever launch','<p>Read more</p>',347).kind,'unverified'));
test('unlabelled body-only mentions are held for review',()=>assert.equal(classify('Weekly updates',`<p>${news} WoW Forever is coming soon.</p>`,1).kind,'unverified'));
test('section parser removes scripts and encoded text safely',()=>assert.ok(!text('<script>Forever false</script><p>A &amp; B</p>').includes('false')));
test('relay rejects arbitrary upstreams and unsafe schemes',()=>{
 for(const u of ['https://evil.example/','http://news.blizzard.com/','https://news.blizzard.com@evil.example/','https://news.blizzard.com:8080/'])assert.throws(()=>safeUrl(u));
 assert.equal(safeUrl('https://news.blizzard.com/en-us/article/123').hostname,'news.blizzard.com');
});
test('public endpoint cannot mutate or proxy arbitrary URLs',async()=>{
 assert.equal((await worker.fetch(new Request('https://relay.example/news?url=https://evil.example'))).status,404);
 assert.equal((await worker.fetch(new Request('https://relay.example/news',{method:'POST'}))).status,405);
 assert.equal((await worker.fetch(new Request('https://relay.example/news',{headers:{Origin:'https://evil.example'}}))).status,403);
});
test('failed refresh preserves verified cache and its successful timestamp',async()=>{
 const originalFetch=globalThis.fetch, originalCaches=globalThis.caches;
 const saved={classifier_version:1,fetched:'2026-10-25T12:00:00Z',posts:[{id:4,kind:'forever'}]};let written;
 globalThis.caches={default:{match:async()=>Response.json(saved),put:async(_,response)=>{written=await response.json();}}};
 globalThis.fetch=async()=>{throw Error('upstream unavailable');};
 try {const r=await worker.fetch(new Request('https://relay.example/news'));const d=await r.json();assert.equal(d.fetched,saved.fetched);assert.equal(d.status,'unavailable');assert.deepEqual(d.posts,saved.posts);assert.equal(written.fetched,saved.fetched);}
 finally {globalThis.fetch=originalFetch;globalThis.caches=originalCaches;}
});
test('unverified legacy cache entries cannot leak into the classified feed',async()=>{
 const originalFetch=globalThis.fetch;globalThis.fetch=async()=>Response.json({posts:[]});
 try {const d=await collect({posts:[{id:999,title:'Unrelated',kind:'forever',posted:new Date().toISOString()}]});assert.deepEqual(d.posts,[]);assert.equal(d.status,'ok');}
 finally {globalThis.fetch=originalFetch;}
});
