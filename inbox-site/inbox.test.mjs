import test from 'node:test';
import assert from 'node:assert/strict';
import worker, {handle, keyLabel, submissionId, containsKey, commitSubmission} from './worker/index.js';

const KEYS = JSON.stringify({'key-1': 'correct-horse-battery-1', 'key-2': 'correct-horse-battery-2'});
const NOW = Date.parse('2026-10-30T12:00:00Z');

import {fakeGitHub, fakeDB} from './test-support.mjs';

// As a browser sends it: a multipart body with its size declared.
async function form(fields, file) {
  const data = new FormData();
  for (const [k, v] of Object.entries(fields)) data.append(k, v);
  if (file) data.append('file', new Blob([file.body]), file.name);
  const draft = new Request('https://inbox.example/submit', {method: 'POST', body: data});
  const body = await draft.arrayBuffer();
  return new Request('https://inbox.example/submit', {method: 'POST', body,
    headers: {accept: 'application/json', 'content-type': draft.headers.get('content-type'), 'content-length': String(body.byteLength)}});
}

const page = {key: 'correct-horse-battery-2', kind: 'page', path: 'content/more/addons.md', version: 'abcdef123456',
              message: 'Addons: WeakAuras still missing', page: '---\nupdated: 2026-10-30\n---\n'};

test('keys are matched to their label, and a wrong key matches nothing', async () => {
  const keys = JSON.parse(KEYS);
  assert.equal(await keyLabel('correct-horse-battery-2', keys), 'key-2');
  assert.equal(await keyLabel('correct-horse-battery', keys), null);
  assert.equal(await keyLabel('', {'key-3': ''}), null);
});

test('ids match what scripts/inbox.py accepts', () => {
  assert.match(submissionId(new Date(NOW), new Uint8Array([1, 2, 171, 255])), /^20261030T120000Z-0102abff$/);
});

test('a page with the right key is committed without the key, labelled', async () => {
  const gh = fakeGitHub(), db = fakeDB();
  const response = await handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: db}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(response.status, 202);
  const record = JSON.parse(gh.calls.find(c => c.path === '/git/blobs').body.content);
  assert.equal(record.key_label, 'key-2');
  assert.equal(record.path, 'content/more/addons.md');
  assert.ok(!JSON.stringify(gh.calls.map(c => c.body)).includes('correct-horse-battery'), 'the key never reaches GitHub');
  const tree = gh.calls.find(c => c.path === '/git/trees').body.tree.map(t => t.path);
  assert.deepEqual(tree, [`inbox/${record.id}/submission.json`, `inbox/${record.id}/page.md`]);
  assert.equal(db.rows.accepted.length, 1);
});

test('a wrong key is refused and logged, and nothing is written', async () => {
  const gh = fakeGitHub(), db = fakeDB();
  const response = await handle(await form({...page, key: 'nope'}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: db}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(response.status, 403);
  assert.equal(gh.calls.length, 0);
  assert.equal(db.rows.refusals.length, 1);
  assert.equal(db.rows.refusals[0][3], "The key isn't right.");
});

test('content containing a key is refused before anything is public', async () => {
  const gh = fakeGitHub();
  const response = await handle(await form({...page, page: 'my key is correct-horse-battery-1'}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(response.status, 400);
  assert.equal(gh.calls.length, 0);
  assert.ok(containsKey(new Uint8Array([0xe2, ...new TextEncoder().encode('xcorrect-horse-battery-2')]), JSON.parse(KEYS)));
  const inNote = await handle(await form({...page, message: 'Addons: correct-horse-battery-2'}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(inNote.status, 400);
  assert.equal(gh.calls.length, 0);
});

test('any addon file is accepted with its own name; a bad name is refused', async () => {
  const gh = fakeGitHub();
  const ok = await handle(await form({key: 'correct-horse-battery-1', kind: 'lua'}, {name: 'AllTheThings.lua', body: 'AllTheThingsAD = {}\n'}),
                          {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(ok.status, 202);
  assert.ok(gh.calls.find(c => c.path === '/git/trees').body.tree.some(t => t.path.endsWith('/AllTheThings.lua')));
  const bad = await handle(await form({key: 'correct-horse-battery-1', kind: 'lua'}, {name: '../evil.lua', body: 'x = 1'}),
                           {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: fakeGitHub().fetcher, now: NOW});
  assert.equal(bad.status, 400);
});

test('limits: a full queue and a busy hour are refused', async () => {
  const full = await handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: fakeGitHub({waiting: 20}).fetcher, now: NOW});
  assert.equal(full.status, 429);
  const db = fakeDB();
  for (let i = 0; i < 30; i++) db.rows.accepted.push([new Date(NOW - 60_000).toISOString()]);
  const busy = await handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: db}, {fetcher: fakeGitHub().fetcher, now: NOW});
  assert.equal(busy.status, 429);
});

test('if main moves, the commit is rebuilt on the new tip', async () => {
  const gh = fakeGitHub({moveOnce: true});
  await commitSubmission({GITHUB_TOKEN: 't'}, 'x', {kind: 'page', received: '2026-10-30T12:00:00Z'}, {name: 'page.md', data: new Uint8Array([65])}, gh.fetcher);
  const commits = gh.calls.filter(c => c.path === '/git/commits' && c.method === 'POST').map(c => c.body.parents[0]);
  assert.deepEqual(commits, ['head1', 'head2']);
});

test('a body without a declared size is refused before it is read', async () => {
  const response = await handle(new Request('https://inbox.example/submit', {method: 'POST', body: new FormData()}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: fakeDB()}, {fetcher: fakeGitHub().fetcher, now: NOW});
  assert.equal(response.status, 411);
});

test('a submission that reached GitHub is reported as received even if the log fails', async () => {
  const db = fakeDB();
  const broken = {...db, prepare(sql) { const s = db.prepare(sql); if (sql.startsWith('UPDATE')) s.run = async () => { throw new Error('db down'); }; return s; }};
  const response = await handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: broken}, {fetcher: fakeGitHub().fetcher, now: NOW});
  assert.equal(response.status, 202);
});

test('reservations count against the hour, so a burst cannot pass the limit together', async () => {
  const db = fakeDB();
  for (let i = 0; i < 29; i++) db.rows.accepted.push([new Date(NOW - 60_000).toISOString(), 'page', 1, `reserved x${i}`]);
  const [a, b] = await Promise.all([1, 2].map(async () => handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't', DB: db}, {fetcher: fakeGitHub().fetcher, now: NOW})));
  assert.deepEqual([a.status, b.status].sort(), [202, 429]);
});

test('only POST /submit receives anything', async () => {
  assert.equal((await worker.fetch(new Request('https://inbox.example/submit'), {})).status, 405);
  assert.equal((await worker.fetch(new Request('https://inbox.example/other', {method: 'POST'}), {})).status, 404);
  assert.equal((await worker.fetch(new Request('https://inbox.example/'), {})).status, 200);
});


test('missing secrets, malformed keys and a missing database close the receiver', async () => {
  for (const env of [{}, {INBOX_KEYS: KEYS, DB: fakeDB()}, {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'},
    {INBOX_KEYS: '[]', GITHUB_TOKEN: 't', DB: fakeDB()},
    {INBOX_KEYS: '{"key-1": ""}', GITHUB_TOKEN: 't', DB: fakeDB()}]) {
    const gh = fakeGitHub();
    const response = await handle(await form(page), env, {fetcher: gh.fetcher, now: NOW});
    assert.equal(response.status, 503);
    assert.equal(gh.calls.length, 0, 'an unconfigured receiver never contacts GitHub');
  }
});

test('health reports configuration without exposing secrets or claiming GitHub access was tested', async () => {
  const missing = await worker.fetch(new Request('https://inbox.example/health'), {});
  assert.equal(missing.status, 503);
  const ready = await worker.fetch(new Request('https://inbox.example/health'), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 'private-token', DB: fakeDB()});
  assert.equal(ready.status, 200);
  assert.equal(ready.headers.get('cache-control'), 'no-store');
  const payload = await ready.text();
  assert.deepEqual(JSON.parse(payload).configured, {keys: true, github: true, database: true});
  assert.ok(!payload.includes('private-token') && !payload.includes('correct-horse-battery'));
  assert.equal(JSON.parse(await missing.text()).ready, false);
});

test('chat reads return the real GitHub blob version and forbid arbitrary paths', async () => {
  const {chatTool} = await import('./worker/index.js');
  const request=new Request('https://example/mcp',{headers:{'oai-authenticated-user-id':'u','oai-authenticated-user-email':'owner@example.com'}});
  const fetcher=async()=>Response.json({type:'file',size:8,encoding:'base64',sha:'a'.repeat(40),content:btoa('# Map\n'),html_url:'https://github.com/faresbn/Tazdingo/blob/main/feed/index.md'});
  const result=await chatTool('read_tazdingo',{},request,{GITHUB_TOKEN:'t'},fetcher);
  assert.equal(result.version,'a'.repeat(12));assert.equal(result.content,'# Map\n');
  await assert.rejects(()=>chatTool('read_tazdingo',{path:'scripts/inbox.py'},request,{},fetcher));
});

test('chat writes require a verified identity and an explicit writer grant', async () => {
  const {chatTool}=await import('./worker/index.js');const gh=fakeGitHub();
  const env={INBOX_KEYS:KEYS,GITHUB_TOKEN:'t',DB:fakeDB(),MCP_WRITERS:JSON.stringify({'owner@example.com':'key-1'})};
  const args={path:page.path,version:page.version,page:page.page,message:page.message};
  await assert.rejects(()=>chatTool('submit_tazdingo_page',args,new Request('https://example/mcp'),env,gh.fetcher));
  const stranger=new Request('https://example/mcp',{headers:{'oai-authenticated-user-id':'other','oai-authenticated-user-email':'other@example.com'}});
  await assert.rejects(()=>chatTool('submit_tazdingo_page',args,stranger,env,gh.fetcher));
  assert.equal(gh.calls.length,0);
  const owner=new Request('https://example/mcp',{headers:{'oai-authenticated-user-id':'owner','oai-authenticated-user-email':'owner@example.com'}});
  const received=await chatTool('submit_tazdingo_page',args,owner,env,gh.fetcher);
  assert.equal(received.outcome,'received');assert.match(received.id,/^\d{8}T\d{6}Z-[a-f0-9]{8}$/);
  assert.ok(!JSON.stringify(gh.calls.map(c=>c.body)).includes('correct-horse-battery'));
});

test('MCP discovery and tool listing work, and errors are tool errors', async () => {
  const {mcp}=await import('./worker/index.js');
  const invoke=async(method,params)=> (await mcp(new Request('https://example/mcp',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:1,method,params}),headers:{'content-type':'application/json'}}),{})).json();
  assert.deepEqual((await invoke('server/discover')).result.supportedVersions,['2026-07-28']);
  assert.equal((await invoke('tools/list')).result.tools.length,4);
  assert.equal((await invoke('tools/call',{name:'submit_tazdingo_page',arguments:{}})).result.isError,true);
});
