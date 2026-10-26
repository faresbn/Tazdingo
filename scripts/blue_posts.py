"""Refresh data/blue.json: Blizzard staff posts about WoW Forever, from Blizzard's own forums.

The forums' "blizzard-tracker" feed lists every staff post across the WoW forums. We keep those
in the WoW: Forever categories, and news posts whose title mentions Forever, with a short
plain-text excerpt and a link to the original. Run by the publish workflow every two hours;
if Blizzard can't be reached, the saved file is used and the build carries on.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORUM = "https://us.forums.blizzard.com/en/wow"
FEED = FORUM + "/groups/blizzard-tracker/posts.json"
FOREVER_CATEGORIES = {346: "WoW: Forever", 347: "Forever General Discussion", 348: "Forever Community Connections",
                      349: "Forever Beta Discussion"}
AGENT = "Forever Ledger blue tracker (unofficial fan site; a few requests every two hours)"
KEEP = 80          # posts kept in data/blue.json
MAX_PAGES = 8      # feed pages read per refresh (20 posts each)
MAX_AGE_DAYS = 120
BUDGET_SECONDS = 45  # the whole refresh, so a slow forum can't hold up publishing


def fetch(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read(2_000_000))


BIDI = re.compile("[\u200e\u200f\u202a-\u202e\u2066-\u2069]")  # invisible direction controls can disguise text


def clean(text: str) -> str:
    return BIDI.sub("", text or "")


def plain(excerpt: str, limit: int = 260) -> str:
    """Forum excerpts are HTML: strip tags, images and links down to a short sentence or two."""
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", excerpt or "", flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    text = re.sub(r"^\[[^\]]{0,200}\]\s*", "", text)  # an image's alt text at the start
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"
    return text


def is_forever(post: dict) -> bool:
    return post.get("category_id") in FOREVER_CATEGORIES or "forever" in (post.get("topic_title") or "").lower()


def valid(post: dict) -> bool:
    return (isinstance(post.get("id"), int) and isinstance(post.get("created_at"), str)
            and isinstance(post.get("url"), str) and post["url"].startswith("/t/") and isinstance(post.get("topic_title"), str))


def record(post: dict) -> dict:
    return {"id": post["id"], "topic_id": post.get("topic_id"), "title": clean(post.get("topic_title")).strip(),
            "author": clean(post.get("name") or post.get("username")), "author_title": post.get("user_title") or "",
            "posted": post["created_at"], "url": FORUM + post["url"],
            "category": FOREVER_CATEGORIES.get(post.get("category_id"), "News"),
            "reply": (post.get("post_number") or 1) > 1, "excerpt": clean(plain(post.get("excerpt", "")))}


def dedupe(posts) -> list[dict]:
    """Blizzard cross-posts announcements in several categories: keep one opening post per title,
    author and day, preferring the Forever category's copy. Replies are all kept, each by its id."""
    best = {}
    for post in posts:
        key = post["id"] if post["reply"] else (re.sub(r"\W+", " ", post["title"].lower()).strip(), post["author"], post["posted"][:10])
        rank = (post["category"] == "News", post["posted"])
        if key not in best or rank < best[key][0]:
            best[key] = (rank, post)
    return [post for _, post in best.values()]


def refresh(path: Path, pages: int = MAX_PAGES, merge: Path | None = None) -> dict:
    """Add new posts to the saved ones. `merge` is the previous run's snapshot (CI keeps it in its
    cache, since the published site isn't committed back), so posts survive between runs."""
    saved = [p for source in (path, merge) if source and source.exists() for p in json.loads(source.read_text()).get("posts", [])]
    known = {p["id"]: {**p, "title": clean(p["title"]), "excerpt": clean(p.get("excerpt", ""))} for p in saved}
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    url, new, began, error = FEED, 0, time.monotonic(), None
    for _ in range(pages):
        if time.monotonic() - began > BUDGET_SECONDS:
            break
        try:
            posts = [p for p in fetch(url).get("posts", []) if valid(p)]
        except Exception as failure:  # keep what was saved and what was already read
            error = f"{type(failure).__name__}: {failure}"
            break
        if not posts:
            break
        for post in posts:
            if is_forever(post):
                new += post["id"] not in known
                known[post["id"]] = record(post)  # rewritten each time, so edits on the forum show up
        oldest = posts[-1]
        if datetime.fromisoformat(oldest["created_at"].replace("Z", "+00:00")) < cutoff:
            break
        url = f"{FEED}?before_post_id={oldest['id']}"
        time.sleep(1)
    kept = sorted(dedupe(known.values()), key=lambda p: p["posted"], reverse=True)[:KEEP]
    result = {"source": FORUM, "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
              "note": "Staff posts from Blizzard's forums about WoW Forever. Excerpts are short; read the full post at its link.",
              "posts": kept}
    path.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
    return {"new": new, "kept": len(kept), "newest": kept[0]["posted"] if kept else None, "error": error}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "data/blue.json")
    parser.add_argument("--pages", type=int, default=MAX_PAGES)
    parser.add_argument("--merge", type=Path, help="an earlier snapshot to keep posts from")
    args = parser.parse_args()
    try:
        print(json.dumps(refresh(args.out, args.pages, args.merge), indent=2))
    except Exception as error:  # any failure: keep the saved posts, and say so
        print(f"Blizzard's forums couldn't be read ({type(error).__name__}: {error}); keeping the saved posts.")
