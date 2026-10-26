"""Refresh data/foreverdb.json: the ForeverDB data the site's tables are built from.

- From ForeverDB's companion addon data (GPL-3.0 with the credit "Data from ForeverDB.net"):
  recipes, camp kits, Waylaid Crates, rare and collection counts, and the client build.
- From ForeverDB's site data (/data/prices/<n>.json, /data/sold/<n>.json): Auction House prices
  other players uploaded, and vendor prices. Shown as a second opinion, with the same credit.

Run on demand (scripts/ingest.py runs it); never during the build, so publishing never
depends on ForeverDB being reachable. Requests are spaced out and identify the site.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import time
from datetime import date
from pathlib import Path

from auctionator import InvalidCapture, LuaData, item_id
from item_names import CREDIT, MANIFEST, SITE, fetch

ROOT = Path(__file__).resolve().parents[1]
SHARDS = 64  # ForeverDB splits item data by item ID modulo 64
PAUSE = 0.15


def addon_file(manifest: dict, name: str) -> bytes:
    entry = next(f for f in manifest["data"]["files"] if f["path"] == f"Data/{name}")
    raw = fetch(SITE + entry["url"], entry["bytes"])
    if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
        raise InvalidCapture(f"{name} does not match ForeverDB's published fingerprint")
    return raw


def lua_text(quoted: str) -> str:
    return LuaData(quoted.encode()).value().decode("utf-8")


def parse_recipes(raw: str) -> dict:
    """ns.recipes = {Alchemy={{spell,"name",skill,yellow,green,grey,item,count,"reagents","learned",camp,new},...},...}"""
    body = raw[raw.index("ns.recipes"):]
    starts = [(m.start(), m.group(1) or lua_text(m.group(2)))
              for m in re.finditer(r'(?:([A-Za-z]+)|\[("(?:[^"\\]|\\.)*")\])=\{\{', body)]
    row = re.compile(r'\{(\d+),("(?:[^"\\]|\\.)*"),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),"([^"]*)","([^"]*)",(\d+),(\d+)\}')
    result = {}
    for n, (start, profession) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(body)
        recipes = []
        for m in row.finditer(body, start, end):
            spell, name, skill, yellow, green, grey, item, count, reagents, learned, camp, new = m.groups()
            recipes.append({"name": lua_text(name), "skill": int(skill), "item": int(item), "count": int(count),
                            "reagents": [[int(a), int(b)] for a, b in (r.split(":") for r in reagents.split(",") if r)],
                            "learned": learned, "new": new == "1"})
        result[profession] = recipes
    if sum(len(r) for r in result.values()) < 1000:
        raise InvalidCapture("Recipes.lua parsed suspiciously few recipes")
    return result


def parse_camp(raw: str) -> list[dict]:
    kits = []
    for entry in re.findall(r'\{(prof=.*?)\}(?=,\{prof=|\})', raw, re.S):
        fields = dict(re.findall(r'(\w+)=("(?:[^"\\]|\\.)*"|-?\d+)', entry))
        value = lambda k: lua_text(fields[k]) if fields.get(k, "").startswith('"') else int(fields[k]) if k in fields else None

        def number(k):
            if not re.fullmatch(r"-?\d+", fields.get(k, "")):
                raise InvalidCapture(f"Camp.lua: {k} should be a number")
            return int(fields[k])
        kits.append({"profession": value("prof"), "tier": number("tier"), "skill": number("skill"), "item": number("item"),
                     "name": value("name"), "kit": value("kit") == 1,
                     "reagents": [[int(a), int(b)] for a, b in (r.split(":") for r in (value("reagents") or "").split(",") if r)],
                     "effect": value("fx")})
    return kits


def parse_crates(raw: str) -> list[dict]:
    """Waylaid Crates: {crate item, required level, {item, count, ...} (fill with ANY one bundle), drops seen}"""
    block = raw[raw.index("crates={"):raw.index("cur=")]
    crates = []
    for item, level, bundles, drops in re.findall(r'\{(\d+),(\d+),\{([\d,]+)\},(\d+)\}', block):
        numbers = [int(n) for n in bundles.split(",")]
        crates.append({"item": int(item), "level": int(level),
                       "bundles": [[numbers[i], numbers[i + 1]] for i in range(0, len(numbers), 2)]})
    return crates


def counts(raw: str, table: str) -> dict:
    match = re.search(table + r'\s*=\s*\{([^}]*)\}', raw)
    return {k: int(v) for k, v in re.findall(r'(\w+)\s*=\s*(\d+)', match.group(1))} if match else {}


def site_shards(kind: str, wanted: set[int]) -> dict:
    """Fetch /data/<kind>/<n>.json for the shards holding the wanted items."""
    found = {}
    for shard in sorted({i % SHARDS for i in wanted}):
        data = json.loads(fetch(f"{SITE}data/{kind}/{shard}.json", 8_000_000))
        for key, value in data.items():
            if key.isdigit() and int(key) in wanted:
                found[int(key)] = value
        time.sleep(PAUSE)
    return found


def summarise_prices(entry: dict) -> dict:
    """Across ForeverDB's realms: the lowest current buyout, the median of medians, units listed."""
    realms = [r for r in entry.get("h", {}).values() if r.get("p")]
    return {"low": min(r["p"] for r in realms), "median": int(statistics.median(r.get("m") or r["p"] for r in realms)),
            "listed": sum(r.get("q") or 0 for r in realms), "realms": len(realms),
            "players": sum(r.get("u") or 0 for r in realms), "latest": max(r.get("d") or "" for r in realms),
            "confirmed": any(r.get("c") for r in realms)} if realms else {}


def wanted_items(recipes: dict, crates: list, kits: list, root: Path) -> set[int]:
    ids = set()
    for rows in recipes.values():
        for r in rows:
            ids.add(r["item"])
            ids.update(i for i, _ in r["reagents"])
    for crate in crates:
        ids.add(crate["item"])
        ids.update(i for i, _ in crate["bundles"])
    for kit in kits:
        ids.add(kit["item"])
        ids.update(i for i, _ in kit["reagents"])
    config = json.loads((root / "data/captures.json").read_text())
    for receipt in config["captures"]:
        for market in json.loads((root / receipt["path"]).read_text())["markets"].values():
            ids.update(item_id(k) for k in market["items"])
    return ids


def refresh(root: Path = ROOT, with_prices: bool = True) -> dict:
    manifest = json.loads(fetch(MANIFEST, 1_000_000))
    raw = {name: addon_file(manifest, name).decode("utf-8") for name in ("Recipes.lua", "Camp.lua", "Favor.lua", "Meta.lua", "Rares.lua", "Collections.lua")}
    meta = dict(re.findall(r'(\w+)="?([\w.:-]+)"?', raw["Meta.lua"][raw["Meta.lua"].index("ns.meta"):]))
    recipes, kits, crates = parse_recipes(raw["Recipes.lua"]), parse_camp(raw["Camp.lua"]), parse_crates(raw["Favor.lua"])
    record = {
        "source": {"credit": CREDIT, "client_build": meta.get("build"), "data_version": manifest["data"]["version"],
                   "fetched_on": date.today().isoformat(),
                   "note": "Recipes, camp kits and crates: ForeverDB addon data (GPL-3.0, credit required). "
                           "Prices and vendor prices: ForeverDB site data (players' uploads)."},
        "recipes": recipes, "camp": kits, "crates": crates,
        "rares": counts(raw["Rares.lua"], "ns.rareMeta"), "collections": counts(raw["Collections.lua"], "ns.collMeta"),
        "prices": {}, "vendor": {}}
    if with_prices:
        wanted = wanted_items(recipes, crates, kits, root)
        record["prices"] = {str(k): v for k, v in sorted((k, summarise_prices(e)) for k, e in site_shards("prices", wanted).items()) if v}
        record["vendor"] = {str(k): {"price": min(v["p"] for v in e["v"] if v.get("p")), "vendors": len(e["v"])}
                            for k, e in sorted(site_shards("sold", wanted).items()) if any(v.get("p") for v in e.get("v", []))}
    (root / "data/foreverdb.json").write_text(json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n")
    return {"build": meta.get("build"), "recipes": sum(len(r) for r in recipes.values()), "camp kits": len(kits),
            "crates": len(crates), "ForeverDB prices": len(record["prices"]), "vendor prices": len(record["vendor"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-prices", action="store_true", help="skip ForeverDB's price and vendor data")
    print(json.dumps(refresh(with_prices=not parser.parse_args().no_prices), indent=2))
