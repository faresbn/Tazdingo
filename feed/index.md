# Tazdingo feed: start here

This is a map. It holds no prices or guide text; it tells you which file to open. Open only the files the question needs.

Every path below is in the public repository: https://raw.githubusercontent.com/faresbn/Tazdingo/main/<path>

## Where to go

- `feed/prices/forever-pvp/index.md`: CAMWOW EU5 Realm 2 PvP (Horde) (Forever), 6168 items, latest scan 2026-11-12 03:40 UTC.
- `feed/prices/forever-beta-pvp/index.md`: Beta PvP realm (Forever Beta), 975 items, latest scan 2026-10-17 12:36 UTC, a Beta sample.
- `feed/prices/forever-beta-classicbetapvp/index.md`: Beta Classic PvP realm (Forever Beta), 6 items, latest scan 2026-10-17 12:36 UTC, a Beta sample.
- `feed/craft/index.md`: what to craft, by profession, with estimated margins.
- `feed/guides.md`: every class, spec, profession, world and More page, with its path and version.
- `feed/characters.md`: the account's own characters (level, gear, talents, professions, reputations), as last saved in the game.
- Combat logs, on the repository's `logs` branch: https://raw.githubusercontent.com/faresbn/Tazdingo/logs/README.md is the guide and the list. Instance runs complete (every player, as the game wrote them) and open-world summaries of our own characters; read the guide first, the instance files are large.

Original addon files, as uploaded (large; open only when asked about that addon):
- `data/captures/forever/auctionator/2026-11-12T0340Z.lua`: the latest of 32 auctionator file(s) (forever), processed into the prices above.

## How the data stays current

- **Auction House prices:** each time the game saves Auctionator's file (a `/reload` or logout after a scan), the scan is imported and published within minutes. A save with no new scan adds nothing. Times quoted are when the scan was made, not when it was imported.
- **ForeverDB data** (recipes, trainers, abilities, vendor and other players' prices, item names): refreshed three times a day. When the game build changes, the full refresh takes a couple of hours.
- **Blizzard's posts:** collected every two hours.
- **Combat logs:** with the ForeverDB refresh, each finished combat log is filed on the `logs` branch: the last 14 days or 10 logs per character below level 60, whichever is more; none for level-60 characters.
- **Characters:** with the ForeverDB refresh, the account's own characters are read from ForeverDB's addon file (`feed/characters.md`), under labels, not names. Each is as of that character's last logout or reload.

## How to answer

- **Prices:** open the market's map, then only the category file the item belongs to, or `alerts.md` for bargains, investments and movers. Quote the latest, typical or usual price with its scan time and steadiness. They're asking prices, not sales. Never mix markets.
- **Guides:** open the page from the guide map and say how current it is; Pre-launch means unverified in the live game.
- **Editing a page:** read it, keep everything still true, and submit the whole file through the inbox with its version from the guide map (instructions: TAZDINGO_INBOX.md in the project). If the page changed since, the inbox holds the edit; read it again.
- **People** use the website, not these files: https://faresbn.github.io/Tazdingo/

Item names, categories, vendor prices and recipes: Data from ForeverDB.net.
