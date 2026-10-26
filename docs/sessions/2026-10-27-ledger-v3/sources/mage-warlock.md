# Source record: Mage and Warlock pages (research agent, 27 Oct 2026)

Pages: `content/classes/mage/` and `content/classes/warlock/`. The agent's own report, kept as written; every page passed the site's header and section checks before commit, and the full build and site check passed with them.

All 12 pages are written and pass the site's own content checks (header, the four sections in order, Markdown rendering, banned-word check). Nothing existed at these paths before. Nothing is committed.

**Files** (all in `/Users/faresb/Documents/Dev/FvrRepo/content/classes/`):
- `mage/`: overview.md, arcane.md, fire.md, frost.md, hybrid.md, macros.md
- `warlock/`: overview.md, affliction.md, demonology.md, destruction.md, hybrid.md, macros.md

**Sources read, all pages:**
- Blizzard's class deep dives for Mage and Warlock (the full articles).
- ForeverDB: class, PvE, talents, builds and macros pages, both levelling guides, and the articles on builds 70425 and 70532, the Mage hotfix report and the hybrid tax.
- Icy Veins: all six spec guides, all six levelling pages and both class overviews.
- Wowhead: Mage overviews plus level 20 and 30 pages; for Warlocks, the overview, talent builds and levelling pages updated 26 October; the macro guide.
- WoWSims: presets.ts, every Mage rotation list and Warlock build file. I decoded the talent strings against WoWSims' tree files and looked up the spell IDs on ForeverDB.
- Kami Labs macro tool.
- Nothing was unreadable, but Wowhead's embedded talent calculators loaded broken and Icy Veins' Arcane levelling calculator showed an invalid 52-point build, so I used their text instead.

**Claims I'm unsure about:**
- Pet scaling with gear and which spells cost Soul Shards: the guides say so, but the client files don't show it.
- Arcane Wrath's cast time and cooldown come from Wowhead only.

**Contradictions between sources (flagged on the pages):**
- **Ice Lance:** the guides say +300% against frozen targets; the current client files say +200%.
- **Elemental Precision and Piercing Ice:** the client still has 5 ranks and Piercing Ice. WoWSims and Icy Veins' calculator show 3 ranks and no Piercing Ice, which matches a single unconfirmed player report of a hotfix.
- **Arcane Blast:** the client was reworked on 16 October. Older guides say to dump stacks with Fire Blast; Wowhead's 21 October overview and the WoWSims rotations keep the stacks running.
- **Outdated advice in guides:**
  - Icy Veins' Fire pages still use "Hot Streak" and "Wake of Fire".
  - Malediction (now renamed Grim Reach) is still cited by Icy Veins and ForeverDB.
  - The WoWSims rotations use the old trainer version of Arcane Wrath, which the live client no longer teaches.
- **Smaller disagreements:**
  - Racials: Wind Blessed, Ruthless, Eureka!, Touch of the Grave and Shatter Curse.
  - Teleport: Dalaran: level 40 or 50, and Alliance-only or both factions.
  - Whether spell damage still boosts wands.
  - Felsteed: trainer spell or class quest.
  - Kami Labs' cast sequence includes Corruption, which ForeverDB warns can break the sequence.
- **The hybrid tax doesn't apply to these classes:** Mage and Warlock are pure classes. The ~5% target is aimed at classes that can fill more than one role, not at builds that mix talent trees. The hybrid pages say so.

**For you:** the site doesn't render "Read more" for the hybrid and macros pages (scripts/sections.py), so I linked their sources inline as well. Most "What the guides say" sections run 850–970 words, slightly over the 900 aim.
