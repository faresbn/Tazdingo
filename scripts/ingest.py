"""Add a new Auctionator scan to the journal.

    python3 scripts/ingest.py            find Forever's Auctionator file, import, test, build, commit
    python3 scripts/ingest.py --push     ... and publish
    python3 scripts/ingest.py --list     show the markets in the file and stop

Only market price records leave your Mac. The original SavedVariables file
(settings, posting history, searches, shopping lists) is fingerprinted and left
where it is.
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

from auctionator import InvalidCapture, day_date, market_extract, newest_day, parse_capture

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


def unfinished_import() -> bool:
    """Data changes that an earlier import left uncommitted (interrupted, or its push failed first)."""
    status = subprocess.run(["git", "status", "--porcelain", "--", "data"], cwd=ROOT,
                            capture_output=True, text=True, check=True)
    return bool(status.stdout.strip())


def ingest(path: Path, environment: str, markets: list[str]) -> dict | None:
    registry_path = ROOT / "data/captures.json"
    registry = json.loads(registry_path.read_text())
    capture = parse_capture(path, markets=markets)
    published = {m for r in registry["captures"] if r["source_sha256"] == capture["source_sha256"] for m in r["publish_markets"]}
    markets = [m for m in markets if m not in published]  # a second market from the same file is still new
    if not markets:
        return None
    capture["markets"] = {m: capture["markets"][m] for m in markets}
    newest = newest_day(capture["markets"])
    scanned = day_date(newest) if newest is not None else datetime.fromtimestamp(scan_time(capture)).date().isoformat()
    folder = ROOT / "data/captures" / environment
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{scanned}.market.json"
    number = 2
    while target.exists():
        target = folder / f"{scanned}-{number}.market.json"
        number += 1
    body = json.dumps(market_extract(capture), sort_keys=True, separators=(",", ":")) + "\n"
    write_whole(target, body)
    registry["captures"].append({
        "path": str(target.relative_to(ROOT)), "environment": environment,
        "received_on": date.today().isoformat(), "source_sha256": capture["source_sha256"],
        "scope_source": "Fares's Auctionator export", "publish_markets": markets,
        "extraction_sha256": hashlib.sha256(body.encode()).hexdigest()})
    registry.setdefault("default_markets", {})[environment] = markets
    write_whole(registry_path, json.dumps(registry, indent=2) + "\n")
    counts = {m: len(capture["markets"][m]["items"]) for m in markets}
    return {"file": str(target.relative_to(ROOT)), "scanned": scanned, "items": counts}


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a new Auctionator scan to the journal.")
    parser.add_argument("--environment", default="forever", choices=sorted(FOLDERS))
    parser.add_argument("--file", type=Path, help="Auctionator.lua to read (default: newest in the WoW folder)")
    parser.add_argument("--market", action="append", default=[], help="market to publish, e.g. 'Realm Horde'")
    parser.add_argument("--list", action="store_true", help="list the file's markets and stop")
    parser.add_argument("--no-commit", action="store_true", help="import and build, but leave git alone")
    parser.add_argument("--push", action="store_true", help="push the commit so the site republishes")
    args = parser.parse_args()

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
    kept = {name: (ROOT / name).read_bytes() for name in ("data/captures.json", "data/items.json") if (ROOT / name).exists()}
    result = ingest(path, args.environment, markets)
    if result is None:
        if not unfinished_import():
            print("This scan is already in the journal; nothing to add.")
            if args.push and not args.no_commit:
                run("git", "push")  # completes a push that failed last time; does nothing when up to date
            return
        print("This scan is recorded, but its import didn't finish last time. Finishing it now.")
        result = {"file": None, "scanned": None, "items": {}}
    else:
        print(f"Added {result['file']}: scanned {result['scanned']}, " +
              ", ".join(f"{m} {n:,} items" for m, n in result["items"].items()))
    try:
        run(sys.executable, "scripts/item_names.py")
    except subprocess.CalledProcessError:
        print("Item names could not be refreshed (ForeverDB unreachable?). New items show their ID until the next refresh.")
    for step, command in (("tests", ("-m", "unittest", "discover", "-s", "tests")),
                          ("build", ("scripts/build.py",)), ("site check", ("scripts/check_site.py",))):
        try:
            run(sys.executable, *command)
        except subprocess.CalledProcessError:
            if not result["file"]:
                raise SystemExit(f"Import stopped: the {step} failed (details above). The earlier, unfinished import "
                                 "is still uncommitted in data/. Fix the problem, or discard it with "
                                 "`git checkout -- data && git clean -fd data`, then run this again.")
            (ROOT / result["file"]).unlink()
            for name, body in kept.items():
                write_whole(ROOT / name, body.decode())
            subprocess.run([sys.executable, "scripts/build.py"], cwd=ROOT, capture_output=True)  # local site matches again
            raise SystemExit(f"Import stopped: the {step} failed (details above). Nothing was kept; "
                             "the journal is as it was before this import.")
    if args.no_commit:
        return
    run("git", "add", "data")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        summary = ", ".join(f"{m} {n:,} items" for m, n in result["items"].items())
        run("git", "commit", "-m", f"Add {args.environment} Auctionator scan of {result['scanned']} ({summary})"
            if result["file"] else "Finish an interrupted Auctionator import")
    if args.push:
        run("git", "push")


if __name__ == "__main__":
    main()
