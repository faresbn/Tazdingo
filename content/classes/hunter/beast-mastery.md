---
updated: 2026-10-27
summary: How Beast Mastery plays in WoW Forever up to the level 30 beta cap, with talents by level, the hawk rotation, pets, gear and where the guides disagree.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and APLs, Blizzard class deep dive
---

## At a glance

- **Role:** Ranged damage. Your pet tanks while you level and does a large share of your damage in groups.
- **How it plays:** Send the pet in, mark the target, keep Serpent Sting up and Auto Shot running. From level 25, [Summon Hawk](https://foreverdb.net/spell/1293241) keeps up to two hawks attacking your target; it shares a cooldown with Arcane Shot.
- **Strengths:** The guides' pick for the easiest and fastest levelling spec. Strong kiting, and pet families that add utility such as armour reduction or a disarm.
- **Weaknesses:** Little area damage, the 8-yard dead zone, pets that struggle to hold several mobs, and (per Wowhead) no group buff to offer.
- **Stats that matter:** Ranged weapon damage first, then Agility, hit and crit. Intellect is worth more than it looks, because mana runs out.
- **New in Forever:** Summon Hawk (tier 4), [Focused Fire](https://foreverdb.net/spell/1223755) (2% more damage for you and the pet), pets that scale with your gear, a melee half for Deadly Aspects, and Intimidation now sitting behind Bestial Swiftness.

## What the guides say

### Talents by level

The sources agree on the core (Deadly Aspects, Unleashed Fury, Summon Hawk) and differ on where the spare points go.

| Level | ForeverDB levelling build | Icy Veins | Wowhead |
|---|---|---|---|
| 10–20 | Deadly Aspects 3, Endurance Training 5, Focused Fire 2, Unleashed Fury 1 | Deadly Aspects 5, Pathfinding 2, Improved Revive Pet 2, Focused Fire 1, Bestial Swiftness | 7/4/0: Deadly Aspects 5, Focused Fire 2, Lethal Attacks 4 |
| 21–30 | Deadly Aspects 5, Unleashed Fury 5, Summon Hawk, Ferocity 2, Bestial Discipline 1 | Unleashed Fury 5, Summon Hawk at 25, Ferocity 3, Intimidation at 30 | Deadly Aspects 5, Focused Fire 2, Improved Revive Pet 2, Pathfinding 1, Unleashed Fury 5, Bestial Swiftness, Ferocity 3, Summon Hawk, Intimidation |
| 31–60 | Not covered | Bestial Discipline 2, Ferocity 5, Frenzy 5, Bestial Wrath at 40, then Lethal Attacks and Careful Aim (39/12/0) | Not covered |

For 21–30, the ForeverDB and Icy Veins cells list the points added after 20. Wowhead's level 30 build is shown in full, because it leaves the level 20 split behind.

[ForeverDB's dungeon version](https://foreverdb.net/class/Hunter/builds) moves points from Endurance Training into Deadly Aspects and Ferocity, since the tank takes the hits. For players with the five extra Legacy points, Icy Veins and Wowhead give the same advice: Ferocity to 5, Bestial Discipline 2 and one point in Frenzy.

The [WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts) level 60 preset is 31/16/4. It takes Bestial Wrath, Frenzy, Ferocity and Bestial Discipline at full rank, plus Lethal Attacks, Improved Stings, Careful Aim and Trueshot Aura, and four points of Improved Tracking. It uses a raptor.

### Rotation and priorities

- **Icy Veins:** Hunter's Mark, pet in first, Serpent Sting once the pet has threat, Summon Hawk whenever it keeps two hawks out, and Aimed Shot on cooldown, with Auto Shot throughout. Arcane Shot only when you're capped on mana and both hawks will last more than 6 seconds. Swap Aimed Shot for Multi-Shot on packs.
- **Wowhead ([level 30](https://www.wowhead.com/forever/guide/classes/hunter/beast-mastery/level-30-dps-overview)):** a fixed cycle of Summon Hawk, Aimed or Multi, Summon Hawk, Aimed or Multi, Arcane Shot, Aimed or Multi.
- **ForeverDB's simulator, level 30:** keep Serpent Sting up, use Multi-Shot whenever it's ready (worth about 7% of your damage even on one target), and fill with Arcane Shot. Use Rapid Fire once mana drops below 95%. The sim spends about 23 seconds of a 60-second fight unable to cast, so start every pull with full mana.
- **WoWSims, level 60 ([turret_hawk](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/turret_hawk.apl.json)):** Hunter's Mark if missing, then a repeating hawk, hawk, Arcane Shot sequence, then Serpent Sting, then Aimed Shot. Multi-Shot is off by default. Cooldowns fire from 5 seconds in. A "Melee Weave (Hawks)" preset adds walking into melee between Auto Shots.

Save Rapid Fire (level 26, 5-minute cooldown) for elites while levelling. Intimidation at 30 is a stun that also builds threat for the pet (Icy Veins).

### Pets

Icy Veins recommends a bear for levelling, because Swipe hits several targets and helps the pet hold them. Wowhead names a fast cat (The Rake) with rank 4 Claw as the best PvE pet at 30, "due to bugs", and lists crabs and bears that teach Claw at 20. Icy Veins' Survival author also prefers a cat or raptor and calls bears only slightly tankier. In groups, turn off Growl's autocast and send the pet only once the tank has the mob. A tallstrider's Dust Cloud lowers the target's armour for every physical attacker, while a bear's Swipe will break a Freezing Trap ([ForeverDB PvE](https://foreverdb.net/class/Hunter/pve)).

### Levelling

Let the pet take the first few hits before you shoot, then send it to the next mob while you loot (Icy Veins). Heal it early with Mend Pet, and use Feign Death from 30 to escape a bad pull. Pathfinding makes Aspect of the Cheetah faster, which Icy Veins rates highly before mounts. Wowhead notes that Legacy points can bring Summon Hawk forward to level 20.

### Gear and consumables

Icy Veins ranks weapon damage first (a slow bow hits harder per shot, which helps Aimed Shot), then hit, Agility, crit, Intellect, Spirit and Stamina. ForeverDB's simulator values Intellect at 2.69, Agility at 2.33 and hit rating at 1.26 per point of ranged attack power at level 30. Good targets include the Venomstrike bow and Fang set from Wailing Caverns at 20, and Truthseeker's Bow, Dusky Leather Armor and the Gnomeregan quest's Triprunner Dungarees at 30 (Icy Veins).

Never run out of ammunition: without it there's no Auto Shot. Buy [Rough Arrow](https://foreverdb.net/item/2512) or [Light Shot](https://foreverdb.net/item/2516) to match your weapon, and a [Light Quiver](https://foreverdb.net/item/2101) or [Small Ammo Pouch](https://foreverdb.net/item/2102) for faster shooting. Wowhead sees no notable change to ammo. ForeverDB's simulator rates [Elixir of Agility](https://foreverdb.net/item/8949) and [Tender Wolf Steak](https://foreverdb.net/item/18045) as the best consumables at 30, each worth about 2.7%.

### Where the guides disagree

- **Level 20 talents:** pure Beast Mastery (ForeverDB, Icy Veins) or a Beast Mastery-Marksmanship split (Wowhead).
- **Arcane Shot:** part of Wowhead's cycle, but Icy Veins uses it only when mana is capped. ForeverDB's simulator finds it gains little, and at levels 20–29 it found leaving it out was 2% better, against ForeverDB's own guide.
- **Single target:** the simulator spends the shared cooldown on Multi-Shot, while Icy Veins and Wowhead use Aimed Shot.
- **Pet choice:** bear (Icy Veins' BM page) or fast cat (Wowhead, Icy Veins' Survival page).

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Beast Mastery Hunter](https://www.wowhead.com/forever/guide/classes/hunter/beast-mastery/level-20-dps-overview): the hybrid level 20 build and where to get Claw
- [Wowhead: Level 30 Beast Mastery Hunter](https://www.wowhead.com/forever/guide/classes/hunter/beast-mastery/level-30-dps-overview): the hawk cycle and level 30 gear
- [Icy Veins: Beast Mastery Hunter levelling](https://www.icy-veins.com/wow-forever/beast-mastery-hunter-leveling): talent order to 60 and levelling habits
- [ForeverDB: Hunter talent builds](https://foreverdb.net/class/Hunter/builds): levelling, dungeon and PvP builds with a reason for every point
- [ForeverDB: Hunter PvE guide](https://foreverdb.net/class/Hunter/pve): group duties, openers and simulator tips
- [WoWSims: turret_hawk APL](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/apls/turret_hawk.apl.json): the level 60 priority list with hawks
- [WoWSims: Hunter presets](https://github.com/wowsims/forever/blob/master/ui/specs/hunter/dps/presets.ts): the level 60 Beast Mastery build and pet
- [Blizzard: Class Deep Dives, Hunter and Druid](https://worldofwarcraft.blizzard.com/en-us/news/24301515): the official list of talent and pet changes
