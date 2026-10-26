# Source record: world topics and More lists (research agent, 27 Oct 2026)

Pages: `content/world/` and `content/more/`. The agent's own report, kept as written; every page passed the site's header and section checks before commit, and the full build and site check passed with them.

All 11 pages are written. The build's own loader (`load_content`) accepts all 77 content pages, and every `ledger:` link points at a page that exists. Nothing is committed and I closed my browser tab. I did not run the full build or `check_site.py`.

**Files** (all under `/Users/faresb/Documents/Dev/FvrRepo/content/`):
- world/camping.md, legacy.md, merchants-favor.md, rares.md, zones.md, dungeons-and-raids.md, collections.md
- more/addons.md, known-issues.md and macros.md (rewritten), launch.md (new)

All use the four standard sections; launch.md's checklist items are ### headings, as you asked.

**Sources read:**
- **Blizzard:** the news articles on camping, raids, dungeons, Legacy, rulesets, names, the Darkspear Islands, the What's Next and Deep Dive recaps, and Carve a New Path. Forum JSON: the known-issues thread, development notes (including the 26 Oct racial changes), the RMT/economy-hold posts, the Mac thread and other player threads.
- **ForeverDB:** llms-full, camping, legacy, rares, mounts, titles, pets, veterans, launch pages, reputation, lore, addons and macros.
- **In the browser:** Icy Veins (dungeons overview, 14 dungeon guides, camping, legacy, raids, zones, news), Wowhead (camping, Legacy, zones, dungeons, raids, mounts, pets, the Azeroth Commerce Authority guide, macros) and CurseForge (Forever filter, checked 26 Oct).
- **Others:** wow-professions.com, Warcraft Tavern, Method, foreverchanges.pro, mmonster.co (a boosting site, used only for the WeakAuras and TSM status) and Kami Labs.
- **Not read:** Mobalytics.

**Claims I'm unsure about:**
- The launch-time table rows other than PST and UTC are my own conversions; the page says so.
- Several statuses on known-issues.md are beta-era player reports with no launch confirmation.
- ClassicUI Forever has more than one project on CurseForge under similar names, each claiming to be the real one.

**Where sources disagree** (each is flagged on its page):
- **Campfire skill levels:** Wowhead and Icy Veins say 90/200, ForeverDB and Warcraft Tavern say 140/220. wow-professions.com explains it: you learn the blueprint at the lower skill and use the kit at the higher one.
- **Arcane Salvager blueprint:** Icy Veins says Rath'mael drops it, wow-professions.com says Shade of the Archmage.
- **Legacy totals:** Blizzard says 65 challenges, ForeverDB counts 81. Wowhead gives Performance Bonus and Luremaster 5 ranks; other sources give 3 and 2.
- **New dungeon levels:** Blizzard's ranges are narrower than the client's. Boss names also differ: Magmatus vs Infurnus, The Baron vs The Butcher, and Chillhowl vs Deepscar Matriarch in the Barrow Deeps.
- **Rend in the Horde Onyxia attunement:** Blizzard's guide places him in Lower Blackrock Spire; in Classic he's in the upper spire.
- **Zone positions:** sources place Shen'dralas and the Riverglades slightly differently.
- **Addon settings resetting:** foreverchanges.pro says it was fixed in the 24 Sept build; an addon author reported it still broken on 7 Oct.

**Corrections to the old pages:**
- The "-forever" file-name tip was wrong. Questie, DBM, Details! and Auctionator ship one download tagged for Forever and other versions, so the page now says to filter by flavour instead.
- The Mac "Secondary Lighting Fair" fix didn't work for some players.
- TSM still has no Forever version on CurseForge.
- ElvUI supports Forever only in its GitHub development version, not the Tukui release.
- A Blizzard article says "3:00 p.m. PDT" where it means PST.
- ForeverDB's rare and pet pages disagree on which of Gorefang and The Rake players have seen in Forever.
