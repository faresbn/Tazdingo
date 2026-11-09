"""Refresh data/characters.json: the account's own characters' progression, from ForeverDB.lua.

ForeverDB's addon saves a snapshot of each of the account's characters whenever one logs out
or reloads (`ForeverDB_DB.armory`): level, gear, talents, professions, skills, reputations,
stats, PvP. This keeps only those snapshots, and only what is listed below, under a label
("Orc Warlock") instead of the character's name.

Everything else in the file stays on the player's computer and is never copied: character
names and player IDs, other players (guild members, inspected players, ForeverDB's suspected-bot
list), and ForeverDB's upload queue. The original file is not committed either, for the same
reason (an exception to committing addon files unchanged; docs/DECISIONS.md).

Run on the player's Mac (the 8-hourly watcher runs it); never during the build. Usage:
    python3 scripts/characters.py <path to ForeverDB.lua>
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from auctionator import InvalidCapture, LuaData

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/characters.json"
LIMIT = 50_000_000  # ForeverDB.lua is a few MB; refuse anything absurd

SLOTS = {1: "Head", 2: "Neck", 3: "Shoulder", 4: "Shirt", 5: "Chest", 6: "Waist", 7: "Legs", 8: "Feet",
         9: "Wrist", 10: "Hands", 11: "Finger", 12: "Finger", 13: "Trinket", 14: "Trinket", 15: "Back",
         16: "Main hand", 17: "Off hand", 18: "Ranged", 19: "Tabard"}
STANDINGS = {1: "Hated", 2: "Hostile", 3: "Unfriendly", 4: "Neutral", 5: "Friendly", 6: "Honored",
             7: "Revered", 8: "Exalted"}
STATS = (("health", "Health"), ("power", "Mana or energy"), ("str", "Strength"), ("agi", "Agility"),
         ("sta", "Stamina"), ("int", "Intellect"), ("spi", "Spirit"), ("armor", "Armour"))


def text(value) -> str:
    return value.decode("utf-8") if isinstance(value, bytes) else str(value)


def rows(table) -> list:
    """A Lua array (a dict keyed 1, 2, 3...) as a list in order, skipping empty entries."""
    if not isinstance(table, dict):
        return []
    return [table[k] for k in sorted(k for k in table if isinstance(k, int)) if isinstance(table[k], dict)]


def number(value) -> int | float | None:
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def load(raw: bytes) -> dict:
    match = re.search(rb"^ForeverDB_DB\s*=\s*", raw, re.M)
    if not match:
        raise InvalidCapture("This isn't ForeverDB.lua: it has no ForeverDB_DB")
    db = LuaData(raw[match.end():]).value()
    if not isinstance(db, dict) or not isinstance(db.get(b"armory"), dict):
        raise InvalidCapture("ForeverDB.lua has no character snapshots (ForeverDB_DB.armory)")
    return db


def own_ids(db: dict) -> set:
    """The account's own characters: ForeverDB's levelling coach and pace tables hold only those."""
    ids = set()
    for table in (b"coachRecaps", b"levelWinPace"):
        if isinstance(db.get(table), dict):
            ids.update(k for k in db[table] if isinstance(k, bytes) and k.startswith(b"Player-"))
    return ids


def gear(record: dict) -> list[dict]:
    worn = record.get(b"gear") if isinstance(record.get(b"gear"), dict) else {}
    out = []
    for slot in sorted(k for k in worn if isinstance(k, int)):
        entry = worn[slot]
        link = entry.get(b"link", b"") if isinstance(entry, dict) else b""
        item, name = re.search(rb"\|Hitem:(\d+)", link), re.search(rb"\|h\[(.*?)\]\|h", link)
        if item and name:
            out.append({"slot": SLOTS.get(slot, f"Slot {slot}"), "item": int(item.group(1)),
                        "name": name.group(1).decode("utf-8"), "item_level": number(entry.get(b"ilvl"))})
    return out


def talents(record: dict) -> dict:
    tal = record.get(b"talents") if isinstance(record.get(b"talents"), dict) else {}
    trees = {}
    for tree in (tal.get(b"trees") or {}).values():
        for group in rows((tree or {}).get(b"groups")):
            trees[text(group.get(b"name"))] = number(group.get(b"spent")) or 0
    loadout = tal.get(b"import")
    return {"points": trees, **({"loadout": text(loadout)} if isinstance(loadout, bytes) else {})}


def character(record: dict, collections: dict) -> dict:
    when = number(record.get(b"time"))
    reps = []
    for r in rows(record.get(b"reps")):
        lo, hi, now = number(r.get(b"lo")), number(r.get(b"hi")), number(r.get(b"standing"))
        reps.append({"name": text(r.get(b"name")), "standing": STANDINGS.get(number(r.get(b"reaction")), "Unknown"),
                     **({"progress": now - lo, "needed": hi - lo} if None not in (lo, hi, now) else {})})
    stats = record.get(b"stats") if isinstance(record.get(b"stats"), dict) else {}
    pvp = record.get(b"pvp") if isinstance(record.get(b"pvp"), dict) else {}
    owned = {k: len(collections.get(k.encode()) or {}) for k in ("mounts", "pets", "titles")}
    return {
        "class": text(record.get(b"class")), "race": text(record.get(b"race")), "faction": text(record.get(b"faction")),
        "level": number(record.get(b"level")), "item_level": number(record.get(b"ilvl")),
        "recorded_at": datetime.fromtimestamp(when, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if when else None,
        "recorded_on": text(record.get(b"reason")) if record.get(b"reason") else None,
        "build": text(record.get(b"build")) if record.get(b"build") else None,
        "gear": gear(record), "talents": talents(record),
        "professions": [{"name": text(p.get(b"name")), "skill": number(p.get(b"rank")), "max": number(p.get(b"max"))}
                        for p in rows(record.get(b"professions"))],
        "skills": [{"name": text(s.get(b"name")), "category": text(s.get(b"cat")), "skill": number(s.get(b"rank")),
                    "max": number(s.get(b"max"))} for s in rows(record.get(b"skills"))],
        "reputations": reps,
        "stats": {label: number(stats.get(key.encode())) for key, label in STATS if number(stats.get(key.encode())) is not None},
        "pvp": {label: number(pvp.get(key.encode())) for key, label in (("hk", "Honourable kills"), ("dk", "Dishonourable kills"),
                                                                        ("honorPoints", "Honour points"), ("renown", "Renown"))
                if number(pvp.get(key.encode())) is not None},
        "collected": {"mounts": owned["mounts"] or number(record.get(b"mounts")) or 0,
                      "pets": owned["pets"] or number(record.get(b"pets")) or 0, "titles": owned["titles"]},
    }


def extract(raw: bytes) -> dict:
    """The record written to data/characters.json: own characters only, labelled, no names or IDs."""
    db = load(raw)
    own = own_ids(db)
    picked = sorted((k, v) for k, v in db[b"armory"].items() if k in own and isinstance(v, dict))  # IDs grow with creation
    if not picked:
        raise InvalidCapture("ForeverDB.lua has no snapshots of the account's own characters")
    collections = db.get(b"collections") if isinstance(db.get(b"collections"), dict) else {}
    chars = [character(record, collections.get(key) or {}) for key, record in picked]
    seen: dict[str, int] = {}
    for c in chars:
        base = f"{c['race']} {c['class']}"
        seen[base] = seen.get(base, 0) + 1
        c["label"] = base if seen[base] == 1 else f"{base} {seen[base]}"
    chars = [{"label": c.pop("label"), **c} for c in chars]
    return {"source": {"addon": "ForeverDB", "table": "ForeverDB_DB.armory",
                       "note": "Each character's snapshot from when it last logged out or reloaded. Labels, not names."},
            "characters": sorted(chars, key=lambda c: (-(c["level"] or 0), c["label"]))}


def refresh(path: Path, root: Path = ROOT) -> dict:
    if path.stat().st_size > LIMIT:
        raise InvalidCapture(f"{path.name} is larger than expected")
    record = extract(path.read_bytes())
    (root / "data/characters.json").write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    return {c["label"]: f"level {c['level']}, recorded {c['recorded_at']}" for c in record["characters"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path, help="ForeverDB.lua from the account's SavedVariables folder")
    print(json.dumps(refresh(parser.parse_args().file), indent=2))
