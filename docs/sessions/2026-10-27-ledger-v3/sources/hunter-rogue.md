# Source record: Hunter and Rogue pages (research agent, 27 Oct 2026)

Pages: `content/classes/hunter/` and `content/classes/rogue/`. The agent's own report, kept as written; every page passed the site's header and section checks before commit, and the full build and site check passed with them.

All 12 pages are written. Your commit 995a375 already picked most of them up. My last pass is still uncommitted: 9 lines across 7 files, mostly extra Read more entries, plus Blizzard removed from combat.md's sources line because that page never cites it. Nothing else in the repo was touched, and nothing existed at these paths before I started.

**Files** (all under /Users/faresb/Documents/Dev/FvrRepo/content/classes/)
- hunter/: overview.md, beast-mastery.md, marksmanship.md, survival.md, hybrid.md, macros.md
- rogue/: overview.md, assassination.md, combat.md, subtlety.md, hybrid.md, macros.md

**Sources read** (no site blocked me)
- **Wowhead:** the overview, Level 20 and Level 30 pages for all six specs, plus the macro guide.
- **Icy Veins:** all six spec guides and all six levelling pages. Their talent orders by level are decoded from the calculator links.
- **ForeverDB:** class, builds, talents, changes, PvE, levelling, poisons and macros pages for both classes; the hybrid-tax, deep-dive, WillE and 16 October build articles; and its digest.
- **WoWSims:** presets.ts, spec.ts, all five Hunter APLs, the Rogue APL, and its talent-tree files, which I used to decode the preset talent strings.
- **Others:** Blizzard's Hunter/Druid and Rogue/Warlock deep-dive articles, and Kami Labs' macro tool and article.
- Not used: Method, Warcraft Tavern and Mobalytics.

**Claims I'm unsure of**
- Wowhead's pet-scaling numbers, smooth Energy regeneration, combo points staying on a target, and poisons scaling with attack power. These are server rules the client can't confirm, and the pages say so.
- My own decoding of the Icy Veins and WoWSims talent strings. Every result fits the tree's prerequisites, but the position-to-talent mapping is my reading.
- Everything at level 60 is projection: WoWSims gear is marked dev-only, and Icy's paths beyond 30 are untested.

**Contradictions between sources** (all flagged on the pages)
- **Human and Orc crit racials:** Icy and Wowhead's Hunter pages still tie them to swords and axes. The 16 October build made both flat.
- **Trueshot Aura:** Wowhead says 50 for the party; the client says 30 for party or raid.
- **Sniper Shot:** Icy says a 4-second cooldown; Blizzard and the client say a 4-second cast and a 15-second cooldown.
- **Survival weaving:** Icy's main guide says hunters no longer weave; Wowhead, Icy's levelling page and the WoWSims default all weave.
- **Expose Prey:** Wowhead gives 5 seconds; the client tooltip says 10.
- **Poison duration:** Icy says 1 hour per coat; the client says 30 minutes.
- **ForeverDB's simulator against the written guides:** it uses Multi-Shot on single targets, builds with Backstab rather than Mutilate at 30, and finds Combat does better without Slice and Dice.
- **ForeverDB against itself:** Deflection is "up to 10%" in one place and 5% in another; Dismember's numbers differ; and one page calls poisons unconfirmed while another names the quest.
- **Kami Labs errors:** it lists Aspect of the Viper (an unused Season of Discovery leftover), describes Disengage as a leap, and calls Mutilate level 60.
- **WoWSims:** its notes say Mutilate isn't automated, yet the APL file includes it.
- **Icy Combat:** its level 30 calculator doesn't match its text by one point.
