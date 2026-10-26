# Source record: Priest and Shaman pages (research agent, 27 Oct 2026)

Pages: `content/classes/priest/` and `content/classes/shaman/`. The agent's own report, kept as written; every page passed the site's header and section checks before commit, and the full build and site check passed with them.

I've written all 12 pages: six for Priest and six for Shaman. Nothing existed at those paths beforehand, and nothing was committed.

**Files**
- /Users/faresb/Documents/Dev/FvrRepo/content/classes/priest/ — overview.md, discipline.md, holy.md, shadow.md, hybrid.md, macros.md
- /Users/faresb/Documents/Dev/FvrRepo/content/classes/shaman/ — overview.md, elemental.md, enhancement.md, restoration.md, hybrid.md, macros.md

**Sources read**
- **Wowhead:** all six spec overviews, all six Level 30 pages and the macro guide. Talent builds came from the embedded calculators where present. The Level 20 and Abilities pages were not read.
- **Icy Veins:** all six assigned spec guides. The calculator layout is dated 16 September, so point counts were cross-checked against each guide's text.
- **ForeverDB (curl):** Priest and Shaman class, PvE, talents and macros pages; both levelling guides; the Dwarf Shaman guide; the hybrid-tax article; the 16 October (70425) and live-client (70532) build articles; deep-dive, class-highlights and creator-check articles; the full plain-text digest.
- **Blizzard:** the Priest/Warrior and Mage/Shaman deep dives, and the race and class article.
- **WoWSims:** every presets.ts, the build/rotation files and talent trees. I decoded the talent strings myself. Restoration Shaman has no talents or rotation, and the healer Priest has no rotation.
- **Kami Labs:** the article and the macro tool page.
- Every site was readable.

**Shamans on both factions:** confirmed by Blizzard, ForeverDB and Wowhead. Dwarf is the only Alliance race; the Horde has Orc, Tauren, Troll and Windshaper Skyborne.

**Claims I'm unsure about**
- How Dwarf and Skyborne Shamans get their totem quests. Wowhead lists Alliance and Skyborne versions; ForeverDB couldn't confirm them in the client.
- Two-handed axes and maces: Blizzard says they're baseline, but ForeverDB can't see how they're taught.
- Skyborne Wind Blessed: 1% haste (ForeverDB, Wowhead's Restoration guide) versus 3% (Wowhead's Elemental and Enhancement guides).
- Icy's Discipline 21-point build skips Penance (16 Discipline / 5 Shadow), going by its calculator.
- Wowhead's Discipline calculator shows only 15 points and doesn't match its own text, so I used the text.

**Contradictions between sources**
- The 16 October build moved Lava Burst to tier 5 and brought back a redesigned Elemental Mastery. Blizzard's 7 October deep dive had said Elemental Mastery was removed.
- Icy says Lava Burst is out of reach at 30; Wowhead's 24 October build and the client have it.
- Older guides still name talents that no longer exist (Call of Thunder, Shadow Affinity). They also give old cooldowns: Devouring Plague 1 min (now 24 sec), Vampiric Embrace 1 min (now 30 sec), Shadow Word: Death 15 sec (now 18 sec).
- Wowhead says skip shielding Warrior and Druid tanks; Blizzard says absorbs no longer cut rage.
- Divine Grace and Contingency Plan: 5 min cooldown per Blizzard, 10 min in the client.
- ForeverDB's level 30 Shadow simulator says drop Devouring Plague and Mind Flay, against its own guide.
- Some Kami Labs macro descriptions don't fit Forever (Lava Burst guaranteed crit, Fire Nova centred on the Shaman). I flagged them on the macros pages.

**Housekeeping**
- Elemental and Enhancement run a little over 900 words in "What the guides say", mostly because of the tables.
- Early on I ran a text converter over the shared scratchpad folder `src/`. That rewrote other agents' `fdb-*.txt` files from their HTML, and I also wrote `scratchpad/scripts/h2t.py`. My own working files are in `scratchpad/ps/` and `scratchpad/ps-scripts/`.
