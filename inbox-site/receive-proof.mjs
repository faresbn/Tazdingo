// Local proof adapter: run the production receiver, capture its GitHub writes, and return them
// to scripts/prove_inbox.py. Never imports credentials or contacts the network.
import {handle} from './worker/index.js';
import {fakeGitHub, fakeDB} from './test-support.mjs';

let input = '';
for await (const chunk of process.stdin) input += chunk;
const {fields, file, now} = JSON.parse(input);
const form = new FormData();
for (const [name, value] of Object.entries(fields)) form.append(name, value);
if (file) form.append('file', new Blob([Buffer.from(file.base64, 'base64')]), file.name);
const draft = new Request('https://local-proof.invalid/submit', {method: 'POST', body: form});
const body = await draft.arrayBuffer();
const request = new Request(draft.url, {method: 'POST', body, headers: {
  accept: 'application/json', 'content-type': draft.headers.get('content-type'), 'content-length': String(body.byteLength)
}});
const gh = fakeGitHub();
const response = await handle(request, {
  INBOX_KEYS: JSON.stringify({'local-proof': 'local-only-proof-key-00000001'}),
  GITHUB_TOKEN: 'local-proof-token', DB: fakeDB()
}, {fetcher: gh.fetcher, now});
const blobs = new Map();
gh.calls.forEach((call, index) => {
  if (call.path === '/git/blobs') blobs.set(`blob${index + 1}`, call.body);
});
const tree = gh.calls.find(call => call.path === '/git/trees')?.body.tree || [];
const files = tree.map(entry => {
  const blob = blobs.get(entry.sha);
  const data = Buffer.from(blob.content, blob.encoding === 'base64' ? 'base64' : 'utf8');
  return {path: entry.path, base64: data.toString('base64')};
});
process.stdout.write(JSON.stringify({status: response.status, reply: await response.json(), files}));
