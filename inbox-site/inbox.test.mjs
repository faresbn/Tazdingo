import test from 'node:test';
import assert from 'node:assert/strict';
import worker, {handle, keyLabel, submissionId, containsKey, commitSubmission} from './worker/index.js';

const KEYS = JSON.stringify({'key-1': 'correct-horse-battery-1', 'key-2': 'correct-horse-battery-2'});
const NOW = Date.parse('2026-10-30T12:00:00Z');

// A fake GitHub: records what was written and can reject the first ref update (main moved).
function fakeGitHub({waiting = 0, moveOnce = false} = {}) {
  const calls = [];
  let moved = !moveOnce, head = 1;
  const fetcher = async (url, init = {}) => {
    const path = url.replace('https://api.github.com/repos/faresbn/Tazdingo', '');
    const body = init.body ? JSON.parse(init.body) : null;
    calls.push({path, method: init.method || 'GET', body, auth: init.headers.authorization});
    const ok = data => new Response(JSON.stringify(data), {status: 200});
    if (path.startsWith('/contents/inbox')) return ok(Array.from({length: waiting}, (_, i) => ({type: 'dir', name: `w${i}`})).concat([{type: 'dir', name: 'held'}]));
    if (path === '/git/blobs') return ok({sha: `blob${calls.length}`});
    if (path === '/git/ref/heads/main') return ok({object: {sha: `head${head}`}});
    if (path.startsWith('/git/commits/')) return ok({tree: {sha: `tree-of-${path.split('/').pop()}`}});
    if (path === '/git/trees') return ok({sha: `tree${calls.length}`});
    if (path === '/git/commits') return ok({sha: `commit-on-${body.parents[0]}`});
    if (path === '/git/refs/heads/main') {
      if (!moved) { moved = true; head = 2; return new Response('{}', {status: 422}); }
      return ok({});
    }
    return new Response('{}', {status: 404});
  };
  return {fetcher, calls};
}

function fakeDB() {
  const rows = {accepted: [], refusals: []};
  return {rows, prepare(sql) {
    let args = [];
    const table = (sql.match(/(?:INTO|FROM|UPDATE|EXISTS) (accepted|refusals)/) || [])[1];
    return {
      bind(...a) { args = a; return this; },
      async run() {
        if (sql.startsWith('INSERT')) rows[table].push(args);
        else if (sql.startsWith('DELETE') && sql.includes('reason')) rows[table] = rows[table].filter(r => r[3] !== args[0]);
        else if (sql.startsWith('DELETE')) rows[table] = rows[table].filter(r => r[0] >= args[0]);
        else if (sql.startsWith('UPDATE')) rows[table].forEach(r => { if (r[3] === args[1]) r[3] = args[0]; });
        return {};
      },
      async first() { return {n: rows[table].filter(r => r[0] > args[0]).length}; }
    };
  }};
}

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
  const response = await handle(await form({...page, page: 'my key is correct-horse-battery-1'}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(response.status, 400);
  assert.equal(gh.calls.length, 0);
  assert.ok(containsKey(new Uint8Array([0xe2, ...new TextEncoder().encode('xcorrect-horse-battery-2')]), JSON.parse(KEYS)));
  const inNote = await handle(await form({...page, message: 'Addons: correct-horse-battery-2'}), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(inNote.status, 400);
  assert.equal(gh.calls.length, 0);
});

test('any addon file is accepted with its own name; a bad name is refused', async () => {
  const gh = fakeGitHub();
  const ok = await handle(await form({key: 'correct-horse-battery-1', kind: 'lua'}, {name: 'AllTheThings.lua', body: 'AllTheThingsAD = {}\n'}),
                          {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'}, {fetcher: gh.fetcher, now: NOW});
  assert.equal(ok.status, 202);
  assert.ok(gh.calls.find(c => c.path === '/git/trees').body.tree.some(t => t.path.endsWith('/AllTheThings.lua')));
  const bad = await handle(await form({key: 'correct-horse-battery-1', kind: 'lua'}, {name: '../evil.lua', body: 'x = 1'}),
                           {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'}, {fetcher: fakeGitHub().fetcher, now: NOW});
  assert.equal(bad.status, 400);
});

test('limits: a full queue and a busy hour are refused', async () => {
  const full = await handle(await form(page), {INBOX_KEYS: KEYS, GITHUB_TOKEN: 't'}, {fetcher: fakeGitHub({waiting: 20}).fetcher, now: NOW});
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
  const response = await handle(new Request('https://inbox.example/submit', {method: 'POST', body: new FormData()}), {INBOX_KEYS: KEYS}, {fetcher: fakeGitHub().fetcher, now: NOW});
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
