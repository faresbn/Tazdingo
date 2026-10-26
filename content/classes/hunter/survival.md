---
updated: 2026-10-27
summary: How Survival works as a melee spec in WoW Forever, from the ranged levels before 30 to the Strider Kick rotation, with talents by level, weaving, weapons and the guides' disagreements.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and APLs, Blizzard class deep dive
---

## At a glance

- **Role:** Melee damage with traps, after a ranged start. Its melee kit arrives at level 30: Aspect of the Beast and [Lacerate](https://foreverdb.net/spell/24118) from the trainer, and [Strider Kick](https://foreverdb.net/spell/1317257) as a tier 5 talent.
- **How it plays:** Queue Raptor Strike (a next-swing attack on a 6-second cooldown), press Strider Kick (8 seconds) and Mongoose Bite whenever it lights up, keep Serpent Sting and Lacerate ticking, and drop traps in combat.
- **Strengths:** Steady damage with almost always a button to press (Wowhead), kiting and trap control, and a parry-based Counterattack for PvP.
- **Weaknesses:** The weakest Hunter spec to level, especially before 40 (Icy Veins). It needs deep talents, melee abilities drain mana, and you compete with Warriors and Rogues for weapons.
- **Stats that matter:** Weapon damage, Agility, hit and crit, with Strength and attack power for melee. ForeverDB's simulator values Agility at 1.33 and haste rating at 0.62 per point of attack power at 30.
- **New in Forever:** Strider Kick, [Predator's Edge](https://foreverdb.net/spell/1310627) (melee crit damage and 50% more off-hand damage), [Expose Prey](https://foreverdb.net/spell/1310532), [Resourcefulness](https://foreverdb.net/spell/440529), Survivalist's Discipline, [Lacerating Strikes](https://foreverdb.net/spell/1310533) at 40, Improved Tracking, and weapon-based Mongoose Bite and Counterattack.

## What the guides say

### What changed

Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301515) rebuilds Survival around melee. Savage Strikes, Surefooted and Entrapment now apply more broadly (Entrapment always roots), and the bottom half of the tree adds the new melee talents. Mongoose Bite and Counterattack now scale with weapon damage and need a melee weapon. Mongoose Bite still requires a dodge, unless Expose Prey procs it: attacks on a target with your Hunter's Mark have a 10% chance to enable it ([ForeverDB changes](https://foreverdb.net/class/Hunter/changes)). Deadly Aspects (Beast Mastery tier 1) gives melee haste procs under Aspect of the Beast.

### Talents by level

| Level | ForeverDB levelling build | Icy Veins | Wowhead |
|---|---|---|---|
| 10–20 | Improved Tracking 5, Savage Strikes 2, Survivalist 3, Deterrence | Main guide: Improved Tracking 5, Savage Strikes 2, Entrapment 3, Surefooted. Levelling page: Lethal Attacks 5 first | 0/4/7: Lethal Attacks 4, Improved Tracking 5, Savage Strikes 2 |
| 21–30 | Survivalist 5, Surefooted 3, Predator's Edge 4, Strider Kick | Surefooted 3, Clever Traps 2, Predator's Edge 5, Strider Kick at 30 | Improved Tracking 5, Deflection 4, Savage Strikes 2, Surefooted 3, Deterrence, Predator's Edge 4, Counterattack, Strider Kick |
| 31–60 | Not covered | Levelling page (Strider Kick waits until 35): Expose Prey 2, Survivalist's Discipline 2, Lightning Reflexes 5, Lacerating Strikes at 45, then Careful Aim, Lone Wolf and other Marksmanship picks (0/17/34) | Not covered |

For 21–30, the ForeverDB and Icy Veins cells list the points added after 20. Wowhead's level 30 build is shown in full, because it leaves the level 20 split behind.

For the five Legacy points, Icy Veins and Wowhead both pick Resourcefulness 2 and Expose Prey 2, which fix mana and make Mongoose Bite regular. [ForeverDB's dungeon version](https://foreverdb.net/class/Hunter/builds) adds Clever Traps for crowd control.

[WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts) opens on its "SV Weave" build (0/20/31, no pet): Lethal Attacks, Improved Stings, Careful Aim, Lone Wolf, Trueshot Aura and Mortal Shots, with Survival down to Lacerating Strikes. Its "SV Melee" build (18/8/25) dual-wields with a raptor and hawks, and takes Deadly Aspects, Unleashed Fury and Summon Hawk alongside Predator's Edge, Expose Prey and Strider Kick.

### Rotation and priorities

- **Before 30, every source plays at range** like the other specs, with Raptor Strike when something reaches you. Wowhead suggests running in and out to mix the two.
- **Icy Veins (melee at 30):** Hunter's Mark, pet in, Serpent Sting, then into melee: Raptor Strike on cooldown, Mongoose Bite when available, Strider Kick on cooldown, and Disengage if you pull threat. Its [levelling page](https://www.icy-veins.com/wow-forever/survival-hunter-leveling) weaves instead: Arcane Shot, run in for Raptor Strike and Mongoose Bite, then Strider Kick and use its speed to get back to range. On packs it adds Multi-Shot, and Explosive Trap from 34.
- **Wowhead ([level 30](https://www.wowhead.com/forever/guide/classes/hunter/survival/level-30-dps-overview)):** always queue Raptor Strike in melee, then Mongoose Bite, Strider Kick and Counterattack in that order. Step out for Arcane Shot, Serpent Sting or Aimed Shot while Raptor Strike and Mongoose Bite recover.
- **ForeverDB's simulator, level 30:** Mongoose Bite within 5 seconds of a proc, Strider Kick on cooldown (about 14% of your damage), Raptor Strike on cooldown, Serpent Sting up. Raptor Strike is 39% of the damage, Strider Kick 18% and the pet 17%.
- **WoWSims, level 60:** the [melee APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/melee.apl.json) starts with Aspect of the Beast and shoots on the walk in (Serpent Sting, Arcane Shot, Multi-Shot). In melee it uses Raptor Strike, Mongoose Bite, Strider Kick, Immolation Trap at your feet and Summon Hawk, with Wing Clip as filler. The default [weave APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/default.apl.json) does the same melee hits but walks in only when the swing delays Auto Shot by no more than about 1.2 seconds. A [clean_weave](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/clean_weave.apl.json) variant fires every shot before weaving.

In dungeons you stand behind the target, so dodges and parries are rare, and ForeverDB advises not to plan around Mongoose Bite or Counterattack there. Wowhead and Icy Veins see Expose Prey as what makes Mongoose Bite a regular button.

### Weapons

Wowhead and WoWSims describe two set-ups: a two-hander to weave between melee and range, or two one-handers to stay in melee, where Predator's Edge's off-hand bonus pays off. Hunters dual-wield from 20, can use polearms from 20 and can't use maces ([ForeverDB](https://foreverdb.net/guide/leveling-hunter)). Wowhead's Hunter pages tie the Orc and Human crit passives to axes and swords, but ForeverDB reports that Blizzard's 16 October build made both flat bonuses on all attacks.

### Gear and consumables

Wowhead's level 30 picks include Morbid Dawn, Pronged Reaver, Bloody Brass Knuckles, Skulker's Leather Belt and any level 28–30 "of the Tiger" item for Agility and Strength. Icy Veins' list matches the other specs, with Armor Piercer from Razorfen Kraul. Keep ammunition stocked for the ranged phase. Elixir of Agility and Tender Wolf Steak each add about 1.9% in ForeverDB's simulator, and Wowhead adds Lodestone to the camping buffs for melee Hunters.

### Where the guides disagree

- **Weaving:** Icy Veins' main guide says Hunters no longer need to weave, but its levelling page, Wowhead and the WoWSims default all weave. A creator claimed melee and ranged share one swing timer; [ForeverDB](https://foreverdb.net/article/wille-hunter-everything-you-need-to-know) says that's server behaviour it can't check yet.
- **When melee starts:** 30 (ForeverDB, Icy Veins) or about 32, once Expose Prey joins Strider Kick (Wowhead).
- **Expose Prey's window:** Wowhead says Mongoose Bite stays usable for 5 seconds; the client tooltip says 10.
- **Aimed Shot:** Icy Veins' Survival author rarely uses it, even on one target, and prefers Multi-Shot. The other specs' guides use Aimed Shot on single targets.

## Ledger findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Survival Hunter](https://www.wowhead.com/forever/guide/classes/hunter/survival/level-20-dps-overview): the hybrid ranged start
- [Wowhead: Level 30 Survival Hunter](https://www.wowhead.com/forever/guide/classes/hunter/survival/level-30-dps-overview): melee priority and level 30 weapons
- [Icy Veins: Survival Hunter levelling](https://www.icy-veins.com/wow-forever/survival-hunter-leveling): the weave rotation and talent path to 60
- [ForeverDB: Hunter talent builds](https://foreverdb.net/class/Hunter/builds): levelling, dungeon and Counterattack PvP builds
- [ForeverDB: Hunter changes vs Classic](https://foreverdb.net/class/Hunter/changes): the new Survival talents and their exact values
- [ForeverDB: WillE's Hunter overview, checked](https://foreverdb.net/article/wille-hunter-everything-you-need-to-know): which Survival claims the client confirms, and which it can't
- [WoWSims: melee APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/melee.apl.json): the level 60 pure melee priority list
- [WoWSims: default weave APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/default.apl.json): when the simulator walks in for a swing
- [WoWSims: Hunter presets](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts): the SV Weave and SV Melee builds
