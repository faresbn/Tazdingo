# Launch-day data update: 5 November 2026

The first live data, two hours after launch: the first Live Auctionator scan, ForeverDB's release build, and a look at two more addon files Fares had locally.

## What was done

- **First Live Auction House scan published.** 78 items on CAMWOW EU5 Realm 2 PvP (Horde), scanned 01:09 UTC. Auctionator keys this realm as `PvP`, the same key as the Beta market, so `market_names` in `data/game.json` is now keyed by market slug (`forever-pvp`, `forever-beta-pvp`); `build.py` falls back to the raw key.
- **The first publish failed** and was fixed: two inbox tests assumed the repository would never hold a live Auctionator original or a remembered market. `ingest.py` runs the tests before committing, against a clone of HEAD, so it couldn't see this; GitHub's run after the push did. The tests now set up their own state.
- **The scan commit's message carried the local file path** (including the WoW account folder number) because `ingest.py` reused a variable name. Fixed for future scans; commit `adbb82f` keeps that message (changing it would rewrite pushed history; Fares's call).
- **ForeverDB refreshed at build 1.60.1.70790, level cap 60** (the launch condition in AGENTS.md): `foreverdb_data.py`, `item_names.py`, `blue_posts.py`, and the API `fetch` + `slim`. The fetch hit a 502 (launch-day load) once and resumed from its cache.

## ForeverDB.lua: what it is, and how it differs from the API

**It's not a copy of ForeverDB's database; it's your own observations waiting to be shared with ForeverDB, plus the addon's settings.** The API serves the aggregated database built from every contributor's uploads and the game client; the Lua file is one contributor's raw input.

What's in it (as of 04:21 local, 5 November):
- `auctions`: ForeverDB's own Auction House capture of the same 01:09 scan. Same 78 items as Auctionator, but per item it records **minimum and maximum price, total quantity and number of auctions** (`"min,max,quantity,auctions"`). Auctionator keeps only the minimum and quantity. Marginally richer; not worth a second parser now.
- `vendors`, `trainers`, `trainerPrices`: vendor stock with prices, trainer services and costs as seen in game on the release build.
- `quests`, `obs`/`obsChar` (an upload queue), `beasts`, `skins`, `disenchants`, `nodes`, `fish`, `encounters`: things the addon recorded for ForeverDB.
- `knowers`, `armory`, `obsChar`: **character names, player GUIDs and inspected players' stats.** This is why the file must not go through the inbox or into the public repository as it is.

The API covers all of this better once players' uploads are merged (vendors with prices and Merchant's Favor costs, trainers, disenchanting with sample counts, `changes-seen` for client-vs-game differences). The only thing the Lua adds is immediacy: your own sightings before ForeverDB merges them.

**API endpoints we don't use yet** that could matter later: `/changes-seen` (verified differences between the client files and what players saw: prices, rewards, stats), `liveClient` on items and spells (what release changed since Beta), `/quests`, `/vendors/{id}`, `/dungeons/{id}`, `/itemsets`. No endpoint serves Auction House prices; those still come from ForeverDB's site data (`foreverdb_data.py`).

## OneForAll.lua: potentially useful later, for one thing

A quality-of-life addon's settings. Mostly window positions and toggles. Useful content:
- `trainerCosts`: **every Warlock trainer spell with its cost and level** (186 entries, release build). Our class pages list abilities by level from the API, which has no training costs. A per-class "training cost by level" table (gold needed at 10, 20, 30…) is a real levelling question. It needs one capture per class, so only worth it if the group plays several classes and someone opens each trainer.
- `altRecipes` and `craftInv`: known recipes and bag contents per character, keyed by character name. Private; not for the site.

Verdict: keep it out of the inbox (it carries character names). Revisit if we want training-cost tables; a small processor would extract only `trainerCosts`.
