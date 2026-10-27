"""Build the Tazdingo site into dist/. Standard-library Python only.

Inputs: data/captures.json (scan receipts), data/captures/** (market-only extracts),
data/items.json (names), data/foreverdb.json (ForeverDB data), data/game.json (classes,
professions, world topics, links) and content/**/*.md (notes).
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
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

import ah_pages
import market
import market_store
import pages
import sections
from auctionator import (InvalidCapture, PARSER_VERSION, day_date, item_id,
                         load_market_extract, newest_day, parse_capture, suffix)
from markup import render

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 2
SITE_URL = "https://faresbn.github.io/Tazdingo/"
ENVIRONMENTS = {"forever": "Forever", "forever-beta": "Forever Beta", "tbc": "TBC Anniversary", "era": "Classic Era"}
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
        markets = [m for m in receipt["publish_markets"] if (parsed["source_sha256"], m) not in seen]
        if not markets:
            continue  # the same file and market published twice counts once
        seen.update((parsed["source_sha256"], m) for m in markets)
        times = [t for t in parsed["source_scan_timestamps"].values() if type(t) is int and t > 0]
        if not times:
            raise InvalidCapture(f"{path.name} records no scan time")
        moment = datetime.fromtimestamp(max(times), timezone.utc)
        newest = newest_day({m: parsed["markets"][m] for m in receipt["publish_markets"] if m in parsed["markets"]})
        captures.append({**receipt, **parsed, "publish_markets": markets, "capture_timestamp": max(times),
                         "capture_time": moment.isoformat().replace("+00:00", "Z"),
                         "capture_date": day_date(newest) if newest is not None else moment.date().isoformat(),
                         "environment_label": ENVIRONMENTS[receipt["environment"]],
                         "source_file": path.name})
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

def build_markets(captures: list[dict], names: dict, store: dict | None = None) -> list[dict]:
    """One record per market: its scans, and per item the latest price, the day it
    was last seen, how many were listed that day, the daily low/high history, and every
    timestamped price observation (one per scan that saw the item on its day).
    `captures` are the original whole-database extracts (the Beta sample); `store` holds
    scan records and the daily archive (scripts/market_store.py)."""
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
            scan_day = max((int(d) for fields in data["items"].values() for d in fields["h"]), default=None)
            stamps = capture.get("source_scan_timestamps", {})
            full = stamps.get("TimeOfLastReplicateScan")
            # Only a full scan that was the file's latest scan, credited to this market by
            # market_store.full_scan_market, makes the file that scan's snapshot of this market.
            owner = market_store.full_scan_market({"source_scan_timestamps": stamps, "markets": capture["markets"]}) if stamps else None
            new_full = owner == raw_key and full > market.get("last_full_scan", 0)
            if new_full:
                market["last_full_scan"] = full
                market.setdefault("full_scan_coverage", []).append(sum(1 for f in data["items"].values() if str(scan_day) in f["h"]))
            for key, fields in data["items"].items():
                item = market["items"].setdefault(key, {"key": key, "id": item_id(key),
                                                       "name": item_name(key, names), "days": {}, "obs": [], "full_obs": []})
                if scan_day is not None and str(scan_day) in fields["h"]:
                    item["obs"].append((capture["capture_timestamp"], fields["m"], scan_day))
                    if new_full:
                        item["full_obs"].append((full, fields["m"], scan_day))
                # Another account's newer file can hold an older sighting of this item.
                seen_here = max((int(d) for d in fields["h"]), default=-1)
                if seen_here >= item.get("price_day", -1):
                    item["price"], item["price_scan"], item["price_day"] = fields["m"], capture["capture_date"], seen_here
                for day, high in fields["h"].items():
                    # Within one account's file a day's values only widen as the day goes on, and two
                    # accounts scanning the same day each hold part of it, so combine rather than overwrite.
                    new = {"low": fields["l"].get(day, high), "high": high, "listed": fields["a"].get(day)}
                    old = item["days"].get(int(day))
                    if old:
                        new = {"low": min(old["low"], new["low"]), "high": max(old["high"], new["high"]),
                               "listed": max((v for v in (old["listed"], new["listed"]) if v is not None), default=None)}
                    item["days"][int(day)] = new
    for slug, entry in (store or {}).items():
        add_store_market(markets, slug, entry, names)
    result = []
    for market in markets.values():
        items = list(market["items"].values())
        last_day = max((max(i["days"]) for i in items if i["days"]), default=None)
        for item in items:
            item["obs"].sort()
            item["full_obs"].sort()
            summarise(item, last_day)
        items.sort(key=lambda i: (i["name"].lower(), i["key"]))
        market["items"] = items
        market["last_day"] = last_day
        market["last_date"] = day_date(last_day) if last_day is not None else market["scans"][-1]["date"]
        market["current"] = [i for i in items if i["current"]]
        market["name"] = market["key"]
        result.append(market)
    return sorted(result, key=lambda m: (m["environment"] != "forever", m["sample"], -(m["last_day"] or 0), m["key"]))


def add_store_market(markets: dict, slug: str, entry: dict, names: dict) -> None:
    """A market kept as scan records and a daily archive: days from the archive and the
    records, the latest price from the newest record that saw the item."""
    if entry["environment"] not in ENVIRONMENTS:
        raise InvalidCapture(f"Unknown environment {entry['environment']!r}")
    market = markets.setdefault(slug, {"slug": slug, "key": entry["market"], "environment": entry["environment"],
                                       "environment_label": ENVIRONMENTS[entry["environment"]],
                                       "sample": False, "scans": [], "items": {}})
    market["folded_scans"] = entry["folded"]
    market.setdefault("full_scan_coverage", []).extend(entry.get("full_scan_items", []))

    def item_of(key):
        return market["items"].setdefault(key, {"key": key, "id": item_id(key), "name": item_name(key, names), "days": {}, "obs": [], "full_obs": []})

    def merge(item, day, low, high, listed):
        old = item["days"].get(day)
        if old:
            low, high = min(old["low"], low), max(old["high"], high)
            listed = max((v for v in (old["listed"], listed) if v is not None), default=None)
        item["days"][day] = {"low": low, "high": high, "listed": listed}

    for day, rows in entry["daily"].items():
        for key, (low, high, listed, _scans, _median) in rows.items():
            merge(item_of(key), day, low, high, listed)
    previous, last_seen, last_full = None, {}, 0
    for record in entry["records"]:
        full = record.get("full_scan_timestamp")
        # Only an upload whose latest scan was a full scan is that scan's snapshot (a later
        # search would otherwise move its prices back to the full scan's time).
        new_full = full is not None and full == record["scan_timestamp"] and full > last_full
        if new_full:
            last_full = full
        moment = datetime.fromtimestamp(record["scan_timestamp"], timezone.utc)
        market["scans"].append({"date": day_date(record["day"]), "time": moment.isoformat().replace("+00:00", "Z"),
                                "source_sha256": record["source_sha256"], "items": len(record["items"]),
                                "payload_sha256": None, "unchanged": record["items"] == previous, "received_on": None})
        previous = record["items"]
        for key, row in record["items"].items():
            latest, low, high, listed = row
            item = item_of(key)
            merge(item, record["day"], low, high, listed)
            # A recorded price when the item is new to this day or something about it changed: an
            # upload carries every item seen earlier in the day, unchanged, whether or not a later
            # scan saw it again (Auctionator keeps one latest price and day-wide figures). Its time
            # is the upload's; Auctionator may have seen it earlier.
            if last_seen.get(key) != (record["day"], row):
                item["obs"].append((record["scan_timestamp"], latest, record["day"]))
                last_seen[key] = (record["day"], row)
            # An upload containing a new full scan is also a sample of every item listed that day,
            # changed or not, at the full scan's own time: the basis for time-of-day patterns.
            if new_full:
                item["full_obs"].append((full, latest, record["day"]))
            if record["day"] >= item.get("price_day", -1):
                item["price"], item["price_day"], item["price_scan"] = latest, record["day"], day_date(record["day"])
    for item in market["items"].values():
        if "price" not in item and item["days"]:  # only in the archive: its scan records have aged out
            day = max(item["days"])
            item["price"], item["price_day"], item["price_scan"] = item["days"][day]["low"], day, day_date(day)


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
    item["seen_day"] = seen
    item["last_seen"] = day_date(seen) if seen is not None else None
    item["listed"] = days[seen]["listed"] if seen is not None else None
    item["current"] = seen is not None and last_day is not None and last_day - seen < CURRENT_DAYS
    recent = [v["low"] for d, v in days.items() if seen is not None and seen - 6 <= d <= seen]
    before = [v["low"] for d, v in days.items() if seen is not None and seen - 13 <= d <= seen - 7]
    item["typical"] = median(recent) if recent else item["price"]
    item["recent_days"], item["before_days"] = len(recent), len(before)
    earlier = median(before)
    item["change"] = (round((item["typical"] - earlier) / earlier * 100)
                      if item["current"] and len(recent) >= 2 and len(before) >= 2 and earlier else None)
    item["spark"] = ([days[d]["low"] if d in days else None for d in range(last_day - SPARK_DAYS + 1, last_day + 1)]
                     if last_day is not None else [])
    item["volatility"] = volatility([v["low"] for d, v in days.items() if seen is not None and seen - 13 <= d <= seen])


def volatility(lows: list[int]) -> str | None:
    """How far an item's daily cheapest listing swings over its last two weeks of records:
    from its cheapest day to its 80th-percentile day, relative to the median. The top is
    trimmed because troll listings only ever spike upwards; a cheap day was a real bargain.
    Early in a game the market is still finding prices, so a price is only as useful as it is steady."""
    if len(lows) < 3:
        return None  # not enough days to tell
    ordered = sorted(lows)
    low, high = ordered[0], ordered[round(0.8 * (len(ordered) - 1))]
    spread = (high - low) / max(median(ordered), 1)
    return "steady" if spread < 0.25 else "moving" if spread < 0.75 else "volatile"


def highlights(market: dict) -> dict:
    """Most listed on the newest day, and the biggest weekly moves among items
    with real volume, for the page and for ChatGPT."""
    newest = [i for i in market["current"] if i["last_seen"] == market["last_date"] and i["listed"]]
    most_listed = sorted(newest, key=lambda i: (-i["listed"], i["name"]))[:12]
    # Moves only count with three days of records in both weeks, at least 50c, and some volume.
    movers = [i for i in market["current"] if i["change"] is not None and i["recent_days"] >= 3
              and market["last_day"] - i["seen_day"] <= 2
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


def sheet_text(value: str) -> str:
    """Spreadsheets run cells starting with = + - @ as formulas; a leading ' stops that."""
    return "'" + value if value[:1] in ("=", "+", "-", "@", "\t", "\r") else value


def tsv(header: list[str], rows) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(header)
    writer.writerows(["" if v is None else v for v in row] for row in rows)
    return buffer.getvalue()


# --- Content ------------------------------------------------------------------

CONFIDENCE = {"idea": "Idea", "testing": "Testing", "tested": "Tested", "outdated": "Outdated"}
STATUS = {"pre-launch": "Pre-launch", "live": "Live"}
CLASS_EXTRAS = {"overview": "Overview", "hybrid": "Hybrid builds", "macros": "Macros"}
SECTION_NAMES = {"at a glance": "glance", "what the guides say": "guides", "ledger findings": "findings", "field findings": "findings", "read more": "more"}
REQUIRED_SECTIONS = ["At a glance", "What the guides say", "Field findings", "Read more"]
FIELDS = {"updated", "summary", "sources", "confidence", "status", "verified"}
# Words that must never appear on the public site: the people behind it and the assistant they use.
PRIVATE = re.compile(r"\b(?:chatgpt|fares|mike)\b", re.I)


def content_places(game: dict) -> dict:
    """Every page a content file can fill, keyed by its path under content/ without .md."""
    places = {}
    for c in game["classes"]:
        for spec in c["specs"]:
            places[f"classes/{c['slug']}/{spec['slug']}"] = {"title": f"{spec['name']} {c['name']}", "url": f"classes/{c['slug']}/{spec['slug']}/"}
        for slug, name in CLASS_EXTRAS.items():
            anchor = "" if slug == "overview" else f"#{slug}"
            places[f"classes/{c['slug']}/{slug}"] = {"title": f"{c['name']}: {name.lower()}", "url": f"classes/{c['slug']}/{anchor}"}
    for p in game["professions"]:
        places[f"professions/{p['slug']}"] = {"title": p["name"], "url": f"professions/{p['slug']}/"}
    for t in game["world"]:
        places[f"world/{t['slug']}"] = {"title": t["name"], "url": f"world/{t['slug']}/"}
    for m in game["more"]:
        places[f"more/{m['slug']}"] = {"title": m["name"], "url": f"more/{m['slug']}/"}
    return places


LEDGER_LINK = re.compile(r'href="ledger:([a-z0-9/#-]*)"')


def ledger_links(html_text: str, base: str) -> str:
    """`ledger:classes/mage/frost/` in a page's Markdown links to that page on this site, whatever its address."""
    return LEDGER_LINK.sub(lambda m: f'href="{base}{m.group(1)}"', html_text)


def split_sections(body: str, base: str = "/", prefix: str = "") -> list[dict]:
    """A note's `## ` sections, each rendered on its own, so the page can style them
    (the guides' summary, our findings and the sources look different)."""
    sections, current = [], {"heading": "", "lines": []}
    for line in body.splitlines():
        if line.startswith("## "):
            if current["heading"] or any(l.strip() for l in current["lines"]):
                sections.append(current)
            current = {"heading": line[3:].strip(), "lines": []}
        else:
            current["lines"].append(line)
    sections.append(current)
    result, used = [], set(SECTION_NAMES.values()) | {"intro", "changes", "guides-and-tools", "on-this-page"}
    for sec in sections:
        text = "\n".join(sec["lines"]).strip()
        kind = SECTION_NAMES.get(sec["heading"].lower(), "other")
        empty = kind == "findings" and text.rstrip(".").lower() in ("", "nothing recorded yet")
        html_text = ledger_links(render(text, used), base)
        if prefix:  # notes embedded in another page (a class's hybrid builds and macros) get their own anchors
            html_text = re.sub(r'<(h[2-4]) id="', rf'<\1 id="{prefix}', html_text)
        result.append({"heading": sec["heading"], "kind": kind, "html": html_text, "empty": empty,
                       "slug": prefix + (kind if kind != "other" else (slugify(sec["heading"]) or "intro")),
                       "toc": re.findall(r'<h3 id="([^"]+)">(.*?)</h3>', html_text)})
    return result


def front_matter(text: str, name: str) -> tuple[dict, str]:
    match = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not match:
        raise ValueError(f"{name}: start with a --- header block (see docs/chatgpt/UPDATING.md)")
    meta = {}
    for line in match.group(1).splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            key, _, value = line.partition(":")
            key = key.strip().lower()
            if key not in FIELDS:
                raise ValueError(f"{name}: unknown header field {key!r}; allowed: {', '.join(sorted(FIELDS))}")
            if key in meta:
                raise ValueError(f"{name}: header field {key!r} appears twice")
            meta[key] = value.split(" #")[0].strip()
    return meta, match.group(2).strip()


def check_sections(name: str, key: str, body: str) -> None:
    """Class, spec, profession and world pages carry the four sections, once each, in order.
    More lists may be shaped freely but must keep Field findings and Read more."""
    headings = [line[3:].strip() for line in body.splitlines() if line.startswith("## ")]
    required = REQUIRED_SECTIONS if not key.startswith("more/") else REQUIRED_SECTIONS[2:]
    found = [h for h in headings if h in REQUIRED_SECTIONS]
    if [h for h in found if h in required] != required or len(found) != len(set(found)):
        raise ValueError(f"{name}: needs these sections once each, in this order: {', '.join('## ' + h for h in required)}"
                         f" (found: {', '.join(headings) or 'none'})")


def embedded_prefix(key: str) -> str:
    """Hybrid builds and macros appear inside the class page, so their anchors are namespaced."""
    part = key.rsplit("/", 1)[-1]
    return f"{part}-" if key.startswith("classes/") and part in ("hybrid", "macros") else ""


def load_content(root: Path, game: dict, launch: date, base: str = "/") -> dict:
    places = content_places(game)
    pages_ = {}
    for path in sorted((root / "content").rglob("*")):
        if path.is_dir():
            continue
        if path.suffix != ".md":
            raise ValueError(f"content/{path.relative_to(root / 'content').as_posix()}: only Markdown pages belong in content/")
        key = path.relative_to(root / "content").with_suffix("").as_posix()
        name = f"content/{key}.md"
        if key not in places:
            raise ValueError(f"{name} isn't a page the site knows. See docs/chatgpt/UPDATING.md for the valid places.")
        meta, body = front_matter(path.read_text(encoding="utf-8"), name)
        for field in ("updated", "summary"):
            if not meta.get(field):
                raise ValueError(f"{name}: missing {field}")
        date.fromisoformat(meta["updated"])
        if meta.get("verified"):
            date.fromisoformat(meta["verified"])
        if meta.get("confidence") and meta["confidence"] not in CONFIDENCE:
            raise ValueError(f"{name}: confidence must be one of {', '.join(CONFIDENCE)}")
        if meta.get("status") and meta["status"] not in STATUS:
            raise ValueError(f"{name}: status must be one of {', '.join(STATUS)}")
        check_sections(name, key, body)
        # A page is Pre-launch until someone marks it Live after checking it in the live game:
        # an edit after launch doesn't make old Beta advice current.
        status = meta.get("status") or "pre-launch"
        pages_[key] = {**meta, **places[key], "key": key, "file": name, "body": body, "html": ledger_links(render(body), base),
                       "sections": split_sections(body, base, embedded_prefix(key)), "status": status, "status_label": STATUS[status],
                       "confidence_label": CONFIDENCE.get(meta.get("confidence", ""), "")}
    return pages_


def history(root: Path, after: str | None = None) -> list[dict]:
    """Every change to the site's content, newest first, from git: the change log writes itself.
    `after` is the commit the public log starts from (data/game.json: log_after)."""
    paths = ["--", "content", "data/captures.json", "data/foreverdb.json"]
    for revisions in ([f"{after}..HEAD"] if after else [], []):
        try:
            out = subprocess.run(["git", "log", "--format=%x1e%cs%x1f%s", "--name-only", *revisions, *paths],
                                 cwd=root, capture_output=True, text=True, check=True).stdout
            break
        except (OSError, subprocess.CalledProcessError):
            out = ""  # not a git checkout, or the start commit isn't in a shallow clone
    entries = []
    for block in out.split("\x1e")[1:]:
        head, *files = block.strip().split("\n")
        when, subject = head.split("\x1f", 1)
        if PRIVATE.search(subject):
            subject = "Page updated"  # commit subjects are public here; one that names someone is replaced, not shown
        entries.append({"date": when, "subject": subject, "files": [f for f in files if f]})
    return entries


def change_url(path: str, places: dict) -> str:
    if path.startswith("content/"):
        key = path[len("content/"):].removesuffix(".md")
        return places.get(key, {}).get("url", "")
    return {"data/captures.json": "prices/", "data/foreverdb.json": "prices/craft/"}.get(path, "")


# --- Price tools ----------------------------------------------------------------

def price_book(market: dict | None, fdb: dict) -> dict:
    """Per item: our scan, ForeverDB's players' prices, and the cheapest vendor price."""
    book = {}
    for item in (market or {}).get("items", []):
        if not suffix(item["key"]) and item["key"].isdigit():
            book.setdefault(item["id"], {})["ours"] = item
    for key, value in fdb.get("prices", {}).items():
        book.setdefault(int(key), {})["fdb"] = value
    for key, value in fdb.get("vendor", {}).items():
        book.setdefault(int(key), {})["vendor"] = value["price"]
    return book


def market_value(entry: dict | None) -> tuple[int, str] | None:
    """Estimated asking value: our typical price when current, sufficiently listed, and steady or
    moving over at least three days; otherwise ForeverDB's median across realms when enough
    players saw it. A price seen on one or two days doesn't feed a gold-making table."""
    if not entry:
        return None
    ours = entry.get("ours")
    if ours and ours["current"] and (ours["listed"] or 0) >= 5 and ours["volatility"] in ("steady", "moving"):
        return ours["typical"], "our scan"
    theirs = entry.get("fdb")
    if theirs and theirs.get("listed", 0) >= 20 and theirs.get("realms", 0) >= 2:
        return theirs["median"], "ForeverDB"
    return None


def buy_cost(entry: dict | None) -> tuple[int, str] | None:
    if entry and entry.get("vendor"):
        return entry["vendor"], "vendor"
    return market_value(entry)


def craft_table(fdb: dict, book: dict, names: dict) -> list[dict]:
    rows = []
    for profession, recipes in fdb.get("recipes", {}).items():
        for r in recipes:
            value = market_value(book.get(r["item"]))
            costs = [(buy_cost(book.get(i)), n, i) for i, n in r["reagents"]]
            if not value or any(c is None for c, _, _ in costs) or book.get(r["item"], {}).get("vendor"):
                continue
            cost = sum(c[0] * n for c, n, _ in costs)
            sells = value[0] * r["count"]
            if sells <= cost:
                continue
            rows.append({"profession": profession, "name": r["name"], "skill": r["skill"], "item": r["item"], "count": r["count"],
                         "new": r["new"], "sells": sells, "cost": cost, "margin": sells - cost,
                         "value_source": value[1], "reagents": [[i, n, names.get(str(i), f"Item {i}"), c[0], c[1]] for c, n, i in costs]})
    return sorted(rows, key=lambda r: -r["margin"])


def crate_table(fdb: dict, book: dict, names: dict) -> list[dict]:
    rows = []
    for crate in fdb.get("crates", []):
        bundles = []
        for item, count in crate["bundles"]:
            price = buy_cost(book.get(item))
            bundles.append({"item": item, "name": names.get(str(item), f"Item {item}"), "count": count,
                            "cost": price[0] * count if price else None, "source": price[1] if price else None})
        priced = [b for b in bundles if b["cost"] is not None]
        rows.append({"item": crate["item"], "name": names.get(str(crate["item"]), f"Crate {crate['item']}"), "level": crate["level"],
                     "bundles": sorted(bundles, key=lambda b: (b["cost"] is None, b["cost"] or 0)),
                     "cheapest": min(priced, key=lambda b: b["cost"]) if priced else None})
    return sorted(rows, key=lambda r: (r["level"], (r["cheapest"] or {}).get("cost") or 10**12))


def materials_table(fdb: dict, book: dict, names: dict) -> list[dict]:
    """Raw materials: reagents no recipe makes and no vendor sells (gathered, skinned or dropped)."""
    made = {r["item"] for recipes in fdb.get("recipes", {}).values() for r in recipes}
    used = {}
    for recipes in fdb.get("recipes", {}).values():
        for r in recipes:
            for i, _ in r["reagents"]:
                used.setdefault(i, set()).add(r["name"])
    rows = []
    for item, recipes in used.items():
        entry = book.get(item, {})
        if item in made or entry.get("vendor"):
            continue
        value = market_value(entry)
        if not value:
            continue
        ours = entry.get("ours")
        rows.append({"item": item, "name": names.get(str(item), f"Item {item}"), "value": value[0], "source": value[1],
                     "volatility": ours["volatility"] if ours else None, "listed": ours["listed"] if ours else None,
                     "used_in": len(recipes)})
    return sorted(rows, key=lambda r: -r["value"])


def search_index(ctx: dict) -> list[list[str]]:
    game, base = ctx["game"], ctx["base"]
    entries = []
    for c in game["classes"]:
        entries.append([c["name"], f"{base}classes/{c['slug']}/", "Class"])
        for spec in c["specs"]:
            entries.append([f"{spec['name']} {c['name']}", f"{base}classes/{c['slug']}/{spec['slug']}/", "Spec"])
    for p in game["professions"]:
        entries.append([p["name"], f"{base}professions/{p['slug']}/", "Profession"])
    for t in game["world"]:
        entries.append([t["name"], f"{base}world/{t['slug']}/", "World"])
    for m in game["more"]:
        entries.append([m["name"], f"{base}more/{m['slug']}/", "More"])
    entries.append(["Auction House: deals, investments and movers", f"{base}prices/", "Auction House"])
    for slug, name in (("craft", "What to craft"), ("crates", "Waylaid Crates: cheapest fill"), ("materials", "Materials worth gathering")):
        entries.append([name, f"{base}prices/{slug}/", "Auction House"])
    market = ctx["primary"]
    if market:
        for item in market["items"]:
            entries.append([item["name"], item["url"], "Item"])
    return entries


def load_api(root: Path) -> dict:
    """The slim ForeverDB API data (scripts/foreverdb_api.py), when it has been fetched."""
    path = root / "data/foreverdb-api.json"
    return json.loads(path.read_text()) if path.exists() else {}


def market_module_analyse(market_record: dict, vendor: dict, categories: dict) -> dict:
    return market.analyse(market_record, vendor, categories)


def recipes_by_item(fdb: dict) -> dict:
    """Which recipes make each item, and which use it as a reagent."""
    makes, uses = {}, {}
    for profession, recipes in fdb.get("recipes", {}).items():
        for recipe in recipes:
            makes.setdefault(recipe["item"], []).append((profession, recipe))
            for reagent, _count in recipe["reagents"]:
                uses.setdefault(reagent, []).append((profession, recipe))
    return {"makes": makes, "uses": uses}


# --- Output -------------------------------------------------------------------

def build(root: Path = ROOT, out: Path | None = None, base: str = "/Tazdingo/") -> dict:
    out = Path(out or root / "dist").resolve()  # follows the iCloud shield's dist -> dist.nosync link
    if out.resolve() in (root.resolve(), (root / "data").resolve()) or not out.resolve().is_relative_to(root.resolve()):
        raise ValueError("Output must be a dedicated directory inside the repository")
    base = "/" + base.strip("/") + "/" if base.strip("/") else "/"
    game = json.loads((root / "data/game.json").read_text())
    launch = date.fromisoformat(game["launch"])
    captures = collect(root)
    names = load_names(root)
    fdb_path = root / "data/foreverdb.json"
    fdb = json.loads(fdb_path.read_text()) if fdb_path.exists() else {}
    markets = build_markets(captures, names["names"], market_store.load(root))
    content = load_content(root, game, launch, base)
    blue_path = root / "data/blue.json"
    blue = json.loads(blue_path.read_text()) if blue_path.exists() else {"posts": []}
    blue["posts"] = [p for p in blue.get("posts", []) if p.get("classifier_version") == 1 and p.get("kind") in ("forever", "mixed")]
    news_config = json.loads((root / "data/news-config.json").read_text())
    log = history(root, game.get("log_after"))
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit = os.environ.get("GITHUB_SHA", "local")
    revision = hashlib.sha256(json.dumps({
        "schema": SCHEMA, "parser": PARSER_VERSION,
        "scans": [[c["source_sha256"], c.get("extraction_sha256")] for c in captures],
        "names": names.get("source", {}) and names["source"].get("sha256"),
        "foreverdb": (fdb.get("source") or {}).get("data_version"),
        "content": {k: [v["body"], {f: v.get(f) for f in sorted(FIELDS)}] for k, v in content.items()},
        "log": [e["subject"] for e in log],
        "blue": hashlib.sha256(json.dumps(blue.get("posts", []), sort_keys=True).encode()).hexdigest()},
        sort_keys=True).encode()).hexdigest()[:12]

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    # Personal captures and sourced art each have an explicit publication allowlist.
    shutil.copytree(root / "site/assets", out / "assets", ignore=shutil.ignore_patterns("screens", "art", ".*", "*.png", "*.psd"))
    art = json.loads((root / "data/art.json").read_text())["assets"]
    for image in art.values():
        if not re.fullmatch(r"[a-z0-9-]+\.(webp|jpg|png)", image["file"]):
            raise ValueError("Invalid sourced artwork filename")
        source = root / "site/assets/art" / image["file"]
        if hashlib.sha256(source.read_bytes()).hexdigest() != image["sha256"]:
            raise ValueError(f"Artwork fingerprint mismatch: {image['file']}")
        (out / "assets/art").mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, out / "assets/art" / image["file"])
    for shot in game.get("screenshots", []):
        source = root / "site/assets/screens" / shot["file"]
        if not re.fullmatch(r"[a-z0-9-]+\.(webp|jpg)", shot["file"]) or not source.is_file():
            raise ValueError(f"Screenshot {shot['file']!r} isn't a .webp or .jpg in site/assets/screens/")
        (out / "assets/screens").mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, out / "assets/screens" / shot["file"])
    fingerprints = {f.relative_to(out / "assets").as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()[:10]
                    for f in (out / "assets").rglob("*") if f.is_file()}
    site = pages.Site(base=base, url=SITE_URL, revision=revision, built=built,
                      credit=bool(names.get("source") or fdb), assets=fingerprints, launch=launch,
                      opens=datetime.fromisoformat(game["opens"]))
    site.news_endpoint = news_config["endpoint"]
    site.art = art

    def write(path: str, text: str) -> str:
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return base + path

    def page(path: str, html_text: str) -> None:
        write(path + "index.html" if path.endswith("/") or not path else path, html_text)

    write(".nojekyll", "")
    api = load_api(root)
    vendor = {int(k): v["sell"] for k, v in api.get("items", {}).items() if v.get("sell")}
    categories = {int(k): {"class": v["class"], "subclass": v.get("subclass")} for k, v in api.get("items", {}).items() if v.get("class")}
    catalogue = []
    for market in markets:
        folder = f"prices/{market['slug']}/"
        market["url"] = base + folder
        market["name"] = game.get("market_names", {}).get(market["key"], market["key"])
        market["highlights"] = highlights(market)
        market["ah"] = market_module_analyse(market, vendor, categories)
        for item in market["items"]:
            item["url"] = f"{base}{folder}item/{ah_pages.item_slug(item['key'])}/"
        market["files"] = {
            "prices_tsv": write(folder + "prices.tsv", tsv(
                ["item_id", "item_key", "name", "typical_copper", "typical", "latest_copper", "latest", "last_seen",
                 "listed_that_day", "change_7d_pct", "volatility", "latest_from_scan"],
                [[i["id"], i["key"], sheet_text(i["name"]), i["typical"], money(i["typical"]), i["price"], money(i["price"]), i["last_seen"],
                  i["listed"], i["change"], i["volatility"], i["price_scan"]] for i in market["items"]])),
            "history_tsv": write(folder + "history.tsv", tsv(
                ["item_id", "item_key", "name", "date", "low_copper", "high_copper", "listed"],
                [[i["id"], i["key"], sheet_text(i["name"]), day_date(d), v["low"], v["high"], v["listed"]]
                 for i in market["items"] for d, v in sorted(i["days"].items())])),
            "prices_json": write(folder + "prices.json", json.dumps({
                "schema_version": SCHEMA, "revision": revision, "market": market["key"],
                "environment": market["environment"], "last_date": market["last_date"],
                "last_day": market["last_day"], "spark_days": SPARK_DAYS,
                "columns": ["key", "id", "name", "typical", "price", "last_seen", "listed", "change", "current", "spark", "volatility",
                            "url", "ref", "deal", "deal_confidence", "invest", "category", "confidence"],
                "rows": [[i["key"], i["id"], i["name"], i["typical"], i["price"], i["last_seen"], i["listed"], i["change"],
                          i["current"], i["spark"], i["volatility"], i["url"], i["ref"],
                          round(i["deal"]["discount"], 3) if i["deal"] and "discount" in i["deal"] else None,
                          i["deal"]["confidence"] if i["deal"] and "discount" in i["deal"] else None,
                          i["invest"]["margin"] if i["invest"] and i["confidence"] != "low" else None,
                          i["category"]["class"] if i.get("category") else None, i["confidence"]] for i in market["items"]]}, separators=(",", ":")) + "\n"),
            "history_json": write(folder + "history.json", json.dumps({
                "schema_version": SCHEMA, "revision": revision,
                "history": {i["key"]: [[day_date(d), v["low"], v["high"], v["listed"]] for d, v in sorted(i["days"].items())]
                            for i in market["items"]}}, separators=(",", ":")) + "\n"),
        }
        catalogue.append({"name": market["name"], "key": market["key"], "environment": market["environment"], "sample": market["sample"],
                          "page": market["url"], "last_date": market["last_date"], "items": len(market["items"]),
                          "current_items": len(market["current"]),
                          "scans": [{k: s[k] for k in ("date", "items", "source_sha256", "unchanged")} for s in market["scans"]],
                          **market["files"]})
    primary = markets[0] if markets else None
    book = price_book(primary, fdb)
    places = content_places(game)
    for entry in log:
        entry["urls"] = sorted({u for u in (change_url(f, places) for f in entry["files"]) if u})
    fdb_source = fdb.get("source") or {}
    ctx = {"game": game, "launch": launch, "base": base, "markets": markets, "primary": primary, "content": content, "blue": blue,
           "log": log, "fdb": fdb, "fdb_source": fdb_source, "names": names["names"], "captures": captures,
           "names_source": names.get("source"),
           "data_prelaunch": not fdb_source.get("fetched_on") or date.fromisoformat(fdb_source["fetched_on"]) < launch,
           "craft": craft_table(fdb, book, names["names"]), "crates": crate_table(fdb, book, names["names"]),
           "materials": materials_table(fdb, book, names["names"])}
    ctx["events"] = game.get("market_events", [])
    ctx["api"] = api
    ctx["recipes_by_item"] = recipes_by_item(fdb)
    site.search_action = f'{primary["url"]}#prices' if primary else f"{base}prices/"
    site.nav = pages.nav_html(site, ctx)
    for market in markets:
        page(f"prices/{market['slug']}/", pages.market_page(site, market, ctx))
        for item in market["items"]:
            page(item["url"][len(base):], ah_pages.item_page(site, market, item, ctx))
    page("", pages.home(site, ctx))
    page("prices/", pages.prices_index(site, ctx))
    page("more/", sections.more_index(site, ctx))
    page("prices/craft/", pages.craft_page(site, ctx))
    page("prices/crates/", pages.crates_page(site, ctx))
    page("prices/materials/", pages.materials_page(site, ctx))
    write("prices/craft.tsv", tsv(["profession", "recipe", "skill", "item_id", "makes", "sells_copper", "cost_copper", "margin_copper", "price_from"],
                                  [[r["profession"], sheet_text(r["name"]), r["skill"], r["item"], r["count"], r["sells"], r["cost"], r["margin"], r["value_source"]]
                                   for r in ctx["craft"]]))
    page("classes/", sections.classes_index(site, ctx))
    for c in game["classes"]:
        page(f"classes/{c['slug']}/", sections.class_page(site, ctx, c))
        for spec in c["specs"]:
            page(f"classes/{c['slug']}/{spec['slug']}/", sections.spec_page(site, ctx, c, spec))
    page("professions/", sections.professions_index(site, ctx))
    for p in game["professions"]:
        page(f"professions/{p['slug']}/", sections.profession_page(site, ctx, p))
    page("world/", sections.world_index(site, ctx))
    for t in game["world"]:
        page(f"world/{t['slug']}/", sections.world_page(site, ctx, t))
    for m in game["more"]:
        page(f"more/{m['slug']}/", sections.more_page(site, ctx, m))
    page("more/about/", sections.about_page(site, ctx))
    write("404.html", pages.not_found(site))
    write("search.json", json.dumps(search_index(ctx), separators=(",", ":"), ensure_ascii=False) + "\n")

    write("llms-full.txt", pages.llms_full(site, ctx))
    write("llms.txt", pages.llms_index(site, ctx))
    urls = ["", "prices/", "prices/craft/", "prices/crates/", "prices/materials/", "classes/", "professions/", "world/",
            "more/about/"] + [f"more/{m['slug']}/" for m in game["more"]] + [f"prices/{m['slug']}/" for m in markets] \
        + [f"classes/{c['slug']}/" for c in game["classes"]] \
        + [f"classes/{c['slug']}/{spec['slug']}/" for c in game["classes"] for spec in c["specs"]] + [f"professions/{p['slug']}/" for p in game["professions"]] \
        + [f"world/{t['slug']}/" for t in game["world"]]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("data/news.json", json.dumps(blue, ensure_ascii=False, indent=1) + "\n")
    write("data/manifest.json", json.dumps({
        "schema_version": SCHEMA, "site": pages.SITE_NAME, "revision": revision, "built": built,
        "source_commit": commit, "workflow_run": os.environ.get("GITHUB_RUN_ID"), "parser_version": PARSER_VERSION,
        "read_first": base + "llms-full.txt",
        "blizzard_posts": {"fetched": blue.get("fetched"), "posts": len(blue.get("posts", [])),
                           "snapshot_sha256": hashlib.sha256(json.dumps(blue.get("posts", []), sort_keys=True).encode()).hexdigest()},
        "markets": catalogue, "pages_with_notes": sorted(content),
        "item_names": names.get("source"), "foreverdb": fdb_source}, indent=1) + "\n")

    for path in out.rglob("*"):
        if path.is_file() and path.suffix not in (".html", ".css", ".js", ".svg", ".webp", ".jpg", ".png", ".json", ".tsv", ".txt", ".xml", ".woff2", ""):
            raise InvalidCapture(f"Unexpected public file type: {path.name}")
    if any(out.rglob("*.lua")):
        raise InvalidCapture("Raw Lua must not be published")
    return {"revision": revision, "scans": len(captures), "markets": len(markets), "items": sum(len(m["items"]) for m in markets),
            "content_pages": len(content), "log_entries": len(log), "craft_rows": len(ctx["craft"]), "output": str(out)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the site into dist/.")
    parser.add_argument("--base-path", default="/Tazdingo/")
    print(json.dumps(build(base=parser.parse_args().base_path), indent=2))
