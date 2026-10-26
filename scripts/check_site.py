"""Check the built publication's data and internal links, including item routes."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        if tag=="h1": self.h1+=1
        for key,value in attrs:
            if key in ("href","src") and value: self.links.append(value)


def check(out=None,base="/FvrRepo/"):
    out=Path(out or ROOT/"dist")
    manifest=json.loads((out/"data/manifest.json").read_text())
    assert manifest["project"]=="FvrRepo"
    assert not list(out.rglob("*.lua")),"Private Lua in public output"
    count=0
    for path in out.rglob("*.html"):
        parser=Links(); parser.feed(path.read_text())
        assert parser.h1==1,f"Expected one page heading: {path}"
        for link in parser.links:
            parts=urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path: continue
            assert parts.path.startswith(base),f"Wrong project base path: {link}"
            relative=unquote(parts.path[len(base):])
            target=(out/relative).resolve()
            assert target.is_relative_to(out.resolve()),f"Escaping public path: {link}"
            if parts.path.endswith("/"): target=target/"index.html"
            assert target.is_file(),f"Broken link in {path}: {link}"
        count+=1
    report=json.loads((out/"data/validation.json").read_text())
    assert report["revision"]==manifest["revision"]
    for market in manifest["markets"]:
        latest=json.loads((out/market["latest_json"].removeprefix(base)).read_text())
        assert len(latest["records"])==market["item_count"]
        assert latest["revision"]==manifest["revision"]
        partition_keys=[]
        for part in market["partitions"]:
            path=out/part["json"].removeprefix(base)
            data=json.loads(path.read_text())
            assert data["revision"]==manifest["revision"]
            assert len(data["records"])==part["records"]
            assert path.stat().st_size<65536,"Price partition exceeds the first-release size budget"
            partition_keys.extend(r["item_key"] for r in data["records"])
            history=json.loads((out/part["history_json"].removeprefix(base)).read_text())
            assert set(history["history"])=={r["item_key"] for r in data["records"]}
            assert history["revision"]==manifest["revision"]
        assert len(partition_keys)==len(set(partition_keys))
        assert set(partition_keys)=={r["item_key"] for r in latest["records"]}
        for record in latest["records"]:
            assert type(record["unit_price_copper"]) is int
            assert record["quote_observed_at"] is None
            assert record["source"] in latest["capture_sources"]
    print(f"Verified {count:,} HTML pages, all internal links, market counts and publication revision {manifest['revision']}")


if __name__=="__main__": check()
