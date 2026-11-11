"""File the game's combat logs into logs/: instance runs complete, open world as summaries of our own characters.

WoW writes one WoWCombatLog-<date>_<time>.txt per logging session in _forever_/Logs. For each one
that has stopped changing:

- **Instance runs** (dungeons, raids, battlegrounds: any zone whose instance ID isn't a continent)
  are cut out from the line entering the instance to the line leaving it, and kept exactly as the
  game wrote them, every player included, behind the log's COMBAT_LOG_VERSION header, so the file
  uploads to Warcraft Logs as it is. A short trip out and back (a corpse run) stays in the run.
- **Open world** is summarised for our own characters and their pets only: every fight, damage
  done and taken by ability, healing, resources, casts, failed casts, kills and deaths. Other
  players appear only as "another player"; nothing else about them is kept.

logs/<character>/<date>/ holds a day's files and an index.md (each run's encounters with their
line numbers); logs/README.md tells a reader how to use the folder and lists everything in it;
logs/sources.json records which game logs were filed. `--prune`, run after the filing is pushed,
deletes game logs older than a week from the game's folder, only if git has everything they wrote. Characters are named by the same labels as
data/characters.json (scripts/characters.py), read from ForeverDB.lua.

Run on the player's Mac (the 8-hourly watcher runs it). Usage:
    python3 scripts/combat_logs.py <_forever_/Logs folder> <ForeverDB.lua>
    python3 scripts/combat_logs.py --prune <_forever_/Logs folder>
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from characters import labels as character_labels, load as load_foreverdb

ROOT = Path(__file__).resolve().parents[1]
CONTINENTS = {0, 1}           # Eastern Kingdoms and Kalimdor: open world. Every other instance ID is an instance.
SETTLED = 30 * 60             # a game log changed in the last 30 minutes may still be written to
KEEP_DAYS = 7                 # filed game logs older than this are deleted from the game's folder
MIN_LINES = 100               # a shorter "run" is a login or logout inside an instance, with no fighting
MERGE_GAP = timedelta(minutes=10)   # a trip out of an instance shorter than this stays in the run
FIGHT_GAP = timedelta(seconds=6)    # no damage to or from us for this long ends an open-world fight
GITHUB_LIMIT = 95_000_000     # GitHub refuses files over 100 MB; bigger runs stay on the Mac (tmp/combat-logs/)
MINE = 0x1                    # unit flag: ours (the logging character, its pet and guardians)
GROUP = 0x7                   # mine, party or raid
PLAYER = 0x400

DAMAGE = {"SPELL_DAMAGE", "SPELL_PERIODIC_DAMAGE", "RANGE_DAMAGE", "DAMAGE_SHIELD", "SPELL_BUILDING_DAMAGE"}
MISSED = {"SPELL_MISSED", "SPELL_PERIODIC_MISSED", "RANGE_MISSED", "DAMAGE_SHIELD_MISSED", "SWING_MISSED"}
HEALS = {"SPELL_HEAL", "SPELL_PERIODIC_HEAL"}
ENERGIZE = {"SPELL_ENERGIZE", "SPELL_PERIODIC_ENERGIZE"}
POWER = {0: "mana", 1: "rage", 2: "focus", 3: "energy", 6: "runic power"}


# --- Reading lines -------------------------------------------------------------------------------

def stamp(line: bytes) -> datetime | None:
    head = line.split(b"  ", 1)[0].decode("ascii", "replace")
    try:
        return datetime.strptime(head, "%m/%d/%Y %H:%M:%S.%f")
    except ValueError:
        return None


def fields(line: bytes) -> list[str]:
    body = line.split(b"  ", 1)
    if len(body) < 2:
        return []
    return next(csv.reader([body[1].decode("utf-8", "replace").rstrip("\r\n")]), [])


def number(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def flags(value: str) -> int:
    try:
        return int(value, 16)
    except (TypeError, ValueError):
        return 0


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "unknown"


# --- Splitting a game log into instance runs and open world --------------------------------------

def zones(lines: list[bytes]) -> list[tuple[int, int, str, int]]:
    """Every ZONE_CHANGE: (line index, instance ID, zone name, difficulty)."""
    out = []
    for i, line in enumerate(lines):
        if b"  ZONE_CHANGE," in line:
            f = fields(line)
            if len(f) >= 4:
                out.append((i, int(number(f[1])), f[2], int(number(f[-1]))))
    return out


def runs(lines: list[bytes]) -> list[dict]:
    """Instance runs as line ranges [start, end): consecutive zone lines with the same non-continent
    instance ID, merged across a short trip out."""
    marks = zones(lines)
    spans = []
    for n, (i, instance, name, difficulty) in enumerate(marks):
        end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
        if instance in CONTINENTS:
            continue
        if spans and spans[-1]["instance"] == instance and spans[-1]["end"] == i:
            spans[-1]["end"] = end
        else:
            spans.append({"instance": instance, "start": i, "end": end, "names": []})
        spans[-1]["names"].append((difficulty, name))
    merged: list[dict] = []
    for span in spans:
        if merged and merged[-1]["instance"] == span["instance"]:
            left, back = stamp(lines[merged[-1]["end"] - 1]), stamp(lines[span["start"]])
            if left and back and back - left <= MERGE_GAP:
                merged[-1]["end"] = span["end"]
                merged[-1]["names"] += span["names"]
                continue
        merged.append(span)
    merged = [s for s in merged if s["end"] - s["start"] >= MIN_LINES]
    for span in merged:   # the instance's own name: the zone line with the highest difficulty, the last if tied
        span["name"] = max(enumerate(span["names"]), key=lambda x: (x[1][0], x[0]))[1][1]
    return merged


def header_before(lines: list[bytes], index: int) -> bytes | None:
    for i in range(index, -1, -1):
        if b"  COMBAT_LOG_VERSION," in lines[i]:
            return lines[i]
    return None


PLAYER_UNIT = re.compile(rb'(Player-\d+-[0-9A-F]+),"([^"]*)",(0x[0-9a-fA-F]+)')


def players(lines: list[bytes]) -> tuple[set[str], dict[str, str]]:
    """(our own player IDs, {player ID: name} for everyone in our group) seen in these lines."""
    own, group = set(), {}
    for line in lines:
        for guid, name, flag in PLAYER_UNIT.findall(line):
            value = int(flag, 16)
            if value & PLAYER and value & GROUP:
                group[guid.decode()] = name.decode("utf-8", "replace")
                if value & MINE:
                    own.add(guid.decode())
    return own, group


def encounters(lines: list[bytes], offset: int = 1) -> list[dict]:
    """ENCOUNTER_START/END pairs; line numbers are 1-based in the written file (offset 2 when a header line goes first)."""
    out, open_ = [], {}
    for i, line in enumerate(lines):
        if b"  ENCOUNTER_START," in line:
            f = fields(line)
            open_[f[1]] = {"name": f[2], "start_line": i + offset, "start": stamp(line)}
        elif b"  ENCOUNTER_END," in line:
            f = fields(line)
            begun = open_.pop(f[1], None)
            if begun:
                out.append({"name": begun["name"], "start_line": begun["start_line"], "end_line": i + offset,
                            "time": begun["start"].strftime("%H:%M") if begun["start"] else "",
                            "seconds": round(number(f[6]) / 1000) if len(f) > 6 else None,
                            "result": "kill" if len(f) > 5 and f[5] == "1" else "wipe"})
    return out


# --- Open-world summary ---------------------------------------------------------------------------

class Ledger:
    """One character's open-world activity in one game log."""

    def __init__(self, label: str):
        self.label = label
        self.fights: list[dict] = []
        self.fight: dict | None = None
        self.done = defaultdict(lambda: {"hits": 0, "crits": 0, "total": 0.0, "max": 0.0, "misses": Counter()})
        self.taken = defaultdict(lambda: {"hits": 0, "total": 0.0, "max": 0.0})
        self.avoided = Counter()
        self.healed = defaultdict(lambda: {"casts": 0, "total": 0.0, "over": 0.0})
        self.healed_by_others = Counter()
        self.buffs_from_others = Counter()
        self.gained = Counter()
        self.casts = Counter()
        self.failed = Counter()
        self.interrupts = Counter()
        self.dispels = Counter()
        self.kills = Counter()
        self.deaths: list[dict] = []
        self.recent_hits: list[str] = []
        self.zones = Counter()
        self.first = self.last = None
        self.zone = ""

    # a fight: our damage done or taken with no gap over FIGHT_GAP
    def touch(self, when: datetime):
        if self.fight is None or when - self.fight["end"] > FIGHT_GAP:
            self.fight = {"start": when, "end": when, "zone": self.zone, "done": 0.0,
                          "taken": 0.0, "healed": 0.0, "kills": Counter(), "died": False, "targets": set(), "foes": {}}
            self.fights.append(self.fight)
        self.fight["end"] = when

    def summary(self) -> str:
        fought = sum(max((f["end"] - f["start"]).total_seconds(), 1) for f in self.fights)
        done = sum(v["total"] for v in self.done.values())
        taken = sum(v["total"] for v in self.taken.values())
        heal = sum(v["total"] for v in self.healed.values())
        span = f"{self.first:%H:%M}–{self.last:%H:%M}" if self.first else ""
        out = [f"# {self.label}: open world, {self.first:%-d %B %Y} {span}", "",
               "Our character and pet only, from the game's combat log (game clock). Other players appear only as "
               "\"another player\". Damage is what landed, overkill excluded.", "",
               "## Totals", "",
               f"- Time in combat: {fought / 60:.1f} minutes over {len(self.fights)} fights; "
               f"zones: {', '.join(f'{z} ({n})' for z, n in self.zones.most_common())}.",
               f"- Damage done: {done:,.0f} ({done / fought if fought else 0:.1f} per second in combat). "
               f"Damage taken: {taken:,.0f}. Healing done: {heal:,.0f}.",
               f"- Kills: {sum(self.kills.values())} ({', '.join(f'{n} {k}' for k, n in self.kills.most_common(12))})."
               if self.kills else "- Kills: none.",
               f"- Deaths: {len(self.deaths)}."]
        if self.gained:
            out.append("- Resources gained: " + ", ".join(f"{s} {n:,.0f}" for s, n in self.gained.most_common()) + ".")
        out += ["", "## Damage done", "", "| Ability | Hits | Crit % | Total | Share | Biggest | Misses |", "|---|---|---|---|---|---|---|"]
        for name, v in sorted(self.done.items(), key=lambda kv: -kv[1]["total"]):
            out.append(f"| {name} | {v['hits']} | {100 * v['crits'] / v['hits'] if v['hits'] else 0:.0f} | {v['total']:,.0f} | "
                       f"{100 * v['total'] / done if done else 0:.0f}% | {v['max']:,.0f} | "
                       f"{', '.join(f'{k.lower()} {n}' for k, n in v['misses'].most_common()) or '–'} |")
        out += ["", "## Damage taken", "", "| From | Hits | Total | Biggest |", "|---|---|---|---|"]
        for name, v in sorted(self.taken.items(), key=lambda kv: -kv[1]["total"])[:25]:
            out.append(f"| {name} | {v['hits']} | {v['total']:,.0f} | {v['max']:,.0f} |")
        if self.avoided:
            out += ["", "Avoided: " + ", ".join(f"{k.lower()} {n}" for k, n in self.avoided.most_common()) + "."]
        if self.healed or self.healed_by_others:
            out += ["", "## Healing", "", "| Spell | Casts or ticks | Healed | Overhealed |", "|---|---|---|---|"]
            out += [f"| {s} | {v['casts']} | {v['total']:,.0f} | {v['over']:,.0f} |" for s, v in
                    sorted(self.healed.items(), key=lambda kv: -kv[1]["total"])]
            if self.healed_by_others:
                out += ["", "From another player: " + ", ".join(f"{s} {n:,.0f}" for s, n in self.healed_by_others.most_common()) + "."]
        out += ["", "## Casts", "", ", ".join(f"{s} {n}" for s, n in self.casts.most_common()) or "None."]
        if self.failed:
            out += ["", "Failed casts: " + "; ".join(f"{s}: {n}" for s, n in self.failed.most_common(15)) + "."]
        if self.interrupts or self.dispels:
            out += ["", "Interrupted: " + (", ".join(f"{s} {n}" for s, n in self.interrupts.most_common()) or "none")
                    + ". Dispelled: " + (", ".join(f"{s} {n}" for s, n in self.dispels.most_common()) or "none") + "."]
        if self.buffs_from_others:
            out += ["", "Buffs from another player: " + ", ".join(f"{s} {n}" for s, n in self.buffs_from_others.most_common()) + "."]
        if self.deaths:
            out += ["", "## Deaths", ""]
            for d in self.deaths:
                out.append(f"- {d['time']} in {d['zone']}: last hits taken, oldest first: {'; '.join(d['hits']) or 'none recorded'}.")
        out += ["", "## Fights", "", "| # | Start | Zone | Enemies | Seconds | Damage done | Per second | Taken | Healed | Kills |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        for n, f in enumerate(self.fights, 1):
            secs = max((f["end"] - f["start"]).total_seconds(), 1)
            enemies = ", ".join(f"{k} ×{v}" if v > 1 else k for k, v in Counter(f["foes"].values()).most_common(4))
            out.append(f"| {n} | {f['start']:%H:%M:%S} | {f['zone']} | {enemies} | {secs:.0f} | {f['done']:,.0f} | "
                       f"{f['done'] / secs:.1f} | {f['taken']:,.0f} | {f['healed']:,.0f} | "
                       f"{sum(f['kills'].values())}{' (died)' if f['died'] else ''} |")
        return "\n".join(out) + "\n"


def open_world(lines: list[bytes], skip: list[tuple[int, int]], names: dict[str, str]) -> dict[str, Ledger]:
    """{own player ID: Ledger} for the lines outside instance runs."""
    inside = bytearray(len(lines))
    for start, end in skip:
        inside[start:end] = b"\x01" * (end - start)
    ledgers: dict[str, Ledger] = {}
    owner_of: dict[str, str] = {}   # our pets and guardians → their owner (our player ID)
    current_player = None
    zone = ""

    def ours(guid: str, flag: int) -> str | None:
        if guid in ledgers or (guid.startswith("Player-") and flag & MINE and flag & PLAYER):
            return guid
        if flag & MINE:
            return owner_of.get(guid) or current_player
        return None

    for i, line in enumerate(lines):
        if inside[i]:
            continue
        if b"  ZONE_CHANGE," in line:
            zone = fields(line)[2] if len(fields(line)) > 2 else zone
            continue
        if b"0x" not in line:
            continue
        f = fields(line)
        if len(f) < 9:
            continue
        event, src, src_name, src_flags, dst, dst_name, dst_flags = f[0], f[1], f[2], flags(f[3]), f[5], f[6], flags(f[7])
        src_own, dst_own = ours(src, src_flags), ours(dst, dst_flags)
        if event == "UNIT_DIED" and not dst_own:
            when = stamp(line)
            for book in ledgers.values():
                if book.fight and dst in book.fight["targets"] and when and when - book.fight["end"] <= FIGHT_GAP * 2:
                    book.kills[dst_name] += 1
                    book.fight["kills"][dst_name] += 1
            continue
        if not (src_own or dst_own):
            continue
        for guid, flag in ((src, src_flags), (dst, dst_flags)):
            if guid.startswith("Player-") and flag & MINE and flag & PLAYER and guid not in ledgers:
                ledgers[guid] = Ledger(names.get(guid, guid))
        if src.startswith("Player-") and src_flags & MINE:
            current_player = src
        player = src_own if src_own else dst_own
        if player not in ledgers:
            continue
        book = ledgers[player]
        when = stamp(line)
        if when is None:
            continue
        book.zone = zone
        book.first = book.first or when
        book.last = when
        if event == "SPELL_SUMMON" and src_own:
            owner_of[dst] = player
            continue
        if event == "SWING_DAMAGE_LANDED":
            continue   # the same hit as SWING_DAMAGE, seen from the target
        other = ("another player" if (dst if src_own else src).startswith("Player-") else (dst_name if src_own else src_name))
        actor = "" if src == player else f" (pet {src_name})"   # a pet's or guardian's own line

        if event in DAMAGE or event == "SWING_DAMAGE" or event == "ENVIRONMENTAL_DAMAGE":
            if event == "SWING_DAMAGE":
                spell, amount, overkill, crit = "Melee", number(f[28]), number(f[30]), f[35] == "1"
            elif event == "ENVIRONMENTAL_DAMAGE":
                spell, amount, overkill, crit = f[28].title(), number(f[29]), number(f[31]), False
            else:
                spell, amount, overkill, crit = f[10], number(f[31]), number(f[33]), f[38] == "1"
            landed = amount - max(overkill, 0)
            book.touch(when)
            if src_own and not dst_own:
                v = book.done[spell + actor]
                v["hits"] += 1; v["crits"] += crit; v["total"] += landed; v["max"] = max(v["max"], landed)
                book.fight["done"] += landed
                book.fight["targets"].add(dst)
                book.fight["foes"][dst] = other
            elif dst_own and not src_own:
                source = "the environment" if event == "ENVIRONMENTAL_DAMAGE" else other
                v = book.taken[f"{source}: {spell}"]
                v["hits"] += 1; v["total"] += landed; v["max"] = max(v["max"], landed)
                book.fight["taken"] += landed
                if event != "ENVIRONMENTAL_DAMAGE":
                    book.fight["foes"][src] = other
                if dst == player:
                    book.recent_hits = (book.recent_hits + [f"{source} {spell} {landed:,.0f}{' (crit)' if crit else ''}"])[-5:]
        elif event in MISSED:
            kind = f[9] if event == "SWING_MISSED" else (f[12] if len(f) > 12 else "MISS")
            spell = "Melee" if event == "SWING_MISSED" else f[10]
            book.touch(when)
            if src_own and not dst_own:
                book.done[spell + actor]["misses"][kind] += 1
            elif dst_own and not src_own:
                book.avoided[kind] += 1
        elif event in HEALS:
            amount, over = number(f[31]), number(f[33])
            if src_own:
                v = book.healed[f[10] + actor]
                v["casts"] += 1; v["total"] += amount - over; v["over"] += over
                if book.fight and when - book.fight["end"] <= FIGHT_GAP:
                    book.fight["healed"] += amount - over
            elif dst_own:
                book.healed_by_others[f[10]] += amount - over
        elif event in ENERGIZE and dst_own:
            book.gained[f"{POWER.get(int(number(f[33])), 'power')} from {f[10]}"] += number(f[31])
        elif event == "SPELL_CAST_SUCCESS" and src_own:
            book.casts[f[10] + actor] += 1
        elif event == "SPELL_CAST_FAILED" and src_own:
            book.failed[f"{f[10]} ({f[12]})" if len(f) > 12 else f[10]] += 1
        elif event == "SPELL_INTERRUPT" and src_own and len(f) > 13:
            book.interrupts[f[13]] += 1
        elif event == "SPELL_DISPEL" and src_own and len(f) > 13:
            book.dispels[f[13]] += 1
        elif event == "SPELL_AURA_APPLIED" and dst_own and not src_own and src.startswith("Player-") and len(f) > 12 and f[12] == "BUFF":
            book.buffs_from_others[f[10]] += 1
        elif event == "UNIT_DIED" and dst == player:
            book.deaths.append({"time": f"{when:%H:%M:%S}", "zone": zone, "hits": book.recent_hits})
            book.recent_hits = []
            if book.fight:
                book.fight["died"] = True
    for book in ledgers.values():
        for fight in book.fights:
            book.zones[fight["zone"]] += 1
        book.zones = Counter({z: n for z, n in book.zones.items() if n and z})
    return {k: v for k, v in ledgers.items() if v.fights}


# --- Filing ---------------------------------------------------------------------------------------

def file_log(path: Path, root: Path, label_of: dict[str, str]) -> list[dict]:
    """File one game log; returns what was written (relative paths with their details)."""
    lines = path.read_bytes().splitlines(keepends=True)
    written = []
    taken: set[Path] = set()

    def place(folder: Path, name: str, ext: str) -> Path:
        target = folder / f"{name}{ext}"
        n = 2
        while target in taken or target.exists():
            target = folder / f"{name}-{n}{ext}"
            n += 1
        taken.add(target)
        return target

    def who(own: set[str], group: dict[str, str]) -> str:
        guid = sorted(own)[0] if own else None
        return label_of.get(guid) or (group.get(guid, "").split("-")[0] if guid else "") or "Unknown character"

    spans = runs(lines)
    for span in spans:
        body = lines[span["start"]:span["end"]]
        first = stamp(body[0]) or stamp(lines[0])
        header = header_before(lines, span["start"])
        out = ([header] if header and not body[0].count(b"  COMBAT_LOG_VERSION,") else []) + body
        own, group = players(body)
        character = who(own, group)
        folder = root / "logs" / slug(character) / f"{first:%Y-%m-%d}"
        target = place(folder, f"{first:%H%M}-{slug(span['name'])}", ".txt")
        size = sum(len(x) for x in out)
        entry = {"kind": "instance", "character": character, "date": f"{first:%Y-%m-%d}", "place": span["name"],
                 "start": f"{first:%H:%M}", "end": f"{(stamp(body[-1]) or first):%H:%M}", "bytes": size, "lines": len(out),
                 "encounters": encounters(body, offset=len(out) - len(body) + 1),
                 "players": sorted(n for g, n in group.items() if g not in own),
                 "source": path.name}
        if size > GITHUB_LIMIT:
            target = root / "tmp/combat-logs" / target.relative_to(root / "logs")
            entry["note"] = "over GitHub's 100 MB limit: kept on the Mac in tmp/combat-logs/, not in the repository"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"".join(out))
        entry["file"] = target.relative_to(root).as_posix()
        written.append(entry)
    names = players(lines)[1]
    for guid, book in open_world(lines, [(s["start"], s["end"]) for s in spans], names).items():
        book.label = label_of.get(guid) or names.get(guid, "").split("-")[0] or "Unknown character"
        folder = root / "logs" / slug(book.label) / f"{book.first:%Y-%m-%d}"
        target = place(folder, f"{book.first:%H%M}-open-world", ".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(book.summary(), encoding="utf-8")
        written.append({"kind": "open world", "character": book.label, "date": f"{book.first:%Y-%m-%d}",
                        "place": ", ".join(book.zones) or "open world", "start": f"{book.first:%H:%M}", "end": f"{book.last:%H:%M}",
                        "fights": len(book.fights), "deaths": len(book.deaths), "file": target.relative_to(root).as_posix(),
                        "source": path.name})
    return written


# --- Indexes and the guide ------------------------------------------------------------------------

GUIDE = """# Combat logs: start here

What's here, for reading and discussing performance. Everything is from the game's own combat log (advanced logging),
filed automatically from the player's Mac. Times are the game's clock (the player's local time). Characters are named
by the same labels as `feed/characters.md`. Every path here is in the public repository:
https://raw.githubusercontent.com/faresbn/Tazdingo/main/<path>

## Two kinds of file

- **Instance runs** (`<time>-<instance>.txt`): the complete combat log of one dungeon, raid or battleground visit,
  exactly as the game wrote it, every player in the group included. Large (megabytes). They're kept unchanged so they
  can be uploaded to Warcraft Logs, and so any number can be checked.
- **Open world** (`<time>-open-world.md`): a summary of one logging session outside instances, for our own character
  and pet only: totals, damage done and taken by ability, healing, resources, casts and failed casts, kills, deaths
  with the hits that caused them, and every fight. Other players appear only as "another player".

## How to use this folder efficiently

1. Find the day below, then open that day's `index.md`: it lists each instance run with its encounters (boss, time,
   kill or wipe, fight length and the **line numbers** where each encounter starts and ends) and the group's players.
2. For open-world questions, the `-open-world.md` summary usually answers it; open nothing else.
3. Open an instance `.txt` only for a question the index can't answer. Read only the encounter's line range if you
   can. If the file is too large to read whole, say so and ask the player to attach it to the conversation so it can
   be analysed with code. Never estimate numbers you haven't read.

## Reading an instance log

Each line is `M/D/YYYY HH:MM:SS.ffff  EVENT,field,field,...` (two spaces after the time; quoted names may contain
commas, so parse as CSV). Fields are numbered from 0 at the event name:

- 1–4: source ID, name, flags, raid flags; 5–8: target ID, name, flags, raid flags. Flags: `0x1` ours (the logging
  character and its pets), `0x2` party, `0x4` raid, `0x400` a player, `0x800` an NPC.
- Spell events (`SPELL_*`, `RANGE_*`, `DAMAGE_SHIELD`): 9 spell ID, 10 spell name, 11 school; then 12–30 the unit's
  state (12 unit ID, 13 owner ID for pets, 14 current health, 15 maximum health, 26 map, 30 level).
- Damage (`SPELL_DAMAGE`, `SPELL_PERIODIC_DAMAGE`, `RANGE_DAMAGE`): 31 amount, 33 overkill (-1 none), 37 absorbed,
  38 critical (1). Melee (`SWING_DAMAGE`): 28 amount, 30 overkill, 35 critical. Count `SWING_DAMAGE` only:
  `SWING_DAMAGE_LANDED` is the same hit again.
- Healing (`SPELL_HEAL`, `SPELL_PERIODIC_HEAL`): 31 amount, 33 overhealing, 35 critical.
- `ENCOUNTER_START`: boss ID, name, difficulty, group size, instance ID. `ENCOUNTER_END`: boss ID, name, difficulty,
  group size, success (1 kill, 0 wipe), fight length in milliseconds.
- `COMBATANT_INFO` (at each encounter start): a player's stats, talents and gear.
- A player's damage per second for an encounter: their damage events (and their pets', by owner ID) between its
  `ENCOUNTER_START` and `ENCOUNTER_END` lines, divided by the fight length.
"""


def write_indexes(root: Path, record: dict) -> None:
    entries = [e for s in record["sources"].values() for e in s.get("written", [])]
    days = defaultdict(list)
    for e in entries:
        days[(e["character"], e["date"])].append(e)
    for (character, date), items in days.items():
        folder = root / "logs" / slug(character) / date
        if not folder.is_dir():
            continue
        lines = [f"# {character}: {date}", "", "Back to [the guide and the full list](../../README.md).", ""]
        for e in sorted(items, key=lambda e: e["start"]):
            name = Path(e["file"]).name
            if e["kind"] == "instance":
                lines += [f"## {e['start']}–{e['end']} {e['place']}", "",
                          f"`{e['file']}`: {e['bytes'] / 1e6:.1f} MB, {e['lines']:,} lines."
                          + (f" {e['note']}." if e.get("note") else ""), ""]
                if e["encounters"]:
                    lines += ["| Encounter | Time | Result | Seconds | Lines |", "|---|---|---|---|---|"]
                    lines += [f"| {x['name']} | {x['time']} | {x['result']} | {x['seconds']} | {x['start_line']}–{x['end_line']} |"
                              for x in e["encounters"]]
                    lines.append("")
                if e["players"]:
                    lines += [f"With: {', '.join(e['players'])}.", ""]
            else:
                lines += [f"## {e['start']}–{e['end']} open world", "",
                          f"[{name}]({name}): {e['place']}; {e['fights']} fights, {e['deaths']} deaths.", ""]
        (folder / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    catalog = ["", "## What's here", "", "Newest first. Each day's `index.md` has the details.", "",
               "| Date | Character | What | Size | Day |", "|---|---|---|---|---|"]
    for e in sorted(entries, key=lambda e: (e["date"], e["start"]), reverse=True):
        what = (f"{e['place']} ({len(e['encounters'])} encounters)" if e["kind"] == "instance"
                else f"open world: {e['place']} ({e['fights']} fights)")
        size = f"{e['bytes'] / 1e6:.1f} MB" if e["kind"] == "instance" else "summary"
        day = f"logs/{slug(e['character'])}/{e['date']}/index.md"
        catalog.append(f"| {e['date']} {e['start']} | {e['character']} | {what} | {size} | `{day}` |")
    (root / "logs").mkdir(exist_ok=True)
    (root / "logs/README.md").write_text(GUIDE + "\n".join(catalog) + "\n", encoding="utf-8")


# --- The run --------------------------------------------------------------------------------------

def refresh(game_logs: Path, foreverdb: Path | None, root: Path = ROOT, now: float | None = None) -> dict:
    now = now or time.time()
    state_path = root / "logs/sources.json"
    record = json.loads(state_path.read_text()) if state_path.is_file() else {"sources": {}}
    label_of = character_labels(load_foreverdb(foreverdb.read_bytes())) if foreverdb and foreverdb.is_file() else {}
    report = {"filed": [], "unchanged": 0, "waiting": []}
    for path in sorted(game_logs.glob("WoWCombatLog-*.txt")):
        info = path.stat()
        seen = record["sources"].get(path.name)
        if seen and seen["bytes"] == info.st_size and seen["modified"] == int(info.st_mtime):
            report["unchanged"] += 1
        elif now - info.st_mtime < SETTLED:
            report["waiting"].append(path.name)
            continue
        else:
            for old in (seen or {}).get("written", []):   # a log that grew: replace what it wrote before
                (root / old["file"]).unlink(missing_ok=True)
            record["sources"][path.name] = {"bytes": info.st_size, "modified": int(info.st_mtime),
                                            "written": file_log(path, root, label_of)}
            report["filed"].append(path.name)
    (root / "logs").mkdir(exist_ok=True)
    state_path.write_text(json.dumps(record, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    write_indexes(root, record)
    return report


def prune(game_logs: Path, root: Path = ROOT, now: float | None = None) -> list[str]:
    """Delete game logs older than a week, only once filed and committed: logs/sources.json in git records the log at
    its current size and time, and every file it wrote is tracked by git. Run only after the filing has been pushed."""
    now = now or time.time()
    committed = subprocess.run(["git", "-C", str(root), "show", "HEAD:logs/sources.json"], capture_output=True, text=True)
    if committed.returncode != 0:
        return []
    sources = json.loads(committed.stdout)["sources"]
    tracked = set(subprocess.run(["git", "-C", str(root), "ls-files", "logs"], capture_output=True, text=True).stdout.split())
    deleted = []
    for path in sorted(game_logs.glob("WoWCombatLog-*.txt")):
        info, seen = path.stat(), sources.get(path.name)
        if (now - info.st_mtime > KEEP_DAYS * 86400 and seen and seen["bytes"] == info.st_size
                and seen["modified"] == int(info.st_mtime)
                and all(w["file"] in tracked or w["file"].startswith("tmp/") for w in seen.get("written", []))):
            path.unlink()
            deleted.append(path.name)
    return deleted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("logs", type=Path, help="the game's _forever_/Logs folder")
    parser.add_argument("foreverdb", type=Path, nargs="?", help="ForeverDB.lua, for character labels")
    parser.add_argument("--prune", action="store_true",
                        help="only delete game logs over a week old that are filed and committed (run after a push)")
    args = parser.parse_args()
    print(json.dumps(prune(args.logs) if args.prune else refresh(args.logs, args.foreverdb), indent=2))
