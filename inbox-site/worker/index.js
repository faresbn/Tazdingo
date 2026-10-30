// Tazdingo inbox: receives the hidden form (or the same fields as JSON), checks the key and
// commits the submission, key removed, to inbox/<id>/ in the repository. Every other rule lives in
// scripts/inbox.py, which a GitHub Action runs on what arrives. Refusals are logged in this Site's
// own database (the private "failed folder") and never reach the public repository.
export const VERSION = 1;
const REPO = 'faresbn/Tazdingo';
const SITE = 'https://faresbn.github.io/Tazdingo/';
const API = 'https://api.github.com';
const MAX_BYTES = 25 * 1024 * 1024;
const MAX_PAGE = 300_000;
const HOURLY_LIMIT = 30;
const QUEUE_LIMIT = 20;
const LUA_NAME = /^[A-Za-z0-9][A-Za-z0-9_.-]{0,60}\.lua$/;
const AUTHOR = {name: 'tazdingo-inbox', email: 'tazdingo-inbox@users.noreply.github.com'};

export class Refused extends Error {
  constructor(message, status = 400) { super(message); this.status = status; }
}

const bytes = text => new TextEncoder().encode(text);

async function digest(text) {
  return new Uint8Array(await crypto.subtle.digest('SHA-256', bytes(text)));
}

// The key's label (e.g. "key-2") or null. Every key is compared, in constant time, whatever matches.
export async function keyLabel(given, keys) {
  const mine = await digest(String(given || ''));
  let found = null;
  for (const [label, key] of Object.entries(keys)) {
    const theirs = await digest(String(key));
    let diff = 0;
    for (let i = 0; i < mine.length; i++) diff |= mine[i] ^ theirs[i];
    if (diff === 0 && found === null && key) found = label;
  }
  return found;
}

export function submissionId(now = new Date(), random = crypto.getRandomValues(new Uint8Array(4))) {
  const stamp = now.toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  return `${stamp}-${[...random].map(b => b.toString(16).padStart(2, '0')).join('')}`;
}

const text = (value, limit) => {
  if (value === undefined || value === null || value === '') return undefined;
  if (typeof value !== 'string' || value.length > limit) throw new Refused('A field is too long or not text.');
  return value.trim();
};

// The submission's fields and its one file, from a form or JSON; throws Refused.
export async function readSubmission(request) {
  const length = Number(request.headers.get('content-length') || 0);
  if (length > MAX_BYTES + 1_000_000) throw new Refused('Too large: the limit is 25 MB.', 413);
  const type = request.headers.get('content-type') || '';
  let fields, file;
  if (type.startsWith('application/json')) {
    fields = await request.json();
    if (fields.kind === 'lua') file = {name: fields.file_name, data: Uint8Array.from(atob(String(fields.file_base64 || '')), c => c.charCodeAt(0))};
  } else if (type.startsWith('multipart/form-data') || type.startsWith('application/x-www-form-urlencoded')) {
    const form = await request.formData();
    fields = Object.fromEntries([...form.entries()].filter(([, v]) => typeof v === 'string'));
    const upload = form.get('file');
    if (fields.kind === 'lua' && upload && typeof upload !== 'string') file = {name: upload.name, data: new Uint8Array(await upload.arrayBuffer())};
  } else {
    throw new Refused('Send the form, or JSON.', 415);
  }
  const kind = fields.kind;
  if (kind !== 'page' && kind !== 'lua') throw new Refused("Choose what you're sending: a guide page or an addon's file.");
  const sub = {kind, key: String(fields.key || ''), message: text(fields.message, 200)};
  if (kind === 'page') {
    sub.path = text(fields.path, 120);
    sub.version = text(fields.version, 64);
    const page = text(fields.page, MAX_PAGE);
    if (!sub.path || !sub.version || !page || !sub.message) throw new Refused('A page needs its path, the version you edited, a one-line change note and the whole page.');
    sub.file = {name: 'page.md', data: bytes(page.replace(/\r\n/g, '\n') + '\n')};
  } else {
    if (!file || !LUA_NAME.test(file.name || '')) throw new Refused("Attach the addon's saved-variables file, named after the addon (e.g. AllTheThings.lua).");
    if (file.data.length > MAX_BYTES) throw new Refused('Too large: the limit is 25 MB.', 413);
    sub.market = text(fields.market, 80);
    sub.file = file;
  }
  return sub;
}

// True if any key appears in the file: a pasted key must never be committed to a public repository.
export function containsKey(data, keys) {
  const body = new TextDecoder().decode(data);  // keys are ASCII, which UTF-8 decoding keeps intact even around invalid bytes
  return Object.values(keys).some(key => key && body.includes(key));
}

async function github(env, path, init = {}, fetcher = fetch) {
  const response = await fetcher(`${API}/repos/${env.REPO || REPO}${path}`, {
    ...init,
    headers: {authorization: `Bearer ${env.GITHUB_TOKEN}`, accept: 'application/vnd.github+json', 'x-github-api-version': '2022-11-28',
              'user-agent': 'tazdingo-inbox', ...(init.body ? {'content-type': 'application/json'} : {})}
  });
  return response;
}

async function json(response, what) {
  if (!response.ok) throw new Error(`GitHub refused ${what}: ${response.status}`);
  return response.json();
}

function base64(data) {
  let out = '';
  for (let i = 0; i < data.length; i += 0x8000) out += String.fromCharCode(...data.subarray(i, i + 0x8000));
  return btoa(out);
}

export async function waitingCount(env, fetcher = fetch) {
  const response = await github(env, '/contents/inbox?ref=main', {}, fetcher);
  if (response.status === 404) return 0;
  const entries = await json(response, 'the inbox listing');
  return entries.filter(e => e.type === 'dir' && e.name !== 'held').length;
}

// One commit adding inbox/<id>/submission.json and the file, built on the latest main; if main
// moves before the ref is updated, rebuilt on the new tip, so nothing pushed meanwhile is lost.
export async function commitSubmission(env, id, record, file, fetcher = fetch) {
  const blob = async (content, encoding) => (await json(await github(env, '/git/blobs', {method: 'POST', body: JSON.stringify({content, encoding})}, fetcher), 'a file')).sha;
  const blobs = [
    {path: `inbox/${id}/submission.json`, sha: await blob(JSON.stringify(record, null, 1) + '\n', 'utf-8')},
    {path: `inbox/${id}/${file.name}`, sha: await blob(base64(file.data), 'base64')}
  ];
  for (let attempt = 0; attempt < 3; attempt++) {
    const head = (await json(await github(env, '/git/ref/heads/main', {}, fetcher), 'the main branch')).object.sha;
    const base = (await json(await github(env, `/git/commits/${head}`, {}, fetcher), 'the latest commit')).tree.sha;
    const tree = (await json(await github(env, '/git/trees', {method: 'POST', body: JSON.stringify({
      base_tree: base, tree: blobs.map(b => ({path: b.path, mode: '100644', type: 'blob', sha: b.sha}))})}, fetcher), 'the tree')).sha;
    const commit = (await json(await github(env, '/git/commits', {method: 'POST', body: JSON.stringify({
      message: `Inbox: ${record.kind} ${id}`, tree, parents: [head], author: {...AUTHOR, date: record.received}})}, fetcher), 'the commit')).sha;
    const moved = await github(env, '/git/refs/heads/main', {method: 'PATCH', body: JSON.stringify({sha: commit, force: false})}, fetcher);
    if (moved.ok) return commit;
    if (moved.status !== 422) throw new Error(`GitHub refused the update: ${moved.status}`);
  }
  throw new Error('main kept moving; try again in a minute');
}

async function log(env, table, row) {
  if (!env.DB) return;
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS ${table} (time TEXT, kind TEXT, size INTEGER, reason TEXT)`).run();
  await env.DB.prepare(`INSERT INTO ${table} (time, kind, size, reason) VALUES (?, ?, ?, ?)`).bind(row.time, row.kind || '', row.size || 0, row.reason || '').run();
}

async function acceptedLastHour(env, now) {
  if (!env.DB) return 0;
  await env.DB.prepare('CREATE TABLE IF NOT EXISTS accepted (time TEXT, kind TEXT, size INTEGER, reason TEXT)').run();
  const row = await env.DB.prepare('SELECT COUNT(*) AS n FROM accepted WHERE time > ?').bind(new Date(now - 3600_000).toISOString()).first();
  return Number(row?.n || 0);
}

const escape = s => String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

function reply(request, status, title, message) {
  if ((request.headers.get('accept') || '').includes('application/json')) {
    return new Response(JSON.stringify({ok: status < 300, title, message}), {status, headers: {'content-type': 'application/json'}});
  }
  const html = `<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>${escape(title)} | Tazdingo inbox</title>
<style>body{font:1rem/1.5 system-ui,sans-serif;max-width:40rem;margin:2rem auto;padding:0 1rem;color:#1d2b33;background:#f6f1e7}@media(prefers-color-scheme:dark){body{color:#eee8db;background:#101e28}a{color:#9fd3d6}}</style>
</head><body><h1>${escape(title)}</h1><p>${escape(message)}</p><p><a href="${SITE}inbox/">Back to the inbox</a> · <a href="${SITE}">Tazdingo</a></p></body></html>`;
  return new Response(html, {status, headers: {'content-type': 'text/html; charset=utf-8'}});
}

export async function handle(request, env, {fetcher = fetch, now = Date.now()} = {}) {
  const url = new URL(request.url);
  if (url.pathname === '/') return reply(request, 200, 'Tazdingo inbox', 'Send pages and addon files through the form on the website.');
  if (url.pathname !== '/submit') return reply(request, 404, 'Not here', 'This address only receives the inbox form.');
  if (request.method !== 'POST') return reply(request, 405, 'Send the form', 'This address only receives the inbox form.');
  const time = new Date(now).toISOString();
  let keys;
  try { keys = JSON.parse(env.INBOX_KEYS || '{}'); } catch { keys = {}; }
  let sub;
  try {
    sub = await readSubmission(request);
    const label = await keyLabel(sub.key, keys);
    if (!label) throw new Refused("The key isn't right.", 403);
    const fields = [sub.path, sub.version, sub.message, sub.market, sub.file.name].filter(Boolean).join('\n');
    if (containsKey(sub.file.data, keys) || containsKey(bytes(fields), keys)) {
      throw new Refused('The page, file or a field contains a key. Remove it and send again: everything sent here is published.');
    }
    if (await acceptedLastHour(env, now) >= HOURLY_LIMIT) throw new Refused('The inbox has had a lot this hour. Try again later.', 429);
    if (await waitingCount(env, fetcher) >= QUEUE_LIMIT) throw new Refused('The inbox is full while earlier submissions are processed. Try again in a few minutes.', 429);
    const id = submissionId(new Date(now));
    const record = {format: 1, id, received: time.replace(/\.\d+Z$/, 'Z'), key_label: label, kind: sub.kind, file: sub.file.name,
                    ...(sub.kind === 'page' ? {path: sub.path, version: sub.version, message: sub.message} : {}),
                    ...(sub.kind === 'lua' ? {...(sub.market ? {market: sub.market} : {}), ...(sub.message ? {message: sub.message} : {})} : {})};
    await commitSubmission(env, id, record, sub.file, fetcher);
    await log(env, 'accepted', {time, kind: sub.kind, size: sub.file.data.length, reason: `${label} ${id}`});
    return reply(request, 202, 'Received', `Submission ${id} is in. If it passes its checks it's live in about two minutes (feed/ in the repository and the website). If it's held, the owner hears why.`);
  } catch (error) {
    if (error instanceof Refused) {
      await log(env, 'refusals', {time, kind: sub?.kind, size: sub?.file?.data?.length, reason: error.message}).catch(() => {});
      return reply(request, error.status, 'Refused', error.message);
    }
    await log(env, 'refusals', {time, kind: sub?.kind, size: sub?.file?.data?.length, reason: `error: ${error.message}`}).catch(() => {});
    return reply(request, 502, 'Not sent', `Something went wrong passing this on (${error.message}). Nothing was published; try again.`);
  }
}

export default {
  async fetch(request, env) { return handle(request, env); }
};
