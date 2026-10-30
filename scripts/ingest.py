"""Add a new Auctionator scan to the journal.

    python3 scripts/ingest.py            find Forever's Auctionator file, import, test, build, commit
    python3 scripts/ingest.py --push     ... and publish
    python3 scripts/ingest.py --list     show the markets in the file and stop
    python3 scripts/ingest.py --inbox    file scan records committed to data/market/inbox/
                                         (the ChatGPT route; GitHub Actions runs this)

Each upload becomes a scan record (scripts/market_store.py): the scan's time and every
item's latest price, kept for the last 30 scans or 30 days. Run it after every scan to
keep each one. The original file is also committed, unchanged, under
data/captures/<environment>/auctionator/ (scripts/originals.py).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import market_store
import originals
from auctionator import InvalidCapture, parse_capture

ROOT = Path(__file__).resolve().parents[1]
WOW = Path("/Applications/World of Warcraft")
# WoW client folder for each environment we publish.
FOLDERS = {"forever": "_forever_", "tbc": "_anniversary_", "era": "_classic_era_"}


def find_file(environment: str) -> Path:
    """The most recently written Auctionator file across this client's accounts."""
    files = list((WOW / FOLDERS[environment] / "WTF/Account").glob("*/SavedVariables/Auctionator.lua"))
    if not files:
        raise SystemExit(f"No Auctionator data in {WOW / FOLDERS[environment]}. "
                         "Log out of the game (or /reload) after scanning so WoW writes the file, "
                         "or pass --file.")
    return max(files, key=lambda f: f.stat().st_mtime)


def choose_markets(path: Path, requested: list[str], remembered: list[str]) -> list[str]:
    available = parse_capture(path, markets=[])["available_markets"]
    if requested:
        return requested
    if remembered and all(m in available for m in remembered):
        return remembered
    usable = []
    for name in available:
        try:
            if parse_capture(path, markets=[name])["markets"][name]["items"]:
                usable.append(name)
        except InvalidCapture:
            pass
    if len(usable) == 1:
        return usable
    raise SystemExit("Choose the market(s) to publish with --market. This file has: "
                     + ", ".join(repr(m) for m in usable or available))


def scan_time(capture: dict) -> int:
    """The newest scan timestamp: browse scans record prices as well as full scans."""
    times = [t for t in capture["source_scan_timestamps"].values() if t > 0]
    if not times:
        raise InvalidCapture("The file records no scan time; scan the Auction House in game first")
    return max(times)


def run(*command: str) -> None:
    print("$", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def write_whole(path: Path, text: str) -> None:
    """Write all of a file or none of it: an interrupted write can't leave half a registry."""
    partial = path.with_name(path.name + ".partial")
    partial.write_text(text)
    os.replace(partial, path)


def push() -> None:
    """Push, first bringing in commits made elsewhere (notes from ChatGPT, the archive's records).
    The local scan commit is kept and replayed on top; nothing is force-pushed."""
    run("git", "pull", "--rebase", "--autostash")
    run("git", "push")


def unfinished_import() -> bool:
    """Data changes that an earlier import left uncommitted (interrupted, or its push failed first)."""
    status = subprocess.run(["git", "status", "--porcelain", "--", "data"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    return bool(status.stdout.strip())


def ingest(path: Path, environment: str, markets: list[str]) -> dict | None:
    """File one upload: a scan record per market, its daily history merged into the archive."""
    everything = market_store.read_all_markets(path)  # every readable market, to tell which one a full scan belongs to
    full_market = market_store.full_scan_market(everything)
    missing = [m for m in markets if m not in everything["markets"]]
    if missing:
        parse_capture(path, markets=missing)  # raises with the reason that market can't be read
    capture = {**everything, "markets": {m: everything["markets"][m] for m in markets}}
    scan_time(capture)  # a file with no scan time can't be placed in time
    filed = []
    for market in markets:
        record = market_store.record_from_capture(capture, market, environment, full_market=full_market)
        rows = market_store.history(capture, market, 0, record["day"])
        result = market_store.add_record(ROOT, record, rows, {"scope_source": "Fares's Auctionator export"})
        if result is None:
            print(f"No new scan data for {market} since the last import; skipping.")
        else:
            filed.append(result)
    if not filed:
        return None
    registry_path = ROOT / "data/captures.json"
    registry = json.loads(registry_path.read_text())
    registry.setdefault("default_markets", {})[environment] = markets
    write_whole(registry_path, json.dumps(registry, indent=2) + "\n")
    return {**summary(filed), "original": (path, environment, scan_time(capture))}


def ingest_inbox() -> dict | None:
    """File every scan record waiting in data/market/inbox/ (the ChatGPT route)."""
    filed, removed = [], 0
    for path in sorted((ROOT / market_store.INBOX).glob("*.json")):
        record = market_store.validate_record(market_store.read_json(path), inbox=True)
        result = market_store.add_record(ROOT, record, record.get("history", {}),
                                         {"scope_source": "Auctionator export uploaded through ChatGPT"})
        path.unlink()
        if result is None:
            print(f"{path.name}: already recorded; removed from the inbox.")
            removed += 1
        else:
            filed.append(result)
    if not filed and not removed:
        return None
    return summary(filed) if filed else {"files": [], "scanned": None, "items": {}, "folded": 0, "removed": removed}


def summary(filed: list[dict]) -> dict:
    return {"files": [r["file"] for r in filed], "scanned": max(r["scan_time"] for r in filed),
            "items": {r["market"]: r["items"] for r in filed}, "folded": sum(r["folded"] for r in filed)}


def snapshot() -> dict[Path, bytes]:
    """Every file an import can change, so a failed check can put them all back."""
    files = [ROOT / "data/captures.json", ROOT / "data/items.json"]
    files += [p for p in (ROOT / market_store.STORE).rglob("*") if p.is_file()]
    return {p: p.read_bytes() for p in files if p.exists()}


def restore(saved: dict[Path, bytes]) -> None:
    """Put every saved file back and remove files and folders the import created."""
    for path in [p for p in (ROOT / market_store.STORE).rglob("*") if p.is_file()]:
        if path not in saved:
            path.unlink()
    folders = {p.parent for p in saved}
    for folder in sorted((ROOT / market_store.STORE).glob("**/"), key=lambda p: -len(p.parts)):
        if folder != ROOT / market_store.STORE and folder not in folders and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    for path, body in saved.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != body:
            path.write_bytes(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a new Auctionator scan to the journal.")
    parser.add_argument("--environment", default="forever", choices=sorted(FOLDERS))
    parser.add_argument("--file", type=Path, help="Auctionator.lua to read (default: newest in the WoW folder)")
    parser.add_argument("--market", action="append", default=[], help="market to publish, e.g. 'Realm Horde'")
    parser.add_argument("--list", action="store_true", help="list the file's markets and stop")
    parser.add_argument("--no-commit", action="store_true", help="import and build, but leave git alone")
    parser.add_argument("--push", action="store_true", help="push the commit so the site republishes")
    parser.add_argument("--inbox", action="store_true", help="file the scan records waiting in data/market/inbox/")
    args = parser.parse_args()

    saved = snapshot()
    if args.inbox:
        try:
            result = ingest_inbox()
        except BaseException:
            restore(saved)  # an error while filing leaves the store as it was
            raise
        if result is None:
            print("Nothing new in the inbox.")
            return
        check_and_commit(result, saved, args, "inbox")
        return
    path = args.file or find_file(args.environment)
    print(f"Reading {path}")
    if args.list:
        for name in parse_capture(path, markets=[])["available_markets"]:
            try:
                print(f"  {name}: {len(parse_capture(path, markets=[name])['markets'][name]['items']):,} items")
            except InvalidCapture as error:
                print(f"  {name}: unreadable ({error})")
        return
    remembered = json.loads((ROOT / "data/captures.json").read_text()).get("default_markets", {}).get(args.environment, [])
    markets = choose_markets(path, args.market, remembered)
    try:
        result = ingest(path, args.environment, markets)
    except BaseException:
        restore(saved)  # an error while filing leaves the store as it was
        raise
    if result is None:
        if not unfinished_import():
            print("Nothing new to add.")
            if args.push and not args.no_commit:
                push()  # completes a push that failed last time; does nothing when up to date
            return
        print("This scan is recorded, but its import didn't finish last time. Finishing it now.")
        result = {"files": [], "scanned": None, "items": {}, "folded": 0}
    check_and_commit(result, saved, args, args.environment)


def check_and_commit(result: dict, saved: dict, args, source: str) -> None:
    """Refresh names, test, build and check; undo the import if any step fails; then commit."""
    if result["files"]:
        print(f"Added {', '.join(result['files'])}: scanned {result['scanned']}, "
              + ", ".join(f"{m} {n:,} items" for m, n in result["items"].items())
              + (f"; {result['folded']} older scan record(s) folded into the daily archive" if result["folded"] else ""))
    try:
        run(sys.executable, "scripts/item_names.py")
    except subprocess.CalledProcessError:
        print("Item names could not be refreshed (ForeverDB unreachable?). New items show their ID until the next refresh.")
    for step, command in (("tests", ("-m", "unittest", "discover", "-s", "tests")),
                          ("build", ("scripts/build.py",)), ("site check", ("scripts/check_site.py",))):
        try:
            run(sys.executable, *command)
        except subprocess.CalledProcessError:
            if not result["files"] and not result.get("removed"):
                raise SystemExit(f"Import stopped: the {step} failed (details above). The earlier, unfinished import "
                                 "is still uncommitted in data/. Fix the problem, or discard it with "
                                 "`git checkout -- data && git clean -fd data`, then run this again.")
            restore(saved)
            subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, capture_output=True)  # local site matches again
            raise SystemExit(f"Import stopped: the {step} failed (details above). Nothing was kept; "
                             "the journal is as it was before this import.")
    if result.get("original"):
        source, environment, stamp = result["original"]
        print(f"Keeping the original as {originals.keep(ROOT, source, environment, 'Auctionator', stamp).relative_to(ROOT)}")
    if args.no_commit:
        return
    run("git", "add", "data", "feed")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        summary = ", ".join(f"{m} {n:,} items" for m, n in result["items"].items())
        message = (f"Add {source} Auctionator scan of {result['scanned']} ({summary})" if result["files"]
                   else "Remove duplicate scan records from the inbox" if result.get("removed") else "Finish an interrupted Auctionator import")
        run("git", "commit", "-m", message)
    if args.push:
        push()


if __name__ == "__main__":
    main()
