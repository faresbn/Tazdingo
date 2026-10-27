"""Write data/foreverdb-api.json from the cached ForeverDB API answers: only what pages use.

Called by `python3 scripts/foreverdb_api.py slim`. Everything kept is labelled with where it
comes from: the Forever client, players' sightings in Forever, or Classic data that Forever
hasn't confirmed yet.
"""
from __future__ import annotations

import json
from pathlib import Path

PROFESSIONS = ["alchemy", "blacksmithing", "cooking", "enchanting", "engineering", "first-aid", "fishing",
               "herbalism", "leatherworking", "mining", "skinning", "tailoring"]
CLASSES = ["Warrior", "Paladin", "Hunter", "Rogue", "Priest", "Shaman", "Mage", "Warlock", "Druid"]


def answer(cache: Path, name: str):
    path = cache / name
    return json.loads(path.read_text()).get("data") if path.exists() else None


def paged(cache: Path, prefix: str) -> tuple[dict | None, list]:
    """The first page's object and every page's records, for /professions/<slug> and /items."""
    first, rows = None, []
    offset = 0
    while True:
        data = answer(cache, f"{prefix}_limit-100_offset-{offset}.json")
        if data is None:
            break
        if isinstance(data, list):
            rows += data
        else:
            first = first or data
            rows += data.get("recipes", [])
        offset += 100
    return first, rows


def vendor(v: dict) -> dict:
    return {"name": v["name"], "faction": v.get("faction"), "zone": v.get("zone"), "x": v.get("x"), "y": v.get("y"),
            "price": v.get("price"), "costs": [[c.get("name"), c.get("amount")] for c in v.get("costs") or []],
            "limited": bool(v.get("limitedStock")), "seen": bool(v.get("seenInForever"))}


def slim(cache: Path, out: Path, credit: str, today: str) -> None:
    meta = answer(cache, "meta.json") or {}
    data = {"source": {"credit": credit, "build": meta.get("build"), "level_cap": meta.get("levelCap"), "fetched_on": today},
            "items": {}, "professions": {}, "gathering": {}, "classes": {}, "disenchant": []}
    _, listed = paged(cache, "items")
    wanted = set()
    for path in cache.glob("items_*.json"):
        if path.stem.split("_", 1)[1].isdigit():
            wanted.add(int(path.stem.split("_", 1)[1]))
    for row in listed:
        if row["id"] in wanted:
            data["items"][str(row["id"])] = {"class": row.get("class"), "subclass": row.get("subclass"), "quality": row.get("quality")}
    for item in wanted:
        detail = answer(cache, f"items_{item}.json")
        if detail:
            entry = data["items"].setdefault(str(item), {"class": detail.get("class"), "subclass": detail.get("subclass"),
                                                        "quality": detail.get("quality")})
            if detail.get("sellPrice"):
                entry["sell"] = detail["sellPrice"]
    for slug in PROFESSIONS:
        first, recipes = paged(cache, f"professions_{slug}")
        if not first:
            continue
        bought = []
        for recipe in recipes:
            sources = recipe["learnedFrom"].get("sources") or {}
            vendors = (sources.get("vendors") or {})
            sellers = [vendor(v) for side in ("horde", "alliance") for v in vendors.get(side, [])]
            if sellers:
                seen = {}
                for s in sellers:  # a vendor serving both factions appears on both lists
                    seen.setdefault((s["name"], s["zone"]), s)
                bought.append({"recipe": recipe["name"], "skill": sources.get("learnAtSkill"), "new": recipe.get("newInForever"),
                               "vendors": sorted(seen.values(), key=lambda s: (not s["seen"], s["faction"] or "", s["name"]))})
        data["professions"][slug] = {
            "ranks": [[r["rank"], r["maxSkill"]] for r in first.get("ranks", [])],
            "trainers": [{"name": t["name"], "title": t.get("title"), "side": t.get("side"), "zone": t.get("zone"),
                          "x": t.get("x"), "y": t.get("y"), "up_to": t.get("trainsUpToSkill"), "seen": bool(t.get("seenInForever"))}
                         for t in first.get("trainers", [])],
            "bought": sorted(bought, key=lambda b: (b["skill"] or 0, b["recipe"])),
            "recipes": first.get("recipeCount"), "new": first.get("newInForever"), "changed": first.get("changedFromClassic")}
    for slug in ("herbalism", "mining", "skinning", "fishing"):
        g = answer(cache, f"gathering_{slug}.json")
        if not g:
            continue
        entry = {"note": g.get("note"),
                 "best": [{"from": b["fromSkill"], "to": b["toSkill"], "zones": [z["name"] for z in b["zones"]]} for b in g.get("bestZones", [])]}
        if slug in ("herbalism", "mining"):
            entry["nodes"] = [{"name": n["name"], "skill": n.get("skill"), "seen": n.get("spotsSeenInForever", 0),
                               "zones": [z["name"] for z in n.get("topZones", [])[:3]]}
                              for n in g.get("nodes", []) if n.get("skill")]
        if slug == "fishing":
            entry["zones"] = sorted(({"name": z["name"], "skill": z.get("skill"), "catch": [[c["name"], c["chance"]] for c in z.get("loot", [])[:3]]}
                                     for z in g.get("zones", []) if z.get("skill")), key=lambda z: (z["skill"], z["name"]))
        data["gathering"][slug] = entry
    for name in CLASSES:
        c = answer(cache, f"classes_{name}.json")
        if c:
            data["classes"][name] = [{"name": a["name"], "line": a.get("line"), "learned": a.get("learned"), "new": bool(a.get("newInForever")),
                                      "levels": sorted({r["level"] for r in a.get("ranks", []) if r.get("level")})}
                                     for a in c.get("abilities", [])]
    for band in answer(cache, "disenchant.json") or []:
        results = ((band.get("forever") or {}).get("results") or (band.get("classic") or {}).get("results") or [])
        data["disenchant"].append({"quality": band["quality"], "kind": band["kind"], "from": band["itemLevelMin"], "to": band["itemLevelMax"],
                                   "skill": band.get("skill"), "seen": bool(band.get("seenInForever")),
                                   "results": [[r["name"], r["chancePercent"], r["min"], r["max"]] for r in results]})
    out.write_text(json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
    print(f"Wrote {out.name}: {len(data['items']):,} items ({sum(1 for v in data['items'].values() if v.get('sell')):,} with vendor prices), "
          f"{len(data['professions'])} professions, {len(data['classes'])} classes; build {data['source']['build']}.")
