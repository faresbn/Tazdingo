---
updated: 2026-10-27
summary: Protection Paladin in WoW Forever: the Mana tank's talents by level, threat priorities compared across guides and the WoWSims list, levelling, gear and where guides disagree.
sources: ForeverDB, Wowhead Level 20 and 30 guides, Icy Veins, WoWSims presets and APL, Blizzard Paladin deep dive and beta notes
---

## At a glance

- **Role:** tank, with a one-hander, a shield and Righteous Fury.
- **How it plays:** keep Seal of Fury up, Judge on cooldown for damage and a taunt, Holy Strike on cooldown, and drop Consecration on packs when Mana allows. Retribution Aura adds threat on every enemy that hits the group.
- **Strengths:** strong pack threat from Consecration and Retribution Aura, a 10 yard taunt, a large absorb cooldown, and a full Paladin utility kit.
- **Weaknesses:** heavy reliance on Mana, no interrupt, and no ranged pull without Engineering or special items (Wowhead, [Icy Veins](https://www.icy-veins.com/wow-forever/protection-paladin-leveling)).
- **Stats that matter:** Stamina, Defense and armour to survive, then hit, spell power and Strength for threat.
- **New in Forever:** [Seal of Fury](https://foreverdb.net/spell/1311649) and its taunting Judgement, [Swift Judgement](https://foreverdb.net/spell/1310994), [Templar's Bulwark](https://foreverdb.net/spell/1311015), [Improved Seal of Fury](https://foreverdb.net/spell/1314103), [Sacred Duty](https://foreverdb.net/spell/1224697) and [Iron Creed](https://foreverdb.net/spell/1311034).

## What the guides say

Iron Creed (35), Holy Shield and Hammer of the Righteous (40) were out of reach in the beta; their value is projection.

### What's different in Forever

From Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24302099):

- **Seal of Fury** adds the same Holy damage to every swing, whatever the weapon speed, and with a shield turns half of it into an absorb. Its Judgement deals Holy damage and taunts for 4 sec.
- **Swift Judgement** (16 points) finishes Judgement's cooldown for a second taunt.
- **Templar's Bulwark** (21 points) absorbs damage equal to your maximum health for 8 sec, on a 5 min cooldown. It shares Forbearance with Divine Protection.
- **Shield Specialization** blocks restore Mana, and **Improved Seal of Fury** returns Mana when an absorb is used up (more against higher-level enemies).
- **Improved Righteous Fury** now cuts damage taken by 6% instead of adding threat. **Reckoning** can also trigger from blocks.
- **Consecration** is baseline at 20 and only hits four enemies hard. Holy Shield (40) now requires Templar's Bulwark.

The 15 October build made Seal of Fury survive Power Word: Shield. It also put Righteous Fury back to 90% Holy threat ([ForeverDB](https://foreverdb.net/article/paladin-deep-dive-seals-judgements-holy-strike-protection-retribution)).

### Talents by level

| Level | Source | Build |
|---|---|---|
| 20 | [ForeverDB](https://foreverdb.net/class/Paladin/builds) dungeon tank | Redoubt 5, Precision 3, Anticipation 2, Shield Specialization 1 |
| 20 | [Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/protection/level-20-tank-overview) | all Retribution: Deflection 1, Benediction 5, Improved Judgement 2, Holy Conduit 2, Pursuit of Justice 1 |
| 30 | ForeverDB dungeon tank | Redoubt 5, Precision 3, Anticipation 2, Shield Specialization 3, Improved Seal of Fury 1, Sacred Duty 2, Swift Judgement 1, Improved Righteous Fury 3, Templar's Bulwark 1 |
| 30 | [Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview) | Redoubt 5, Precision 3, Anticipation 2, Improved Seal of Fury 1, Improved Righteous Fury 1, Shield Specialization 3, Sacred Duty 2, One-Handed Weapon Specialization 3, Templar's Bulwark 1 |
| 30 | Icy Veins (25 points) | Redoubt 5, Precision 3, Anticipation 5, Improved Seal of Fury 1, Improved Righteous Fury 1, Shield Specialization 3, plus Retribution's Deflection 5 and Holy Conduit 2 |
| 10–60 | [Icy Veins levelling](https://www.icy-veins.com/wow-forever/protection-paladin-leveling) (projection) | 11 points in Retribution first (Deflection, Improved Judgement, Holy Conduit, Pursuit of Justice), then Protection, with Holy Shield at 60; ends 35 Protection, 16 Retribution |
| 60 | [WoWSims default](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/protection/presets.ts) | 8 Holy (Divine Strength, Improved Seals), 34 Protection (Swift Judgement, Templar's Bulwark, Reckoning, Iron Creed 3, Holy Shield), 9 Retribution (Deflection, Improved Judgement, Holy Conduit) |

Wowhead's level 20 build goes into Retribution because Benediction and Holy Conduit save more Mana for Consecration than Improved Seal of Fury, and Pursuit of Justice adds speed. It also noted a beta bug that gave Seal of Fury Mana returns without the talent; Blizzard fixed that on 8 October. With Legacy points, Wowhead adds Reckoning 5.

### Threat and priorities

- **ForeverDB (30):** Righteous Fury before the pull, then Seal of Fury, Judgement, Holy Strike, and Exorcism on Undead and Demons. Use Retribution Aura on multi-enemy pulls and Devotion Aura on single enemies. Consecration only on real packs, as it is expensive.
- **Wowhead (30):** one target: Seal of Fury, Judgement, Exorcism, Holy Strike, then Consecration if Mana allows. On packs Consecration moves to the front.
- **Icy Veins:** Seal of Fury, Consecration as long as Mana allows, Judgement, Holy Strike, Exorcism. While learning, hold Judgement back for taunting enemies you have lost.

The [WoWSims APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/protection/apls/default.apl.json), built for level 60, prepares Righteous Fury, Retribution Aura and Seal of the Crusader before the pull. It then runs:

1. Judgement
2. Swift Judgement
3. Seal of Fury, if missing
4. Consecration
5. Holy Shock, if talented
6. Holy Shield
7. Holy Strike
8. Exorcism

Opening with a Crusader Judgement before switching to Seal of Fury also appears in Wowhead's advice for Undead and Demons.

### Levelling

Wowhead says the road to 16 is rough, and a two-hander is better until Righteous Fury and Retribution Aura arrive. After 20, sword and board handles the open world better than Retribution. Templar's Bulwark at 30 makes dungeon pulls close to risk-free. ForeverDB's levelling build (Redoubt, Precision, Benediction, then Shield Specialization and Swift Judgement) rarely needs to drink and can tank as it is. Icy Veins starts in Retribution for Pursuit of Justice and cheaper spells. Wowhead notes a beta bug where Consecration sometimes dealt less than full damage at its edge; moving enemies fixed it.

### Gear and consumables

Wowhead's level 30 picks: Painwalker Buckler and Scorn's Icy Choker (Scarlet Monastery), Worgenbane Talisman (Shadowfang Keep), Blacksmithing's Crusader's chain set, and the Enchanting libram Tenets of the Silver Hand. ForeverDB adds Forever's Protector's Silvered Chain Shirt and Leggings and Warder's Belt. Wowhead warns against spell power weapons before 20, as they carry about a 25% melee damage penalty. Icy Veins recommends Lesser Arcane Elixir. WoWSims' level 60 defaults use Flask of Supreme Power, Elixir of Holy Power, Greater Stoneshield Potion and Brilliant Wizard Oil. Icy Veins prefers Dwarf for Stoneform; WoWSims assumes Human.

| Source | Stat order |
|---|---|
| ForeverDB | Defense, Stamina, armour, block value, hit, Strength, spell power, Intellect |
| Icy Veins | Stamina, spell power, Strength, block, hit, Defense, armour, Intellect, Agility |

### Where guides disagree

- **Righteous Fury's threat:** current client data and Blizzard's 15 October notes give 90%. ForeverDB's PvE, builds and levelling pages, checked against an older build, still say 60%. Wowhead says 90%.
- **Judgement:** ForeverDB and WoWSims press it on cooldown; Icy Veins suggests saving it for taunts at first.
- **Damage or survival in row 3–4:** Wowhead takes One-Handed Weapon Specialization for threat. ForeverDB now prefers Improved Righteous Fury, arguing Righteous Fury already covers threat.
- **Talent numbers:** Blizzard's deep dive gives Iron Creed up to 15% threat and Shield Specialization 6% Mana per block. The client tooltips on ForeverDB show 25% and 4%.

## Ledger findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Protection Paladin](https://www.wowhead.com/forever/guide/classes/paladin/protection/level-20-tank-overview): the Retribution-tree tanking build and early tips.
- [Wowhead: Level 30 Protection Paladin](https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview): level 30 routes, priorities, gear and camp buffs.
- [Icy Veins: Protection Paladin Leveling](https://www.icy-veins.com/wow-forever/protection-paladin-leveling): a level-by-level talent order to 60 and stat notes.
- [ForeverDB: Paladin PvE guide](https://foreverdb.net/class/Paladin/pve): tank job, opener, cooldowns and stats.
- [ForeverDB: Paladin talent builds](https://foreverdb.net/class/Paladin/builds): levelling, dungeon and battleground Protection builds with reasons.
- [ForeverDB: Paladin deep dive and the 15 October build](https://foreverdb.net/article/paladin-deep-dive-seals-judgements-holy-strike-protection-retribution): the Seal of Fury and Righteous Fury fixes.
- [WoWSims: Protection Paladin presets](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/protection/presets.ts): level 60 talents and consumables.
- [WoWSims: Protection Paladin APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/protection/apls/default.apl.json): the simulator's priority list.
- [Blizzard: Class Deep Dives, Paladin](https://worldofwarcraft.blizzard.com/en-us/news/24302099): the Protection talent changes.
