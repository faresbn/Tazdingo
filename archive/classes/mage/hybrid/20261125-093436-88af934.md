---
updated: 2026-10-27
summary: Mage builds that mix Arcane, Fire and Frost talents in WoW Forever: the levelling dips the guides suggest, the simulators' level 60 hybrids, and why the hybrid tax doesn't apply.
sources: Icy Veins, Wowhead, WoWSims presets, Blizzard class deep dive, ForeverDB
---

## Cheatsheet

- **Why mixing is easy:** You get one point per level from 10, and a row opens once you have 5 points in the rows above it in the same section, so a few points elsewhere cost little ([ForeverDB](https://foreverdb.net/class/Mage/talents)).
- **The common levelling dip:** Two points in [Missile Barrage](https://foreverdb.net/spell/400588), now in Arcane's first row. Icy Veins takes it in its Frost and Fire builds.
- **The wand phase:** Two points in Wand Specialization (Arcane) early on, then a respec once your spec's key talents arrive (Wowhead, Icy Veins).
- **Frostfire:** [Frostfire Bolt](https://foreverdb.net/spell/401502) at 40 benefits from both Fire and Frost talents, which Blizzard says was the point.
- **The simulators:** All five WoWSims Mage presets at 60 spend points in at least two sections.
- **Hybrid tax:** It doesn't apply. Mages are a pure class, and the tax is about classes that can fill more than one role, not about mixing trees.
- **Respeccing:** At a class trainer in a capital city; dual specialisation opens at 40 (Blizzard).

## What the guides say

### Tazdingo recommendation

Take an early wand or Missile Barrage dip when it improves the spells you actually use, and account for the later Frost or Fire milestone it delays. Frostfire Bolt is a level-40 option, not a level-30 levelling spell. Compare deep Fire and Frostfire at equal gear, level and target conditions; their level-60 presets cannot settle an early questing choice. Mixing Mage trees does not incur the hybrid damage target.

### Levelling hybrids

- **Frost with Missile Barrage.** The [Icy Veins Frost levelling build](https://www.icy-veins.com/wow-forever/frost-mage-leveling) puts levels 21 and 22 into Missile Barrage, so Frostbolt can proc free, fast Arcane Missiles that cut drinking. Later it adds Incineration from Fire (around 46–50), and Arcane Focus and Arcane Subtlety near 60. Icy Veins also suggests an alternative: play Arcane with Missile Barrage and Wand Specialization early, then respec into Frost from level 22.
- **Fire into Frost.** The [Icy Veins Fire levelling build](https://www.icy-veins.com/wow-forever/fire-mage-leveling) goes into Frost after Combustion at 40: Elemental Precision, Improved Frostbolt, Ice Shards, Frostbite, Permafrost, Ice Block and Shatter, ending at 32 Fire and 19 Frost. Its reason is Frostfire Bolt, which replaces Fireball at 40 and gains from Ice Shards and Shatter.
- **Arcane with Fire dips.** Icy Veins' [Arcane levelling page](https://www.icy-veins.com/wow-forever/arcane-mage-leveling) takes Incineration for Arcane Blast crit and the old Wake of Fire, now Improved Fire Blast. It says Frost only adds defence for Arcane.
- **Wands first.** Wowhead's level 20 and level 30 guides start Frost and Arcane with Wand Specialization, then respec once Ice Lance or Arcane Blast takes over ([Level 30 Arcane](https://www.wowhead.com/forever/guide/classes/mage/arcane/level-30-dps-overview)). ForeverDB notes that Blizzard set the 1 silver respec price for the beta only, so the launch price may differ.
- **Single-section builds.** ForeverDB's published levelling builds keep every point in one section up to 30 ([ForeverDB](https://foreverdb.net/guide/leveling-mage)).

### Level 60 hybrids (projections)

Every WoWSims Forever preset mixes trees ([presets](https://github.com/wowsims/forever/blob/master/ui/specs/mage/dps/presets.ts)). The beta stopped at 30, so treat these as theory.

| Preset | Arcane / Fire / Frost | Points outside the main section | Filler |
|---|---|---|---|
| Arcane Frost (the default) | 37 / 3 / 11 | Incineration 3; Improved Frostbolt 5, Elemental Precision 3, Ice Shards 3 | Frostbolt |
| Arcane Fire | 32 / 16 / 3 | Improved Fire Blast, Incineration, Ignite, Burning Soul, Pyroblast, Heating Up; Elemental Precision 3 | Scorch, with Fire Blast and Pyroblast |
| Fire | 16 / 32 / 3 | Arcane Focus, Missile Barrage, Arcane Subtlety, Arcane Concentration, Arcane Blast, 1 point of Arcane Meditation; Elemental Precision 3 | Fireball |
| FFB | 0 / 29 / 22 | Elemental Precision, Ice Shards, Frost Channeling, Ice Lance, Ice Block, Shatter, Fingers of Frost and more | Frostfire Bolt |
| Frost | 19 / 0 / 32 | Arcane Focus, Missile Barrage, Arcane Subtlety, Arcane Concentration, Arcane Blast, Arcane Meditation | Frostbolt |

Why these mixes work, according to the sources:
- **Missile Barrage** procs from Fireball, Frostbolt, Frost Blast and Frostfire Bolt as well as Arcane Blast ([ForeverDB talent list](https://foreverdb.net/class/Mage/talents)), so Fire and Frost builds get free Arcane Missiles.
- **Arcane Blast's stacks** add spell damage that helps your other spells, so the simulator's Fire and Frost rotations keep one to three stacks rolling.
- **Incineration** in Fire's first row raises Ice Lance and Arcane Blast crit as well as Fire Blast and Scorch.
- **Frostfire Bolt** takes the higher of your Fire or Frost spell damage. Blizzard's own example pairs Ignite with Ice Shards, so a Frostfire crit deals 200% damage plus another 40% of that as Ignite, 280% in total ([Blizzard](https://worldofwarcraft.com/en-us/news/24302097)).

Wowhead's [Fire overview](https://www.wowhead.com/forever/guide/classes/mage/fire/overview-pve-dps) compares the Frostfire hybrid, which skips both capstones and the Arcane tree, with deep Fire. It says Frostfire needs less gear to do well early but scales less, while deep Fire needs more gear but feels more consistent. It doesn't yet know which will be best.

### The hybrid tax

On episode 2 of the WoW: Forever Podcast, the developers said they aim for hybrid damage specs to deal about 5% less damage than the pure classes: Hunters, Mages, Rogues and Warlocks ([ForeverDB](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)). It is a design target from a video, not a number in the client or the patch notes. It applies to classes that can fill more than one role, such as Warriors, Druids and Shaman. Mages set the bar rather than pay it. None of the sources mention any penalty for spreading a Mage's points across sections.

## Field findings

Nothing recorded yet.

## Read more

- [Icy Veins: Frost Mage levelling](https://www.icy-veins.com/wow-forever/frost-mage-leveling): the Missile Barrage dip and the Arcane-first alternative
- [Icy Veins: Fire Mage levelling](https://www.icy-veins.com/wow-forever/fire-mage-leveling): the Fire into Frost path for Frostfire Bolt
- [Icy Veins: Arcane Mage levelling](https://www.icy-veins.com/wow-forever/arcane-mage-leveling): Arcane's Fire dips
- [Wowhead: Fire Mage overview](https://www.wowhead.com/forever/guide/classes/mage/fire/overview-pve-dps): deep Fire against the Frostfire hybrid
- [Wowhead: Level 30 Arcane Mage](https://www.wowhead.com/forever/guide/classes/mage/arcane/level-30-dps-overview): Wand Specialization early, then respec
- [WoWSims Forever: Mage presets](https://github.com/wowsims/forever/blob/master/ui/specs/mage/dps/presets.ts): the five level 60 hybrid builds
- [Blizzard: Class Deep Dives, Mage and Shaman](https://worldofwarcraft.com/en-us/news/24302097): Frostfire Bolt and its hybrid example
- [ForeverDB: The hybrid tax in WoW Forever](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): who counts as a hybrid and what the 5% means
