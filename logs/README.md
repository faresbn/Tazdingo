# Combat logs: start here

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

## What's here

Newest first. Each day's `index.md` has the details.

| Date | Character | What | Size | Day |
|---|---|---|---|---|
| 2026-11-09 23:04 | Orc Warlock | Excavation Site: Wetlands (4 encounters) | 7.4 MB | `logs/orc-warlock/2026-11-09/index.md` |
| 2026-11-08 23:57 | Orc Warlock | Excavation Site: Wetlands (3 encounters) | 7.2 MB | `logs/orc-warlock/2026-11-08/index.md` |
| 2026-11-08 21:18 | Orc Warlock | Shadowfang Keep (8 encounters) | 9.4 MB | `logs/orc-warlock/2026-11-08/index.md` |
| 2026-11-08 17:54 | Orc Warlock | Blackfathom Deeps (6 encounters) | 11.3 MB | `logs/orc-warlock/2026-11-08/index.md` |
| 2026-11-07 19:22 | Orc Warlock | Shadowfang Keep (8 encounters) | 8.8 MB | `logs/orc-warlock/2026-11-07/index.md` |
| 2026-11-07 10:13 | Orc Warlock | Wailing Caverns (8 encounters) | 7.0 MB | `logs/orc-warlock/2026-11-07/index.md` |
| 2026-11-06 18:28 | Orc Warlock | Shadowfang Keep (8 encounters) | 10.2 MB | `logs/orc-warlock/2026-11-06/index.md` |
| 2026-11-06 16:27 | Orc Warlock | Ruins of Lordaeron (6 encounters) | 8.0 MB | `logs/orc-warlock/2026-11-06/index.md` |
| 2026-11-05 10:10 | Orc Warlock | Ragefire Chasm (9 encounters) | 10.1 MB | `logs/orc-warlock/2026-11-05/index.md` |
