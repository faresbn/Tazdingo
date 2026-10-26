---
updated: 2026-10-27
summary: How Assassination plays in WoW Forever up to the level 30 beta cap, with talents by level, the Mutilate rotation, poisons, gear and where the guides disagree.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and APL, Blizzard class deep dive
---

## At a glance

- **Role:** Melee damage built on daggers and poisons.
- **How it plays:** Before 30 it plays like Combat (Wowhead). At 30, build with [Mutilate](https://foreverdb.net/spell/1310707): 60 Energy, both weapons, 2 combo points, 20% more damage on poisoned targets. Spend points on Slice and Dice and Eviscerate. From 40, Blizzard expects your finishers to keep Venom and Slice and Dice running.
- **Strengths:** A big power spike at 30, poison damage that ignores armour (Wowhead), sure crits from Cold Blood, and Seal Fate's extra combo points from 35.
- **Weaknesses:** Mutilate needs a dagger in each hand, enemies immune to poison or Nature blunt it, it's weak at 20, it brings no raid buff and, like every Rogue spec, it's limited by Energy.
- **Stats that matter:** Dagger damage (a high top end helps Mutilate), then hit and expertise, Agility, crit and Strength (Icy Veins). WoWSims' level 60 weights rate hit (2.80) and expertise (2.77) above Agility (2.06), with attack power as 1.
- **New in Forever:** Mutilate (tier 5, level 30), [Venom](https://foreverdb.net/spell/1310703) (level 40 capstone), [Coup de Grace](https://foreverdb.net/spell/1310709) (a level 30 trainer passive), Improved Poisons' charge saving, Malice covering poisons, Murder for Humanoids and Giants only, Improved Expose Armor reworked, and Cold Blood and Vigor moved up the tree.

## What the guides say

### Talents by level

| Level | ForeverDB levelling build | Icy Veins | Wowhead |
|---|---|---|---|
| 10–20 | Malice 5, Ruthlessness 3, Murder 2, Relentless Strikes | Remorseless Attacks 2, Malice 5, Ruthlessness 3, Relentless Strikes | Dagger build 0/9/2 (Improved Eviscerate 3, Improved Sinister Strike 2, Puncturing Wounds 3, Precision 1, Opportunity 2), or Malice 5, Ruthlessness 3, Improved Slice and Dice 2, Relentless Strikes |
| 21–30 | Remorseless Attacks 2, Lethality 2, Improved Poisons 4, Cold Blood, Mutilate | Lethality 4, Cold Blood at 25, Improved Poisons 4, Mutilate at 30 | Malice 5, Ruthlessness 3, Murder 2, Improved Slice and Dice 3, Relentless Strikes, Lethality 1, Cold Blood, Improved Poisons 4, Mutilate |
| 31–60 | Not covered | Vigor 2, Improved Poisons 5, Lethality 5, Seal Fate 5, Venom at 40, then Opportunity, Improved Eviscerate, Lightning Reflexes, Puncturing Wounds, Precision, Vile Poisons and Murder (38/11/2) | Not covered |

For 21–30, the ForeverDB and Icy Veins cells list the points added after 20. Wowhead's level 30 build is shown in full, because it leaves its level 20 builds behind.

ForeverDB's [group build](https://foreverdb.net/class/Rogue/builds) takes Improved Slice and Dice instead of Murder. Icy Veins skips Improved Slice and Dice, arguing that mobs at these levels die before the extra duration matters. With five Legacy points, Wowhead adds Improved Eviscerate 3 and Opportunity 2, while Icy Veins finishes Improved Poisons and puts the rest into Vile Poisons.

The [WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts) level 60 "Asn Muti" preset is 31/20/0. It runs down to Venom with Vile Poisons 5, Improved Poisons 5 and Seal Fate 3, and takes Improved Eviscerate, Lightning Reflexes, Puncturing Wounds, Precision, Endurance, Improved Sprint, Flawless Execution and Dual Wield Specialization in Combat. A "Combat Muti" variant (21/29/1) keeps Mutilate but goes deeper into Combat.

### Rotation and priorities

- **Wowhead ([level 30](https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-30-dps-overview)):** Mutilate only at 3 combo points or fewer, never at 4 or more. Keep Slice and Dice up and refresh it as late as possible. Expose Armor when the group is mostly physical damage and the mob will live. Spend spare points on Eviscerate against low-armour enemies and Rupture against high-armour ones.
- **Icy Veins:** Instant Poison on both weapons, open with Ambush from Stealth, then Mutilate (or Backstab, or Sinister Strike from the front). At 5 points, Slice and Dice if the target will outlive it, otherwise Eviscerate. Its [levelling page](https://www.icy-veins.com/wow-forever/assassination-rogue-leveling) prefers Cheap Shot on dangerous mobs or Garrote for damage, and adds Venom upkeep from 40.
- **ForeverDB:** Save Cold Blood for a 5-point Eviscerate on a tough mob. In groups, Deadly Poison on one weapon lets Coup de Grace raise Eviscerate by 2% per Deadly Poison application, with Instant Poison on the other ([builds](https://foreverdb.net/class/Rogue/builds)).
- **WoWSims, level 60 ([default APL](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/apls/default.apl.json)):** Open with Garrote from Stealth and use Vanish (and Preparation) to open again. Keep Slice and Dice up and recast Venom whenever it's missing at 3 or more points. Use Cold Blood at 5 points before Eviscerate, and Eviscerate at 5 points, or at 4 when you know Mutilate. Mutilate is the builder. The sim's own notes warn that Mutilate isn't yet used automatically, so its Mutilate results need care.

### Poisons

Poisons arrive at 20 through a class quest. Deadly Poison comes at 30 and stacks up to five times ([ForeverDB poisons](https://foreverdb.net/class/Rogue/poisons)). Improved Poisons at 4–5 points makes poisons land more often and gives each hit a good chance not to use a charge. Icy Veins suggests Instant Poison on both weapons while levelling, or Crippling Poison against runners. The WoWSims level 60 default puts Instant Poison on the main hand and Deadly Poison on the off hand.

### Levelling

The real choice is when to switch. ForeverDB and Icy Veins build Assassination from level 10. Wowhead plays a dagger or Combat-style build until 30 because the spec's core tools aren't available yet. Keep your second-best dagger for the off hand, since Mutilate needs two ([ForeverDB](https://foreverdb.net/guide/leveling-rogue)). Remorseless Attacks gives the first builder after each kill a better chance to crit, which Icy Veins rates highly while questing.

### Gear and consumables

Icy Veins' level 30 picks include Torturing Poker (Scarlet Monastery) for the main hand, Serrated Raptor Claw or Subdued Dragon's Fang (quests) for the off hand, Leatherworking's Brawler's and Skulker's pieces, Triprunner Dungarees and Ironspine's Eye. Wowhead adds Defias Jailbreakers, Skullduggery Belt and Toxic Revenger. Poisons and [Rough Sharpening Stone](https://foreverdb.net/item/2862) can now share a weapon, so use both. ForeverDB's simulator rates [Elixir of Agility](https://foreverdb.net/item/8949) and [Tender Wolf Steak](https://foreverdb.net/item/18045) at about 3.2% each at 30.

### Where the guides disagree

- **Which builder at 30:** ForeverDB's simulator card for level 30 builds with Backstab, not Mutilate, and its change log shows that pick flipping between rebuilds on 24 October. Every written guide uses Mutilate.
- **Level 20 build:** an Assassination start (ForeverDB, Icy Veins) or a Combat dagger build (Wowhead).
- **Rupture:** Wowhead uses it on high-armour targets; Blizzard expects Assassination to rank damaging finishers below Venom and Slice and Dice.
- **Improved Slice and Dice:** Icy Veins skips it before 30; Wowhead and ForeverDB's group build take it.

## Ledger findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Assassination Rogue](https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-20-dps-overview): the dagger and Relentless Strikes builds
- [Wowhead: Level 30 Assassination Rogue](https://www.wowhead.com/forever/guide/classes/rogue/assassination/level-30-dps-overview): the Mutilate priority and level 30 gear
- [Icy Veins: Assassination Rogue levelling](https://www.icy-veins.com/wow-forever/assassination-rogue-leveling): talent order to 60 and key abilities
- [ForeverDB: Rogue talent builds](https://foreverdb.net/class/Rogue/builds): levelling, group and PvP builds with reasons
- [ForeverDB: Rogue poisons](https://foreverdb.net/class/Rogue/poisons): poison levels, reagents and the level 20 quest
- [WoWSims: Rogue default APL](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/apls/default.apl.json): the shared level 60 priority list
- [WoWSims: Rogue presets](https://github.com/wowsims/forever/blob/master/ui/specs/rogue/dps/presets.ts): Mutilate builds and stat weights
- [Blizzard: Class Deep Dives, Rogue and Warlock](https://worldofwarcraft.blizzard.com/en-us/news/24310968): the official list of talent changes and Blizzard's intent for each tree
- [ForeverDB: Levelling a Rogue to 30](https://foreverdb.net/guide/leveling-rogue): abilities by level, Energy costs and the two-dagger note for Mutilate
