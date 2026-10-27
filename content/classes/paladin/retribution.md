---
updated: 2026-10-27
summary: Retribution Paladin in WoW Forever: the two-handed damage spec's talents by level, rotation compared across guides and the WoWSims priority lists, levelling, gear and where guides disagree.
sources: ForeverDB, Wowhead Level 20 and 30 guides, Icy Veins, WoWSims presets and APLs, Blizzard Paladin deep dive
---

## At a glance

- **Role:** melee damage with a slow two-handed weapon, plus group utility.
- **How it plays:** keep a damage Seal up (Seal of Command or Seal of Righteousness), and press Judgement and Holy Strike on cooldown. Add Consecration on packs and Exorcism on Undead and Demons. Twist of Light at 40 brings back seal twisting.
- **Strengths:** good single-target damage, self-healing, Blessings and auras, and several immunities. Icy Veins calls it very efficient for levelling.
- **Weaknesses:** no interrupt, no slow, little range, a small Mana pool and no major damage cooldown ([Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/retribution/overview-pve-dps)).
- **Stats that matter:** weapon damage first, then Strength, hit and crit. Spell power matters more than in Classic, because Seals, Judgement and Holy Strike scale with it.
- **New in Forever:** [Holy Strike](https://foreverdb.net/spell/679), [Sacred Arbiter](https://foreverdb.net/spell/1311087), [Sanctified Judgement](https://foreverdb.net/spell/1311074), [Holy Conduit](https://foreverdb.net/spell/1237268), [Champion of the Light](https://foreverdb.net/spell/1311084), [Instrument of Law](https://foreverdb.net/spell/1311085) and [Twist of Light](https://foreverdb.net/spell/1310735).

## What the guides say

### Tazdingo recommendation

Use **a strong slow two-hander with a sustainable Seal/Judgement/Holy Strike loop** before adding costly area damage. Seal of Command versus Righteousness depends on weapon speed, spell power and current tuning; neither is universally best at every level ([Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-30-dps-overview)). Skip a costly finishing spell when the next auto attack is enough. Vengeance favours damage, while Repentance buys control: choose for the encounter. Shockadin and Twist of Light are different builds and mana budgets, not interchangeable rotations. The [later official notes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696/6) reduce Champion of the Light to **10/20/30% of Intellect as spell damage**, superseding the 60% figure.

Champion of the Light (35) and Twist of Light (40) were out of reach in the beta without Legacy points; their value is projection.

### What's different in Forever

From Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24302099):

- **Judgement** no longer uses up your Seal, so you Judge on cooldown.
- **Sacred Arbiter** (16 points) adds 20% to Holy Strike and makes it refresh every Judgement on the target, even other Paladins'.
- **Sanctified Judgement** refunds up to 60% of the judged Seal's cost.
- **[Vengeance](https://foreverdb.net/spell/20049)** now gives 3% damage per stack, up to three stacks, for 30 sec after a crit.
- **Instrument of Law** makes Hammer of Wrath instant and cuts your threat by 20% while Righteous Fury is off, so you can still turn it on to off-tank.
- **Twist of Light** (31 points) makes a replaced damage Seal leave an Echo that also applies on your next swing. Blizzard calls it a more forgiving take on seal twisting.
- **Holy Shock** sits in Holy as an alternative for a hybrid "Shockadin" (see the hybrid page).

### Talents by level

| Level | Source | Build |
|---|---|---|
| 20 | [ForeverDB](https://foreverdb.net/class/Paladin/builds), [Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-20-dps-overview) | Benediction 5, Improved Judgement 2, Conviction 3, [Seal of Command](https://foreverdb.net/spell/20375) 1 |
| 20 | Wowhead "Shockadin" | Holy only: Divine Strength 5, Divine Intellect 3, Improved Seals 3. Wowhead rated it stronger in PvE at 20. |
| 30 | ForeverDB levelling | the 20 build plus Conviction 5, Sanctified Judgement 3, Pursuit of Justice 2, Vindication 1, Sacred Arbiter 1, Vengeance 1 |
| 30 | [Wowhead](https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-30-dps-overview) | as ForeverDB, but Holy Conduit 1 instead of Vindication |
| 30 | Icy Veins | Benediction 5, Improved Judgement 2, Holy Conduit 2, Conviction 4, Sanctified Judgement 3, Seal of Command 1, Pursuit of Justice 2, Sacred Arbiter 1, Repentance 1 |
| 10–60 | [Icy Veins levelling](https://www.icy-veins.com/wow-forever/retribution-paladin-leveling) (projection) | Champion of the Light and Twist of Light by 40; ends 16 Holy (Divine Strength, Divine Intellect, Improved Seals, Reverence), 35 Retribution |
| 60 | [WoWSims Twist of Light](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/presets.ts) | 16 Holy (the same four talents), 35 Retribution including Champion of the Light 3, Instrument of Law 2, Twist of Light |
| 60 | WoWSims Holy Shock | 23 Holy (adds Purifying Power, Infusion of Light, Divine Favor, Holy Shock, Consecrated Ground), 28 Retribution (no Seal of Command or Twist of Light) |

With Legacy points, Wowhead and Icy Veins both finish Vengeance and add a point of Champion of the Light.

### Rotation and priorities

- **ForeverDB's level 30 sim card** ([PvE guide](https://foreverdb.net/class/Paladin/pve)): Seal of the Crusader and its Judgement, then Judgement on cooldown, Seal of Command kept up, and Holy Strike as the filler. The sim credits Judgement with 48% of damage, Seal of Command 34.5% and Holy Strike 19.7%. ForeverDB flags that its Seal of Command proc rate is Classic's, since the client doesn't give one.
- **Wowhead:** Judge Seal of the Crusader on long fights, keep your main Seal up, then Judgement and Holy Strike on cooldown (it suggests one macro for both). Add Consecration on packs, Exorcism on Undead and Demons, and Hammer of Justice on dangerous enemies.
- **Icy Veins:** the same core. Stun with Hammer of Justice or Repentance before a Seal of Command Judgement, which nearly doubles against stunned or incapacitated targets.

The [WoWSims default APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/apls/default.apl.json) is built for level 60 with Twist of Light. It Judges between swings, uses Hammer of Wrath when instant, and presses Holy Strike right after each Judgement. It keeps swapping Seal of Command and Seal of Righteousness to keep Echoes going, and only fits in Consecration or Exorcism between swings. The [Holy Shock APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/apls/holy_shock.apl.json) adds Divine Favor into Holy Shock after Holy Strike.

### Levelling

ForeverDB and Icy Veins both rate Retribution the quickest Paladin to level. Icy Veins advises turning leftover Mana into health with Holy Light instead of drinking, and skipping Judgement or Holy Strike when an auto attack will finish the enemy.

### Gear and consumables

Weapon first. Wowhead and Icy Veins list Corpsemaker (Razorfen Kraul), Manual Crowd Pummeler (Gnomeregan) and Strike of the Hydra (Blackfathom Deeps). Wowhead says Seal of Command suits weapons of about 3.0 speed or slower, and Seal of Righteousness everything else. Icy Veins puts Seal of Righteousness at 22% of spell power per hit with a two-hander, against 20.3% on Seal of Command's procs. ForeverDB's sim ranks Bear Brisket (+1.7%) and Scroll of Strength II (+1.5%) as the best level 30 consumables; Icy Veins adds Lesser Arcane Elixir and Lesser Wizard Oil.

| Source | Stat order |
|---|---|
| ForeverDB | weapon DPS > Strength > hit > crit > Agility > Stamina > Intellect |
| Icy Veins | weapon DPS > hit and expertise > crit > spell power > Strength > Intellect > Agility > Stamina |
| ForeverDB sim, level 30 | Strength 2, hit rating 1.45, Agility 1.07 (attack power = 1) |
| WoWSims, level 60 | Twist of Light values haste far above everything, then hit and crit. Holy Shock values hit, spell damage, crit and Intellect. |

### Where guides disagree

- **Seal of Command at 20:** ForeverDB makes it your main Seal. Wowhead said at 20 it wasn't clearly better than a spell-power-boosted Seal of Righteousness. Icy Veins says it depends on weapon speed and spell power.
- **Row 5 at 30:** Wowhead and ForeverDB take Vengeance; Icy Veins takes Repentance for crowd control.
- **Shockadin:** Wowhead skips it at 30 because of Mana. Icy Veins offers an all-Holy alternative, and WoWSims has a level 60 Holy Shock preset.
- **Spell power or melee gear:** Wowhead calls the shift to spell power divisive, and says some seal-twisters find Twist of Light a let-down.
- **Champion of the Light — resolved:** [16 October official notes](https://us.forums.blizzard.com/en/wow/t/wow-forever-beta-development-notes-%E2%80%93-updated-october-26/2360696/6) specify 10/20/30% of Intellect as spell damage. Older 20/40/60% client or guide values are superseded.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 20 Retribution Paladin](https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-20-dps-overview): the Shockadin and Seal of Command builds at 20.
- [Wowhead: Level 30 Retribution Paladin](https://www.wowhead.com/forever/guide/classes/paladin/retribution/level-30-dps-overview): level 30 build, Legacy points, dungeon gear and camp buffs.
- [Icy Veins: Retribution Paladin Leveling](https://www.icy-veins.com/wow-forever/retribution-paladin-leveling): a talent order to 60 and the Seal of Command or Righteousness maths.
- [ForeverDB: Paladin PvE guide](https://foreverdb.net/class/Paladin/pve): group role, stats, the level 30 sim card and damage split.
- [ForeverDB: Paladin talent builds](https://foreverdb.net/class/Paladin/builds): levelling, group and PvP Retribution builds with reasons.
- [WoWSims: Retribution presets](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/presets.ts): Twist of Light and Holy Shock talents, weights and consumables.
- [WoWSims: default APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/apls/default.apl.json) and [Holy Shock APL](https://github.com/wowsims/forever/blob/master/ui/specs/paladin/retribution/apls/holy_shock.apl.json): the simulator's priority lists.
- [Blizzard: Class Deep Dives, Paladin](https://worldofwarcraft.blizzard.com/en-us/news/24302099): the Retribution talent changes and Twist of Light.
