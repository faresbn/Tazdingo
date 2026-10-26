---
updated: 2026-10-27
summary: The Rogue talent builds that mix trees in WoW Forever, from Wowhead's dagger split at level 20 to the level 60 projections, and why Blizzard's hybrid tax doesn't touch them.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets, Blizzard class deep dive
---

## At a glance

- **Why mixing is common:** One talent point per level from 10 to 60 (51 in all), and each row needs 5 more points in that tree. At the level 30 cap you have 21 points, and every Rogue tree has cheap, strong talents near the top.
- **The usual borrowed talents:** Combat's Improved Eviscerate, Improved Sinister Strike, Puncturing Wounds and Precision; Assassination's Malice, Ruthlessness, Relentless Strikes and Improved Slice and Dice; Subtlety's Opportunity.
- **The dagger split:** Puncturing Wounds sits in Combat's second tier and Opportunity in Subtlety's first, so a dagger Backstab build crosses trees in any spec.
- **Legacy points:** The account-wide Legacy perk Talented gives up to five extra points early. Wowhead often spends them in a second tree.
- **Hybrid tax:** Doesn't apply. Blizzard's roughly 5% damage gap is aimed at hybrid classes, and Rogues are one of the four pure classes that set the bar.
- **Respecs:** 1 silver during the beta if you haven't reset recently (launch price unknown). Dual Specialization opens at level 40 (Blizzard).

## What the guides say

### The hybrid tax, briefly

Blizzard said on its podcast that hybrid damage specs should deal about 5% less than Hunters, Mages, Rogues and Warlocks. It defined a hybrid as a class that can fill more than one role ([ForeverDB](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)). That's about classes, not talent mixes, so a split Rogue build pays nothing. The figure is a design target, not a number in the client.

### Levelling hybrids

**Wowhead's dagger split (level 20).** Wowhead's [Assassination](https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-20-dps-overview), [Combat](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-20-dps-overview) and [Subtlety](https://www.wowhead.com/forever/guide/classes/rogue/subtlety/level-20-dps-overview) pages all offer the same 0/9/2 Backstab build. In Combat it takes Improved Eviscerate 3, Improved Sinister Strike 2, Puncturing Wounds 3 and Precision 1; in Subtlety, Opportunity 2. Wowhead says Puncturing Wounds brings Backstab's effective cost down to about 41 Energy, level with Sinister Strike, and Improved Sinister Strike covers the times a mob turns to face you.

**Other Wowhead splits.** The level 20 Combat sword build is 3/8/0: Malice 3 with Combat's core, or Remorseless Attacks 2 and Malice 1 when soloing. The Subtlety Ambush build is 1/2/8: Malice 1, Improved Sinister Strike 2, Master of Deception 3, Opportunity 2 and Improved Ambush 3. At 30, "Relentless Strikes Combat" is 13/8/0, with Malice 5, Ruthlessness 3, Murder 1, Improved Slice and Dice 3 and Relentless Strikes, plus Improved Eviscerate, Improved Sinister Strike and Precision. With Legacy points, Wowhead's Assassination build adds Improved Eviscerate 3 and Opportunity 2 (21/3/2), and its dagger Blade Flurry build adds Opportunity 2.

**Icy Veins' paths to 60.** Each Icy Veins levelling page completes one tree, then spreads into the others:

| Spec | Path | At 60 |
|---|---|---|
| [Assassination](https://www.icy-veins.com/wow-forever/assassination-rogue-leveling) | Venom at 40, then Opportunity, Improved Eviscerate, Lightning Reflexes, Puncturing Wounds, Precision, Vile Poisons and Murder | 38/11/2 |
| [Combat](https://www.icy-veins.com/wow-forever/combat-rogue-leveling) | Adrenaline Rush at 40, then Malice, Ruthlessness, Murder, Relentless Strikes, Lethality, Cold Blood and Vile Poisons | 18/33/0 |
| [Subtlety](https://www.icy-veins.com/wow-forever/subtlety-rogue-leveling) | Hemorrhage at 30 and Preparation at 31, then Assassination's crit and Energy talents and Combat's Improved Eviscerate, Lightning Reflexes and Precision | 19/9/23 |

Icy Veins' Subtlety page also offers an early hybrid: take Improved Sinister Strike and Remorseless Attacks first, then reset at 30 for Hemorrhage.

**ForeverDB stays mostly pure to 30.** [ForeverDB's builds](https://foreverdb.net/class/Rogue/builds) are single-tree, except its level 20 Assassination PvP build, which borrows Combat's Improved Eviscerate. Its Combat group build notes that without a good dagger, Puncturing Wounds' three points are better spent on Malice in Assassination.

### Level 60 projections

The [WoWSims presets](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts) are all hybrids. The talent strings are decoded against the simulator's own Forever talent tree.

| Preset | Split | Notes |
|---|---|---|
| Combat SS (default) | 18/33/0 | Assassination to Cold Blood with two points of Improved Poisons; Combat to Adrenaline Rush, including Puncturing Wounds |
| Combat BS | 16/33/2 | Dagger version, with Subtlety's Opportunity |
| Asn Muti | 31/20/0 | Assassination to Venom; Combat to Dual Wield Specialization |
| Combat Muti | 21/29/1 | Mutilate plus Blade Flurry and Hack and Slash |
| Subtlety Hemo | 20/0/31 | Quietus and Thousand Cuts; Assassination to Cold Blood |
| Subtlety BS | 12/8/31 | Cutthroat and Thousand Cuts; Puncturing Wounds from Combat |

Every preset takes Malice, Ruthlessness, Improved Slice and Dice and Relentless Strikes from Assassination's first three tiers. Icy Veins' Combat path reaches the same 18/33/0 split with different points: Deflection, Riposte and Lethality instead of Puncturing Wounds, Improved Sprint and Improved Slice and Dice. These are projections with unconfirmed level 60 data.

### Where the guides disagree

- **Split early or stay pure:** Wowhead splits at 20 in every spec; ForeverDB and Icy Veins' main guides stay mostly in one tree until 30.
- **How far to go in Subtlety:** Icy Veins stops after Preparation while levelling, while both WoWSims Subtlety presets go all the way to Thousand Cuts at 60.

## Ledger findings

Nothing recorded yet.

## Read more

- [ForeverDB: The hybrid tax](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): what Blizzard said and which classes count as pure
- [Wowhead: Level 20 Assassination Rogue](https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-20-dps-overview): the 0/9/2 dagger split explained
- [Wowhead: Level 30 Combat Rogue](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview): Relentless Strikes Combat and the Legacy-point dagger build
- [Icy Veins: Subtlety Rogue levelling](https://www.icy-veins.com/wow-forever/subtlety-rogue-leveling): the three-tree levelling finish
- [Icy Veins: Assassination Rogue levelling](https://www.icy-veins.com/wow-forever/assassination-rogue-leveling): which Combat and Subtlety talents help Mutilate
- [ForeverDB: Rogue talent builds](https://foreverdb.net/class/Rogue/builds): single-tree builds with the reason for every point
- [WoWSims: Rogue presets](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts): the six level 60 builds
