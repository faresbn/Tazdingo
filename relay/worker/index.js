// Tazdingo: a read-only news relay. No user-supplied upstream URLs or publishing secrets.
export const VERSION = 1;
const FORUM = 'https://us.forums.blizzard.com/en/wow';
const CATEGORIES = new Set([346, 347, 348, 349]);
const ORIGIN = 'https://faresbn.github.io';
const FRESH_MS = 5 * 60 * 1000;
const FOREVER = /\b(?:wow[:\s-]*)?forever\b/i;
const OTHER = /\b(?:midnight|the war within|dragonflight|the last titan|mists of pandaria|burning crusade|wrath of the lich king|legion remix|gods of zul[’']?aman)\b/i;
const ROUNDUP = /\b(?:wow weekly|this week in wow|weekly roundup|weekly news|warcraft direct)\b/i;
const ALLOWED_HOSTS = new Set(['us.forums.blizzard.com', 'worldofwarcraft.blizzard.com', 'worldofwarcraft.com', 'news.blizzard.com']);
let inFlight;
const requests = new Map();

export function text(html = '') {
  return String(html).replace(/<(script|style|nav|footer|aside)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, ' ')
    .replace(/<[^>]+>/g, ' ').replace(/&#(x[0-9a-f]+|\d+);/gi, (_, n) => {
      const c = n[0].toLowerCase() === 'x' ? parseInt(n.slice(1), 16) : Number(n);
      return c > 0 && c <= 0x10ffff ? String.fromCodePoint(c) : '';
    }).replace(/&(?:nbsp|amp|quot|apos|lt|gt);/g, m => ({'&nbsp;':' ', '&amp;':'&', '&quot;':'"', '&apos;':"'", '&lt;':'<', '&gt;':'>'}[m]))
    .replace(/[\u200e\u200f\u202a-\u202e\u2066-\u2069]/g, '').replace(/\s+/g, ' ').trim().replace(/^.{0,200}?\bShare Tweet (?:\d+ )?Comments?\s*/i, '');
}

export function sections(html) {
  // Keep heading context, excluding page chrome and related-story lists before classification.
  html = html.replace(/<(script|style|nav|footer|aside)\b[^>]*>[\s\S]*?<\/\1\s*>/gi, '');
  const article = html.match(/<article\b[^>]*>([\s\S]*?)<\/article>/i);
  if (article) html = article[1];
  const parts = html.split(/(<h[1-6]\b[^>]*>[\s\S]*?<\/h[1-6]>)/gi);
  let heading = '', result = [];
  for (const part of parts) {
    if (/^<h[1-6]\b/i.test(part)) heading = text(part);
    else if (text(part)) result.push({heading, body: text(part)});
  }
  return result;
}

function brief(value) { return value.split(/\s+/).slice(0, 24).join(' ').replace(/[,;:-]$/, '') + (value.split(/\s+/).length > 24 ? '…' : ''); }

export function classify(title, html, categoryId) {
  const parts = sections(html);
  const body = parts.map(s => s.body).join(' ');
  if (body.length < 35) return {kind:'unverified', reason:'Full article text is too short to verify relevance.'};
  const dedicatedTitle = FOREVER.test(title) && !ROUNDUP.test(title) && !OTHER.test(title);
  const foreverSections = parts.filter(s => FOREVER.test(s.heading) && !OTHER.test(s.heading) && s.body.length >= 50);
  const otherSections = parts.filter(s => OTHER.test(s.heading) && s.body.length >= 50);
  const mentions = parts.filter(s => FOREVER.test(s.body) && s.body.length >= 100);
  if (foreverSections.length && (otherSections.length || ROUNDUP.test(title) || OTHER.test(title))) {
    return {kind:'mixed', reason:'A substantive Forever section appears alongside other games or expansions.', excerpt:brief(foreverSections[0].body), section:foreverSections[0].heading};
  }
  if (ROUNDUP.test(title) || OTHER.test(title)) {
    return {kind:mentions.length ? 'unverified' : 'unrelated', reason:'No separately identifiable substantive Forever section in this roundup.'};
  }
  if (dedicatedTitle || (CATEGORIES.has(categoryId) && !otherSections.length)) {
    return {kind:'forever', reason:dedicatedTitle ? 'Dedicated Forever article; full text retrieved.' : 'Full staff post from a Forever forum category.', excerpt:brief(foreverSections[0]?.body || body)};
  }
  if (foreverSections.length && !otherSections.length) return {kind:'forever', reason:'Substantive Forever section, with no other game section identified.', excerpt:brief(foreverSections[0].body)};
  return {kind:FOREVER.test(body) ? 'unverified' : 'unrelated', reason:'A passing reference or ambiguous article is insufficient for promotion.'};
}

export function safeUrl(value, base = FORUM) {
  const u = new URL(value, base);
  if (u.protocol !== 'https:' || !ALLOWED_HOSTS.has(u.hostname) || u.username || u.password || (u.port && u.port !== '443')) throw new Error('Unapproved upstream URL');
  return u;
}

async function read(url, accept = 'application/json') {
  let target = safeUrl(url);
  for (let redirect = 0; redirect < 4; redirect++) {
    const response = await fetch(target, {headers:{Accept:accept, 'User-Agent':'Tazdingo unofficial Forever news reader'}, redirect:'manual', signal:AbortSignal.timeout(10000)});
    if ([301,302,303,307,308].includes(response.status)) { target = safeUrl(response.headers.get('Location'), target); continue; }
    if (!response.ok) throw new Error(`Blizzard returned ${response.status}`);
    const reader = response.body.getReader(); let count = 0, chunks = [];
    while (true) { const {done,value} = await reader.read(); if (done) break; count += value.length; if (count > 1_500_000) { await reader.cancel(); throw new Error('Upstream document exceeds the read limit'); } chunks.push(value); }
    const bytes = new Uint8Array(count); let at = 0; for (const chunk of chunks) { bytes.set(chunk, at); at += chunk.length; }
    return new TextDecoder().decode(bytes);
  }
  throw new Error('Too many upstream redirects');
}

async function json(url) { return JSON.parse(await read(url)); }

async function digest(value) {
  const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
  return [...new Uint8Array(hash)].map(n => n.toString(16).padStart(2,'0')).join('');
}

async function inspect(p) {
  const full = await json(`${FORUM}/posts/${p.id}.json`);
  if (!full.cooked || Number(full.topic_id) !== Number(p.topic_id)) throw new Error('Full forum post did not match the source');
  let article = full.cooked, url = `${FORUM}${p.url}`;
  // News cards often link to the original article: inspect it rather than classify the teaser.
  const links = [...article.matchAll(/href=["']([^"']+)["']/gi)].map(m => m[1].replace(/&amp;/g,'&'));
  for (const link of links) {
    let target; try { target = safeUrl(link); } catch { continue; }
    if (target.hostname !== 'us.forums.blizzard.com' && /\/(?:news|article)\//.test(target.pathname)) {
      article = await read(target, 'text/html'); url = target.href; break;
    }
  }
  const result = classify(p.topic_title, article, p.category_id);
  return {id:p.id, topic_id:p.topic_id, title:text(p.topic_title), author:text(p.name || p.username), author_title:text(p.user_title || ''),
    posted:p.created_at, url:`${FORUM}${p.url}`, article_url:url, category:CATEGORIES.has(p.category_id) ? 'WoW: Forever' : 'News',
    category_id:p.category_id, reply:(p.post_number || 1)>1, ...result, classifier_version:VERSION,
    checked_at:new Date().toISOString(), article_sha256:await digest(article)};
}

export async function collect(previous = {posts:[]}) {
  const now = new Date().toISOString();
  let feed = `${FORUM}/groups/blizzard-tracker/posts.json`, candidates = [], feedSucceeded = false;
  for (let page = 0; page < 3; page++) {
    const data = await json(feed); feedSucceeded = true;
    const posts = (data.posts || []).filter(p => Number.isSafeInteger(p.id) && p.topic_id && typeof p.url === 'string' && p.url.startsWith('/t/') && typeof p.created_at === 'string');
    candidates.push(...posts.filter(p => CATEGORIES.has(p.category_id) || FOREVER.test(p.topic_title || '') || ROUNDUP.test(p.topic_title || '')));
    if (!posts.length) break;
    feed = `${FORUM}/groups/blizzard-tracker/posts.json?before_post_id=${posts.at(-1).id}`;
  }
  const known = new Map((previous.posts || []).filter(p=>p.classifier_version===VERSION && ['forever','mixed'].includes(p.kind)).map(p=>[p.id,p]));
  const diagnostics = []; let verified = 0;
  // Re-read recent candidates, including edits. Bounded batches keep each public refresh small.
  candidates = [...new Map(candidates.map(p=>[p.id,p])).values()].slice(0,10);
  for (let i = 0; i < candidates.length; i += 3) {
    await Promise.all(candidates.slice(i,i+3).map(async p => {
      try {
        const record = await inspect(p); verified++;
        if (['forever','mixed'].includes(record.kind)) known.set(p.id,record); else known.delete(p.id);
        diagnostics.push({id:p.id,title:text(p.topic_title),kind:record.kind,reason:record.reason});
      } catch { diagnostics.push({id:p.id,title:text(p.topic_title),kind:'unverified',reason:'Full article could not be read; prior verified classification retained if available.'}); }
    }));
  }
  const cutoff = Date.now()-120*86400000;
  const seen = new Set();
  const posts = [...known.values()].filter(p=>Date.parse(p.posted)>=cutoff).sort((a,b)=>b.posted.localeCompare(a.posted)).filter(p=>{
    const key = p.reply ? String(p.id) : `${p.title.toLowerCase()}|${p.author}|${p.posted.slice(0,10)}`;
    if (seen.has(key)) return false; seen.add(key); return true;
  }).slice(0,80);
  const success = feedSucceeded && (verified>0 || candidates.length===0);
  return {schema_version:1,classifier_version:VERSION,source:FORUM,attempted_at:now,
    fetched:success ? now : previous.fetched || null, last_successful_refresh:success ? now : previous.last_successful_refresh || previous.fetched || null,
    status:!success ? 'unavailable' : diagnostics.some(d=>d.kind==='unverified') ? 'partial' : 'ok',
    posts,diagnostics,note:'Full-text checked official Blizzard posts. Mixed roundups appear only on the news page.'};
}

function answer(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json; charset=utf-8','Access-Control-Allow-Origin':ORIGIN,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff',...extra}});
}

export default {
  async fetch(request, env, ctx) {
    const u = new URL(request.url);
    if (!['/','/news','/health'].includes(u.pathname) || u.search) return answer({error:'Not found'},404);
    if (request.method === 'OPTIONS') return new Response(null,{status:204,headers:{'Access-Control-Allow-Origin':ORIGIN,'Access-Control-Allow-Methods':'GET, OPTIONS','Access-Control-Max-Age':'3600'}});
    if (request.method !== 'GET') return answer({error:'Read-only endpoint'},405,{'Allow':'GET, OPTIONS'});
    if (u.pathname === '/health' || u.pathname === '/') return answer({service:'Tazdingo news relay',classifier_version:VERSION});
    const origin=request.headers.get('Origin'); if(origin && origin!==ORIGIN) return answer({error:'Origin not allowed'},403);
    const ip=request.headers.get('CF-Connecting-IP') || 'anonymous'; const bucket=Math.floor(Date.now()/60000);
    const entry=requests.get(ip); const hits=entry?.bucket===bucket ? entry.count+1 : 1;
    requests.set(ip,{bucket,count:hits}); if(requests.size>2000) for(const [key,value] of requests) if(value.bucket<bucket) requests.delete(key);
    if(hits>15) return answer({error:'Please wait before checking again'},429,{'Retry-After':'60'});
    const key = new Request(`${u.origin}/_verified-news-v${VERSION}`);
    const cached = await caches.default.match(key); const previous = cached ? await cached.json() : {posts:[]};
    if (previous.attempted_at && Date.now()-Date.parse(previous.attempted_at)<FRESH_MS) return answer({...previous,cached:true,next_check_at:new Date(Date.parse(previous.attempted_at)+FRESH_MS).toISOString()});
    if (!inFlight) inFlight=(async()=>{
      let data;
      try { data=await collect(previous); }
      catch { data={...previous,status:'unavailable',attempted_at:new Date().toISOString(),error:'Blizzard could not be reached; showing the last verified news.'}; }
      await caches.default.put(key,new Response(JSON.stringify(data),{headers:{'Content-Type':'application/json','Cache-Control':'public, max-age=86400'}}));
      return data;
    })().finally(()=>{inFlight=undefined;});
    const data=await inFlight;
    return answer({...data,cached:false,next_check_at:new Date(Date.parse(data.attempted_at)+FRESH_MS).toISOString()});
  }
};
