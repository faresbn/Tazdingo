"""Check the built site before it's published: links, headings, data files agree."""
import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.title, self._in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        self.h1 += tag == "h1"
        self._in_title = tag == "title"
        self.handlers = getattr(self, "handlers", []) + [f"<{tag} {k}>" for k, _ in attrs if k.startswith("on")]
        for key, value in attrs:
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

    pages = 0
    for path in out.rglob("*.html"):
        page = Page()
        page.feed(path.read_text())
        assert page.h1 == 1, f"Expected exactly one h1: {path}"
        assert not getattr(page, "handlers", []), f"Event-handler attribute in {path}: {page.handlers}"
        assert page.title.strip(), f"Missing title: {path}"
        assert "noindex" not in path.read_text(), f"Page hidden from search: {path}"
        for link in page.links:
            target = local(link)
            assert target is None or target.is_file(), f"Broken link in {path.relative_to(out)}: {link}"
        pages += 1

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
    import re
    for path in out.rglob("*"):
        if path.suffix in (".html", ".txt", ".json", ".tsv", ".xml", ".css", ".js"):
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
    print(f"Checked {pages} pages, {len(manifest['markets'])} markets, {len(manifest['pages_with_notes'])} pages of notes "
          f"and {len(search):,} search entries (revision {manifest['revision']}).")


if __name__ == "__main__":
    check()
