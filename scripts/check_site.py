"""Check the built site before it's published: links, headings, data files agree."""
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.title, self._in_title, self.ids = [], 0, "", False, set()

    def handle_starttag(self, tag, attrs):
        self.h1 += tag == "h1"
        self._in_title = tag == "title"
        self.handlers = getattr(self, "handlers", []) + [f"<{tag} {k}>" for k, _ in attrs if k.startswith("on")]
        for key, value in attrs:
            if key == "id" and value:
                if value in self.ids:
                    self.duplicate_ids = getattr(self, "duplicate_ids", []) + [value]
                self.ids.add(value)
            if key in ("href", "src", "action") and value and value.strip().lower().startswith(("javascript:", "data:text", "ledger:")):
                self.handlers.append(f"<{tag} {key}={value[:30]}>")
            if key in ("href", "src", "srcset", "action") and value:
                self.links.append(value.split()[0])

    def handle_endtag(self, tag):
        self._in_title = False if tag == "title" else self._in_title

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def check(out=None, base="/FvrRepo/"):
    out = Path(out or ROOT / "dist")
    manifest = json.loads((out / "data/manifest.json").read_text())
    assert not list(out.rglob("*.lua")), "Raw Lua in public output"
    for required in ("index.html", "llms.txt", "llms-full.txt", "sitemap.xml", "search.json", "prices/index.html", "prices/craft/index.html",
                     "prices/crates/index.html", "prices/materials/index.html", "classes/index.html", "professions/index.html",
                     "world/index.html", "more/addons/index.html", "more/macros/index.html", "more/known-issues/index.html", "more/about/index.html"):
        assert (out / required).is_file(), f"Missing {required}"

    def local(link):
        parts = urlsplit(link)
        if parts.scheme or parts.netloc or not parts.path or link.startswith("#"):
            return None
        assert parts.path.startswith(base), f"Link outside the site's base path: {link}"
        target = (out / unquote(parts.path[len(base):])).resolve()
        assert target.is_relative_to(out.resolve()), f"Link escapes the site: {link}"
        return target / "index.html" if parts.path.endswith("/") else target

    # Every page the game data promises must exist.
    game = json.loads((ROOT / "data/game.json").read_text())
    expected = ["classes/", "professions/", "world/", "prices/", "more/about/"]
    expected += [f"classes/{c['slug']}/" for c in game["classes"]] + [f"classes/{c['slug']}/{s['slug']}/" for c in game["classes"] for s in c["specs"]]
    expected += [f"professions/{p['slug']}/" for p in game["professions"]] + [f"world/{t['slug']}/" for t in game["world"]]
    expected += [f"more/{m['slug']}/" for m in game["more"]]
    for route in expected:
        assert (out / route / "index.html").is_file(), f"Missing page {route}"

    parsed, fragments = {}, []
    for path in out.rglob("*.html"):
        page = Page()
        text = path.read_text()
        page.feed(text)
        parsed[path.resolve()] = page
        assert page.h1 == 1, f"Expected exactly one h1: {path}"
        assert not getattr(page, "handlers", []), f"Event handler or script link in {path}: {page.handlers}"
        assert page.title.strip(), f"Missing title: {path}"
        assert not getattr(page, "duplicate_ids", []), f"Duplicate section ids in {path}: {page.duplicate_ids[:5]}"
        assert "noindex" not in text, f"Page hidden from search: {path}"
        assert len(re.findall(r"<script(?![^>]*\bsrc=)", text)) <= 1, f"Unexpected inline script in {path}"  # only the theme snippet
        for link in page.links:
            target = local(link)
            assert target is None or target.is_file(), f"Broken link in {path.relative_to(out)}: {link}"
            fragment = urlsplit(link).fragment
            if fragment and (target is not None or link.startswith("#")):
                fragments.append((path, target.resolve() if target else path.resolve(), fragment, link))
    for source, target, fragment, link in fragments:
        assert fragment in parsed[target].ids, f"Link in {source.relative_to(out)} points to a missing section: {link}"
    pages = len(parsed)

    for market in manifest["markets"]:
        prices = json.loads((out / market["prices_json"].removeprefix(base)).read_text())
        assert prices["revision"] == manifest["revision"], "Stale prices.json"
        assert len(prices["rows"]) == market["items"]
        with open(out / market["prices_tsv"].removeprefix(base), newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        assert len(rows) == market["items"], "TSV and catalogue disagree"
        assert all(r["typical_copper"].isdigit() and r["latest_copper"].isdigit() for r in rows), "Non-integer price"
        assert len({r["item_key"] for r in rows}) == len(rows), "Duplicate item key"
        history = json.loads((out / market["history_json"].removeprefix(base)).read_text())
        assert set(history["history"]) == {r["item_key"] for r in rows}
    # The public site never names the people behind it or the assistant they use (the
    # faresbn.github.io address is the one exception: it's the host's name, not text).
    for path in out.rglob("*"):
        if path.suffix in (".html", ".txt", ".json", ".tsv", ".xml", ".css", ".js", ".svg"):
            text = re.sub(r"faresbn\.github\.io", "", path.read_text())
            found = re.findall(r"\b(?:ChatGPT|Fares|Mike)\b", text, re.I)
            assert not found, f"{path.relative_to(out)} mentions {sorted(set(found))}"
    full = (out / "llms-full.txt").read_text()
    for market in manifest["markets"]:
        assert market["name"] in full, f"{market['name']} missing from llms-full.txt"
    search = json.loads((out / "search.json").read_text())
    for title, url, _ in search:
        target = local(url)
        assert target is None or target.is_file(), f"Search result {title!r} points nowhere: {url}"
        fragment = urlsplit(url).fragment
        if target is not None and fragment and fragment != "prices":
            assert fragment in parsed[target.resolve()].ids, f"Search result {title!r} points to a missing section: {url}"
    print(f"Checked {pages} pages, {len(manifest['markets'])} markets, {len(manifest['pages_with_notes'])} pages of notes "
          f"and {len(search):,} search entries (revision {manifest['revision']}).")


if __name__ == "__main__":
    check()
