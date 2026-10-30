---
updated: 2026-10-27
summary: How Marksmanship plays in WoW Forever up to the level 30 beta cap, with talents by level, the shot priority, the pet versus Lone Wolf question, gear and the guides' disagreements.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and APLs, Blizzard class deep dive
---

## At a glance

- **Role:** Ranged damage built on your own shots rather than the pet's.
- **How it plays:** Auto Shot, Serpent Sting, then Aimed Shot and Arcane Shot on cooldown. Rapid Killing rewards the first shot after a kill, Trueshot Aura buffs the group, and Sniper Shot (level 40) is a long-range capstone.
- **Strengths:** Burst, the longest range in the game, strong kiting, and a Trueshot Aura that reaches the whole raid since the 16 October build.
- **Weaknesses:** Mana-hungry, punished hardest by the dead zone, and per Wowhead the hardest Hunter spec to play well. Wowhead also argues it adds little to a group beyond damage, since Trueshot Aura no longer helps melee.
- **Stats that matter:** Ranged weapon damage, Agility, hit and crit. With Careful Aim, Intellect also adds attack power, and ForeverDB's simulator rates it above Agility at 30.
- **New in Forever:** [Careful Aim](https://foreverdb.net/spell/1223984), [Rapid Killing](https://foreverdb.net/spell/415405), [Rapid Recuperation](https://foreverdb.net/spell/1223987), [Lone Wolf](https://foreverdb.net/spell/415370), Improved Stings and [Sniper Shot](https://foreverdb.net/spell/1310687). Lethal Attacks now covers all attacks, Aimed Shot is baseline, and Trueshot Aura moved up to tier 4 (level 25).

## What the guides say

### Tazdingo recommendation

**Keep a pet for solo levelling** unless a comparable test shows Lone Wolf improves the whole route, including incoming damage and recovery. The level-30 guide favours the pet; petless level-60 presets assume a different loadout and role ([Wowhead](https://www.wowhead.com/forever/guide/classes/hunter/marksmanship/level-30-dps-overview)). Use Aimed Shot for a single target and consider Multi-Shot for safe packs: they share a cooldown, so cannot both be unconditional priorities. Spend more on Arcane Shot when mana is plentiful; hold it back when drinking time is the limiting cost. Intellect's high value in one mana-starved model is not a universal reason to replace weapon damage or Agility.

### Talents by level

| Level | ForeverDB levelling build | Icy Veins | Wowhead |
|---|---|---|---|
| 10–20 | Lethal Attacks 5, Efficiency 5, Rapid Killing 1 | Lethal Attacks 5, Careful Aim 5, then Rapid Killing (levelling) or Lone Wolf (dungeon build) | 7/4/0: Deadly Aspects 5, Focused Fire 2, Lethal Attacks 4 |
| 21–30 | Careful Aim 5, Rapid Killing 2, Trueshot Aura, Mortal Shots 2, Rapid Recuperation 1 | Levelling: Rapid Killing 2, Hawk Eye 3, Trueshot Aura, Mortal Shots 4, Rapid Recuperation at 30. Dungeon: Rapid Killing 2, Efficiency 2, Trueshot Aura, Mortal Shots 5 | Lethal Attacks 5, Careful Aim 5, Improved Arcane Shot 5, Trueshot Aura, Mortal Shots 4, Scatter Shot |
| 31–60 | Not covered | Rapid Recuperation 2, Mortal Shots 5, Barrage, Ranged Weapon Specialization 5, Sniper Shot at 40, then Beast Mastery up to Summon Hawk (19/32/0) | Not covered |

For 21–30, the ForeverDB and Icy Veins cells list the points added after 20. Wowhead's level 30 build is shown in full, because it leaves the level 20 split behind.

[ForeverDB's dungeon build](https://foreverdb.net/class/Hunter/builds) takes Careful Aim before Efficiency, because you drink between pulls in a group. Icy Veins warns that its 21-point Marksmanship build is meant for dungeons. For general play at 30 it points to the Beast Mastery build, and it would spend Legacy points on Deadly Aspects.

The [WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts) level 60 preset is 5/41/5 with no pet. It takes Deadly Aspects, almost the whole Marksmanship tree up to Ranged Weapon Specialization (including Lone Wolf), and Improved Tracking. Notably it skips Sniper Shot, and its priority list has Sniper Shot switched off by default.

### Rotation and priorities

- **Icy Veins:** Hunter's Mark, pet in first, Serpent Sting, Aimed Shot on cooldown, Auto Shot throughout, and Arcane Shot only when mana is capped. Its levelling page adds: keep Serpent Sting on the target as it dies, then open the next fight with Sniper Shot (or Aimed Shot) while Rapid Killing is up.
- **Wowhead ([level 30](https://www.wowhead.com/forever/guide/classes/hunter/marksmanship/level-30-dps-overview)):** Hunter's Mark, Serpent Sting, then Arcane Shot and Aimed Shot (single target) or Multi-Shot (packs) on cooldown.
- **ForeverDB's simulator, level 30:** Serpent Sting up (about 84% of the fight), Aimed Shot on cooldown, Arcane Shot as filler. Rapid Fire once mana is below 95%. Mana still runs dry for about 23 seconds of every minute.
- **WoWSims, level 60 ([turret](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/turret.apl.json)):** Hunter's Mark if missing, Aimed Shot, Serpent Sting if not ticking, Sniper Shot only during Rapid Fire or a Quick Shots proc (when switched on), Arcane Shot, then Multi-Shot if switched on. A "Turret (Multi-Shot)" variant spends the shared cooldown on Multi-Shot instead of Aimed Shot.

Multi-Shot breaks Freezing Trap, so keep it and Serpent Sting away from a frozen mob. Rapid Killing also takes 2 minutes off Rapid Fire's cooldown ([ForeverDB PvE guide](https://foreverdb.net/class/Hunter/pve), [builds](https://foreverdb.net/class/Hunter/builds)).

### Pet or Lone Wolf

[Lone Wolf](https://foreverdb.net/spell/415370) gives 20% more damage while no pet is out. At level 20–30 the guides keep the pet. Wowhead says a fast cat currently out-damages the bonus, and ForeverDB's simulator shows about 20% less damage without a pet at 30. Icy Veins takes Lone Wolf only for dungeon area damage, where the bonus boosts Multi-Shot. Looking further ahead, Wowhead's overview expects most Marksmanship Hunters to drop the pet in dungeons and raids, and every WoWSims Marksmanship preset at 60 runs without one.

### Levelling

Marksmanship levels well but behind Beast Mastery ([Icy Veins](https://www.icy-veins.com/wow-forever/marksmanship-hunter-leveling)). You deal more damage yourself, so the pet loses threat more easily and you spend more mana. Efficiency (ForeverDB), and later Rapid Killing with Rapid Recuperation (Icy Veins), are the guides' answer to mana. When you run low, stop casting and let Auto Shot work, since it's free.

### Gear and consumables

Icy Veins ranks weapon damage first, then hit, Agility, crit (which Mortal Shots rewards) and Intellect through Careful Aim. ForeverDB's simulator values Intellect at 3.38, Agility at 2.4 and hit rating at 1.22 per point of ranged attack power at 30. Gear picks match the other specs: Venomstrike and the Fang set at 20; Truthseeker's Bow and Dusky Leather Armor at 30. Wowhead's Beast Mastery page adds Stalker's Leather Belt and the Master Hunter's Rifle quest reward.

Carry plenty of ammunition ([Rough Arrow](https://foreverdb.net/item/2512) or [Light Shot](https://foreverdb.net/item/2516)) in a quiver or ammo pouch, which also speeds up your shots. [Elixir of Agility](https://foreverdb.net/item/8949) and [Tender Wolf Steak](https://foreverdb.net/item/18045) top ForeverDB's consumable list. The WoWSims level 60 default pairs Thorium Headed Arrows with a high-end quiver.

### Where the guides disagree

- **Trueshot Aura's size:** Wowhead lists 50 ranged attack power for the party. In the client, rank 1 gives 30 ranged attack power to party or raid members ([ForeverDB](https://foreverdb.net/class/Hunter/changes)).
- **Sniper Shot:** Icy Veins describes a 4-second cooldown. Blizzard and the client give a 4-second cast and a 15-second cooldown.
- **Level 20 build:** a Marksmanship start (ForeverDB, Icy Veins) or a Beast Mastery-heavy split (Wowhead, which calls the tree awkward for levelling).
- **Arcane Shot:** on cooldown (Wowhead, ForeverDB's simulator) or only when mana-capped (Icy Veins).
- **Wowhead's Legacy-points build** includes Lone Wolf, even though the same page advises keeping the pet.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Marksmanship Hunter](https://www.wowhead.com/forever/guide/classes/hunter/marksmanship/level-20-dps-overview): why it starts in Beast Mastery
- [Wowhead: Level 30 Marksmanship Hunter](https://www.wowhead.com/forever/guide/classes/hunter/marksmanship/level-30-dps-overview): the level 30 build and pet advice
- [Icy Veins: Marksmanship Hunter levelling](https://www.icy-veins.com/wow-forever/marksmanship-hunter-leveling): the talent path to Sniper Shot and beyond
- [ForeverDB: Hunter talent builds](https://foreverdb.net/class/Hunter/builds): levelling, dungeon and PvP Marksmanship builds
- [ForeverDB: Hunter changes vs Classic](https://foreverdb.net/class/Hunter/changes): exact talent and spell numbers from the client
- [WoWSims: turret APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/turret.apl.json): the level 60 ranged priority list
- [WoWSims: Hunter presets](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts): level 60 Marksmanship builds without a pet
- [Blizzard: Class Deep Dives, Hunter and Druid](https://worldofwarcraft.blizzard.com/en-us/news/24301515): the official list of talent and pet changes
- [ForeverDB: Hunter PvE guide](https://foreverdb.net/class/Hunter/pve): group duties, crowd control and simulator tips
