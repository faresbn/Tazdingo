---
updated: 2026-10-30
summary: How Shadow Priest plays in WoW Forever, the guides' talent builds at 20, 30 and 60, and how their rotations compare with the simulators.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and rotation, Blizzard class deep dive
---

## Cheatsheet

- **Pick it for:** ranged damage over time with party healing from Vampiric Embrace; strong one-on-one PvP, but the identity arrives late (Mind Flay 20, Shadowform 40).
- **Levelling build:** at 30, Wowhead (2/0/19): Wand Specialization 2, Spirit Tap 5, Improved Shadow Word: Pain 2, Shadow Focus 5, Mind Flay, Improved Mind Flay 2, Vampiric Embrace, Shadow Weaving 3 ([Wowhead](https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview)). ForeverDB goes all Shadow; Icy Veins also has a 13/0/8 Meditation build.
- **Build at 60:** projection only: WoWSims' "Standard" (17/0/34) takes Shadowform, Darkness 5, Dark Inspiration 5, Devouring Contagion 2, Shadow Weaving 3, Vampiric Embrace and Improved Mind Blast 5, plus Discipline's Meditation 3, Inner Focus and Twin Disciplines 5; no Spirit Tap or Early Demise ([WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/priest/dps/presets.ts)).
- **Priority:** at 30 (Wowhead), Mind Blast to open, Shadow Word: Pain, Devouring Plague if available, Mind Flay only if mana allows, then the wand. At 60 (WoWSims), Shadowform, Shadow Word: Pain up, Devouring Plague whenever it isn't ticking, Mind Blast, [Shadow Word: Death](https://foreverdb.net/spell/1309595) on cooldown, Mind Flay filler.
- **Stats:** spell power first; ForeverDB then hit, Intellect, crit, while Icy Veins (levelling) puts crit before hit. WoWSims at 60: hit 1.14, spell power 1, crit 0.84, haste 0.73. ForeverDB's level-30 sim values Intellect far higher; treat both as bracket-specific ([ForeverDB](https://foreverdb.net/class/Priest/pve)).
- **Key levels:** 20 [Mind Flay](https://foreverdb.net/spell/15407) · about 24 Mind Flay starts to earn its mana over the wand (Wowhead) · 32 Shadow Word: Death · 35 Early Demise · 40 [Shadowform](https://foreverdb.net/spell/15473).
- **Gear and consumables:** Tailoring and Enchanting in every source. ForeverDB's sim rates Scroll of Intellect II (+6.3%) and Elixir of Wisdom (+5.7%) best at 30 ([ForeverDB](https://foreverdb.net/class/Priest/pve)); Icy Veins lists Lesser Wizard Oil, Spellblasting Potion and mana potions.
- **Watch out:** Wowhead still offers Shadow Affinity (now Improved Mind Blast) and gives one-minute Devouring Plague and Vampiric Embrace cooldowns; the final client shows 24 and 30 sec ([ForeverDB](https://foreverdb.net/article/build-1-60-1-70425-game-files)). Shadow Word: Death hurts you if the target survives. ForeverDB's sim dropping Devouring Plague is a lead to test.

## What the guides say

### Tazdingo recommendation

**Use the wand to conserve mana while levelling**, rather than filling every spare moment with Mind Flay. Cast more when damage, safety or the group's pace warrants it; on short-lived targets, a full set of damage-over-time spells may not repay its mana. A single-target level-30 model dropping Devouring Plague does not prove the spell is bad on a durable target or with Devouring Contagion ([Wowhead](https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview)). At 60, compare damage with equal buffs, target lifetime and mana support. Shadow Word: Death also risks self-damage when the target survives; a damage-maximising preset is not a safety recommendation.

### Talents

| Level | Build | Points |
|---|---|---|
| 20 | ForeverDB "Spirit Tap and Mind Flay" | Spirit Tap 5, Shadow Focus 1, Improved Shadow Word: Pain 2, Shadow Reach 2, Mind Flay 1 |
| 30 | ForeverDB "Vampiric Embrace" (all Shadow) | the level 20 build plus Improved Mind Blast 5, Vampiric Embrace, Shadow Weaving 3, Devouring Contagion 1 |
| 30 | Wowhead (2/0/19) | Wand Specialization 2; Spirit Tap 5, Improved Shadow Word: Pain 2, Shadow Focus 5, Mind Flay, Improved Mind Flay 2, Vampiric Embrace, Shadow Weaving 3 |
| 30 | Icy Veins "Deep Shadow" (2/0/19) | Wand Specialization 2; Spirit Tap, Improved Shadow Word: Pain, Improved Mind Blast, Mind Flay, Improved Mind Flay, Shadow Reach 1, Vampiric Embrace, Dark Inspiration 3 |
| 30 | Icy Veins "Meditation" (13/0/8) | rushes [Meditation](https://foreverdb.net/spell/14521) 3/3 in Discipline, with Wand Specialization, Spirit Tap, Improved Shadow Word: Pain 2 and Improved Mind Blast 1 |
| 60 | WoWSims "Standard" (17/0/34) | Shadowform, Darkness 5, Devouring Contagion 2, Dark Inspiration 5, Shadow Weaving 3, Vampiric Embrace, Improved Mind Blast 5, Improved Mind Flay 2, Shadow Focus 5; in Discipline, Meditation 3, Inner Focus, Twin Disciplines 5 |

The WoWSims level 60 build takes no Spirit Tap, Silence or Early Demise. For Legacy points, Wowhead adds Devouring Contagion and Improved Mind Blast. Icy Veins adds Dark Inspiration, Devouring Contagion and Shadow Weaving.

### Rotation: the guides

- **Wowhead (level 30):** Mind Blast to open, then Shadow Word: Pain, Devouring Plague if available, Mind Flay only if mana allows, then the wand. In dungeons, put Shadow Word: Pain on every enemy, but watch mana and threat with Mind Blast.
- **Icy Veins:** shield, then Mind Blast to pull, Devouring Plague, Shadow Word: Pain and Mind Flay, then the wand. Drop Devouring Plague if mana runs short.
- **ForeverDB:** at 30, open with Vampiric Embrace, then Shadow Word: Pain, Mind Blast whenever ready and Mind Flay as filler to keep [Shadow Weaving](https://foreverdb.net/spell/15257) stacked. Add Devouring Plague on tough enemies. Against packs, put the plague on the enemy that will die first so Devouring Contagion carries it on ([ForeverDB](https://foreverdb.net/guide/leveling-priest)).

### Rotation: the simulators

**WoWSims (level 60 default list):** cast Mind Blast before the pull, then:

1. Shadowform if missing.
2. Dark Sacrifice below 2,000 mana (Undead only).
3. Racial burst and other cooldowns.
4. Keep Shadow Word: Pain up.
5. Devouring Plague whenever it isn't ticking.
6. Mind Blast.
7. Shadow Word: Death, on cooldown.
8. Inner Focus paired with Mind Flay, then Mind Flay as the filler.

Vampiric Embrace and Starshards are in the list but switched off by default.

**ForeverDB's simulator (level 30, one target, 60 sec):** keep Shadow Word: Pain up about 79% of the time. Use Starshards (Night Elf) and Mind Blast on cooldown, and the wand only when out of mana ([ForeverDB](https://foreverdb.net/class/Priest)). It found 4.9% more damage without Devouring Plague and 3.9% more without Mind Flay. ForeverDB itself flags this as a lead to test, since its own guide disagrees.

The damage priorities favour Shadow Word: Pain and Mind Blast when the target lives long enough and mana permits; levelling advice also relies on wanding. They split on two points:

- **Devouring Plague:** the guides use it when mana allows, ForeverDB's level 30 simulator drops it, and WoWSims keeps it running at 60.
- **Shadow Word: Death:** Wowhead treats it as an execute below 20% health with Early Demise. WoWSims casts it on cooldown and skips Early Demise.

### Levelling

Wowhead finds Mind Flay rarely worth its mana over the wand before about level 24. It also restarts the five-second rule and suffers pushback. [Spirit Tap](https://foreverdb.net/spell/15270) needs your killing blow, or an enemy dying with your Vampiric Embrace on it. Wowhead notes that Vampiric Embrace has two jobs, healing the party for 30 sec or setting up Spirit Tap on an add, and you sometimes have to choose. Icy Veins advises casting your spells together and then wanding, so the five-second timer runs out sooner.

### Gear and consumables

- **Stat order:** Icy Veins (levelling) gives spell power, critical strike, hit, Intellect, Stamina, mana per 5, with hit rising at endgame. ForeverDB's order is spell power, hit, Intellect, crit, Spirit, Stamina.
- **WoWSims weights (level 60):** hit 1.14, spell power 1, crit 0.84, haste 0.73, Intellect 0.24.
- **ForeverDB's level 30 simulator** values Intellect at 3.04 spell power. That is far above WoWSims' level 60 figure, so treat both as bracket-specific.
- **Why spell power matters:** Mind Blast now gains 0.429 of spell power and Shadow Word: Pain 0.2, both higher than Classic ([ForeverDB](https://foreverdb.net/class/Priest/pve)). Icy Veins says lower base damage is offset by more spell power on gear.
- **Consumables:** ForeverDB's simulator rates Scroll of Intellect II (+6.3%) and Elixir of Wisdom (+5.7%) best at 30. At 20 to 29 it rates Lesser Arcane Elixir and Briny Seafood Stew best. Icy Veins lists Lesser Wizard Oil, Spellblasting Potion and mana potions. WoWSims' level 60 default uses Flask of Supreme Power, Elixir of Shadow Power, Greater Arcane Elixir, Brilliant Wizard Oil and Major Spellblasting Potion.
- **Professions:** Tailoring and Enchanting in every source.

### Where guides disagree or are unsure

- Wowhead's level 30 guide offers Shadow Affinity as an option. That talent became Improved Mind Blast on 16 October ([ForeverDB](https://foreverdb.net/article/build-1-60-1-70425-game-files)).
- Wowhead's overview gives one-minute cooldowns for Devouring Plague and Vampiric Embrace and 15 sec for Shadow Word: Death. The final client shows 24, 30 and 18 sec.
- Shadow Word: Death (32), Early Demise (35) and Shadowform (40) are above the beta cap and untested.

## Field findings

Nothing recorded yet.

## Read more

- [Wowhead: Level 30 Shadow Priest](https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview): build reasoning, Mind Flay and Vampiric Embrace advice
- [ForeverDB: Priest PvE guide](https://foreverdb.net/class/Priest/pve): simulator tips, stat values and consumables by bracket
- [ForeverDB: Levelling a Priest to 30](https://foreverdb.net/guide/leveling-priest): Shadow levelling builds and pack tactics
- [ForeverDB: Build 1.60.1.70425 changes](https://foreverdb.net/article/build-1-60-1-70425-game-files): the 16 October Shadow rework
- [ForeverDB: The hybrid tax](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): why Shadow's healing counts against its damage
- [Blizzard: Class Deep Dives, Priest and Warrior](https://worldofwarcraft.blizzard.com/en-us/news/24301514): design notes on Shadowform, Shadow Weaving and Vampiric Embrace
- [WoWSims Forever: Priest DPS presets](https://github.com/wowsims/forever/blob/master/ui/specs/priest/dps/presets.ts): level 60 talents, stat weights and consumables
- [WoWSims Forever: Shadow rotation build file](https://github.com/wowsims/forever/blob/master/ui/specs/priest/dps/builds/testing.build.json): the default priority list
