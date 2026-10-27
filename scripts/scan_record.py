"""Turn an Auctionator.lua into a scan record for data/market/inbox/ (the ChatGPT route).

    python3 scan_record.py Auctionator.lua --list
    python3 scan_record.py Auctionator.lua --market "Realm Faction" [--environment forever]

Needs only this file and auctionator.py from the repository's scripts/ folder, and the
standard library. The record holds market prices only: the scan time, each item's latest
price and recent daily low, high and most listed. The uploaded file itself (settings,
posting history, searches) must never be committed; commit only the record this writes,
to data/market/inbox/. A GitHub Action files it, applies retention and republishes.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auctionator import InvalidCapture, parse_capture  # noqa: E402
import market_store  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Make an inbox scan record from an Auctionator.lua.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--market", action="append", default=[], help="market to record, e.g. 'Realm Horde'")
    parser.add_argument("--environment", default="forever")
    parser.add_argument("--list", action="store_true", help="list the file's markets and stop")
    parser.add_argument("--out", type=Path, default=Path("."), help="folder to write the record(s) into")
    args = parser.parse_args()
    if args.list or not args.market:
        names = parse_capture(args.file, markets=[])["available_markets"]
        print("Markets in this file: " + ", ".join(repr(n) for n in names))
        if not args.market:
            print("Choose one with --market.")
        return
    capture = market_store.read_all_markets(args.file)  # every readable market, to tell which one a full scan belongs to
    full_market = market_store.full_scan_market(capture)
    args.out.mkdir(parents=True, exist_ok=True)
    for market in args.market:
        if market not in capture["markets"]:
            raise SystemExit(f"No market {market!r} in this file. It has: " + ", ".join(repr(n) for n in capture["markets"]))
        record = market_store.record_from_capture(capture, market, args.environment, market_store.INBOX_HISTORY_DAYS,
                                                  full_market=full_market)
        market_store.validate_record(record, inbox=True)
        stamp = datetime.fromtimestamp(record["scan_timestamp"], timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        path = args.out / f"{stamp}-{market_store.market_slug(args.environment, market)}.json"
        path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        print(f"Wrote {path} ({len(record['items']):,} items, scanned {market_store.iso(record['scan_timestamp'])}, "
              f"{path.stat().st_size:,} bytes). Commit it to data/market/inbox/{path.name}.")


if __name__ == "__main__":
    try:
        main()
    except InvalidCapture as error:
        raise SystemExit(f"Can't read that file: {error}")
