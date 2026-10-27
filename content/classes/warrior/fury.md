---
updated: 2026-10-27
summary: Fury Warrior in WoW Forever: the dual-wield damage spec's talents by level, rotation compared across guides and the WoWSims priority list, levelling, gear and where guides disagree.
sources: ForeverDB, Wowhead Level 20 and 30 guides, Icy Veins, WoWSims presets and APL, Blizzard deep dive and beta notes
---

## At a glance

- **Role:** melee damage, usually with a weapon in each hand from level 20. Until then, a two-hander.
- **How it plays:** crits and Rage-generating talents do most of the work early. Death Wish arrives at 30, Flurry at 35, Whirlwind at 36 and Bloodthirst at 40, which is when the rotation fills out.
- **Strengths:** strong cleave on two to four enemies and burst from Death Wish ([Icy Veins](https://www.icy-veins.com/wow-forever/fury-warrior-leveling)).
- **Weaknesses:** two weapons to keep upgraded, off-hand misses that starve Rage, and its core attacks arrive late. Wowhead says it is not a strong solo leveller.
- **Stats that matter:** hit (especially for the off-hand), weapon damage, Strength and crit.
- **New in Forever:** [Furious Precision](https://foreverdb.net/spell/1323963), [Lingering Rage](https://foreverdb.net/spell/1323964), [Raging Blows](https://foreverdb.net/spell/1310315) and [Gore Drinker](https://foreverdb.net/spell/1323967). Whirlwind always hits with both weapons, and [Bloodthirst](https://foreverdb.net/spell/23881) no longer heals.

## What the guides say

The beta stopped at 30, so Flurry, Whirlwind and Bloodthirst haven't been played; everything about them is projection.

### What's different in Forever

Fury took the biggest reshuffle in Blizzard's [2 October Warrior notes](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360):

- Whirlwind now always strikes with both weapons, without a talent.
- Raging Blows instead cuts 3 Rage off Cleave and Whirlwind.
- Furious Precision adds up to 10% off-hand hit.
- Dual Wield Specialization adds off-hand damage and Rage (50% more at 5/5) but no hit.
- Unbridled Wrath no longer favours two-handers.
- Death Wish, not Enrage, now leads to Flurry.

From the [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301514): [Enrage](https://foreverdb.net/spell/12317) triggers from any damage taken (a 30% chance for 10% more Physical damage), and Bloodthirst gives 10% movement speed instead of healing. [Death Wish](https://foreverdb.net/spell/12328) raises the damage you take by 5% instead of lowering armour. Queued Heroic Strikes no longer raise off-hand hit ([ForeverDB](https://foreverdb.net/class/Warrior/pve)).

### Talents by level

| Level | Source | Build |
|---|---|---|
| 20 | [ForeverDB](https://foreverdb.net/class/Warrior/builds), [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/fury/level-20-dps-overview) | Cruelty 5, Unbridled Wrath 5, Piercing Howl 1. ForeverDB swaps Piercing Howl for Furious Precision 1 if dual-wielding. |
| 30 | ForeverDB levelling | Cruelty 5, Unbridled Wrath 5, Lingering Rage 1, Piercing Howl 1, Blood Craze 3, Enrage 5, Death Wish 1 |
| 30 | ForeverDB dungeon | Cruelty 5, Booming Voice 2, Unbridled Wrath 5, Furious Precision 3, Dual Wield Specialization 4, Raging Blows 1, Death Wish 1 |
| 30 | [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/fury/level-30-dps-overview) | Cruelty 5, Lingering Rage 2, Unbridled Wrath 5, Furious Precision 3, Dual Wield Specialization 5, Death Wish 1 |
| 30 | Icy Veins | Cruelty 5, Lingering Rage 1, Unbridled Wrath 5, Furious Precision 3, Piercing Howl 1, Dual Wield Specialization 5, Death Wish 1 |
| 31–43 | [Icy Veins levelling](https://www.icy-veins.com/wow-forever/fury-warrior-leveling) (projection) | Flurry 5 at 35–39, Bloodthirst at 40, Enrage 5 by 41, Gore Drinker 2 at 42–43 |
| 60 | [WoWSims default](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts) | 32 Fury (Flurry, Bloodthirst, Raging Blows, Improved Execute, Improved Berserker Rage; no Enrage), 19 Arms (Improved Heroic Strike, Improved Rend, Improved Tactical Mastery, Improved Overpower, Anger Management, Deep Wounds, Impale) |

With Legacy points, Wowhead adds Enrage 4 and a point of Flurry. Icy Veins adds Raging Blows, Improved Berserker Rage and Improved Bloodrage.

### Rotation and priorities

- **ForeverDB's level 30 sim card:** Execute below 20%, Overpower after dodges, Slam on cooldown, Rend (kept up 87% of the fight), Heroic Strike as filler. Bloodrage and Death Wish on the pull. Death Wish is worth 8.8% of damage. Auto attacks make up 30% and off-hand swings 25%.
- **Wowhead (30):** Overpower, Sunder Armor while the target is above 70% health, Execute, then Heroic Strike or Cleave. It warns that both are Rage-inefficient, so don't overuse them.
- **Icy Veins:** Battle Shout, Bloodrage, Charge, Demoralizing Shout, Victory Rush, Rend on enemies that will live, Overpower, one or two Sunders.

The [WoWSims APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/apls/fury.apl.json), built for level 60, runs:

1. Death Wish on cooldown
2. Whirlwind on two or more targets
3. Execute below 20%
4. Whirlwind
5. Bloodthirst
6. Heroic Strike on a single target above 40 Rage, or Cleave on packs
7. Overpower and Rend woven in from Battle Stance
8. Bloodrage below 90 Rage, plus Berserker Rage with its talent

Whirlwind sits above Bloodthirst there. Before 36 Fury has neither, which is why the levelling guides lean on Overpower and Rend.

### Levelling

Icy Veins and Wowhead both call Fury a slow solo leveller that shines in groups. Icy Veins suggests levelling another spec and respeccing once Flurry and good weapons arrive. You can't dual-wield before 20. Icy Veins switches to two weapons at 20, and Wowhead's level 30 build is built around them. ForeverDB's levelling builds stay on a two-hander and keep dual-wielding for its dungeon build. Wowhead's tips: keep weapons current, never waste an Overpower, and don't fear taking a few hits in dungeons, since damage taken is Rage.

### Gear and consumables

ForeverDB's level 30 list suggests Swinetusk Shank (Razorfen Kraul) and Bloody Brass Knuckles (Scarlet Monastery), drop sources from Classic data. Wowhead lists the Whirlwind Axe, Saltscale Girdle (Excavation Site: Wetlands) and Blacksmithing's Officer's Belt. ForeverDB's sim ranks Bear Brisket (+2.8%) and Scroll of Strength II (+2.6%) as the best level 30 consumables, and Blessing of Might as the best party buff (+5.2%). Wowhead likes Skinning's Camp Chair at campfires, because crit feeds Rage. For professions, Wowhead favours Engineering, with Alchemy as an option; Icy Veins suggests Mining and Blacksmithing while levelling.

| Source | Stat order |
|---|---|
| ForeverDB | hit > Strength > crit > Agility > weapon DPS > Stamina |
| Icy Veins | weapon damage > hit > crit > Strength > Agility > Stamina |
| ForeverDB sim, level 30 | Strength 2, Agility 0.73, haste rating 0.62 |
| WoWSims, level 60 pre-raid | crit 2.92, hit 2.29, haste 2.29, Agility 2.25, Strength 2.2, expertise 1.9 |

### Where guides disagree

- **Enrage:** levellers rate it highly because you are hit constantly. WoWSims gives it no points, explaining that its simulated boss attacks no one, so Enrage never procs.
- **Slam:** ForeverDB keeps Slam in Fury's rotation despite the swing delay (Improved Slam is out of Fury's reach). Wowhead and Icy Veins leave it out.
- **Execute and Heroic Strike:** Icy Veins skips Execute while levelling and treats Heroic Strike as an endgame Rage dump. ForeverDB and WoWSims use both.
- **Off-hand hit:** Icy Veins says dual-wielding adds a 19% miss penalty, for a 27% total off-hand miss chance. No other source confirms the number.
- **Outdated text:** Wowhead's Fury overview still describes crits as giving no extra Rage, Bloodthirst at 35% attack power and Dual Wield Specialization giving hit. All three changed on 30 September and 1–2 October.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Fury Warrior](https://www.wowhead.com/forever/guide/classes/warrior/fury/level-20-dps-overview): early talents, Legacy points and priority.
- [Wowhead: Level 30 Fury Warrior](https://www.wowhead.com/forever/guide/classes/warrior/fury/level-30-dps-overview): the level 30 dual-wield build and dungeon tips.
- [Icy Veins: Fury Warrior Leveling](https://www.icy-veins.com/wow-forever/fury-warrior-leveling): a level-by-level talent order to 60 and when to switch to two weapons.
- [ForeverDB: Warrior talent builds](https://foreverdb.net/class/Warrior/builds): Fury levelling, dungeon and PvP builds with reasons.
- [ForeverDB: Warrior PvE guide](https://foreverdb.net/class/Warrior/pve): group role, stats and the level 30 sim card.
- [WoWSims: DPS Warrior presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts): level 60 default talents, stat weights and consumables.
- [WoWSims: Fury APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/apls/fury.apl.json): the simulator's priority list.
- [Blizzard forums: Warrior updates in today's beta build](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360): the 2 October Fury rework.
