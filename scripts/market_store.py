"""Scan records, retention and the daily archive: how each Auctionator upload is kept.

Auctionator's file holds, per item, the latest minimum price seen (`m`) and, per day, the
lowest and highest minimum price (`l`, `h`) and the most units seen listed (`a`); it keeps
21 days. Each upload therefore becomes:

- a scan record, data/market/<market>/scans/<UTC time>.json: the scan's time and, for every
  item seen on the scan's day, [latest price, that day's low, high, most listed];
- the upload's earlier days merged into a monthly daily archive,
  data/market/<market>/daily/<YYYY-MM>.json: per item per finished day
  [low, high, most listed, scans that day, median scan price].

Scan records are kept for the last 30 days or the last 30 scans, whichever reaches further
back; older ones are folded (their day is already in the archive) and their files removed.
Every kept record and every archive file is fingerprinted in data/captures.json, so a
changed file stops the build, as the original extracts' fingerprints do.
"""
from __future__ import annotations

import hashlib
import json
import re
import statistics
from datetime import date, datetime, timezone
from pathlib import Path

from auctionator import ITEM_KEY, InvalidCapture, day_date, parse_capture

RECORD_FORMAT = "scan-record-v1"
ARCHIVE_FORMAT = "daily-archive-v1"
WINDOW_DAYS = 30
WINDOW_SCANS = 30
INBOX_HISTORY_DAYS = 21  # an inbox record carries all of Auctionator's daily history (it keeps 21 days)
STORE = "data/market"
INBOX = "data/market/inbox"
MAX_RECORD = 16 * 1024 * 1024


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def market_slug(environment: str, market: str) -> str:
    """The same slug the build uses for a market's pages."""
    return slugify(environment + "-" + market)


def scan_timestamp(capture: dict) -> int:
    times = [t for t in capture["source_scan_timestamps"].values() if type(t) is int and t > 0]
    if not times:
        raise InvalidCapture("The file records no scan time")
    return max(times)


def iso(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z")


def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def dump(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n"


# --- Records ----------------------------------------------------------------------

def read_all_markets(path: Path) -> dict:
    """A parsed file with every market that can be read; an old market Auctionator stored in
    its earlier format is skipped rather than stopping the import."""
    names = parse_capture(path, markets=[])["available_markets"]
    capture = None
    for name in names:
        try:
            one = parse_capture(path, markets=[name])
        except InvalidCapture:
            continue
        if capture is None:
            capture = one
        else:
            capture["markets"].update(one["markets"])
    return capture or parse_capture(path, markets=[])


def full_scan_market(capture: dict) -> str | None:
    """The market a file's full scan belongs to, when that can be told. Auctionator keeps one
    full-scan time for the whole file, not per market: it counts only when it is the file's
    latest scan, and goes to the one market whose records reach the file's newest day. When
    several markets share that day, no market gets it. `capture` must hold every market."""
    stamps = capture["source_scan_timestamps"]
    full = stamps.get("TimeOfLastReplicateScan")
    if type(full) is not int or full <= 0 or full != max((t for t in stamps.values() if type(t) is int), default=0):
        return None
    newest = {name: max((int(d) for f in m["items"].values() for d in f["h"]), default=-1) for name, m in capture["markets"].items()}
    top = max(newest.values(), default=-1)
    leaders = [name for name, day in newest.items() if day == top]
    return leaders[0] if top >= 0 and len(leaders) == 1 else None


def record_from_capture(capture: dict, market: str, environment: str, history_days: int | None = None,
                        full_market: str | None = None) -> dict:
    """One market of a parsed upload as a scan record. With history_days, the record also
    carries that many days of daily history (for the inbox, where the original file isn't)."""
    items = capture["markets"][market]["items"]
    days = [int(d) for fields in items.values() for d in fields["h"]]
    if not days:
        raise InvalidCapture(f"Market {market!r} has no price records")
    day = max(days)
    seen = {}
    for key, fields in items.items():
        high = fields["h"].get(str(day))
        if high is None:
            continue  # not seen on the scan's day: its latest price is stale
        seen[key] = [fields["m"], fields["l"].get(str(day), high), high, fields["a"].get(str(day))]
    full = capture["source_scan_timestamps"].get("TimeOfLastReplicateScan") if market == full_market else None
    record = {"format": RECORD_FORMAT, "environment": environment, "market": market,
              "source_sha256": capture["source_sha256"], "scan_timestamp": scan_timestamp(capture),
              "full_scan_timestamp": full if type(full) is int and full > 0 else None,
              "day": day, "items": dict(sorted(seen.items()))}
    if history_days is not None:
        record["history"] = history(capture, market, day - history_days + 1, day)
    return record


def history(capture: dict, market: str, first: int, last: int) -> dict:
    """{item key: {day: [low, high, most listed]}} for days first..last."""
    result = {}
    for key, fields in capture["markets"][market]["items"].items():
        days = {}
        for code, high in fields["h"].items():
            if first <= int(code) <= last:
                days[code] = [fields["l"].get(code, high), high, fields["a"].get(code)]
        if days:
            result[key] = dict(sorted(days.items(), key=lambda kv: int(kv[0])))
    return dict(sorted(result.items()))


def validate_record(data: dict, inbox: bool = False) -> dict:
    allowed = {"format", "environment", "market", "source_sha256", "scan_timestamp", "full_scan_timestamp", "day", "items"}
    if inbox:
        allowed |= {"history"}
    if not isinstance(data, dict) or not set(data) <= allowed or not set(data) >= allowed - {"history"}:
        raise InvalidCapture("Not a scan record")
    full = data["full_scan_timestamp"]
    if full is not None and (type(full) is not int or not 1_500_000_000 < full <= data.get("scan_timestamp", 0)):
        raise InvalidCapture("Invalid full-scan time")
    if data["format"] != RECORD_FORMAT:
        raise InvalidCapture("Unsupported scan record format")
    if not re.fullmatch(r"[a-z-]{2,40}", data["environment"]) or not isinstance(data["market"], str) \
            or not 0 < len(data["market"]) <= 80 or re.search(r"[\x00-\x1f]", data["market"]):
        raise InvalidCapture("Invalid market in scan record")
    if not re.fullmatch(r"[a-f0-9]{64}", data["source_sha256"]):
        raise InvalidCapture("Invalid source fingerprint in scan record")
    if type(data["scan_timestamp"]) is not int or not 1_500_000_000 < data["scan_timestamp"] < 4_000_000_000:
        raise InvalidCapture("Invalid scan time")
    if type(data["day"]) is not int or not 0 <= data["day"] < 100_000:
        raise InvalidCapture("Invalid scan day")
    if not isinstance(data["items"], dict) or not data["items"]:
        raise InvalidCapture("Scan record has no items")
    for key, row in data["items"].items():
        if not ITEM_KEY.fullmatch(key) or not isinstance(row, list) or len(row) != 4:
            raise InvalidCapture("Invalid scan record item")
        if any(type(v) is not int or v < 0 for v in row[:3]) or not (row[3] is None or (type(row[3]) is int and row[3] >= 0)):
            raise InvalidCapture("Invalid scan record values")
    for key, days in data.get("history", {}).items():
        if not ITEM_KEY.fullmatch(key) or not isinstance(days, dict):
            raise InvalidCapture("Invalid scan record history")
        for code, row in days.items():
            if not code.isdigit() or int(code) > data["day"] or not isinstance(row, list) or len(row) != 3 \
                    or any(type(v) is not int or v < 0 for v in row[:2]) or not (row[2] is None or (type(row[2]) is int and row[2] >= 0)):
                raise InvalidCapture("Invalid scan record history values")
    return data


def read_json(path: Path, limit: int = MAX_RECORD) -> dict:
    with path.open("rb") as source:
        raw = source.read(limit + 1)
    if len(raw) > limit:
        raise InvalidCapture(f"{path.name} is too large")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidCapture("Duplicate key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


# --- The archive --------------------------------------------------------------------

def month_of(day: int) -> str:
    return day_date(day)[:7]


def load_archive(folder: Path) -> dict:
    """{day: {item key: [low, high, most listed, scans, median scan price]}} from every month file."""
    days = {}
    for path in sorted((folder / "daily").glob("*.json")):
        data = read_json(path)
        if set(data) != {"format", "month", "days"} or data["format"] != ARCHIVE_FORMAT or path.stem != data["month"]:
            raise InvalidCapture(f"{path.name} is not a daily archive")
        for code, items in data["days"].items():
            if not code.isdigit() or month_of(int(code)) != data["month"]:
                raise InvalidCapture(f"{path.name} holds a day from another month")
            for key, row in items.items():
                if not ITEM_KEY.fullmatch(key) or not isinstance(row, list) or len(row) != 5:
                    raise InvalidCapture(f"Invalid archive row in {path.name}")
            days[int(code)] = items
    return days


def merge_day(old: list | None, low: int, high: int, listed: int | None) -> list:
    if old is None:
        return [low, high, listed, 0, None]
    best = max((v for v in (old[2], listed) if v is not None), default=None)
    return [min(old[0], low), max(old[1], high), best, old[3], old[4]]


def archive_days(archive: dict, rows: dict, before: int) -> set[int]:
    """Merge {item: {day: [low, high, most listed]}} for finished days (before `before`)."""
    touched = set()
    for key, days in rows.items():
        for code, (low, high, listed) in days.items():
            day = int(code)
            if day >= before:
                continue
            items = archive.setdefault(day, {})
            items[key] = merge_day(items.get(key), low, high, listed)
            touched.add(day)
    return touched


def archive_scan_stats(archive: dict, records: list[dict], before: int, complete: set[int]) -> set[int]:
    """Each finished day's scan count and median scan price per item, from that day's records.
    Only days whose records are all still kept (`complete`): once retention has removed some
    of a day's records, the archive already holds that day's figures."""
    by_day = {}
    for record in records:
        if record["day"] < before and record["day"] in complete:
            by_day.setdefault(record["day"], []).append(record)
    for day, group in by_day.items():
        items = archive.setdefault(day, {})
        prices = {}
        for record in group:
            for key, (latest, low, high, listed) in record["items"].items():
                prices.setdefault(key, []).append(latest)
                items[key] = merge_day(items.get(key), low, high, listed)
        for key, values in prices.items():
            items[key][3] = len(values)
            items[key][4] = int(statistics.median(values))
    return set(by_day)


def write_archive(folder: Path, archive: dict, months: set[str]) -> dict[str, str]:
    """Rewrite the given months; returns {relative path: fingerprint}."""
    written = {}
    for month in sorted(months):
        days = {str(d): dict(sorted(items.items())) for d, items in sorted(archive.items()) if month_of(d) == month}
        path = folder / "daily" / f"{month}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        body = dump({"format": ARCHIVE_FORMAT, "month": month, "days": days})
        write_whole(path, body)
        written[path.as_posix()] = fingerprint(body)
    return written


def write_whole(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text)
    temporary.replace(path)


# --- Retention ------------------------------------------------------------------------

def to_keep(receipts: list[dict]) -> set[str]:
    """Paths of the records to keep: within 30 days of the newest, or among the newest 30."""
    kept = sorted((r for r in receipts if r["status"] == "kept"), key=lambda r: r["scan_timestamp"])
    if not kept:
        return set()
    newest = kept[-1]["scan_timestamp"]
    recent = {r["path"] for r in kept if newest - r["scan_timestamp"] <= WINDOW_DAYS * 86400}
    return recent | {r["path"] for r in kept[-WINDOW_SCANS:]}


# --- Adding an upload ------------------------------------------------------------------

JOURNAL = "data/market/.journal.json"


def recover(root: Path) -> bool:
    """Undo an import that was cut off part-way (the process killed between writing the
    archive and the registry): put back every file the journal saved and remove the files
    it was adding. Returns True when there was something to undo."""
    path = root / JOURNAL
    if not path.exists():
        return False
    journal = json.loads(path.read_text())
    for relative in journal["created"]:
        (root / relative).unlink(missing_ok=True)
    for relative, body in journal["saved"].items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        write_whole(target, body)
    path.unlink()
    return True


def tidy(root: Path, registry: dict) -> None:
    """Remove record files and empty folders that no receipt keeps (left behind when an
    import stopped after its registry was written but before folded files were removed)."""
    kept = {(root / r["path"]).resolve() for r in registry.get("scans", []) if r["status"] == "kept"}
    for path in (root / STORE).glob("*/scans/*.json"):
        if path.resolve() not in kept:
            path.unlink()
    for folder in sorted((root / STORE).glob("**/"), key=lambda p: -len(p.parts)):
        if folder != root / STORE and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()


def add_record(root: Path, record: dict, rows: dict, receipt_extra: dict) -> dict | None:
    """File one scan record (with its upload's daily rows), update the archive, apply
    retention and the receipts. Returns a summary, or None when nothing is new."""
    if recover(root):
        print("An earlier import was cut off part-way; it has been undone.")
    registry_path = root / "data/captures.json"
    tidy(root, json.loads(registry_path.read_text()))
    load(root)  # the store must match its fingerprints before anything is added to it
    registry = json.loads(registry_path.read_text())
    receipts = registry.setdefault("scans", [])
    slug = market_slug(record["environment"], record["market"])
    content = fingerprint(dump({k: record[k] for k in ("day", "items", "scan_timestamp")}))
    if any(r["market_slug"] == slug and r["content_sha256"] == content for r in receipts):
        return None  # this exact scan is already recorded
    if any(r["market_slug"] == slug and r["status"] == "folded" and r["day"] == record["day"] for r in receipts):
        raise InvalidCapture(f"This scan's day ({day_date(record['day'])}) has already been folded into the archive; "
                             "an upload that old can't be added any more.")
    folder = root / STORE / slug
    stamp = datetime.fromtimestamp(record["scan_timestamp"], timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    path = folder / "scans" / f"{stamp}.json"
    number = 2
    while path.exists():
        path = folder / "scans" / f"{stamp}-{number}.json"
        number += 1
    journal = {"created": [], "saved": {"data/captures.json": registry_path.read_text()}}
    path.parent.mkdir(parents=True, exist_ok=True)
    stored = {k: record[k] for k in ("format", "environment", "market", "source_sha256", "scan_timestamp", "full_scan_timestamp", "day", "items")}
    body = dump(validate_record(stored))
    journal["created"].append(path.relative_to(root).as_posix())
    write_whole(root / JOURNAL, json.dumps(journal))
    write_whole(path, body)
    receipts.append({"path": path.relative_to(root).as_posix(), "market_slug": slug, "environment": record["environment"],
                     "market": record["market"], "scan_timestamp": record["scan_timestamp"], "scan_time": iso(record["scan_timestamp"]),
                     "day": record["day"], "source_sha256": record["source_sha256"], "content_sha256": content,
                     "record_sha256": fingerprint(body), "status": "kept", "received_on": date.today().isoformat(),
                     # A full scan that was the file's latest scan: the record is that scan's snapshot, and its item
                     # count is a full market's size. Kept in the receipt so it outlives the record.
                     "full_scan_items": len(record["items"]) if record["full_scan_timestamp"] == record["scan_timestamp"] else None,
                     **receipt_extra})

    mine = [r for r in receipts if r["market_slug"] == slug]
    newest_day = max(r["day"] for r in mine if r["status"] == "kept")
    archive = load_archive(folder)
    touched = archive_days(archive, rows, newest_day)
    kept_records = [read_json(root / r["path"]) for r in mine if r["status"] == "kept"]
    complete = {r["day"] for r in mine} - {r["day"] for r in mine if r["status"] == "folded"}
    touched |= archive_scan_stats(archive, kept_records, newest_day, complete)

    keep = to_keep(mine)
    retired = []
    for receipt in mine:
        if receipt["status"] == "kept" and receipt["path"] not in keep and receipt["day"] < newest_day:  # never fold an unfinished day
            receipt["status"] = "folded"
            retired.append(root / receipt["path"])

    # The archive (already holding the folded days' figures) and the registry are written
    # first; the folded records' files are removed only once both are in place.
    months = {month_of(d) for d in touched}
    for month in months:
        existing = folder / "daily" / f"{month}.json"
        relative = existing.relative_to(root).as_posix()
        if existing.exists():
            journal["saved"][relative] = existing.read_text()
        else:
            journal["created"].append(relative)
    write_whole(root / JOURNAL, json.dumps(journal))
    written = write_archive(folder, archive, months)
    archives = registry.setdefault("archives", {})
    for absolute, sha in written.items():
        archives[Path(absolute).relative_to(root).as_posix()] = sha
    write_whole(registry_path, json.dumps(registry, indent=2) + "\n")
    (root / JOURNAL).unlink()  # committed: from here on the new state stands
    for retired_path in retired:
        retired_path.unlink(missing_ok=True)
    folded = len(retired)
    return {"file": path.relative_to(root).as_posix(), "market": record["market"], "items": len(record["items"]),
            "scan_time": iso(record["scan_timestamp"]), "folded": folded}


# --- Reading the store for the build ------------------------------------------------------

def load(root: Path) -> dict:
    """Every market's kept scan records and daily archive, verified against their receipts."""
    if (root / JOURNAL).exists():
        raise InvalidCapture("An import was cut off part-way; run scripts/ingest.py again to undo it before building.")
    registry = json.loads((root / "data/captures.json").read_text())
    markets = {}
    store = (root / STORE).resolve()
    for receipt in registry.get("scans", []):
        if receipt["status"] not in ("kept", "folded"):
            raise InvalidCapture("Unknown scan record status")
        entry = markets.setdefault(receipt["market_slug"], {"environment": receipt["environment"], "market": receipt["market"],
                                                            "records": [], "folded": 0, "receipts": 0, "full_scan_items": []})
        entry["receipts"] += 1
        if receipt.get("full_scan_items"):
            entry["full_scan_items"].append(receipt["full_scan_items"])
        if receipt["status"] == "folded":
            entry["folded"] += 1
            continue
        path = (root / receipt["path"]).resolve()
        if not path.is_relative_to(store):
            raise InvalidCapture("Scan record path escapes the market store")
        body = path.read_bytes()
        if hashlib.sha256(body).hexdigest() != receipt["record_sha256"]:
            raise InvalidCapture(f"{path.name} differs from its receipt fingerprint")
        record = validate_record(json.loads(body))
        if record["scan_timestamp"] != receipt["scan_timestamp"] or record["source_sha256"] != receipt["source_sha256"]:
            raise InvalidCapture(f"{path.name} doesn't match its receipt")
        entry["records"].append(record)
    for relative, sha in registry.get("archives", {}).items():
        path = (root / relative).resolve()
        if not path.is_relative_to(store) or hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            raise InvalidCapture(f"{Path(relative).name} differs from its archive fingerprint")
    listed = {(root / relative).resolve() for relative in registry.get("archives", {})}
    for slug, entry in markets.items():
        entry["records"].sort(key=lambda r: r["scan_timestamp"])
        for path in (root / STORE / slug / "daily").glob("*.json"):
            if path.resolve() not in listed:
                raise InvalidCapture(f"{path.name} has no archive fingerprint")
        entry["daily"] = load_archive(root / STORE / slug)
    for folder in sorted(p for p in (root / STORE).glob("*") if p.is_dir() and p.name != "inbox"):
        if folder.name not in markets and any(f.is_file() for f in folder.rglob("*")):
            raise InvalidCapture(f"{folder.name} has no receipts")
    return markets
