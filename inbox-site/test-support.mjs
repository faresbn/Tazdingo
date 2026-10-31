// A fake GitHub: records what was written and can reject the first ref update (main moved).
export function fakeGitHub({waiting = 0, moveOnce = false} = {}) {
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

export function fakeDB() {
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

