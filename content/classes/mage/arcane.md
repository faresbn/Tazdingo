---
updated: 2026-10-27
summary: How Arcane Mage plays in WoW Forever, the talents and rotation the guides and simulators use, and where advice changed after the late Arcane Blast rework.
sources: Icy Veins, Wowhead, ForeverDB, WoWSims presets and APLs, Blizzard class deep dive
---

## At a glance

- **Role:** Ranged damage, with burst from Arcane Power and very strong Arcane Explosion AoE in dungeons.
- **How it plays:** Build [Arcane Blast](https://foreverdb.net/spell/400574) stacks, cast [Arcane Missiles](https://foreverdb.net/spell/5143) when [Missile Barrage](https://foreverdb.net/spell/400588) makes them free and fast, and manage your mana.
- **Key talents:** Arcane Blast (11-point talent, level 20), Missile Barrage (first row, from 10), [Arcane Wrath](https://foreverdb.net/spell/1326079) (row 4, new in the live client), [Presence of Mind](https://foreverdb.net/spell/12043) (21 points) and [Arcane Power](https://foreverdb.net/spell/12042) (31 points).
- **Strengths:** Burst, dungeon AoE with low threat thanks to Arcane Subtlety, and good mana talents (Arcane Concentration, Arcane Meditation).
- **Weaknesses:** Burns mana fast, leans on procs, has little control or survivability, and the rotation is not intuitive (Wowhead).
- **Stats:** Hit (Arcane Focus gives 5%), spell power, Intellect and Spirit; crit grows in value with Arcane Impact and Arcane Mind.
- **New in Forever:** Arcane Blast, Missile Barrage, Arcane Wrath and Arcane Geometry; Arcane Mind now adds 100% Arcane crit damage, and Arcane Meditation keeps 50% of regeneration while casting.

## What the guides say

### Arcane Blast changed late in the beta

Blizzard's 7 October [deep dive](https://worldofwarcraft.com/en-us/news/24302097) described a 2.5 second Arcane Blast whose stacks raised your other spells' damage, lasted 8 seconds and ended when you cast anything else. Build 1.60.1.70425 (16 October) changed it in the client: a 1.5 second cast, each stack grants spell damage equal to 15% of your Intellect, stacks last 15 seconds from the first cast, and each one still raises the next Blast's cost by 175% ([ForeverDB](https://foreverdb.net/article/build-1-60-1-70425-game-files)). Wowhead's 21 October [overview](https://www.wowhead.com/forever/guide/classes/mage/arcane/overview-pve-dps) says the buff now runs until the first stack's timer ends.

That splits the advice. Guides written earlier tell you to dump stacks with Fire Blast; the WoWSims rotations keep stacks running while casting other spells. Test it in game before following either.

### Talents by level

| Level | Build | Source |
|---|---|---|
| 20 | Improved Channeling 5, Arcane Concentration 5, Arcane Blast | [ForeverDB levelling build](https://foreverdb.net/guide/leveling-mage), written before the rework |
| 30 | Adds Arcane Impact 3, Arcane Geometry 2, Missile Barrage 1, Arcane Meditation 3, Presence of Mind | ForeverDB, same build |
| 30 | Wand Specialization 2, Improved Channeling 5, Missile Barrage 2, Arcane Subtlety 2, Arcane Concentration 5, Arcane Geometry 2, Arcane Blast, Arcane Wrath, Presence of Mind | Icy Veins guide calculator |
| 60 | Arcane Focus 5, Improved Channeling 5, Missile Barrage 2, Arcane Subtlety 2, Arcane Concentration 5, Arcane Impact 3, Arcane Blast, Arcane Meditation 3, Arcane Wrath, Presence of Mind, Arcane Mind 5, Arcane Instability 3, Arcane Power, plus 3 Fire and 11 Frost | WoWSims "Arcane Frost", the simulator's default |

Icy Veins takes Wand Specialization while wands carry your damage and suggests respeccing out of it at 30, skipping Arcane Focus unless you fight higher-level mobs. Wowhead's [level 30 guide](https://www.wowhead.com/forever/guide/classes/mage/arcane/level-30-dps-overview) gives the same wand advice, prefers Improved Channeling over Arcane Focus if you only fight mobs at or below your level, and puts Legacy bonus points into Arcane Mind. Icy Veins' levelling calculator showed an invalid 52-point build when read, so only its talent list is used here: Improved Channeling, Arcane Subtlety, Arcane Blast, Missile Barrage, Arcane Meditation and Arcane Mind, with a Fire dip into Incineration.

### Rotation

**Levelling and dungeons at 30:**
- [Icy Veins](https://www.icy-veins.com/wow-forever/arcane-mage-ranged-dps-pve-guide): pull with Frostbolt when solo, cast Arcane Blast two or three times, then Fire Blast to dump the stacks; cast Arcane Missiles whenever Missile Barrage procs and wand low targets. Its [levelling page](https://www.icy-veins.com/wow-forever/arcane-mage-leveling) adds: don't spend a Clearcasting proc on Missiles that Missile Barrage already makes free.
- Wowhead: never go above two stacks except on bosses; Fire Blast if Missile Barrage hasn't procced after two or three Blasts.
- AoE: Arcane Explosion when a tank holds the pack; solo, gather, Frost Nova, Cone of Cold, then Arcane Explosion (Icy Veins). Wowhead pre-casts Flamestrike first.
- ForeverDB's own simulator at 30 credits Arcane Missiles with about 60% of damage and Arcane Blast with 40%, and pairs Presence of Mind with Arcane Blast ([ForeverDB PvE](https://foreverdb.net/class/Mage/pve)).

**WoWSims at 60** ([APLs](https://github.com/wowsims/forever/tree/master/ui/specs/mage/dps/apls)):
1. Pre-cast Arcane Wrath.
2. Evocation below 10% mana, after the Skyborne racial Read Leyline if you have it.
3. Cooldowns when Missile Barrage is up or Arcane Wrath is ready; Presence of Mind to make Arcane Wrath instant.
4. Arcane Missiles on Missile Barrage.
5. Refresh Arcane Blast before it expires; build to four stacks if your mana budget allows, never fewer than two.
6. Fill with Frostbolt ("Arcane Frost") or Scorch ("Arcane Fire", which also casts Fire Blast and three-stack Heating Up Pyroblasts).

The simulator's rotations use the old trainer version of Arcane Wrath, which the live client no longer teaches, so they may lag the current talent.

### Gear and consumables

- **Stats:** Icy Veins says talent hit makes hit a non-factor while levelling and ranks Spirit and Intellect high for downtime, noting that 5 Intellect plus 5 Spirit beats 7 Intellect. ForeverDB's dungeon guide puts hit first, because bosses are often above your level. Wowhead says hit now caps at 17%; WoWSims uses the same Arcane hit cap.
- **Level 30 items** (Icy Veins): Tailoring's Pearly pieces (Arcane damage only), [Belt of Arugal](https://foreverdb.net/item/6392), [Gaze Dreamer Pants](https://foreverdb.net/item/6903), Scorn's Icy Choker, Bloodmage Mantle and Nether Force Wand from the Mage quest at 30.
- **Consumables:** Lesser Arcane Elixir is the top consumable in ForeverDB's simulator at 30 (+5.1%), with Briny Seafood Stew close behind; Icy Veins adds Wizard Oils, Spellblasting Potion and mana gems from 28. WoWSims' level 60 defaults include Flask of Supreme Power, Greater Arcane Elixir, Brilliant Wizard Oil and Major Mana Potion.

### Where the guides disagree or aren't sure

- **Arcane Blast stacks:** dump or keep, as above.
- **Missile Barrage timing:** Icy Veins' milestone table still lists it at 25; the current client places it in the first row from level 10.
- **Arcane Concentration:** Wowhead saw it proc once per target hit on AoE during the beta, which made Arcane Explosion nearly free, and expects a fix.
- **Arcane Wrath:** Wowhead gives a 3.5 second cast and 6 second cooldown; ForeverDB's talent tooltip shows only its damage and mana scaling.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 30 Arcane Mage](https://www.wowhead.com/forever/guide/classes/mage/arcane/level-30-dps-overview): first-hand levelling notes, wand advice and the Arcane Concentration bug
- [Icy Veins: Arcane Mage levelling](https://www.icy-veins.com/wow-forever/arcane-mage-leveling): levelling rotation and AoE grinding
- [ForeverDB: Mage PvE guide](https://foreverdb.net/class/Mage/pve): dungeon role, stats and simulator results at 20 and 30
- [ForeverDB: Levelling a Mage to 30](https://foreverdb.net/guide/leveling-mage): the published Arcane levelling builds
- [ForeverDB: Build 1.60.1.70425 changes](https://foreverdb.net/article/build-1-60-1-70425-game-files): the Arcane Blast rework in the client files
- [Blizzard: Class Deep Dives, Mage and Shaman](https://worldofwarcraft.com/en-us/news/24302097): the design intent behind Arcane Blast and Missile Barrage
- [WoWSims Forever: Mage presets](https://github.com/wowsims/forever/blob/master/ui/specs/mage/dps/presets.ts) and [rotation lists](https://github.com/wowsims/forever/tree/master/ui/specs/mage/dps/apls): level 60 builds and priorities
