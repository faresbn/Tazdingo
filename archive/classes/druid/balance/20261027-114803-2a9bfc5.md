---
updated: 2026-10-27
summary: How Balance Druid plays in WoW Forever: talents at 20, 30 and 60, the rotation in guides and in WoWSims, stats, gear and where sources disagree.
sources: ForeverDB (PvE guide, builds, simulator tips), Wowhead (overview, level 20 and 30 guides), Icy Veins, WoWSims presets and default APL, Blizzard class deep dive
---

## At a glance

- **Role:** ranged caster. [Starfire](https://foreverdb.net/spell/2912) and [Moonfire](https://foreverdb.net/spell/8921) deal Arcane damage; [Wrath](https://foreverdb.net/spell/5176) and [Insect Swarm](https://foreverdb.net/spell/5570) deal Nature damage.
- **How it plays:** keep Moonfire and Insect Swarm on the target and fill with Wrath and Starfire. From 30, [Eclipse](https://foreverdb.net/spell/408248) makes each Wrath speed up your next two Starfires. [Moonkin Form](https://foreverdb.net/spell/24858) arrives at 40.
- **Strengths:** group buffs, spot heals and crowd control. Moonkin Aura gives 3% crit to all spells and attacks for your party or raid within 45 yards, but doesn't stack with Leader of the Pack. Mark of the Wild, Faerie Fire and Rebirth come too.
- **Weaknesses:** mana limits you more than talents do. You have no interrupt and no area spell before [Hurricane](https://foreverdb.net/spell/17402) at 40, and levelling is slow.
- **Stats that matter:** hit, spell power, crit, then Intellect and Spirit at 20 to 30 ([ForeverDB](https://foreverdb.net/class/Druid/pve)). WoWSims' level 60 weights put hit first, with haste close behind spell power.
- **New in Forever:** Insect Swarm is now a Balance talent at 25, and Eclipse, [Nature's Splendor](https://foreverdb.net/spell/1223083), [Genesis](https://foreverdb.net/spell/1223081) and Nature's Majesty are new. [Improved Wrath](https://foreverdb.net/spell/16814) now halves Wrath's mana cost, and Hurricane has no cooldown.
- **Simulator:** WoWSims has a full Balance simulation with default talents and a priority list, tuned for level 60.

## What the guides say

### Levelling from 1 to 30

Wrath carries you until Starfire arrives at 20. Insect Swarm opens at 25, and Eclipse and [Nature's Grace](https://foreverdb.net/spell/16880) at 30. Wowhead's [level 20 guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-20-dps-overview) says Balance levels more slowly than in Classic and drinks more, so pull one mob at a time. Your weapon is the biggest upgrade, since caster weapons carry spell damage from level 10. High Order Skyborne get an easier ride from Read Leyline. Wowhead suggests other races might skip Improved Wrath, buy a good weapon and level partly in melee. It also rates "Spellbear" (Bear Form with spell power gear and Thorns) as the most comfortable way to level; see the hybrid builds page.

At 30, Wowhead's [level 30 guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-30-dps-overview) offers two styles. A damage over time build spreads Moonfire and Insect Swarm and lets Thorns and melee swings do the rest. A hard-casting build roots the target first, because nothing protects Wrath or Starfire from pushback yet.

### Talents

| Build (source) | Level | Points |
|---|---|---|
| Fast Wrath caster ([ForeverDB](https://foreverdb.net/class/Druid/builds)) | 20 | Improved Wrath 5, Moonglow 3, Nature's Majesty 2, Nature's Splendor 1 |
| Hard casting (Wowhead) | 20 | Improved Wrath 5, Nature's Reach 2, Moonglow 3, Nature's Majesty 1 |
| Root-and-nuke (ForeverDB) | 30 | Improved Wrath 5, Moonglow 3, Nature's Majesty 2, Nature's Reach 2, Improved Entangling Roots 3, Nature's Splendor 1, Insect Swarm 1, Improved Starfire 3, Nature's Grace 1 |
| Group caster (ForeverDB) | 30 | Improved Wrath 5, Moonglow 3, Improved Moonfire 2, Nature's Majesty 2, Nature's Reach 2, Nature's Splendor 1, Insect Swarm 1, Improved Starfire 4, Nature's Grace 1 |
| Hard casting (Wowhead) | 30 | Improved Wrath 5, Moonglow 3, Nature's Majesty 2, Nature's Reach 2, Improved Entangling Roots 3, Improved Starfire 5, Eclipse 1 |
| Damage over time (Wowhead) | 30 | Genesis 5, Nature's Majesty 2, Improved Moonfire 2, Moonglow 3, Nature's Splendor 1, Nature's Reach 2, Insect Swarm 1, Vengeance 4 |
| Levelling ([Icy Veins](https://www.icy-veins.com/wow-forever/balance-druid-ranged-dps-pve-guide)) | 30 | Improved Wrath 5, Nature's Reach 2, Moonglow 3, Improved Moonfire 2, Nature's Majesty 2, Nature's Splendor 1, Insect Swarm 1, plus Nature's Focus 5 (Restoration) |
| "Moonkin", WoWSims default ([presets.ts](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/presets.ts)) | 60 | 38 Balance down to Moonkin Form, with Eclipse 3, Vengeance 5, Improved Starfire 5, Moonfury 5 and Nature's Grace, but no Improved Entangling Roots or Overgrowth; 13 Restoration (Nature's Focus 5, Naturalist 5, Reflection 3) |

Wowhead's damage over time build spends only 20 of the 21 points. Every guide values Nature's Reach for its 4% hit, and ForeverDB and Wowhead point to higher-level dungeon bosses. Icy Veins notes that crit-based talents such as Vengeance are weak while levelling, when gear has little crit. ForeverDB takes Nature's Grace over Eclipse at 30 because it works off every crit. Wowhead says Eclipse is "somewhat muted" at 30 without Legacy points.

### Rotation: guides against WoWSims

The guides, at 20 to 30:

- **ForeverDB** (its own [simulator tips](https://foreverdb.net/class/Druid/guide)): keep Insect Swarm and Moonfire up at least 90% of the time, fill with Starfire, and spend Nature's Grace procs on Starfire. At 30 the simulated damage splits Starfire 66%, Moonfire 19% and Insect Swarm 15%. At 20 to 29 Wrath does 84%.
- **Wowhead** ([overview](https://www.wowhead.com/forever/guide/classes/druid/balance/overview-pve-dps)): precast Wrath, keep both damage over time spells up and alternate Wrath and Starfire under Eclipse, with Starfire as the main nuke. Use a downranked Moonfire or Insect Swarm while moving. On two to four targets, put both on two of them; from five, Hurricane. The level 30 hard-cast loop is Wrath, root, Starfire twice, then Wrath and two more Starfires.
- **Icy Veins:** Moonfire everything in combat with you, then Wrath, adding Insect Swarm after Moonfire from 25.

WoWSims' [default APL](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/apls/default.apl.json), for level 60:

1. Precast Wrath 1.5 seconds before the pull (when there are fewer than four targets).
2. Innervate yourself below 70% mana in a long fight, or below 40% mana with more than 30 seconds left.
3. Moonfire if it's missing.
4. Insect Swarm if it's missing.
5. Hurricane on four or more targets.
6. Starfire (rank 6) while Eclipse charges are up.
7. Otherwise Wrath.

At 60 the simulator treats Wrath as the filler and Starfire as the Eclipse payoff, which matches Wowhead's Wrath-into-Starfire pattern. ForeverDB's level 30 simulation, run on a build without Eclipse, fills with Starfire instead. The two disagree on when Hurricane pays: four targets in WoWSims, five in Wowhead.

### Stats, gear and consumables

- **Stats:** Starfire gets the full spell power coefficient (1.0) and Wrath rank 3 gets 0.571, so every point of spell power counts. WoWSims' [presets](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/presets.ts) weigh hit 1.45 to 1.48, haste 0.95 to 0.99, crit 0.76, Intellect 0.2 to 0.28 and Spirit 0 per point of spell power (1.0). School-specific spell power is worth 0.68 for Arcane and 0.32 for Nature.
- **Gear:** a caster weapon first. Leatherworking makes Stormrider's Leather Armor and Pants at 15 to 20, the Totemic Leather Helm at 25 and the Skycaller's Leather Belt at 30 ([ForeverDB levelling guide](https://foreverdb.net/guide/leveling-druid)). Wowhead adds Tailoring pieces and the Enchanting idol Mystic Mushroom, and suggests Skinning with Leatherworking.
- **Consumables:** ForeverDB's simulator ranks Lesser Arcane Elixir first at 30 (+6.5% damage), then Briny Seafood Stew (+6.1%). Icy Veins and Wowhead add Minor Arcane Elixir, wizard oils, spellblasting potions and plenty of water. WoWSims' level 60 defaults are Flask of Supreme Power, Greater Arcane Elixir, Brilliant Wizard Oil, Major Mana Potion, Demonic Rune and Lobster Stew.
- **Camping:** Wowhead notes the Skinning campsite's crit buff overlaps Moonkin Aura, and the Enchanting one overlaps Mark of the Wild.

### Where the guides disagree or are unsure

- **Improved Wrath first:** ForeverDB and Icy Veins take it first. Wowhead says races without Read Leyline may do better skipping it while levelling.
- **Wrath's damage:** Blizzard redesigned Wrath to be much cheaper but weaker, as its deep dive describes, and the 24 September beta notes raised its base damage by about 50%. ForeverDB says the client tooltips didn't show the raise. Blizzard expects the buff to add about 2% Druid damage at 60 and may trim something else to pay for it ([ForeverDB](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)).
- **Wowhead's abilities page** still carries Classic values: a 5% Moonkin crit aura, a 20 minute Rebirth and Nature's Grasp as a talent. The client says 3%, 30 minutes, and a trainer spell at 10.
- **Above 30:** Moonkin Form, Hurricane, Moonfury and the WoWSims numbers are untested projections on assumed level 60 gear.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Balance Druid guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-20-dps-overview): levelling advice, the 20 builds, dungeon drops and crafted gear
- [Wowhead: Level 30 Balance Druid guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-30-dps-overview): hard-cast, damage over time and Spellbear builds with rotations
- [Wowhead: Balance Druid abilities](https://www.wowhead.com/forever/guide/classes/druid/balance/dps-abilities): a tour of the spellbook (check numbers against the client)
- [ForeverDB: Druid PvE guide](https://foreverdb.net/class/Druid/pve): group role, opener, cooldowns and stat order at 20 to 30
- [ForeverDB: Druid talent builds](https://foreverdb.net/class/Druid/builds): every published Balance build, point by point
- [ForeverDB: Levelling a Druid to 30](https://foreverdb.net/guide/leveling-druid): spells by level and crafted gear
- [Blizzard: Class Deep Dives — Hunter and Druid](https://worldofwarcraft.blizzard.com/en-us/news/24301515): the official list of Balance talent changes
- [WoWSims: Balance presets.ts](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/presets.ts): default talents, stat weights and consumables at 60
- [WoWSims: Balance default APL](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/apls/default.apl.json): the simulator's priority list
