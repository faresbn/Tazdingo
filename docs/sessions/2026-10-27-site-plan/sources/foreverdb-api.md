# ForeverDB API: what our key gives us

Researched 27 October 2026 with the key in `FOREVERDB_API_KEY`. 73 API requests plus 8 page fetches, about one a second; the daily counter went from 10,000 to about 9,930. Trimmed samples of every endpoint are in `foreverdb-api/` (35 files, about 95 KB; the key appears in none of them). **Checked** means I saw it in a response or on ForeverDB's own docs. **Inferred** means I worked it out and haven't confirmed it.

## Summary

**What it means for the site.** The API is a big step up from the addon files and price shards we read now. It has where things are (trainers, vendors, quest givers, herbs, fish, beasts, with map coordinates), how each recipe is learned and what it costs, including Merchant's Favor, plus abilities by level, disenchanting and quests. It does **not** have Auction House prices, talents (tree positions), Legacy, rares, camping as a topic, mounts or reputation. Price pages keep running on our own scans plus the `/data/prices` shards. Everything is still the **last Beta build** (1.60.1.70532, extracted 24 October, level cap 30) (checked). The "live vs Beta" fields are documented but empty for now (checked: no `liveClient` key appeared in any response).

**Correcting the 26 October note.** It said the API offers "vendor prices, disenchanting, gathering, beta-vs-live changes" and needs a visible credit link. Those are right, but they're a small part of it. The API also covers items, spells, quests, vendors, dungeons, zones, classes, item sets, professions, poisons, battlegrounds, player-observed changes, ForeverDB's articles and Blizzard's posts. Beta-vs-live is promised (`liveClient`) but can't return anything until a live client build is extracted (checked: `/developers`; inferred: when that happens).

**Most useful to least, for our pages:**

1. **Profession detail** (`/professions/{slug}`): for profession pages. Every recipe comes with skill colours, reagents, category, how it's learned (trainer, vendor, drop, quest, automatic) and where: trainers and vendors per faction with zone and x/y, vendor price and **Merchant's Favor cost**, plus what Forever changed from Classic, with the Classic values. Rank caps and the full trainer list with locations, each marked seen in Forever or Classic data. The recipes are the same 2,491 we already have from the addon (checked), but with all of the above added. This is the biggest gain.
2. **Gathering** (`/gathering/{herbalism|mining|skinning|fishing}`): for the four gathering pages. Every node with its skill and its busiest zones, per-zone counts, and "best zones for each skill range". Skinning lists each zone's beasts and their skill. Fishing gives each zone's skill, catch with percentages, and pools. One request per profession. Spawn data is mostly Classic, and labelled as such (checked).
3. **Class abilities** (`/classes/{name}`): for class and spec pages. Every ability with its ranks and the level each rank is learned, grouped by tree ("line": Arms, Fury, Protection...). It's tagged trainer, `sod` (Season of Discovery-style rune abilities carried into Forever), quest or other, and flagged `newInForever`. Spell detail gives the tooltip text. This is enough for "what you learn and when" tables. It isn't talent trees (no positions or prerequisites) (checked).
4. **Vendors** (`/vendors`, `/vendors/{id}`): for the Merchant's Favor, camping and profession pages. Each vendor's stock with copper price, stack size, limited stock and **currency costs** (example: Nina Surefire in Redridge sells 29 items, all for Merchant's Favor only, 45 to 1,000 each, Alchemy recipes among them; Happy Camper in Durotar sells camp blueprints for 15 silver each). It also gives the reputation faction that discounts prices. 337 of 930 vendors have been seen in Forever (checked).
5. **Disenchanting** (`/disenchant`): for the Enchanting page. 52 bands (quality × weapon/armour × item-level range) with results, chances and counts. Today every band is Classic's table; none has Forever results yet (checked). Item detail adds `disenchant` and `sellPrice` per item.

Next in usefulness: **dungeons** (47 instances with level ranges and status, five new Forever dungeons; detail gives bosses only, `notableLoot` was empty in both I checked); **changes-seen** (400 things players' addons saw that differ from the client: vendor prices, item stats, quest rewards; 189 verified vendor changes), useful for Known Issues and "what's different" notes; **battlegrounds** (7, including Darkspear Islands from Blizzard's rules and three client-only ones); **quests** (6,614, with giver/turn-in locations and chains); **posts** (120 Blizzard posts, which our relay already covers); **articles** (139 ForeverDB articles, to link to, not copy); **zones** (60 UiMap IDs to join everything on); and **lang** (en, es, es-MX, de, fr game names).

## Access, terms, credit (all checked)

| Topic | Finding | Where |
|---|---|---|
| Base URL | `https://foreverdb.net/api/v1/`; `GET /api/v1` returns a machine-readable endpoint list | `/api/v1` response |
| Auth | Header `X-API-Key: $FOREVERDB_API_KEY`, or `Authorization: Bearer $FOREVERDB_API_KEY`. Keys belong to a ForeverDB account (Battle.net login), are approved by ForeverDB, up to 3 per account | https://foreverdb.net/developers |
| Limits | "60 requests a minute and 10,000 a day per key". Headers `x-ratelimit-limit/remaining/reset` and `x-daily-limit/remaining`; past a limit you get "429 with Retry-After" | `/developers`; headers seen on every response |
| Caching | `Cache-Control: private, max-age=60` on answers; errors `no-store` | response headers |
| Envelope | `{data, meta}`; `meta.build` on every answer; lists add `total`, `limit`, `offset`, `next` | every response |
| Paging | `limit` 1 to 100 (default 25), `offset`; `limit=101` gives 400 `bad_parameter` "limit must be between 1 and 100." | `error-bad-limit.json` |
| Credit | "You must credit ForeverDB.net as the source, with a visible link to https://foreverdb.net, wherever you show the data." Suggested markup: `<a href="https://foreverdb.net">Data from ForeverDB.net</a>` (also in every `meta.attribution`, and `attributionHtml` in the index) | `/developers`, `/api/v1` |
| Rules | "Don't resell the data or present it as your own, and keep to the limits." Client data "is Blizzard's"; Classic data and player observations are labelled | `/developers` |
| Republishing on a public site | Allowed: the API is described as data "for your own site, bot, addon tool or spreadsheet", on condition of the visible credit link | `/developers` |
| Licence | No licence named for the API (no GPL or CC). The only terms are the Rules above. Classic quest data comes from CMaNGOS classic-db (GPL-3.0) per `/about`. The addon files we use now are GPL-3.0 with the credit (from the earlier note). There's no `/terms` page (404) | `/developers`, `/about` |
| Affiliation | "ForeverDB isn't affiliated with Blizzard Entertainment." `meta.notAffiliated` repeats it | `/developers`, `/api/v1/meta` |

What it means for us: the credit we already show for addon data ("Data from ForeverDB.net") works if it's a **visible link** next to anything built from API data (checked rule; inferred that our current rendering needs a quick look to confirm it's linked on every such table). The API key must stay out of the public site. It belongs only in a local or Actions-secret fetch script, like the relay rule ("never receives GitHub publishing credentials"). The fetched data gets committed, not the key.

## Endpoints

Sizes are what I received. "Freshness" for everything is `meta.build` 1.60.1.70532, the last Beta build, extracted 2026-10-24 (checked: `/changelog` lists it as "Beta build 1.60.1.70532 (2026-10-24)"). Player-observed fields carry their own dates.

| Path | Purpose | Key fields | Bulk / per item | Notes |
|---|---|---|---|---|
| `/meta` | Data summary | `build`, `levelCap` (30), counts: items 22,459, spells 31,930, quests 6,614, vendors 930, dungeons 47, item sets 545, articles 139 | one call | levelCap is still the Beta's 30 (checked) |
| `/items` | Item list | id, name, quality, itemLevel, requiredLevel, class/subclass, inventoryType, icon, url | paged, 100 max; filters `q`, `quality`, `class`, `slot`, `minLevel`, `maxLevel` | 225 calls to list everything (inferred) |
| `/items/{id}` | One item | `stats[]`, `damage`, `speed`, `bonding`, **`sellPrice`** (copper), `unique`, `effects[]` with text, `disenchantable`, `disenchant{source, results[]}`; documented `liveClient`, `dataFromBuild` | per item, ~1 KB | `disenchant.source` says Classic or Forever (checked) |
| `/spells`, `/spells/{id}` | Spells | name, rank, description, icon; documented `liveClient` | paged / per item, ~0.5 KB | no cost, cooldown or range fields (checked) |
| `/quests`, `/quests/{id}` | Quests | level, requiredLevel, side, zone{n, slug, m}, `knownInForever`, `starts`/`ends` {type, id, name, location{uiMapId, x, y}, source, players}, `chain{previous, next, questLine}`, `updated` | paged (filters `q`, `zone`, `minLevel`, `maxLevel`, `side`) / per item | the "guide link" in the docs isn't a separate field; `url` is the quest page (checked) |
| `/vendors`, `/vendors/{id}` | Vendors and stock | name, title, side, zone, mapId, x, y, `seenInForever`, `reputationFaction`; detail `sells[]` {itemId, price, stack, pricePerItem, limited, **costs[]** (currency id 3402 = Merchant's Favor)} | paged (filters `q`, `zone`, `seen`) / per vendor, 2 to 6 KB | `q` matches name/title only; the Favor vendors have blank titles, so "Commerce" finds nothing (checked) |
| `/poisons` | Rogue poisons | 26 poisons (makes, reagents, learnAtLevel, skill colours, trainers seen, trainerCost), 27 trainers, 11 suppliers, `unusedReagents` | one call, 55 KB | the most complete single topic page |
| `/disenchant` | Disenchant table | 52 bands: quality, kind, itemLevelMin/Max, skill, `seenInForever`, `classic.results[]` {itemId, chancePercent, min, max} | one call, 20 KB | all Classic for now (checked) |
| `/dungeons`, `/dungeons/{id}` | Instances | kind, players, levelRange, `newInForever`, `status` (classic 28 / forever 5 / other 14); detail `bosses[]`, `notableLoot[]` | 1 call for all 47 / per instance | no Barrow Deeps or Hyjal Summit (the 9 December raids) yet; "other" covers Season of Discovery leftovers (inferred) |
| `/zones` | Zones/continents | id (UiMap), name, type, parentId, newInForever | one call (60) | the join key for every location |
| `/classes`, `/classes/{name}` | Classes and abilities | `abilities[]` {name, line (tree), learned: trainer/sod/quest/other, newInForever, ranks[] {spellId, rank, level}} | 9 calls, 8 to 23 KB | Warrior 46, Mage 64, Priest 64, Druid 66, Hunter 98, Paladin 68, Rogue 36, Shaman 57, Warlock 63 abilities. Lines include oddities such as Priest "Meditation", Hunter "Engraving", Warlock "Explorer Imp" (checked) |
| `/itemsets`, `/itemsets/{id}` | Item sets | items[]; detail `bonuses[]` {pieces, spellId, text} | paged / per set | 545 sets |
| `/professions` | 12 professions | recipeCount, newInForever, changedFromClassic, trainerCount, trainersSeenInForever, description, icon | one call | totals 2,491 recipes, matching our addon data (checked) |
| `/professions/{slug}` | One profession | `ranks[]` (maxSkill), `trainers[]` (location, trainsUpToSkill, seenInForever), `recipes[]` {spellId, category{parent}, skill{orange, yellow, green, grey}, makes, reagents, tools, needsNearby, learnedFrom{automatic, trainer, recipeItems, sources{ways, learnAtSkill, vendors{alliance, horde}[] with price/costs/limitedStock, quests, drops}}, newInForever, changedFromClassic[], classic{...old values}, campTier, speculation, speculationReasons} | paged, 100 per page, ~3.4 KB per recipe; filters `q`, `new`, `changed` | a full sweep is about 30 calls and 8 to 9 MB raw (inferred from 345 KB per 100) |
| `/gathering/{slug}` | Where to gather | herbalism/mining: `nodes[]` {skill, item, spawnPoints, spotsSeenInForever, topZones}, `zones[]` {nodes with counts}, `bestZones[]` {fromSkill, toSkill, zones}; skinning: zone levels and skill, `?zone=` adds `beasts[]` {levels, skill, gives}; fishing: zone skill, `loot[]` with chance, `pools[]`, casts in Forever | one call each, 8 to 38 KB | Classic spawn data, labelled; 78 herb and 109 mining spots seen in Forever so far (checked) |
| `/battlegrounds` | BGs and arenas | levels, teamSize, kind, winCondition, objectives with x/y, `rulesSource` blizzard/classic/client, howToPlay | one call, 9 KB | 7: WSG, AB, AV (Classic rules), Darkspear Islands (Blizzard), Battle for Blackrock, Battle for Gilneas, Mak'gora Arena (client only) |
| `/changes-seen` | Player-seen differences | kind, id, name, what, before, seen, comparedWith, players, firstSeen, lastSeen, verified | paged, 400 total; filters `kind`, `verified` | counts only, no player names (checked) |
| `/articles`, `/articles/{slug}` | ForeverDB articles | title, type, date, summary; detail `blocks[]`, `sources[]` | paged / per article | summarise in our own words and link; don't republish |
| `/posts` | Blizzard posts | source, kind, author, authorTitle, date, title, url (Blizzard), page (ForeverDB) | paged, 120 total | duplicates what `scripts/blue_posts.py` already gets |
| `?lang=` | Localised game names | `es`, `es-MX`, `de`, `fr`; English kept as `nameEn` etc. | any endpoint | checked on items/19019 (de) |

## Overlap with what we already have

| We have now (no key) | API equivalent | Gain |
|---|---|---|
| Recipes from `Recipes.lua` (name, skill, item, reagents, learned text, new flag) | `/professions/{slug}` | Same 2,491 recipes, plus trainers and vendors with locations, Favor costs, categories, the Classic diff, and speculation flags |
| Camp kits (`Camp.lua`) | none (`/camping` is a 404); `campTier` on recipes; camp blueprint vendor via `/vendors/{id}` | Small: where blueprints are sold and for how much |
| Waylaid Crates (`Favor.lua`) | none directly; Favor costs on vendor stock and recipe sources | The **spending** side of Merchant's Favor (what costs how much, at which vendor) |
| Rares, collection counts | none (`/rares`, `/mounts` are 404s) | none |
| AH prices (`/data/prices` shards) | none | none: keep the shards and our scans |
| Vendor prices (`/data/sold` shards) | `/vendors/{id}` and item `sellPrice` | Vendor names and locations next to each price, and the sell-to-vendor price |
| Item names (`SearchNames.lua`) | `/items` | Quality, level, slot and icon; but 225 calls for the full list, so the addon file stays better for names |

## Ideas: how each dataset could feed pages

- **Profession pages (12).** A "Where to learn" table per rank (trainer, zone, coordinates, seen in Forever or Classic). A "Recipes you buy" table (vendor, faction, price or Favor cost, limited stock). A "What Forever changed" list built from `changedFromClassic` plus `classic`. Skill-up colour bands for a levelling route. *Extra work:* a fetch script like `foreverdb_data.py` (about 35 calls; needs the key and keeps it local), a slimmer derived JSON (the raw pages are about 9 MB), and labels that keep "Classic data" visibly separate from "seen in Forever".
- **Gathering pages (Herbalism, Mining, Skinning, Fishing).** "Best zones by skill" straight from `bestZones`; node and skill tables; fishing catch tables per zone. *Extra work:* 4 calls, plus a clear "Classic spawn data" badge until Forever spots grow.
- **Enchanting.** A disenchant table by item-level band from `/disenchant`. *Extra work:* re-fetch after launch, once `seenInForever` fills in.
- **Merchant's Favor.** A "What Favor buys" table assembled from vendors whose stock has `costs` id 3402. *Extra work:* there's no "list vendors by currency", so finding the Favor vendors means walking the 337 seen vendors' detail pages (about 340 calls, which fits a day's quota) or collecting vendor IDs from recipe sources.
- **Class and spec pages (27).** An "Abilities by level" table per class, split by tree (`line`), marking rune-style (`sod`) and new-in-Forever abilities, with tooltip text from `/spells/{id}`. *Extra work:* spell text costs one call per rank (hundreds of calls), or show names only. Talents and Legacy still need the addon data or ForeverDB's talent calculator links.
- **Dungeons and raids.** A level-range table with new-in-Forever flags and boss lists. *Extra work:* the 9 December raids aren't in it yet; loot is empty.
- **Rogue page.** The poison table from `/poisons` (one call).
- **Known issues and launch checklist.** Verified `changes-seen` rows (vendor price corrections, stat differences) as "the game differs from the files" notes.
- **Zones and PvP.** `/zones` as the shared map-ID reference; `/battlegrounds` for a PvP summary with rule sources marked.
- **After launch.** Re-run once `meta.build` changes from 1.60.1.70532 and `levelCap` reads 60. Then `liveClient` should start showing what launch changed (inferred).

## Missing, unclear or failed (to retry or ask)

- **Not in the API (404 "No such endpoint"):** talents, Legacy, rares, camping, consumables, NPCs, races, reputation, mounts, prices, trainers, search, `openapi.json` (checked). Talents, Legacy, rares, camping and collections stay on the addon files.
- **No Auction House data** in the API (checked: no endpoint, `/prices/{id}` is a 404).
- **Live data:** none yet. `meta.build` is the Beta build, `levelCap` is 30, and no `liveClient` field appeared on items 19019 and 288906 or spells 12288 and 403196 (checked). Retry after launch.
- **Dungeon loot:** `notableLoot` was empty for The Hall of Thanes (3065) and Onyxia's Lair (249) (checked); maybe it's empty everywhere (inferred).
- **Vendor search** can't find the Favor vendors by title (they have none); `q=Commerce`, `q=Logistics` and `q=Quartermaster` returned 0 (checked).
- **Licence:** no explicit licence for API data, only the Rules. If we want certainty about republishing derived tables (as opposed to "showing the data"), ask ForeverDB through `/contact?topic=data` (that would be messaging someone, so Fares's call).
- **Quests' "guide" field** isn't a separate field in the responses I saw; only `url` (checked).
- No 429s or server errors were hit. The only error besides the 404s was the deliberate `limit=101` → 400.
