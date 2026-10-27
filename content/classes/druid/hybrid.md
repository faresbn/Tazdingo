---
updated: 2026-10-27
summary: Druid builds that mix talent trees in WoW Forever, from Spellbear and caster-healers while levelling to the level 60 simulator presets, plus Blizzard's 5% hybrid tax.
sources: ForeverDB (builds, hybrid tax article, levelling guide), Wowhead (Balance and Restoration level 20 and 30 guides, healer overview), Icy Veins, WoWSims presets, Blizzard class deep dive
---

## At a glance

- **Why it's common:** you get one talent point per level from 10, and each row of a tree needs only five points above it. The first two rows of any tree are cheap to reach.
- **The usual borrowings:** from Balance, [Genesis](https://foreverdb.net/spell/1223081) (+5% to periodic damage and healing, bleeds included), [Nature's Majesty](https://foreverdb.net/spell/1223082) (+4% crit to spells and melee), [Nature's Reach](https://foreverdb.net/spell/16819) (+4% hit) and [Improved Wrath](https://foreverdb.net/spell/16814). From Restoration, [Nature's Focus](https://foreverdb.net/spell/17063), [Furor](https://foreverdb.net/spell/17056) and [Naturalist](https://foreverdb.net/spell/17069) (+5% to all damage).
- **Levelling hybrids:** Wowhead's "Spellbear" (spell power gear, Thorns and Swipe in Bear Form) and caster-healers built on Improved Wrath and Nature's Focus.
- **Level 60 presets:** every WoWSims Feral preset spends 9 points in Balance, and the Balance preset spends 13 in Restoration.
- **The limit:** the capstones (Moonkin Form, Berserk, Wild Growth) need 30 points in one tree first, and two capstones can't share 51 points. Dual Specialization at 40 lets you keep two builds instead of one compromise.
- **The hybrid tax:** Blizzard aims for hybrid damage specs to deal about 5% less than pure damage classes, and Balance and Cat count.
- **Healing from a damage build:** Blizzard deliberately keeps hybrid damage specs from healing strongly. Leaving form to heal costs 55% of your base mana to get back in.

## What the guides say

### Why Druids mix trees

Forever's tree puts strong general talents near the top of each section. Blizzard's [deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24301515) moved Heart of the Wild to Feral's first row, Nature's Reach to Balance's second (now with hit for all damaging spells), and Natural Shapeshifter to Restoration. Genesis and Nature's Majesty are new near the top of Balance. Genesis boosts any periodic effect, so it helps a Cat's Rake and Rip and a healer's heals over time alike. ForeverDB's [levelling guide](https://foreverdb.net/guide/leveling-druid) adds two points from Blizzard's deep dive recap: bonus healing now also gives a third as much bonus damage, and caster weapons carry spell damage. Both help a Druid who fights and heals.

### Levelling hybrids

| Build (source) | Level | Points | How it plays |
|---|---|---|---|
| Spellbear ([Wowhead](https://www.wowhead.com/forever/guide/classes/druid/balance/level-20-dps-overview)) | 20 | Feral: Ferocity 5, Feral Instinct 3, Heart of the Wild 2, Savage Fury 1 | Moonfire three or four mobs, put heals over time on yourself, then Bear Form, Demoralizing Roar and Swipe |
| Spellbear ([Wowhead](https://www.wowhead.com/forever/guide/classes/druid/balance/level-30-dps-overview)) | 30 | Balance: Genesis 5, Nature's Majesty 2, Nature's Reach 2. Feral: Ferocity 5, Heart of the Wild 2, Feral Instinct 3, Savage Fury 2 | As above, geared in leather with spell power and Strength |
| Cat damage ([Wowhead](https://www.wowhead.com/forever/guide/classes/druid/feral/level-20-dps-overview)) | 20 | Balance: Genesis 5, Nature's Reach 1. Feral: Ferocity 5 | Most damage at 20, at the cost of travel speed |
| Caster-healer ([ForeverDB](https://foreverdb.net/class/Druid/builds)) | 20 to 30 | Balance: Improved Wrath 5. Restoration: Nature's Focus 5, Naturalist 1, rising to Naturalist 5, Reflection 3, Gift of Nature 2 and Swiftmend 1 at 30 | Moonfire then fast, cheap Wraths; Swiftmend your own Rejuvenation in an emergency |
| Caster with Nature's Focus ([Icy Veins](https://www.icy-veins.com/wow-forever/balance-druid-ranged-dps-pve-guide)) | 30 | 16 Balance points plus Nature's Focus 5 | A levelling Balance build with pushback protection |
| "The Splendid" healer ([Wowhead](https://www.wowhead.com/forever/guide/classes/druid/restoration/level-20-healer-overview)) | 20 | Balance only: Improved Wrath 3, Genesis 5, Nature's Majesty 2, Nature's Splendor 1 | Damage talents that also help healing: Genesis boosts heals over time and Nature's Splendor lengthens them |
| "Deep Balance" healer ([Wowhead](https://www.wowhead.com/forever/guide/classes/druid/restoration/level-30-healer-overview)) | 30 | 21 Balance points (Genesis, Moonglow, Improved Entangling Roots, Insect Swarm and more) | Insect Swarm everything, root mobs away from the tank, heal in between |

Icy Veins' [Restoration guide](https://www.icy-veins.com/wow-forever/restoration-druid-healer-pve-guide) describes a similar "World Content" healer. It takes Improved Wrath, then Nature's Focus, then Insect Swarm, and spends everything after that in Restoration. Wowhead's level 30 Balance guide calls Spellbear the highest-performing levelling build it found from 20 to 30. Its level 20 guide is cooler, saying Spellbear trails a pure Feral setup for either role. Wowhead also lists Spellbear-only loot, such as the Twilight Maul and the Spiked Shell Band from Blackfathom Deeps.

### Dual-role builds at 60

WoWSims publishes its level 60 talent presets in each spec's presets.ts:

- **Cat, 9/35/7** ([feralcat](https://github.com/wowsims/forever/blob/master/ui/specs/druid/feralcat/presets.ts)): Genesis, Nature's Majesty and Nature's Reach in Balance, plus Furor 5 and Naturalist 2 from Restoration. The file notes it takes Naturalist rather than Natural Shapeshifter.
- **Bear, 9/38/4** ([feralbear](https://github.com/wowsims/forever/blob/master/ui/specs/druid/feralbear/presets.ts)): the same Balance points and Furor 4, with Thick Hide and Feral Instinct in Feral.
- **Hybrid, 9/42/0:** offered in both the Cat and Bear simulators. It keeps the bear talents (Thick Hide, Feral Instinct) and the cat ones (Improved Shifting Power, both points of Blood Frenzy), with nothing in Restoration.
- **Moonkin, 38/0/13** ([balance](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/presets.ts)): Nature's Focus 5, Naturalist 5 and Reflection 3 from Restoration, for damage and mana.

Healers face a harder trade. Wowhead's [healer overview](https://www.wowhead.com/forever/guide/classes/druid/restoration/overview-pve-healer) points out that [Nature's Grace](https://foreverdb.net/spell/16880) (21 points into Balance) and [Wild Growth](https://foreverdb.net/spell/408120) (31 into Restoration) can't both fit. It calls Genesis an easy pick for any build and Heart of the Wild strong for little investment.

### Feral with restoration utility

No guide publishes a Feral build that reaches deep Restoration utility. [Nature's Swiftness](https://foreverdb.net/spell/17116) alone needs 20 Restoration points. What Ferals borrow from Restoration is Furor (Rage and Energy on shifting) and Naturalist (damage). The utility comes from leaving form instead. Wowhead's Feral overview expects you to be ready to tank if the tank dies, or to shift out and heal while the healer drinks. Every Druid keeps Rebirth, Revive, Remove Curse, Abolish Poison, and Innervate from 40. Within Feral, [Natural Instinct](https://foreverdb.net/spell/1223242) adds spell healing equal to 25% of your Intellect, by its client text. Blizzard has otherwise said it is deliberately not giving hybrid damage specs strong healing. Asked whether Ferals would get bonus healing, the developers said no ([ForeverDB](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)).

Before 40 you have one build, changed at a class trainer. ForeverDB notes the beta charged 1 silver, with more for a quick repeat, and Blizzard called that beta-only. Icy Veins says the cost rises each time. Launch prices aren't known.

### The hybrid tax

ForeverDB's [write-up](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids) of episode 2 of Blizzard's WoW: Forever Podcast (1 October) is the main source:

- **The target:** hybrid damage specs should deal about 5% less damage than the pure classes: Hunter, Mage, Rogue and Warlock. Anyone who can fill more than one role must, in the developers' words, "pay just a little bit for it".
- **Who it covers:** Blizzard didn't list specs. ForeverDB reads it as Balance and Feral Cat for Druids, and Warriors count too because they can tank.
- **What it isn't:** a number in the client or the patch notes. It's a design target, averaged across fights, so a hybrid can still shine on some fights. ForeverDB illustrates it as 950 damage per second against a pure class's 1,000.
- **Healing counts:** for a damage spec that also heals, that healing counts as part of its output.
- **The budget:** Blizzard says it raised hybrid budgets so they aren't weak, but each buff costs something. The Wrath buff should add about 2% Druid damage at 60 and may be balanced by a cut elsewhere.
- **Player reaction:** Druid players worry their mana already has to cover both damage and healing. One forum thread argues Druids, as the most flexible class, should do the least damage. Others call a 5% gap too small to matter.

Blizzard's deep dive frames the same trade in utility terms: Druids can fill any role, but lack snares, silences, interrupts and reliable crowd control. Above the level 30 beta cap, nobody has measured the gap.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: The hybrid tax in WoW Forever](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): Blizzard's 5% target, who it covers and how players reacted
- [ForeverDB: Druid talent builds](https://foreverdb.net/class/Druid/builds): the caster-healer and other mixed builds, point by point
- [Wowhead: Level 30 Balance Druid guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-30-dps-overview): Spellbear builds, rotation and Spellbear-only loot
- [Wowhead: Level 20 Balance Druid guide](https://www.wowhead.com/forever/guide/classes/druid/balance/level-20-dps-overview): the first Spellbear build
- [Wowhead: Level 20 Feral DPS guide](https://www.wowhead.com/forever/guide/classes/druid/feral/level-20-dps-overview): the Balance-dipping Cat build at 20
- [Wowhead: Level 20 Restoration guide](https://www.wowhead.com/forever/guide/classes/druid/restoration/level-20-healer-overview): "The Splendid", a healer in the Balance tree
- [Wowhead: Level 30 Restoration guide](https://www.wowhead.com/forever/guide/classes/druid/restoration/level-30-healer-overview): Deep Resto against Deep Balance
- [Blizzard: Class Deep Dives — Hunter and Druid](https://worldofwarcraft.blizzard.com/en-us/news/24301515): which talents moved between rows and trees
- [WoWSims: Feral Cat presets.ts](https://github.com/wowsims/forever/blob/master/ui/specs/druid/feralcat/presets.ts): the Cat and Hybrid talent presets
- [WoWSims: Feral Bear presets.ts](https://github.com/wowsims/forever/blob/master/ui/specs/druid/feralbear/presets.ts): the Bear and Hybrid talent presets
- [WoWSims: Balance presets.ts](https://github.com/wowsims/forever/blob/master/ui/specs/druid/balance/presets.ts): the Moonkin preset with its Restoration points
