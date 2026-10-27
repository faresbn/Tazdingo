"""Refresh data/items.json: names for the items in our captures and journal.

Names come from ForeverDB's companion addon (Data/SearchNames.lua). ForeverDB
publishes its addon data for reuse with the credit "Data from ForeverDB.net"
(addon NOTICE.txt, GPL-3.0 section 7(b)); the names themselves are the game
client's. Run when a scan is added (ingest.py does this), never during the
build, so publishing never depends on ForeverDB being reachable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from datetime import date
from pathlib import Path

from auctionator import InvalidCapture, LuaData, item_id

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://foreverdb.net/"
MANIFEST = SITE + "downloads/addon-manifest.json"
NAMES_FILE = "Data/SearchNames.lua"
CREDIT = "Data from ForeverDB.net (https://foreverdb.net)"
AGENT = "Tazdingo item-name refresh (private fan project)"


def fetch(url: str, limit: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise InvalidCapture(f"{url} is larger than expected")
    return body


def parse_names(raw: bytes) -> dict[int, str]:
    """The ns.searchItemNames table: {[id]="Name", ...}. Read as data, never run."""
    match = re.search(rb"ns\.searchItemNames=\{(.*?)\}\s*$", raw, re.S | re.M)
    if not match:
        raise InvalidCapture("SearchNames.lua no longer has ns.searchItemNames")
    names = {}
    for item, quoted in re.findall(rb'\[(\d+)\]=("(?:[^"\\]|\\.)*")', match.group(1)):
        names[int(item)] = LuaData(quoted).value().decode("utf-8")
    if len(names) < 1000:
        raise InvalidCapture("SearchNames.lua has suspiciously few names")
    return names


def download_names() -> tuple[dict[int, str], dict]:
    manifest = json.loads(fetch(MANIFEST, 1_000_000))
    entry = next(f for f in manifest["data"]["files"] if f["path"] == NAMES_FILE)
    raw = fetch(SITE + entry["url"], entry["bytes"])
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise InvalidCapture("SearchNames.lua does not match ForeverDB's published fingerprint")
    build = re.search(rb"build ([0-9]+(?:\.[0-9]+)*)", raw[:300])
    source = {"credit": CREDIT, "file": NAMES_FILE, "data_version": manifest["data"]["version"],
              "client_build": build.group(1).decode() if build else None, "sha256": entry["sha256"],
              "fetched_on": date.today().isoformat()}
    return parse_names(raw), source


def wanted_ids(root: Path = ROOT) -> set[int]:
    """Every item in our captures, in the ForeverDB tables (recipes, crates, camp items),
    and in ForeverDB item links in the notes."""
    ids = set()
    config = json.loads((root / "data/captures.json").read_text())
    for receipt in config["captures"]:
        extract = json.loads((root / receipt["path"]).read_text())
        for market in extract["markets"].values():
            ids.update(item_id(key) for key in market["items"])
    fdb_path = root / "data/foreverdb.json"
    if fdb_path.exists():
        fdb = json.loads(fdb_path.read_text())
        for recipes in fdb.get("recipes", {}).values():
            for r in recipes:
                ids.add(r["item"])
                ids.update(i for i, _ in r["reagents"])
        for crate in fdb.get("crates", []):
            ids.add(crate["item"])
            ids.update(i for i, _ in crate["bundles"])
        for kit in fdb.get("camp", []):
            ids.add(kit["item"])
            ids.update(i for i, _ in kit["reagents"])
    for note in (root / "content").rglob("*.md"):
        ids.update(int(i) for i in re.findall(r"foreverdb\.net/item/(\d+)", note.read_text()))
    return ids


def refresh(root: Path = ROOT) -> dict:
    names, source = download_names()
    ids = wanted_ids(root)
    found = {str(i): names[i] for i in sorted(ids) if i in names}
    record = {"source": source, "names": found,
              "missing": sorted(i for i in ids if i not in names)}
    (root / "data/items.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    return {"items": len(ids), "named": len(found), "missing": len(record["missing"])}


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
    print(json.dumps(refresh(), indent=2))
