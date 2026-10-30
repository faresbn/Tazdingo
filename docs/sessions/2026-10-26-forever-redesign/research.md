# Research: what shapes the redesign

26 October 2026. Four parallel research sweeps (ForeverDB; other Forever sites; ChatGPT-to-GitHub write routes; Blizzard's fan and naming rules), plus my own reading of ForeverDB's addon data. The claims that decide things were re-checked at the source (marked ✔).

## The game, as of the first live client (build 1.60.1.70532)

- **Level cap 60 at launch** ✔. The Beta stopped at 30. Raids open 9 December: Barrow Deeps (10), Hyjal Summit (20), Onyxia's Lair (40). https://foreverdb.net/launch
- **Nine classes, three talent trees each (27 specs).** One point per level from 10, so hybrid builds that mix two trees are normal. Blizzard targets about 5% less damage for hybrid DPS specs, and counts warriors as hybrids. https://foreverdb.net/class/Warrior/talents
- **Camping is a system, not waiting for rares** ✔: a Cooking campfire plus one buff object per profession. Rares are a separate topic (354 known, 19 seen in Forever). https://foreverdb.net/camping, https://foreverdb.net/rares
- **Legacy:** account-wide points from challenges, up to 16 spent per character on 21 perks in three trees. https://foreverdb.net/legacy
- **Professions:** 940 of 2,491 recipes are new; healing potions moved to First Aid; gathering professions craft. **Merchant's Favor:** a currency earned by turning in Waylaid Crates of materials to the Azeroth Commerce Authority or Durotar Supply and Logistics. https://foreverdb.net/veterans
- **New:** the Skyborne race; zones Mount Hyjal, Zephras Isle, Darkspear Islands, Riverglades, Shen'dralas.
- **Build 1.60.1.70532 is "the first live client"** ✔, so pre-launch data is from the live client, but still unconfirmed in play.

## What players come to sites for (judged by what each site puts first)

1. **Launch timing and roadmap.** A countdown leads most hubs (Icy Veins, Warcraft Tavern, WoW Eternity, The Forever Era, Raider.IO, TheWoWDB).
2. **Talent and Legacy calculators, and class changes.** First in Wowhead's tools and the first tile on Warcraft Tavern and Method.
3. **Spec and levelling guides with tier lists**, reached through a class or spec picker.
4. **Item price lookup:** search box plus movers on every Auction House site.

Wowhead's Forever hub leads with an icon bar (Classes, Class Changes, Talent Calculator, Tier Lists, Dungeons, Raids, Professions, Collections), then community findings, blue tracker and news. ForeverDB leads with counts, quick links and "what's new in the game files", and answers through search.

## Prices

- **Blizzard publishes no auction data for Forever.** Every price site runs on player scans uploaded through an addon. Sites: ForeverDB (4,455 items, 43 scans, price confirmed when two players agree ✔), TheWoWDB, auctionhouse.fyi (groups by ruleset and faction), goldcap.gg, AHledger, Booty Bay Broker.
- In real Beta data, prices swing wildly (troll listings, one-day spikes, items worth 1s one week and 75s the next), so volatility matters as much as the price.

## Sources we can use, and how

| Source | Use | Terms |
|---|---|---|
| Our own Auctionator scans | Primary prices, volatility, history | Ours |
| ForeverDB addon data (recipes, Favor crates, camp kits, consumables, talents, rares, collections, item new/changed flags) | Republish derived tables | GPL-3.0 with credit "Data from ForeverDB.net" ✔ |
| ForeverDB API (vendor prices, disenchanting, gathering, beta-vs-live changes) | Republish with credit | Needs a key: Fares logs in with Battle.net and requests it; visible credit link |
| ForeverDB Auction House, TheWoWDB, auctionhouse.fyi, goldcap.gg | Secondary prices: link per item to cross-check | No API; link only |
| Wowhead (guides, calculators, blue tracker), Icy Veins, Method, Warcraft Tavern, WoW Eternity, Eternadex, wowtbc.gg | Cited links; summaries in our own words | Wowhead's terms forbid copying and scraping; tooltips are free to embed |
| CMaNGOS classic-db | Classic quest/spawn data where Forever matches | GPL-3.0 |
| Blizzard forums and blue posts | Known issues, patch notes: link and summarise | Link and short quotes |
| Kami Labs (240 macros), CurseForge "-forever" files | Macro and addon lists: link | Link |

## Addons and known issues

- Forever runs the **modern client** (interface 16001), so Classic addons don't load. Confirmed Forever versions: Questie, RestedXP, Auctionator, Details!, DBM, BigWigs, Leatrix Plus/Maps, Bagnon, Baganator, Plater, TomTom, Bartender4. WeakAuras has no Forever version (forks: ForeverAuras, Musca Auras). TSM is disputed.
- Known issues: Blizzard's Beta known-issues thread (edited in place) and the Forever blue tracker. **macOS:** players report a Metal/GPU hang on Apple silicon (macOS 26/27) that can kill WindowServer; the reported workaround is Secondary Lighting set to Fair (not confirmed by Blizzard). An addon-settings reset bug is reported, also unconfirmed.

## ChatGPT and GitHub

- **ChatGPT's GitHub connector is read-only** ✔: "only lets you read from your repositories". It's per person, so each co-player would need their own GitHub account.
- **ChatGPT Business allows custom MCP servers with write actions** ✔. Only admins and owners create and publish them for the workspace. Web only (not mobile). ChatGPT asks for confirmation on writes depending on the app's permissions. **Not documented: whether they work inside shared projects.**
- GitHub Models was retired on 30 July 2026. GitHub Pro includes no Copilot; Copilot's coding agent needs Copilot Pro or higher.
- A push made with the workflow's own token doesn't start other workflows, so a router Action must trigger the publish workflow explicitly.

## Blizzard's rules and naming

- **Blizzard's Legal FAQ:** domains containing "some portion of your product names": **"No."** ✔ Screenshots you take in game: yes, non-commercial, notices kept ✔. Official art, logos and key art: not licensed for display.
- "WOW" is a registered US trademark. Established sites avoid marks in their names (Icy Veins, Raider.IO) and carry "Not affiliated with or endorsed by Blizzard Entertainment" plus Blizzard's trademark notice.
- **Avoid:** logos, key art, Friz Quadrata (the game's interface lettering) and Morpheus (its quest-header lettering), official frames, copied layouts. **Fine in practice:** your own screenshots, icons from the client via tooltips, item-quality colours, class colours.
