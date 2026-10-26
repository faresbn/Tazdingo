# Source record: Warrior and Paladin pages (research agent, 27 Oct 2026)

Pages: `content/classes/warrior/` and `content/classes/paladin/`. The agent's own report, kept as written; every page passed the site's header and section checks before commit, and the full build and site check passed with them.

All 12 files are written and nothing was committed. I checked first and none of the target paths existed.

**Files** (all under `/Users/faresb/Documents/Dev/FvrRepo/content/classes/`):
- `warrior/`: overview, arms, fury, protection, hybrid, macros
- `paladin/`: overview, holy, protection, retribution, hybrid, macros

`git status` shows the warrior files as *modified*, so it looks like an earlier draft was committed while I was working. The current files are final.

**Your macros correction:** both macros pages are now a short selection with credits, not near-complete copies. Warrior has 19 macros (ForeverDB 9 of its 17, Kami Labs 5, Wowhead 3, Icy Veins 2). Paladin has 16 (ForeverDB 7 of its 19, Kami Labs 6, Icy Veins 1, Wowhead 1). Each has a one-line description in my own words and an "untested in the live game" note.

**Sources read, all pages:**
- Blizzard's Warrior and Paladin deep dives and its 2 October Warrior notes.
- ForeverDB class, PvE, builds, talents, changes and macros pages, both levelling guides, the hybrid-tax article and the Paladin 15 October article.
- WoWSims `presets.ts` and APLs for all six specs. I decoded the talent strings against WoWSims' own tree files.
- Wowhead: all six overviews plus their Level 20 and 30 pages, and the macro guide.
- Icy Veins: all six spec guides and all six levelling pages, with talents sampled at levels 20–60.
- Kami Labs' macro tool.

I didn't read Method, Warcraft Tavern or Mobalytics. Every site I needed was readable.

**Claims I'm unsure of:**
- WoWSims builds and weights are level-60 projections on placeholder gear. Holy has no simulation in WoWSims at all, only a gear planner.
- Icy Veins' 27% off-hand miss figure isn't confirmed anywhere else.
- Vanguard Charge macros: ForeverDB says edit the stance condition; Icy Veins says shift-click the separate Charge spell.

**Contradictions between sources** (all flagged on the pages):
- **Righteous Fury:** 90% in the client and Blizzard's 15 October notes. ForeverDB's guide pages still say 60%.
- **Flash of Light vs Holy Light:** Wowhead and Icy Veins make Flash of Light the main heal. ForeverDB's client numbers say Holy Light is more efficient.
- **Talent numbers:** Blizzard's text conflicts with client tooltips for Champion of the Light (30% vs 60%), Iron Creed (15% vs 25%) and Protection Shield Specialization (6% vs 4%).
- **Slam:** Icy Veins' main Arms page says level 30; the client says 20. Wowhead's overview has the old 15 sec cooldown.
- **Outdated pages:** Wowhead's Fury overview predates the October Rage changes.
- **Sunder Armor threat:** Wowhead says it's too low to tab-Sunder; ForeverDB says Blizzard fixed it.
- **Icy Veins' own calculators:** the "level 30" Holy and Protection Paladin builds spend 25–26 points, and the Protection Warrior text mentions Defiance but the calculator leaves it out.
- **Spearing Strike dismount:** ForeverDB's builds page and talent page disagree.
- **Bloodrage:** the current client tooltip no longer says it puts you in combat.

Spec pages run about 960–990 words counting table markup, slightly over the 900 target.
