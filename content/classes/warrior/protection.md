---
updated: 2026-10-27
summary: Protection Warrior in WoW Forever: the shield tank's talents by level, threat priorities compared across guides and the WoWSims list, why guides rate it for levelling, gear and where guides disagree.
sources: ForeverDB, Wowhead Level 20 and 30 guides, Icy Veins, WoWSims presets and APL, Blizzard deep dive and beta notes
---

## At a glance

- **Role:** tank, with a one-handed weapon and a shield in Defensive Stance.
- **How it plays:** keep Shield Block rolling so Revenge keeps lighting up, open packs with Thunder Clap, and spend spare Rage on Sunder Armor, Rend or Heroic Strike. Shield Slam arrives at 40.
- **Strengths:** blocks, dodges and parries all give Rage through talents, it handles several melee enemies well, and Icy Veins calls it the fastest Warrior spec to level.
- **Weaknesses:** a slow start in the early teens, weaker against casters and elementals, and no ranged way to pull ([Icy Veins](https://www.icy-veins.com/wow-forever/protection-warrior-leveling)). It is the only tank with no thorns-style damage of its own ([Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview)).
- **Stats that matter:** Stamina, armour and Defense to survive, then hit and Strength for threat. Guides weight these differently.
- **New in Forever:** [Vanguard](https://foreverdb.net/spell/1310317) (Charge in Defensive Stance), [Master of Defense](https://foreverdb.net/spell/1310316), [Focused Rage](https://foreverdb.net/spell/29787), [Bastion](https://foreverdb.net/spell/16538), Thunder Clap in Defensive Stance, and [Shield Specialization](https://foreverdb.net/spell/12298) worth 5 Rage per block.

## What the guides say

Shield Slam (40), Bastion (35) and everything past 30 are untested projections.

### What's different in Forever

From Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301514) and [2 October notes](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360):

- Shield Specialization gives 5 Rage on a block instead of 1.
- Master of Defense gives 5 Rage on a dodge or parry with a shield on.
- [Improved Revenge](https://foreverdb.net/spell/12797) adds 60% damage instead of a stun.
- [Defiance](https://foreverdb.net/spell/12792) adds 15% threat in Defensive Stance, but now needs a shield.
- [Anticipation](https://foreverdb.net/spell/12297) gives 20 Defense.
- Improved Shield Wall cuts 11 min off Shield Wall's cooldown.
- Toughness was removed, and Improved Taunt and Improved Shield Block became baseline.
- Iron Will, Improved Bloodrage, Improved Disarm and Improved Shield Bash moved up the tree, so players without a shield can reach Last Stand. Blizzard wants Protection usable as a PvP secondary spec.
- Blizzard's 24 September notes moved Focused Rage up to tier 5 (30) and Bastion down to tier 6 (35), so tanks get cheaper attacks before Shield Slam ([ForeverDB](https://foreverdb.net/article/outlook-warrior)).

[Shield Block](https://foreverdb.net/spell/2565) blocks two attacks, and [Shield Wall](https://foreverdb.net/spell/871) gives 60% less damage for 12 sec on a 15 min cooldown.

### Talents by level

| Level | Source | Build |
|---|---|---|
| 20 | [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-20-tank-overview), [Icy Veins levelling](https://www.icy-veins.com/wow-forever/protection-warrior-leveling) | Shield Specialization 5, Improved Revenge 3, Improved Thunder Clap 2, Master of Defense 1 |
| 20 | [ForeverDB](https://foreverdb.net/class/Warrior/builds) | Shield Specialization 5, Improved Bloodrage 2, Improved Revenge 3 (levelling) or Improved Thunder Clap 3 (dungeons), Master of Defense 1 |
| 30 | ForeverDB levelling | Shield Specialization 5, Improved Bloodrage 2, Improved Revenge 3, Anticipation 3, Master of Defense 2, Last Stand 1, Improved Disarm 3, Vanguard 1, Concussion Blow 1 |
| 30 | ForeverDB dungeon | Shield Specialization 5, Improved Bloodrage 2, Improved Thunder Clap 3, Master of Defense 2, Defiance 3, Last Stand 1, Improved Revenge 1, Improved Sunder Armor 3, Focused Rage 1 |
| 30 | [Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview) | 3 in Arms' Improved Rend, then Shield Specialization 5, Improved Revenge 3, Improved Thunder Clap 3, Last Stand 1, Master of Defense 2, Defiance 3, Vanguard 1 |
| 30 | Icy Veins | Improved Rend 3, Cruelty 2, Improved Bloodrage 2, Shield Specialization 5, Improved Revenge 3, Improved Thunder Clap 3, Master of Defense 2, Vanguard 1 |
| 30–40 | Icy Veins levelling (projection) | Focused Rage 30–32, Concussion Blow 33, Defiance 34, Bastion, Shield Slam at 40 |
| 60 | [WoWSims default](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/presets.ts) | 31 Protection (Shield Slam, Bastion, Focused Rage, Defiance, Vanguard, Concussion Blow, full Anticipation), 17 Arms (Improved Heroic Strike, Deflection, Improved Rend, Deep Wounds, Impale), 3 Cruelty |

With Legacy points, Wowhead adds Improved Sunder Armor 2 and Focused Rage 3. Icy Veins finishes Cruelty and takes Last Stand.

### Threat and priorities

- **Wowhead (30), one target:** Charge, Bloodrage, Shield Block, Revenge, Thunder Clap, Demoralizing Shout, Sunder Armor (five stacks on bosses), Rend if threat is safe, Heroic Strike with spare Rage. On packs it moves Thunder Clap up, then tabs Rend between enemies and uses Cleave with excess Rage.
- **Icy Veins:** Shield Block on cooldown (two blocks refund its 10 Rage), Revenge whenever it lights up, Thunder Clap on cooldown on packs, Rend early, one or two Sunders. Tab between enemies every few seconds to spread threat.
- **ForeverDB's level 30 card:** Charge, Defensive Stance, Shield Block, Revenge, Sunder Armor, Heroic Strike.

The [WoWSims APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/apls/default.apl.json), built for level 60, runs:

1. Last Stand below 40% health and Shield Wall below 35%
2. Shield Block above 40 Rage or just before Revenge comes back
3. Thunder Clap on three or more targets
4. Shield Slam
5. Revenge
6. Thunder Clap on two targets
7. Demoralizing Shout and Battle Shout refreshes
8. Rend, then Sunder Armor to five stacks
9. Cleave or Heroic Strike above 40 Rage

At every level the core is Shield Block into Revenge, with Thunder Clap for packs.

### Levelling

[Icy Veins](https://www.icy-veins.com/wow-forever/protection-warrior-leveling) recommends Protection as the fastest Warrior levelling spec. It suggests a two-hander until Revenge at 14, then sword and board. Wowhead agrees that after Revenge it matches a two-hander, and after 20 cleaves packs well. Vanguard at 25 lets you chain pulls without leaving Defensive Stance. Wowhead notes that thorns effects (Retribution Aura, Thorns) do a lot of dungeon damage right now, so a Paladin or Druid in the group helps.

### Gear and consumables

Wowhead's level 30 picks include Pronged Reaver (Razorfen Kraul), Thermaplugg Medal of Honor (Gnomeregan) and Blacksmithing's Officer's Belt. At 20 it likes Bandsaw Wristbands, which pair with Shield Block. ForeverDB points to Forever's new Guard's Silvered Chain Leggings and Sentinel's Belt. WoWSims' level 60 kit: Major Frenzy Potion, Elixirs of Greater Defense, the Phalanx and the Mongoose, and Major Healthstone. Icy Veins adds Scroll of Protection III. Wowhead notes that Engineering's grenades solve ranged pulling.

| Source | Stat order |
|---|---|
| ForeverDB | Stamina, armour, Defense, block, block value, dodge, parry, hit, Strength |
| Icy Veins | weapon damage, hit, Strength, Agility, armour, Stamina, crit |
| WoWSims, level 60 | blends threat and survival weights: Stamina 1.15, hit 1.13, Agility 0.66, Strength 0.62, block value 0.6; its pre-raid set aims for 140 Defense, which stops a level 63 boss landing crits |

### Where guides disagree

- **Sunder Armor threat:** Wowhead's level 20 page says it has a very low threat value in the beta, so tab-Sundering packs isn't worth it. ForeverDB, citing Blizzard's 24 September fix, recommends tab-Sundering. Both agree that Demoralizing Shout causes no threat right now, a known issue Blizzard has listed.
- **Defiance at 30:** ForeverDB's dungeon build and Wowhead take all three ranks. Icy Veins' calculator leaves it out, though its text mentions it.
- **Survival or threat first:** ForeverDB ranks survival stats first; Icy Veins puts weapon damage, hit and Strength first.

## Ledger findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Protection Warrior](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-20-tank-overview): early talents, threat notes and the Brutal Hauberk chain.
- [Wowhead: Level 30 Protection Warrior](https://www.wowhead.com/forever/guide/classes/warrior/protection/level-30-tank-overview): level 30 build, priorities and dungeon gear.
- [Icy Veins: Protection Warrior Leveling](https://www.icy-veins.com/wow-forever/protection-warrior-leveling): a level-by-level talent order to 60 and the Vanguard macro tip.
- [ForeverDB: Warrior talent builds](https://foreverdb.net/class/Warrior/builds): levelling, dungeon and PvP Protection builds with reasons.
- [ForeverDB: Warrior PvE guide](https://foreverdb.net/class/Warrior/pve): tank job, opener, cooldowns and stats.
- [WoWSims: Protection Warrior presets](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/presets.ts): level 60 talents, threat and survival weights, consumables.
- [WoWSims: Protection Warrior APL](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/protection/apls/default.apl.json): the simulator's priority list.
- [Blizzard forums: Warrior updates in today's beta build](https://us.forums.blizzard.com/en/wow/t/warrior-updates-in-todays-beta-build/2369360): the 2 October Protection tree reshuffle.
- [ForeverDB: Warrior outlook](https://foreverdb.net/article/outlook-warrior): the 24 September notes that swapped Bastion and Focused Rage.
- [Blizzard: Class Deep Dives, Priest and Warrior](https://worldofwarcraft.blizzard.com/en-us/news/24301514): the official Protection talent changes.
