---
updated: 2026-10-27
summary: Warrior builds that mix talent trees in WoW Forever, the levelling hybrids the guides suggest, Blizzard's 5% hybrid tax on Arms and Fury, and switching between tanking and damage.
sources: ForeverDB, Wowhead, Icy Veins, WoWSims presets, Blizzard deep dive and WoW: Forever Podcast
---

## Cheatsheet

- **How mixing works:** one talent point per level from 10, 51 by 60. Each row of a tree needs 5 more points in that tree, so 21 points at 30 can just reach row 5 of one tree.
- **Common dip:** Fury's [Cruelty](https://foreverdb.net/spell/12320) (5% melee crit) is the talent other specs borrow most, since crits also give double Rage.
- **Levelling hybrids:** Wowhead's level 20 Arms build and both Wowhead and Icy Veins' level 30 Protection builds spend points outside their main tree.
- **Level 60 projections:** every WoWSims default and every Icy Veins levelling plan ends with points in a second tree.
- **Hybrid tax:** Blizzard aims Arms and Fury at about 5% less damage than pure damage classes. It is a design target, not a number in the game files.
- **Dual roles:** Dual Specialization opens at level 40, and talents are changed at a capital-city class trainer.

## What the guides say

### Tazdingo recommendation

Choose cross-tree points for the job being performed: solo recovery and damage taken, dungeon tanking, or damage behind a separate tank. Enrage cannot be judged in a model where the character is never hit, while a raid damage preset need not fund solo defensive tools. State weapon setup, level and Legacy allowance before comparing. The hybrid target concerns Warrior class design, not an additional cost for mixing talent trees.

### How mixing works

[ForeverDB](https://foreverdb.net/class/Warrior/talents) reads the rules from the client: a point at every level from 10 to 60, and each row of a tree opens once you have 5 more points in the rows above it. Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301514) adds one-point milestone talents at 11, 16, 21 and 31 points. That makes deep capstones expensive and shallow dips cheap. The Legacy perk Talented gives the same points up to five levels early, but Wowhead notes it sits behind Well Rested in the Legacy tree, so most players won't have all five. Respeccing cost 1 silver in the beta as a temporary measure; the launch price isn't known.

### Levelling hybrids the guides suggest

| Build | Points | The reasoning |
|---|---|---|
| [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-20-dps-overview) Arms, level 20 | Improved Heroic Strike 2, Improved Rend 3, Improved Overpower 2, Cruelty 4 | Cruelty beats deeper Arms points until 21 points open Two-Handed Weapon Specialization. At 30, go fully Arms. |
| [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview) Protection, level 30 | Improved Rend 3 plus 18 Protection | Tab-targeting Rend usually beats Cleave. The 3 points can move to Cruelty, Deflection, or Improved Sunder Armor and Focused Rage. |
| [Icy Veins](https://www.icy-veins.com/wow-forever/protection-warrior-tank-pve-guide) Protection, level 30 | Improved Rend 3, Cruelty 2, 16 Protection | Rend damage and crit while levelling. For dungeon-only play it swaps them for Defiance, Concussion Blow and Focused Rage. |

ForeverDB's published [builds](https://foreverdb.net/class/Warrior/builds) stay in one tree at both 20 and 30, so not every guide sees mixing as necessary before 30.

The level 60 plans all mix trees. These are projections nobody has played:

| Spec | [WoWSims default](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts) (Arms/Fury/Protection) | Icy Veins levelling plan at 60 |
|---|---|---|
| Arms | 39/10/2: Cruelty, Unbridled Wrath, Improved Bloodrage | 33/16/2: Cruelty, Lingering Rage, Unbridled Wrath, Raging Blows, Improved Bloodrage |
| Fury | 19/32/0: Improved Heroic Strike, Improved Rend, Improved Tactical Mastery, Improved Overpower, Anger Management, Deep Wounds, Impale | 13/36/2: Deflection, Improved Charge, Improved Tactical Mastery, Anger Management, Improved Bloodrage |
| Protection | 17/3/31 ([presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/presets.ts)): Deflection, Improved Rend, Deep Wounds, Impale, Cruelty 3 | 0/20/31: Cruelty, Lingering Rage, Unbridled Wrath, Piercing Howl, Raging Blows, Enrage |

The pattern: damage specs borrow Rage and crit talents, mostly from the top rows of the other damage tree, and both tank plans borrow crit. Blizzard's [2 October notes](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360) also moved Iron Will, Improved Bloodrage, Improved Disarm and Improved Shield Bash up the Protection tree. The goal was a path for players without a shield, so Protection could serve "as a PvP tech secondary specialization".

### The hybrid tax

On episode 2 of the WoW: Forever Podcast, Blizzard's developers said they aim for hybrid damage specs to deal about 5% less than Hunters, Mages, Rogues and Warlocks ([ForeverDB's write-up](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)). Every other class counts as a hybrid, and Warriors are included because they can pick up a shield, switch to Defensive Stance and tank. In practice, if a pure class does 1,000 damage per second, the target for Arms or Fury is around 950.

Key points from that write-up:

- It is an average across fights, not a cap, and a hybrid can still top some encounters.
- The developers also said they don't believe in the old hybrid tax. They would rather keep every role competitive and leave hybrids missing some tools and buffs.
- As compensation, Blizzard wants Warriors to be the best class for cleave.
- Damage tuning lives on Blizzard's servers, so the 5% can't be checked in the client, and no patch notes mention it. Nobody can measure level 60 damage yet.
- Forum reaction is mixed. A long thread argues Warriors aren't hybrids at all, and another fears the label will make the levelling tank shortage worse. As of 8 October, ForeverDB found no Blizzard follow-up.

### Dual-role play

Blizzard says Dual Specialization becomes available at level 40, so tank and damage builds can sit side by side later. Before that, the guides describe flexing within one build:

- **Damage Warriors can tank in an emergency.** If the tank dies, switch to Defensive Stance and Taunt. Tactical Mastery keeps 10 Rage through the switch, and up to 25 with Improved Tactical Mastery ([ForeverDB](https://foreverdb.net/class/Warrior/pve)). Wowhead's Fury guides add that taking some hits in dungeons is fine, because damage taken is Rage.
- **Keep a shield in your bags.** Icy Veins suggests carrying a one-hander and shield so you can Shield Bash dangerous casts in any build. ForeverDB has a weapon-swap macro (see the macros page).
- **Protection levels and tanks without a respec.** ForeverDB says its level 30 levelling build also tanks dungeons well.
- **Two-hander for Retaliation.** Wowhead suggests a tank swap to a two-hander while Retaliation is active against several enemies.

The forum objection still applies: a Warrior in damage gear and talents tanks poorly, which is the main argument against the hybrid label.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: The hybrid tax](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): the podcast quotes, who counts as a hybrid, and the forum reaction.
- [ForeverDB: Warrior talent builds](https://foreverdb.net/class/Warrior/builds): single-tree levelling, dungeon and PvP builds for comparison.
- [Wowhead: Level 20 Arms Warrior](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-20-dps-overview): the Arms-into-Cruelty levelling build.
- [Wowhead: Level 30 Protection Warrior](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview): the Improved Rend tank build and Legacy points.
- [Icy Veins: Protection Warrior guide](https://www.icy-veins.com/wow-forever/protection-warrior-tank-pve-guide): the level 30 Protection build with Arms and Fury points.
- [Icy Veins: Arms](https://www.icy-veins.com/wow-forever/arms-warrior-leveling), [Fury](https://www.icy-veins.com/wow-forever/fury-warrior-leveling) and [Protection](https://www.icy-veins.com/wow-forever/protection-warrior-leveling) levelling guides: talent orders to 60.
- [WoWSims: DPS Warrior presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts) and [Protection presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/presets.ts): level 60 default talent strings.
- [Blizzard: Class Deep Dives, Priest and Warrior](https://worldofwarcraft.blizzard.com/en-us/news/24301514): talent structure and Dual Specialization.
- [Blizzard forums: Warrior updates in today's beta build](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360): the non-shield path through Protection.
