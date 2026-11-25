---
updated: 2026-10-30
summary: How Combat plays in WoW Forever up to the level 30 beta cap, with talents by level, the Sinister Strike and Backstab rotations, Blade Flurry, weapons and where the guides disagree.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and APL
---

## Cheatsheet

- **Pick it for:** the most forgiving Rogue leveller (ForeverDB): any one-handed weapon, no reliance on poisons or bleeds, and the only real Rogue cleave in Blade Flurry.
- **Levelling build:** at 30, Wowhead: Improved Eviscerate 3, Improved Sinister Strike 2, Precision 3, Deflection 3, Endurance 2, Riposte, Improved Sprint 1, Flawless Execution, Dual Wield Specialization 4, Blade Flurry ([Wowhead](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview)). ForeverDB and Icy Veins also reach Blade Flurry with Riposte; ForeverDB's group build swaps Riposte for Puncturing Wounds.
- **Build at 60:** projection only: WoWSims' default "Combat SS" is 18/33/0, down to Adrenaline Rush with Hack and Slash, Weapon Expertise and Aggression, plus Malice, Ruthlessness, Murder, Relentless Strikes and Cold Blood ([WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts)). "Combat BS" (16/33/2) is the dagger version; Icy Veins' route also ends 18/33/0.
- **Priority:** at 30 (Wowhead), Sinister Strike or Backstab, keep Slice and Dice up and refresh it late, Riposte when lit (Icy Veins), Blade Flurry on packs or bosses, then Eviscerate (low armour) or Rupture (high armour). At 60 WoWSims adds Adrenaline Rush, Thistle Tea and Blade Flurry recasts.
- **Stats:** main-hand weapon damage first (a slow weapon for Sinister Strike), then hit and expertise, Agility, crit, Strength. WoWSims' level-60 "Combat Sinister" weights: expertise 2.55, hit 2.42, Agility 1.96, haste 1.72, crit 1.70, attack power 1 ([WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts)).
- **Key levels:** 20 Riposte (Icy Veins) · 30 Blade Flurry and the Ruby-Adorned Blade from The Eye of Bhossca · 40 Adrenaline Rush.
- **Gear and consumables:** a slow axe, mace, sword or fist main hand early; a main-hand dagger only for the Backstab build. Wowhead rates the Ruby-Adorned Blade best at 30 ([Wowhead](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview)). Instant Poison plus a Rough Sharpening Stone; ForeverDB's sim rates Elixir of Agility and Tender Wolf Steak highest.
- **Watch out:** never press Blade Flurry next to a Sapped or Gouged mob ([ForeverDB](https://foreverdb.net/class/Rogue/pve)). ForeverDB's sim did 2.7% more on one target without Slice and Dice at 30, but flags it for testing and every written guide keeps it. Puncturing Wounds needs a main-hand dagger.

## What the guides say

### Tazdingo recommendation

Use **Sinister Strike with a strong slow main hand for straightforward solo play**; a dagger/Backstab build is worthwhile when you can reliably attack from behind. Choose Riposte for enemies attacking you, while a dungeon damage build can spend those points elsewhere. Keep Slice and Dice when enough fighting remains to repay it, including the next mob; finish a nearly dead target directly when that is better. A model's small gain from dropping the buff is a test hypothesis, not enough to overturn the written guides ([Wowhead](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview)). Blade Flurry is valuable cleave only when the second target is safe to hit.

### What changed

Hack and Slash's bonus follows your weapon: swords and axes get a 5% chance of an extra attack, daggers and fist weapons 5% crit, and maces ignore 15% of armour. You no longer need to respec when you swap weapon type ([ForeverDB changes](https://foreverdb.net/class/Rogue/changes); Wowhead). Puncturing Wounds (tier 2) gives Backstab 30% more crit and a 45% chance of a second combo point, which makes dagger Combat a real option. Wowhead reckons that brings Backstab's effective cost to about 41 Energy, level with Sinister Strike.

### Talents by level

| Level | ForeverDB levelling build | Icy Veins | Wowhead |
|---|---|---|---|
| 10–20 | Improved Eviscerate 3, Improved Sinister Strike 2, Lightning Reflexes 2, Precision 3, Endurance 1 | Improved Sinister Strike 2, Improved Eviscerate 3, Precision 2, Deflection 3, Riposte at 20 | Sword: Improved Eviscerate 3, Improved Sinister Strike 2, Precision 3, Malice 3 (or Remorseless Attacks 2 and Malice 1 solo). Dagger: 0/9/2 with Puncturing Wounds and Opportunity |
| 21–30 | Deflection 3, Endurance 2, Riposte, Flawless Execution, Dual Wield Specialization 3, Blade Flurry | Precision 3, Endurance 2, Lightning Reflexes 1, Flawless Execution, Dual Wield Specialization 4, Blade Flurry | Improved Eviscerate 3, Improved Sinister Strike 2, Precision 3, Deflection 3, Endurance 2, Riposte, Improved Sprint 1, Flawless Execution, Dual Wield Specialization 4, Blade Flurry |
| 31–60 | Not covered | Hack and Slash 5, Weapon Expertise 2, Aggression 3, Adrenaline Rush at 40, Dual Wield Specialization 5, then Malice, Ruthlessness, Murder, Relentless Strikes, Lethality, Cold Blood and Vile Poisons (18/33/0) | Not covered |

For 21–30, the ForeverDB and Icy Veins cells list the points added after 20. Wowhead's level 30 build is shown in full, because it leaves its level 20 builds behind.

[ForeverDB's group build](https://foreverdb.net/class/Rogue/builds) drops Riposte, since you stand behind mobs, and takes Puncturing Wounds for a main-hand dagger. Wowhead's alternative "Relentless Strikes Combat" at 30 is a 13/8/0 split (see [Hybrid builds](hybrid.md)). For Legacy points, Wowhead and Icy Veins both put the extras into Hack and Slash.

[WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts) defaults to "Combat SS" at 60 (18/33/0). It takes Assassination's Malice, Ruthlessness, Murder, Improved Slice and Dice, Relentless Strikes, Cold Blood and two points of Improved Poisons, then Combat down to Adrenaline Rush with Puncturing Wounds, Improved Sprint, Hack and Slash, Weapon Expertise and Aggression. "Combat BS" (16/33/2) is the dagger version, with two points of Opportunity.

### Rotation and priorities

- **Icy Veins:** Instant Poison on both weapons. Open from Stealth with Ambush (dagger) or Garrote, use Blade Flurry early and often, Riposte whenever it lights up, then Backstab from behind with a dagger or Sinister Strike otherwise. At 5 points, Slice and Dice if the target will outlive it, otherwise Eviscerate. Its [levelling page](https://www.icy-veins.com/wow-forever/combat-rogue-leveling) opens with Cheap Shot on mobs that can be stunned.
- **Wowhead ([level 30](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview)):** Backstab or Sinister Strike, keep Slice and Dice up and refresh it as late as possible. Expose Armor for physical groups, and Blade Flurry with high Energy on packs or bosses. Spend spare points on Eviscerate against low armour and Rupture against high armour.
- **ForeverDB:** Spend the first 1–2 points on Slice and Dice on longer fights, then Eviscerate at 5. Never press Blade Flurry next to a Sapped or Gouged mob, because the extra hits break it ([PvE guide](https://foreverdb.net/class/Rogue/pve)).
- **WoWSims, level 60 ([default APL](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/apls/default.apl.json)):** Before the pull, Blade Flurry and Stealth. Open with Garrote, and Vanish to open again. Pair Adrenaline Rush with Blood Fury or Elune's Light, and drink Thistle Tea when Energy runs low. Recast Blade Flurry unless Slice and Dice is about to drop, and reapply Slice and Dice once it falls off. Use Cold Blood before a 5-point Eviscerate, and Eviscerate at 5 points (or 4 if Slice and Dice has 6 seconds or less left). The builder is Sinister Strike, or Backstab when the "Use Backstab" option is on.

### Weapons and levelling

Wowhead's levelling tip is to get a slow axe, mace, sword or fist weapon early and train the matching weapon skill. ForeverDB recommends any one-handed weapon for Combat and a main-hand dagger only for the dagger build. Puncturing Wounds does nothing without one. Icy Veins' Combat levelling guide treats Riposte (20) and Blade Flurry (30) as the big power spikes; pair Blade Flurry with Evasion when two mobs are on you.

### Gear and consumables

Icy Veins' level 30 list starts with the Ruby-Adorned Blade from the Stealth quest The Eye of Bhossca, Bloody Brass Knuckles for the off hand, and Leatherworking pieces. Wowhead rates the Ruby-Adorned Blade the best weapon at 30. Poisons and stones stack, so carry [Rough Sharpening Stone](https://foreverdb.net/item/2862) alongside Instant Poison. ForeverDB's simulator rates [Elixir of Agility](https://foreverdb.net/item/8949) and [Tender Wolf Steak](https://foreverdb.net/item/18045) at about 3.2% each. WoWSims' level 60 defaults add [Thistle Tea](https://foreverdb.net/item/7676), weightstones and sharpening stones on top of poisons.

### Where the guides disagree

- **Slice and Dice at 30:** ForeverDB's simulator did 2.7% more damage on one target without it and flags the result for testing. Every written guide, ForeverDB's included, keeps it up.
- **Sword or dagger:** ForeverDB's simulator builds with Backstab at 30, Icy Veins and ForeverDB's levelling build favour Sinister Strike, and Wowhead offers both.
- **Riposte or not:** in the solo builds (ForeverDB, Icy Veins, Wowhead) but dropped from ForeverDB's group build and the WoWSims presets.
- **Icy Veins' level 30 calculator** puts a point in Improved Sprint where its text says Lightning Reflexes. Its levelling page uses Lightning Reflexes.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Combat Rogue](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-20-dps-overview): sword and dagger builds at 20
- [Wowhead: Level 30 Combat Rogue](https://www.wowhead.com/forever/guide/classes/rogue/combat/level-30-dps-overview): Blade Flurry builds and Legacy-point variants
- [Icy Veins: Combat Rogue levelling](https://www.icy-veins.com/wow-forever/combat-rogue-leveling): talent order to 60 and the levelling rotation
- [ForeverDB: Rogue talent builds](https://foreverdb.net/class/Rogue/builds): Riposte, group and PvP Combat builds
- [ForeverDB: Rogue PvE guide](https://foreverdb.net/class/Rogue/pve): group duties, cooldowns and simulator tips
- [WoWSims: Rogue default APL](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/apls/default.apl.json): the level 60 priority list
- [WoWSims: Rogue presets](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts): Combat builds, stat weights and consumables
