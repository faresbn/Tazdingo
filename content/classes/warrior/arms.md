---
updated: 2026-10-27
summary: Arms Warrior in WoW Forever: the two-handed damage spec's talents by level, rotation compared across guides and the WoWSims priority list, levelling, gear and where guides disagree.
sources: ForeverDB, Wowhead Level 20 and 30 guides, Icy Veins, WoWSims presets and APL, Blizzard deep dive
---

## At a glance

- **Role:** melee damage with a two-handed weapon.
- **How it plays:** keep Rend up, press Overpower whenever it lights up, Slam on cooldown, and spend spare Rage on Heroic Strike or Cleave. Mortal Strike joins at 40.
- **Strengths:** strong burst on two enemies with Sweeping Strikes, cheap Overpower crits, and one talent that rewards any weapon type.
- **Weaknesses:** little self-healing, slow swings make misses costly, and bleed-immune enemies blunt Rend and Bloodthrill ([Icy Veins](https://www.icy-veins.com/wow-forever/arms-warrior-leveling)).
- **Stats that matter:** weapon damage first, then Strength, hit and crit. Agility and Stamina come last.
- **New in Forever:** [Weaponmaster](https://foreverdb.net/spell/1290261), [Bloodthrill](https://foreverdb.net/spell/1289682), [Spearing Strike](https://foreverdb.net/spell/1310222), [Improved Slam](https://foreverdb.net/spell/12862) as an Arms talent, and a level 20 [Slam](https://foreverdb.net/spell/1240193) with an 18 sec cooldown.

## What the guides say

### Tazdingo recommendation

Use **a current two-hander and affordable Rend/Overpower damage** as the baseline. Slam before Improved Slam can delay a swing, so place it carefully rather than copying the level-60 priority blindly. Save Rage on a nearly dead enemy when an auto attack will finish it; spend Execute when ending the fight now is worth that cost. Five Sunders are more plausible on a long boss than an ordinary quest mob ([Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-30-dps-overview)). The Whirlwind weapon is a substantial reward but its quest includes much higher-level opposition; count the help and travel required before calling it the fastest upgrade.

Everything above level 30 is projection from the game files; nobody could play past 30 in the beta.

### What's different in Forever

Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301514) merged the old weapon specialisations into Weaponmaster. It gives axes and polearms 5% crit, lets maces and staves ignore 15% of armour, and gives swords a 5% chance of an extra attack. Bloodthrill lets main-hand hits on a target with your [Rend](https://foreverdb.net/spell/772) enable [Overpower](https://foreverdb.net/spell/7384) (20% at 5/5). Spearing Strike deals 40% weapon damage, plus 80% more against Giants, Dragonkin and mounted targets. Improved Slam (tier 6, level 35) shortens Slam and stops it delaying your swing. Two-Handed Weapon Specialization dropped to 3% from 5%. Wowhead notes that Rend and Deep Wounds can now crit.

### Talents by level

| Level | Source | Build |
|---|---|---|
| 20 | [ForeverDB](https://foreverdb.net/class/Warrior/builds) | Improved Heroic Strike 3, Deflection 2, Improved Tactical Mastery 5, Anger Management 1 |
| 20 | [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-20-dps-overview) | Improved Heroic Strike 2, Improved Rend 3, Improved Overpower 2, then 4 in Fury's Cruelty |
| 30 | ForeverDB | the 20 build plus Improved Charge 2, Improved Overpower 2, Two-Handed Weapon Specialization 3, Impale 2, Sweeping Strikes 1 |
| 30 | [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-30-dps-overview) | Improved Heroic Strike 2, Improved Rend 3, Improved Tactical Mastery 5, Improved Overpower 2, Anger Management 1, Deep Wounds 3, Spearing Strike 1, Two-Handed Weapon Specialization 1, Impale 2, Sweeping Strikes 1 |
| 30 | Icy Veins | Deflection 2, Improved Rend 3, Improved Tactical Mastery 5, Improved Overpower 2, Anger Management 1, Deep Wounds 3, Spearing Strike 1, Two-Handed Weapon Specialization 3, Sweeping Strikes 1 |
| 31–40 | [Icy Veins levelling](https://www.icy-veins.com/wow-forever/arms-warrior-leveling) (projection) | Bloodthrill 5 at 31–35, Improved Slam 1 at 36, Weaponmaster from 37, Mortal Strike at 40 |
| 60 | [WoWSims default](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts) | 39 Arms (no Deflection; full Rend, Overpower, Deep Wounds and Impale paths, Spearing Strike, Bloodthrill 5, Weaponmaster 5, Improved Slam 2, Mortal Strike), 10 Fury (Cruelty 5, Unbridled Wrath 5), 2 Improved Bloodrage |

With the Legacy perk Talented (up to 5 extra points), Icy Veins puts all five into Bloodthrill. Wowhead puts one into Bloodthrill, finishes Two-Handed Weapon Specialization, then adds the rest to Bloodthrill.

### Rotation and priorities

The single-target advice from the levelling guides:

- **ForeverDB's level 30 sim card** ([PvE guide](https://foreverdb.net/class/Warrior/pve)): Execute below 20%, keep Rend up, Overpower after dodges, Slam on cooldown, Heroic Strike as filler. Bloodrage on the pull. Its sim puts Slam at 11.9% of damage, Overpower at 5.3% and Rend at 4.4%.
- **Wowhead (30):** Battle Shout, Rend, Overpower, Thunder Clap for its attack slow, five Sunder Armors, Spearing Strike, Slam just after a swing, Victory Rush, then Heroic Strike. On packs, save Rage for Sweeping Strikes and use it once Overpower is ready.
- **Icy Veins:** Battle Shout and Bloodrage between pulls, Charge, Demoralizing Shout, Rend, Victory Rush, Overpower, one or two Sunders, Slam after a swing, and Spearing Strike as a Rage dump.

The [WoWSims APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/apls/arms.apl.json) is built for level 60 with Mortal Strike. On a single target it stays in Battle Stance and runs:

1. Overpower when it lights up
2. Mortal Strike
3. Slam (outside the execute phase)
4. Rend, refreshed as it runs out
5. Spearing Strike
6. Execute below 20%
7. Heroic Strike only above 90 Rage, and only without Improved Slam

It adds Sweeping Strikes on two or more targets, Whirlwind from Berserker Stance on three or more, and Cleave on packs above 40 Rage. The common thread at every level is Rend, Overpower and Slam. Heroic Strike is a last resort.

### Levelling

Icy Veins rates Arms weak solo but strong in groups. Wowhead finds it smooth from 20 thanks to Victory Rush, and recommends questing on green-level enemies. Sweeping Strikes at 30 lets you pull two at a time. The Whirlwind Weapon chain (see the overview) gives the best two-hander at this level.

### Gear and consumables

Weapon first, every guide agrees. Wowhead's level 30 picks include Corpsemaker from Razorfen Kraul, the Whirlwind Axe, and Blacksmithing's Officer's Belt and Veteran's Silvered Chain set. ForeverDB's sim ranks Elixir of Agility (+2.1%) and Bear Brisket (+1.7%) as the best level 30 consumables, and Blessing of Kings as the best party buff. Icy Veins adds Rage Potions and Elixir of Ogre Strength. For campfires, Wowhead prefers Mining's Lodestone, but it doesn't stack with Blessing of Might, so use Blacksmithing's Sharpening Wheel instead next to a Paladin.

| Source | Stat order |
|---|---|
| ForeverDB | weapon DPS > Strength > hit > crit > Agility > Stamina |
| Icy Veins | weapon damage > hit > crit > Strength > Agility > Stamina |
| ForeverDB sim, level 30 | Strength 2, Agility 1.61, crit rating 1.13 (attack power = 1) |
| WoWSims, level 60 pre-raid | hit (below the 8% cap) 4.59, crit 2.36, expertise 2.23, Strength 2.2, haste 2.0, Agility 1.82 |

### Where guides disagree

- **Slam's level:** the client, Blizzard and Icy Veins' levelling page say 20; Icy Veins' main Arms page says 30. Wowhead's overview gives a 15 sec cooldown, but Blizzard raised it to 18 on 24 September.
- **Execute:** Icy Veins says skip it while levelling and keep the Rage for the next enemy. ForeverDB and WoWSims use it below 20%.
- **Deep Wounds at 30:** Wowhead and Icy Veins take it; ForeverDB's levelling build skips it, since Impale no longer requires it.
- **Spearing Strike:** ForeverDB's builds page says the 1 October tooltip dropped the dismount. The current client tooltip on its talent page includes it again.
- **Bloodrage:** ForeverDB's guides say it puts you in combat, so Charge first. The current client tooltip on its changes page no longer says so. Charging first is safe either way.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Arms Warrior](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-20-dps-overview): early talents, priority and dungeon drops.
- [Wowhead: Level 30 Arms Warrior](https://www.wowhead.com/forever/guide/classes/warrior/arms/level-30-dps-overview): level 30 build, Legacy points, gear and the Whirlwind Weapon chain.
- [Icy Veins: Arms Warrior Leveling](https://www.icy-veins.com/wow-forever/arms-warrior-leveling): a level-by-level talent order to 60.
- [ForeverDB: Warrior PvE guide](https://foreverdb.net/class/Warrior/pve): group play, stats and the level 30 sim card.
- [ForeverDB: Warrior talent builds](https://foreverdb.net/class/Warrior/builds): levelling, dungeon and PvP builds with a reason for each point.
- [WoWSims: DPS Warrior presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts): level 60 default talents, stat weights and consumables.
- [WoWSims: Arms APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/apls/arms.apl.json): the simulator's priority list.
- [Blizzard: Class Deep Dives, Priest and Warrior](https://worldofwarcraft.blizzard.com/en-us/news/24301514): the official Arms talent changes.
