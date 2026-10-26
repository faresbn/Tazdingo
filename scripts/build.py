"""Build the WoW Forever Journal site into dist/. Standard-library Python only.

Inputs: data/captures.json (scan receipts), data/captures/** (market-only
extracts), data/items.json (names) and journal/*.md (entries).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pages
from auctionator import (InvalidCapture, PARSER_VERSION, day_date, item_id,
                         load_market_extract, parse_capture, suffix)
from markup import render

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 2
SITE_URL = "https://faresbn.github.io/FvrRepo/"
ENVIRONMENTS = {"forever": "Forever", "forever-beta": "Forever Beta", "tbc": "TBC Anniversary", "era": "Classic Era"}
JOURNAL_TYPES = {"guide": "Guide", "build": "Build", "discovery": "Discovery"}
JOURNAL_STATUS = {"idea": "Idea", "testing": "Testing", "tested": "Tested", "outdated": "Outdated"}
CURRENT_DAYS = 14  # items seen within this many days of a market's newest day count as current
SPARK_DAYS = 14


# --- Inputs -------------------------------------------------------------------

def collect(root: Path = ROOT) -> list[dict]:
    """Every receipted scan, verified against its fingerprints, oldest first."""
    config = json.loads((root / "data/captures.json").read_text())
    if config.get("schema_version") != 1:
        raise InvalidCapture("Unsupported capture registry schema")
    captures, seen = [], set()
    for receipt in config["captures"]:
        path = (root / receipt["path"]).resolve()
        if not path.is_relative_to((root / "data/captures").resolve()):
            raise InvalidCapture("Capture path escapes capture directory")
        if path.name.endswith(".market.json"):
            if hashlib.sha256(path.read_bytes()).hexdigest() != receipt["extraction_sha256"]:
                raise InvalidCapture(f"{path.name} differs from its receipt fingerprint")
            parsed = load_market_extract(path)
        else:
            parsed = parse_capture(path, markets=receipt["publish_markets"])
        if parsed["source_sha256"] != receipt["source_sha256"]:
            raise InvalidCapture("Source hash differs from capture receipt")
        if receipt["environment"] not in ENVIRONMENTS:
            raise InvalidCapture(f"Unknown environment {receipt['environment']!r}")
        datetime.strptime(receipt["received_on"], "%Y-%m-%d")
        if parsed["source_sha256"] in seen:
            continue
        seen.add(parsed["source_sha256"])
        times = [t for t in parsed["source_scan_timestamps"].values() if type(t) is int and t > 0]
        if not times:
            raise InvalidCapture(f"{path.name} records no scan time")
        moment = datetime.fromtimestamp(max(times), timezone.utc)
        captures.append({**receipt, **parsed, "capture_timestamp": max(times),
                         "capture_time": moment.isoformat().replace("+00:00", "Z"),
                         "capture_date": moment.date().isoformat(), "source_file": path.name})
    return sorted(captures, key=lambda c: (c["capture_timestamp"], c["source_sha256"]))


def load_names(root: Path = ROOT) -> dict:
    path = root / "data/items.json"
    if not path.exists():
        return {"names": {}, "source": None}
    return json.loads(path.read_text())


def item_name(key: str, names: dict) -> str:
    base = names.get(str(item_id(key))) or f"Item {item_id(key)}"
    return f"{base} {suffix(key)}" if suffix(key) else base


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# --- Markets ------------------------------------------------------------------

def build_markets(captures: list[dict], names: dict) -> list[dict]:
    """One record per market: its scans, and per item the latest price, the day it
    was last seen, how many were listed that day, and the daily low/high history.
    Later scans overwrite the same day from earlier scans."""
    markets = {}
    for capture in captures:
        for raw_key in capture["publish_markets"]:
            if raw_key not in capture["markets"]:
                raise InvalidCapture(f"Requested market {raw_key!r} is absent")
            slug = slugify(capture["environment"] + "-" + raw_key)
            market = markets.setdefault(slug, {
                "slug": slug, "key": raw_key, "environment": capture["environment"],
                "environment_label": ENVIRONMENTS[capture["environment"]],
                "sample": False, "scans": [], "items": {}})
            data = capture["markets"][raw_key]
            sample = capture.get("sample", {})
            market["sample"] |= not sample.get("complete_market", True)
            if sample.get("original_market_counts", {}).get(raw_key):
                market["original_count"] = sample["original_market_counts"][raw_key]
            repeat = bool(market["scans"]) and market["scans"][-1]["payload_sha256"] == data["payload_sha256"]
            market["scans"].append({"date": capture["capture_date"], "time": capture["capture_time"],
                                    "source_sha256": capture["source_sha256"], "items": len(data["items"]),
                                    "payload_sha256": data["payload_sha256"], "unchanged": repeat,
                                    "received_on": capture["received_on"]})
            for key, fields in data["items"].items():
                item = market["items"].setdefault(key, {"key": key, "id": item_id(key),
                                                       "name": item_name(key, names), "days": {}})
                item["price"], item["price_scan"] = fields["m"], capture["capture_date"]
                for day, high in fields["h"].items():
                    item["days"][int(day)] = {"low": fields["l"].get(day, high), "high": high,
                                              "listed": fields["a"].get(day)}
    result = []
    for market in markets.values():
        items = list(market["items"].values())
        last_day = max((max(i["days"]) for i in items if i["days"]), default=None)
        for item in items:
            summarise(item, last_day)
        items.sort(key=lambda i: (i["name"].lower(), i["key"]))
        market["items"] = items
        market["last_day"] = last_day
        market["last_date"] = day_date(last_day) if last_day is not None else market["scans"][-1]["date"]
        market["current"] = [i for i in items if i["current"]]
        market["name"] = market["key"]
        result.append(market)
    return sorted(result, key=lambda m: (m["environment"] != "forever", m["sample"], -(m["last_day"] or 0), m["key"]))


def median(values: list[int]) -> int | None:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if not ordered:
        return None
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) // 2


def summarise(item: dict, last_day: int | None) -> None:
    """Typical price: the median of each day's lowest price over the item's last
    seven days of records. A median ignores one-day spikes and troll listings
    (real scans include 99,999,999,999-copper listings), which the latest
    price alone does not. Weekly change compares this week's median with the
    week before's."""
    days = item["days"]
    seen = max(days) if days else None
    item["last_seen"] = day_date(seen) if seen is not None else None
    item["listed"] = days[seen]["listed"] if seen is not None else None
    item["current"] = seen is not None and last_day is not None and last_day - seen < CURRENT_DAYS
    recent = [v["low"] for d, v in days.items() if seen is not None and seen - 6 <= d <= seen]
    before = [v["low"] for d, v in days.items() if seen is not None and seen - 13 <= d <= seen - 7]
    item["typical"] = median(recent) if recent else item["price"]
    item["recent_days"], item["before_days"] = len(recent), len(before)
    earlier = median(before)
    item["change"] = (round((item["typical"] - earlier) / earlier * 100)
                      if len(recent) >= 2 and len(before) >= 2 and earlier else None)
    item["spark"] = ([days[d]["low"] if d in days else None for d in range(last_day - SPARK_DAYS + 1, last_day + 1)]
                     if last_day is not None else [])


def highlights(market: dict) -> dict:
    """Most listed on the newest day, and the biggest weekly moves among items
    with real volume, for the page and for ChatGPT."""
    newest = [i for i in market["current"] if i["last_seen"] == market["last_date"] and i["listed"]]
    most_listed = sorted(newest, key=lambda i: (-i["listed"], i["name"]))[:12]
    # Moves only count with three days of records in both weeks, at least 50c, and some volume.
    movers = [i for i in market["current"] if i["change"] is not None and i["recent_days"] >= 3
              and i["before_days"] >= 3 and i["typical"] >= 50 and (i["listed"] or 0) >= 5]
    rising = sorted((i for i in movers if i["change"] > 0), key=lambda i: -i["change"])[:6]
    falling = sorted((i for i in movers if i["change"] < 0), key=lambda i: i["change"])[:6]
    return {"most_listed": most_listed, "rising": rising, "falling": falling}


def money(copper: int | None) -> str:
    if copper is None:
        return ""
    gold, rest = divmod(copper, 10000)
    silver, copper = divmod(rest, 100)
    parts = [f"{gold:,}g" if gold else "", f"{silver}s" if silver or gold else "", f"{copper}c"]
    return " ".join(p for p in parts if p)


def tsv(header: list[str], rows) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(["" if v is None else v for v in row] for row in rows)
    return buffer.getvalue()


# --- Journal ------------------------------------------------------------------

def load_journal(root: Path = ROOT) -> list[dict]:
    entries = []
    for path in sorted((root / "journal").glob("*.md")):
        if path.name.startswith("_"):
            continue  # templates and drafts
        text = path.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if not match:
            raise ValueError(f"{path.name}: start with a --- header block (see journal/_template.md)")
        meta = {}
        for line in match.group(1).splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                key, _, value = line.partition(":")
                meta[key.strip().lower()] = value.split(" #")[0].strip()
        for field in ("title", "type", "date"):
            if not meta.get(field):
                raise ValueError(f"{path.name}: missing {field}")
        if meta["type"] not in JOURNAL_TYPES:
            raise ValueError(f"{path.name}: type must be one of {', '.join(JOURNAL_TYPES)}")
        if meta.get("status") and meta["status"] not in JOURNAL_STATUS:
            raise ValueError(f"{path.name}: status must be one of {', '.join(JOURNAL_STATUS)}")
        for field in ("date", "updated"):
            if meta.get(field):
                date.fromisoformat(meta[field])
        entries.append({**meta, "slug": slugify(path.stem), "body": match.group(2).strip(),
                        "html": render(match.group(2)), "file": f"journal/{path.name}",
                        "type_label": JOURNAL_TYPES[meta["type"]],
                        "status_label": JOURNAL_STATUS.get(meta.get("status", ""), "")})
    return sorted(entries, key=lambda e: (e.get("updated") or e["date"], e["title"]), reverse=True)


# --- Output -------------------------------------------------------------------

def build(root: Path = ROOT, out: Path | None = None, base: str = "/FvrRepo/") -> dict:
    out = Path(out or root / "dist")
    if out.resolve() in (root.resolve(), (root / "data").resolve()) or not out.resolve().is_relative_to(root.resolve()):
        raise ValueError("Output must be a dedicated directory inside the repository")
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
    captures = collect(root)
    names = load_names(root)
    markets = build_markets(captures, names["names"])
    journal = load_journal(root)
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit = os.environ.get("GITHUB_SHA", "local")
    revision = hashlib.sha256(json.dumps({
        "schema": SCHEMA, "parser": PARSER_VERSION,
        "scans": [[c["source_sha256"], c.get("extraction_sha256")] for c in captures],
        "names": names.get("source", {}) and names["source"].get("sha256"),
        "journal": [e["body"] for e in journal]}, sort_keys=True).encode()).hexdigest()[:12]

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(root / "site/assets", out / "assets")
    fingerprints = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:10] for f in (root / "site/assets").iterdir() if f.is_file()}
    site = pages.Site(base=base, url=SITE_URL, revision=revision, built=built,
                      credit=bool(names.get("source")), assets=fingerprints)

    def write(path: str, content: str) -> str:
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return base + path

    def page(path: str, html_text: str) -> None:
        write(path + "index.html" if path.endswith("/") or not path else path, html_text)

    write(".nojekyll", "")
    catalogue = []
    for market in markets:
        folder = f"prices/{market['slug']}/"
        market["url"] = base + folder
        market["highlights"] = highlights(market)
        market["files"] = {
            "prices_tsv": write(folder + "prices.tsv", tsv(
                ["item_id", "item_key", "name", "typical_copper", "typical", "latest_copper", "latest", "last_seen",
                 "listed_that_day", "change_7d_pct", "latest_from_scan"],
                [[i["id"], i["key"], i["name"], i["typical"], money(i["typical"]), i["price"], money(i["price"]), i["last_seen"],
                  i["listed"], i["change"], i["price_scan"]] for i in market["items"]])),
            "history_tsv": write(folder + "history.tsv", tsv(
                ["item_id", "item_key", "name", "date", "low_copper", "high_copper", "listed"],
                [[i["id"], i["key"], i["name"], day_date(d), v["low"], v["high"], v["listed"]]
                 for i in market["items"] for d, v in sorted(i["days"].items())])),
            "prices_json": write(folder + "prices.json", json.dumps({
                "schema_version": SCHEMA, "revision": revision, "market": market["key"],
                "environment": market["environment"], "last_date": market["last_date"],
                "last_day": market["last_day"], "spark_days": SPARK_DAYS,
                "columns": ["key", "id", "name", "typical", "price", "last_seen", "listed", "change", "current", "spark"],
                "rows": [[i["key"], i["id"], i["name"], i["typical"], i["price"], i["last_seen"], i["listed"], i["change"],
                          i["current"], i["spark"]] for i in market["items"]]}, separators=(",", ":")) + "\n"),
            "history_json": write(folder + "history.json", json.dumps({
                "schema_version": SCHEMA, "revision": revision,
                "history": {i["key"]: [[day_date(d), v["low"], v["high"], v["listed"]] for d, v in sorted(i["days"].items())]
                            for i in market["items"]}}, separators=(",", ":")) + "\n"),
        }
        page(folder, pages.market_page(site, market))
        catalogue.append({"name": market["key"], "environment": market["environment"], "sample": market["sample"],
                          "page": market["url"], "last_date": market["last_date"], "items": len(market["items"]),
                          "current_items": len(market["current"]),
                          "scans": [{k: s[k] for k in ("date", "items", "source_sha256", "unchanged")} for s in market["scans"]],
                          **market["files"]})
    for entry in journal:
        entry["url"] = base + f"journal/{entry['slug']}/"
        page(f"journal/{entry['slug']}/", pages.journal_entry(site, entry))
    page("", pages.home(site, markets, journal))
    page("prices/", pages.markets_index(site, markets))
    page("journal/", pages.journal_index(site, journal))
    page("about/", pages.about(site, markets, captures, names.get("source")))

    full = pages.llms_full(site, markets, journal, names.get("source"))
    write("llms-full.txt", full)
    write("llms.txt", pages.llms_index(site, markets, journal))
    urls = [""] + ["prices/", "journal/", "about/"] + [f"prices/{m['slug']}/" for m in markets] + [f"journal/{e['slug']}/" for e in journal]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("data/manifest.json", json.dumps({
        "schema_version": SCHEMA, "site": pages.SITE_NAME, "revision": revision, "built": built,
        "source_commit": commit, "parser_version": PARSER_VERSION, "read_first": base + "llms-full.txt",
        "markets": catalogue,
        "journal": [{k: e.get(k) for k in ("title", "type", "class", "status", "date", "updated", "summary", "url")} for e in journal],
        "item_names": names.get("source")}, indent=1) + "\n")

    for path in out.rglob("*"):
        if path.is_file() and path.suffix not in (".html", ".css", ".js", ".svg", ".webp", ".jpg", ".png", ".json", ".tsv", ".txt", ".xml", ".woff2", ""):
            raise InvalidCapture(f"Unexpected public file type: {path.name}")
    if any(out.rglob("*.lua")):
        raise InvalidCapture("Raw Lua must not be published")
    return {"revision": revision, "scans": len(captures), "markets": len(markets),
            "items": sum(len(m["items"]) for m in markets), "journal": len(journal), "output": str(out)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the site into dist/.")
    parser.add_argument("--base-path", default="/FvrRepo/")
    print(json.dumps(build(base=parser.parse_args().base_path), indent=2))
