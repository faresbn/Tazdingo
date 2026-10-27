"""Full-text Blizzard news collection for the static build; shares the relay's classifier.

GitHub Actions reads Blizzard directly. The public relay is only for browser refreshes.
No private GitHub token is needed by the news reader.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FORUM='https://us.forums.blizzard.com/en/wow'
VERSION=1
CATEGORIES={346,347,348,349}
HOSTS={'us.forums.blizzard.com','worldofwarcraft.blizzard.com','worldofwarcraft.com','news.blizzard.com'}


def safe(url):
    u=urlsplit(url)
    if u.scheme!='https' or u.hostname not in HOSTS or u.username or u.password or u.port not in (None,443):
        raise ValueError('Unapproved upstream URL')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return super().redirect_request(req,fp,code,msg,headers,safe(newurl))


def read(url):
    req=urllib.request.Request(safe(url),headers={'Accept':'application/json, text/html','User-Agent':'Tazdingo unofficial Forever news snapshot'})
    with urllib.request.build_opener(Redirects).open(req,timeout=15) as r:
        data=r.read(1_500_001)
    if len(data)>1_500_000:raise ValueError('Article exceeds read limit')
    return data.decode('utf-8')


class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            value=dict(attrs).get('href')
            if value:self.urls.append(unescape(value))


def valid_post(post):
    if not isinstance(post,dict):return False
    url=urlsplit(str(post.get('url','')))
    return (type(post.get('id')) is int and post.get('classifier_version')==VERSION
            and post.get('kind') in ('forever','mixed') and isinstance(post.get('title'),str)
            and url.scheme=='https' and url.hostname=='us.forums.blizzard.com'
            and url.path.startswith('/en/wow/t/') and not url.username and not url.password
            and isinstance(post.get('posted'),str) and isinstance(post.get('checked_at'),str))


def inspect(post):
    full=json.loads(read(f"{FORUM}/posts/{post['id']}.json"))
    if not full.get('cooked') or full.get('topic_id')!=post['topic_id']:raise ValueError('Forum post did not match')
    article=full['cooked'];url=FORUM+post['url']
    links=Links();links.feed(article)
    for link in links.urls:
        target=urljoin(FORUM+'/',link)
        try:safe(target)
        except ValueError:continue
        u=urlsplit(target)
        if u.hostname!='us.forums.blizzard.com' and ('/news/' in u.path or '/article/' in u.path):
            article=read(target);url=target;break
    return {'id':post['id'],'topic_id':post['topic_id'],'title':post['topic_title'],'html':article,
            'author':post.get('name') or post.get('username') or 'Blizzard','author_title':post.get('user_title') or '',
            'posted':post['created_at'],'url':FORUM+post['url'],'article_url':url,'category_id':post.get('category_id'),
            'category':'WoW: Forever' if post.get('category_id') in CATEGORIES else 'News','reply':post.get('post_number',1)>1,
            'article_sha256':hashlib.sha256(article.encode()).hexdigest()}


def refresh(path: Path,pages=3,merge: Path|None=None):
    saved=[]
    for source in (path,merge):
        if source and source.exists():
            try:saved.append(json.loads(source.read_text()))
            except (ValueError,OSError):pass
    previous=max(saved,key=lambda d:d.get('fetched') or '',default={'posts':[]})
    known={p['id']:p for p in previous.get('posts',[]) if valid_post(p)}
    attempted=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
    diagnostics=[];error=None;verified=0;feed_ok=False;began=time.monotonic()
    try:
        url=FORUM+'/groups/blizzard-tracker/posts.json';candidates={}
        for _ in range(pages):
            posts=json.loads(read(url)).get('posts',[]);feed_ok=True
            posts=[p for p in posts if type(p.get('id')) is int and p.get('topic_id') and isinstance(p.get('url'),str) and p['url'].startswith('/t/') and p.get('created_at') and p.get('topic_title')]
            for p in posts:
                title=p['topic_title'].lower()
                if p.get('category_id') in CATEGORIES or 'forever' in title or 'wow weekly' in title or 'this week in wow' in title:candidates[p['id']]=p
            if not posts:break
            url=FORUM+f"/groups/blizzard-tracker/posts.json?before_post_id={posts[-1]['id']}"
        raw=[]
        def attempt(p):
            try:return inspect(p)
            except Exception:return {'id':p['id'],'title':p['topic_title'],'failed':True}
        with ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(attempt,list(candidates.values())[:10]):
                if result.get('failed'):diagnostics.append({**result,'kind':'unverified','reason':'Full article unavailable; prior verified record retained if present.'})
                else:raw.append(result)
        classified=subprocess.run(['node',str(ROOT/'scripts/classify_news.mjs')],input=json.dumps(raw),text=True,capture_output=True,check=True,timeout=20)
        results={p['id']:p for p in json.loads(classified.stdout)}
        for p in raw:
            verdict=results[p['id']];verified+=1
            diagnostics.append({'id':p['id'],'title':p['title'],'kind':verdict['kind'],'reason':verdict['reason']})
            p.pop('html');record={**p,**verdict,'checked_at':attempted}
            if verdict['kind'] in ('forever','mixed'):known[p['id']]=record
            else:known.pop(p['id'],None)
        success=feed_ok and (verified>0 or not candidates)
        if not success:error='Full-text verification unavailable'
    except Exception as failure:
        success=False;error=f'{type(failure).__name__}: {failure}'
    seen=set();posts=[]
    for p in sorted(known.values(),key=lambda p:p['posted'],reverse=True):
        key=str(p['id']) if p.get('reply') else (p['title'].lower(),p.get('author'),p['posted'][:10])
        if key not in seen:posts.append(p);seen.add(key)
    result={'schema_version':1,'classifier_version':VERSION,'source':FORUM,'attempted_at':attempted,
            'fetched':attempted if success else previous.get('fetched'),
            'last_successful_refresh':attempted if success else previous.get('last_successful_refresh') or previous.get('fetched'),
            'status':'unavailable' if not success else 'partial' if any(d['kind']=='unverified' for d in diagnostics) else 'ok',
            'posts':posts[:80],'diagnostics':diagnostics,'note':'Full-text checked Blizzard news; mixed roundups appear only on the news page.'}
    if error:result['error']='Refresh unavailable; showing the last verified news.'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')
    return {'kept':len(result['posts']),'verified':verified,'seconds':round(time.monotonic()-began,1),'status':result['status'],'error':error}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'data/blue.json');parser.add_argument('--merge',type=Path)
    args=parser.parse_args();print(json.dumps(refresh(args.out,merge=args.merge),indent=2))
