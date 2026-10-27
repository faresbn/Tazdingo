"""Fetch ForeverDB API data into a local cache, then write the slim data/foreverdb-api.json.

    python3 scripts/foreverdb_api.py fetch     download what the site uses (resumable; about 20 minutes)
    python3 scripts/foreverdb_api.py slim      write data/foreverdb-api.json from the cache

The API needs a key: set FOREVERDB_API_KEY. The key is sent only to foreverdb.net and
is never written anywhere. Raw answers are cached in tmp/foreverdb-api/ (not committed),
so a rerun only fetches what's missing. ForeverDB asks for a visible link to
https://foreverdb.net wherever its data is shown, at most 60 requests a minute and
10,000 a day; this script stays near one request a second. Run on demand, never during
the build, so publishing never depends on ForeverDB being reachable.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://foreverdb.net/api/v1"
CACHE = ROOT / "tmp/foreverdb-api"
OUT = ROOT / "data/foreverdb-api.json"
AGENT = "Tazdingo data refresh (private fan project; https://faresbn.github.io/Tazdingo/)"
CREDIT = "Data from ForeverDB.net (https://foreverdb.net)"
PAUSE = 1.05
PROFESSIONS = ["alchemy", "blacksmithing", "cooking", "enchanting", "engineering", "first-aid", "fishing",
               "herbalism", "leatherworking", "mining", "skinning", "tailoring"]
GATHERING = ["herbalism", "mining", "skinning", "fishing"]
CLASSES = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Shaman", "Mage", "Warlock", "Druid"]


def get(path: str, key: str) -> dict:
    """One API answer, from the cache when we already have it."""
    name = path.strip("/").replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "-") + ".json"
    cached = CACHE / name
    if cached.exists():
        return json.loads(cached.read_text())
    for attempt in range(5):
        request = urllib.request.Request(API + path, headers={"User-Agent": AGENT, "X-API-Key": key,
                                                              "Accept": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read())
            break
        except urllib.error.HTTPError as error:
            if error.code == 429:
                time.sleep(int(error.headers.get("Retry-After") or 60) + 1)
                continue
            if error.code == 404:
                body = {"data": None, "error": 404}
                break
            raise
        except urllib.error.URLError:
            time.sleep(10 * (attempt + 1))
    else:
        raise SystemExit(f"Gave up on {path} after repeated failures")
    CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps(body))
    time.sleep(PAUSE)
    return body


def pages(path: str, key: str) -> list:
    """Every record of a paged list (100 a page)."""
    records, offset = [], 0
    while True:
        sep = "&" if "?" in path else "?"
        answer = get(f"{path}{sep}limit=100&offset={offset}", key)
        data = answer.get("data")
        rows = data if isinstance(data, list) else (data or {}).get("recipes", [])
        records += rows
        total = (answer.get("meta") or {}).get("total") or 0
        offset += 100
        if not rows or offset >= total:
            return records


def market_items() -> set[int]:
    """Item IDs in our scans, recipes and crates: the ones whose vendor price we need."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from auctionator import item_id
    ids = set()
    for path in (ROOT / "data/captures").rglob("*.json"):
        for market in json.loads(path.read_text()).get("markets", {}).values():
            ids.update(item_id(k) for k in market.get("items", {}))
    return ids


def fetch(key: str) -> None:
    meta = get("/meta", key)
    print(f"ForeverDB build {meta['data']['build']}, level cap {meta['data']['levelCap']}")
    for slug in PROFESSIONS:
        pages(f"/professions/{slug}", key)
    for slug in GATHERING:
        get(f"/gathering/{slug}", key)
    for name in CLASSES:
        get(f"/classes/{name}", key)
    for path in ("/disenchant", "/poisons", "/dungeons", "/battlegrounds", "/zones"):
        get(path, key)
    print("Item list…")
    pages("/items", key)
    wanted = sorted(market_items())
    print(f"Item details for {len(wanted)} items (vendor prices)…")
    for n, item in enumerate(wanted, 1):
        get(f"/items/{item}", key)
        if n % 100 == 0:
            print(f"  {n}/{len(wanted)}")
    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("step", choices=("fetch", "slim"))
    args = parser.parse_args()
    if args.step == "fetch":
        key = os.environ.get("FOREVERDB_API_KEY")
        if not key:
            raise SystemExit("Set FOREVERDB_API_KEY first.")
        fetch(key)
    else:
        from foreverdb_slim import slim  # written once the cached answers' shapes are known
        slim(CACHE, OUT, CREDIT, date.today().isoformat())


if __name__ == "__main__":
    main()
