---
updated: 2026-10-27
summary: Which popular addons have a Forever version, the addons made just for Forever, and how to install them on the modern client.
sources: CurseForge (checked 26 October 2026), ForeverDB, foreverchanges.pro, Icy Veins, mmonster.co, Blizzard forums, ElvUI on GitHub and Tukui
---

## At a glance

- **Modern client, modern rules:** Forever uses the current game's interface and addon rules, interface number 16001 (game version 1.60.1). Classic Era and Anniversary addons won't load properly.
- **Addons show, they don't act:** in combat, addons see less than they used to and can't play for you.
- **Find the right file:** on CurseForge, filter by the **Forever** game flavour. Big addons ship one download that covers Forever and other versions, so don't rely on file names.
- **Already built in:** a damage meter, a Cooldown Manager, Edit Mode, combined bags and quest objectives on the map.
- **Missing:** WeakAuras and TradeSkillMaster have no Forever download on CurseForge. Forks such as ForeverAuras and Musca Auras stand in for WeakAuras.
- **Settings don't carry over:** the live game is a new install, so copy your beta settings across yourself.
- **Stay safe:** download only from CurseForge, Wago, GitHub or the author's own site.

## What the guides say

### Before you install

- **The rules.** A Blizzard representative told addon authors that Forever shares the modern game's interface, including the vast majority of APIs available in patch 12.1.5 ([Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/)). That brings the same combat restrictions as the modern game. ForeverDB notes that Forever hides cooldowns and damage-over-time effects from addons in combat, and an addon author on [Blizzard's forums](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-addon-feedback/2385926) describes "secret" values that addons can't read. Addons written for the modern game need little work to run on Forever.
- **Where addons go.** The live game installs into its own `_forever_` folder inside your World of Warcraft folder, so addons go in `World of Warcraft\_forever_\Interface\AddOns`. The beta used `_classic_beta_` ([ForeverDB](https://foreverdb.net/addon)).
- **Choosing the file.** Use CurseForge's [Forever filter](https://www.curseforge.com/wow/search?class=addons&gameVersionTypeId=88568). Questie, Details!, Deadly Boss Mods and Auctionator each ship a single download tagged for Forever and several other versions, so there's no separate "-forever" file to look for. Other authors publish separate Forever projects with "Forever" in the name, such as Spy (Forever) or ForeverAuras.
- **Out-of-date addons.** Classic addons show as "Out of date". Ticking "Load out of date AddOns" may work but can throw errors ([foreverchanges.pro](https://foreverchanges.pro/addons)).
- **Bringing your beta setup.** Nothing comes over by itself. Copy the files you want from the beta's `WTF` folder into the same place under `_forever_` with the game closed; per-character settings only fit if the names match ([ForeverDB](https://foreverdb.net/launch/beta)). See [Known issues](ledger:more/known-issues/).
- **Built-in features.** Turn on the Cooldown Manager (Options, Advanced Options) and the Damage Meter (Options) before hunting for an addon; since 8 October the Cooldown Manager covers every class (foreverchanges.pro).

### Popular addons and their Forever status

"Yes" means a file tagged for Forever was on CurseForge on 26 October 2026.

| Addon | What it's for | Forever version | Source |
|---|---|---|---|
| **Questing and levelling** | | | |
| Questie | Quest givers, objectives and hand-ins on the map | Yes; Forever's new quests are still being added (foreverchanges.pro) | [CurseForge](https://www.curseforge.com/wow/addons/questie) |
| RestedXP Guide | Step-by-step levelling routes | Yes; the addon and early routes are free, the full guide is paid ([ForeverDB](https://foreverdb.net/addons/best)) | [CurseForge](https://www.curseforge.com/wow/addons/restedxp-guide) |
| Forever Quest Pins | Marks quests you haven't picked up yet | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/forever-quest-pins) |
| DungeonJournal | Dungeon quests, bosses and loot | Yes | [CurseForge](https://www.curseforge.com/wow/addons/dungeonjournal) |
| **Maps and travel** | | | |
| Leatrix Maps | Full zone maps, coordinates, dungeon icons | Yes | [CurseForge](https://www.curseforge.com/wow/addons/leatrix-maps) |
| TomTom | Waypoint arrow | Yes | [CurseForge](https://www.curseforge.com/wow/addons/tomtom) |
| Shortest Path Forever | Plans routes with flights, boats and portals | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/shortest-path-forever) |
| HandyNotes: WoW Forever | Map notes for things to find | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/handynotes-wow-forever) |
| RareScanner, SilverDragon | Rare spawn alerts | Yes | [RareScanner](https://www.curseforge.com/wow/addons/rarescanner), [SilverDragon](https://www.curseforge.com/wow/addons/silver-dragon) |
| **Auction House and gold** | | | |
| Auctionator | Scanning, pricing, quick posting | Yes | [CurseForge](https://www.curseforge.com/wow/addons/auctionator) |
| TradeSkillMaster | Auction and crafting automation | **No Forever version on CurseForge** (Retail and Classic versions only); mmonster.co lists a Forever entry on the developer's site but hasn't checked it | [CurseForge](https://www.curseforge.com/wow/addons/tradeskill-master), [mmonster.co](https://mmonster.co/wow-forever/guides/addons/tradeskillmaster) |
| Syndicator | Find items across your characters | Yes (foreverchanges.pro) | [foreverchanges.pro](https://foreverchanges.pro/addons) |
| **Bags** | | | |
| Bagnon | All bags in one window | Yes | [CurseForge](https://www.curseforge.com/wow/addons/bagnon) |
| Baganator | Sorted bags with cross-character search | Yes | [CurseForge](https://www.curseforge.com/wow/addons/baganator) |
| **Interface and action bars** | | | |
| Bartender4 | Action bars | Yes | [CurseForge](https://www.curseforge.com/wow/addons/bartender4) |
| Dominos | Action bars | Yes | [CurseForge](https://www.curseforge.com/wow/addons/dominos) |
| ElvUI | Full interface replacement | **Development version only:** the GitHub code lists interface 16001, but the 13 October Tukui release doesn't list Forever | [GitHub](https://github.com/tukui-org/ElvUI), [Tukui](https://tukui.org/elvui) |
| EllesmereUI | Full interface with its own editor | Yes | [CurseForge](https://www.curseforge.com/wow/addons/ellesmereui) |
| ForeverUI | Full interface built around Forever's rules | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/foreverui) |
| ClassicUI Forever | Classic's look on the modern interface | Yes (more than one project uses similar names) | [CurseForge](https://www.curseforge.com/wow/addons/classicui-forever) |
| MoveAny | Move any Blizzard window | Yes | [CurseForge](https://www.curseforge.com/wow/addons/moveany) |
| Leatrix Plus | Small conveniences: auto-repair, faster loot | Yes | [CurseForge](https://www.curseforge.com/wow/addons/leatrix-plus) |
| **Nameplates and frames** | | | |
| Plater | Customisable nameplates | Yes | [CurseForge](https://www.curseforge.com/wow/addons/plater-nameplates) |
| Platynator | Simpler nameplates | Yes | [CurseForge](https://www.curseforge.com/wow/addons/platynator) |
| Grid2, Clique | Raid frames and click-casting | Yes | [Grid2](https://www.curseforge.com/wow/addons/grid2), [Clique](https://www.curseforge.com/wow/addons/clique) |
| **Combat** | | | |
| Details! | Damage meter; reads the built-in meter | Yes | [CurseForge](https://www.curseforge.com/wow/addons/details) |
| Deadly Boss Mods, BigWigs | Boss timers and warnings | Yes | [DBM](https://www.curseforge.com/wow/addons/deadly-boss-mods), [BigWigs](https://www.curseforge.com/wow/addons/bigwigs) |
| GTFO | Alarm when standing in fire | Yes | [CurseForge](https://www.curseforge.com/wow/addons/gtfo) |
| ForeverThreat | Omen-style threat meter | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/foreverthreat-threat-meter-for-wow-forever) |
| WeakAuras | Custom alerts | **No Forever version**: it wasn't updated for the modern restrictions Forever uses | [foreverchanges.pro](https://foreverchanges.pro/addons) |
| ForeverAuras, Musca Auras | WeakAuras forks for Forever | Yes. Musca Auras imports WeakAuras, but triggers that read the combat log never fire ([mmonster.co](https://mmonster.co/wow-forever/guides/addons/weakauras-forever)) | [ForeverAuras](https://www.curseforge.com/wow/addons/foreverauras), [Musca Auras](https://www.curseforge.com/wow/addons/musca-auras) |
| **Professions** | | | |
| SkillUp Forever | Skill-up chances, levelling routes, shopping lists | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/skillup-forever) |
| ForeverArtisan | All twelve professions and camping | Yes, made for Forever | [CurseForge](https://www.curseforge.com/wow/addons/foreverartisan) |
| GatherLite | Remembers gathering spots | Yes | [CurseForge](https://www.curseforge.com/wow/addons/gatherlite) |
| Forever Fishing, FishFry | One-button fishing | Yes, made for Forever | [Forever Fishing](https://www.curseforge.com/wow/addons/forever-fishing), [FishFry](https://www.curseforge.com/wow/addons/fishfry-forever) |
| **Chat, PvP and errors** | | | |
| Prat 3.0 | Chat timestamps, colours, filters | Yes | [CurseForge](https://www.curseforge.com/wow/addons/prat-3-0) |
| Spy (Forever) | Warns when enemy players are near | Yes | [CurseForge](https://www.curseforge.com/wow/addons/spy-forever) |
| BugSack | Catches Lua errors quietly | Yes | [CurseForge](https://www.curseforge.com/wow/addons/bugsack) |

### Made for Forever

| Addon | What it does | Source |
|---|---|---|
| ForeverDB | ForeverDB's free companion: quest helper, dungeon run plans, gear tips, a rotation assistant, a wishlist and raid tools in one download of two folders (ForeverDB and ForeverDB_Helper) | [ForeverDB](https://foreverdb.net/addon), [CurseForge](https://www.curseforge.com/wow/addons/foreverdb) |
| TheWoWDB - Forever | Auction House companion: scan, see every live listing of an item, undercut by a copper, and share prices with thewowdb.com. Last updated 20 September | [CurseForge](https://www.curseforge.com/wow/addons/thewowdb-forever) |
| ForeverMapNotes | Map notes for ore and herb spawns, flight paths you haven't found, treasure chests and rares, with drops filtered for your class | [CurseForge](https://www.curseforge.com/wow/addons/forevermapnotes-bysiberiano12) |
| ZMacros | Ready-made class macros in your language, placed on the key you choose | [CurseForge](https://www.curseforge.com/wow/addons/zmacros) |
| Macro Bench | Build macros from blocks, with every line checked | [CurseForge](https://www.curseforge.com/wow/addons/macro-bench) |
| AzerothArchive Campsite Tracker | Records campsites and their buffs and shares them with your group and guild | [CurseForge](https://www.curseforge.com/wow/addons/azerotharchive-campsites) |
| PathForever | Trainer skills, class quest chains and a dungeon journal | [CurseForge](https://www.curseforge.com/wow/addons/pathforever) |

ForeverDB keeps a running list of [new addons to watch](https://foreverdb.net/addons/watch), picked from the addon community but untested. Several are small games or social tools rather than gameplay aids.

## Ledger findings

Nothing recorded yet.

## Read more

- [CurseForge: Forever addons](https://www.curseforge.com/wow/search?class=addons&gameVersionTypeId=88568): the flavour filter to check any addon yourself
- [ForeverDB: The best WoW Forever addons](https://foreverdb.net/addons/best): addons by job, with Forever file dates and overlap with ForeverDB's own
- [ForeverDB: The ForeverDB addon](https://foreverdb.net/addon): the companion addon and install steps, including Linux
- [foreverchanges.pro: Addons](https://foreverchanges.pro/addons): 76 addons with Forever versions, built-in replacements and beta fixes
- [Icy Veins: Addons in WoW Forever](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/): Blizzard's statement on addon rules
- [Blizzard forums: Addon compatibility feedback](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-addon-feedback/2385926): an addon author's technical notes on the client
- [mmonster.co: WeakAuras Forever](https://mmonster.co/wow-forever/guides/addons/weakauras-forever) and [TradeSkillMaster](https://mmonster.co/wow-forever/guides/addons/tradeskillmaster): status checks on two big addons (a boosting site's guide pages)
- [ElvUI on GitHub](https://github.com/tukui-org/ElvUI): the development version with Forever support
