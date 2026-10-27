---
updated: 2026-10-27
summary: Priest builds that mix talent trees in WoW Forever, the Smite damage build, Blizzard's "hybrid tax" on damage specs, and playing both healer and damage.
sources: Wowhead, Icy Veins, ForeverDB, WoWSims presets and rotation, Blizzard class deep dive and podcast
---

## At a glance

- **Why mixing is common:** one talent point per level from 10, and each row needs five more points in its own tree. Small dips into a second tree are cheap.
- **The usual dips:** two points in [Wand Specialization](https://foreverdb.net/spell/14524) (Discipline), five in [Spirit Tap](https://foreverdb.net/spell/15270) (Shadow), or a rush to [Meditation](https://foreverdb.net/spell/14521) (Discipline).
- **Endgame mixes:** every WoWSims level 60 Priest preset spends points in two or three trees.
- **Smite:** a Holy damage build that mixes Discipline and Holy. WoWSims has a preset and rotation for it.
- **Hybrid tax:** Blizzard's target is about 5% less damage for hybrid damage specs than for Hunters, Mages, Rogues and Warlocks. Priests count as hybrids.
- **Dual roles:** respec at a class trainer in a major city. Dual Specialization unlocks at level 40 ([Blizzard](https://worldofwarcraft.blizzard.com/en-us/news/24301514)).

## What the guides say

### How the trees allow it

You get 21 talent points at level 30 and 51 at 60. Each row of a tree opens after five more points in that tree ([ForeverDB](https://foreverdb.net/class/Priest/talents)). The Legacy perk Talented grants points up to five levels sooner, which Wowhead and Icy Veins both plan around. Blizzard's Class Highlights video mentions a Discipline dip for Meditation's in-combat mana regeneration. [ForeverDB](https://foreverdb.net/article/class-highlights-druid-warlock-priest) notes that Shadow builds into it for mana.

### Levelling hybrids

| Build | Source | Split at 30 | What the off-tree points buy |
|---|---|---|---|
| Shadow with Wand Specialization | [Wowhead](https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview), [Icy Veins](https://www.icy-veins.com/wow-forever/shadow-priest-ranged-dps-pve-guide) | 2/0/19 | 25% more wand damage, the main finisher while levelling |
| Shadow "Meditation" | Icy Veins | 13/0/8 | Meditation 3/3, so mana keeps returning while you cast |
| Holy "Holy Nova" | [Icy Veins](https://www.icy-veins.com/wow-forever/holy-priest-healer-pve-guide) | 2/14/5 | Wand Specialization plus Spirit Tap's mana after kills |
| Discipline "Deep Discipline" | [Icy Veins](https://www.icy-veins.com/wow-forever/discipline-priest-healer-pve-guide) | 16/0/5 | Spirit Tap, at the cost of Penance |
| Discipline with a Holy start | [Wowhead](https://www.wowhead.com/forever/guide/classes/priest/discipline/level-30-healer-overview) | varies | [Twilight Focus](https://foreverdb.net/spell/14913) and [Divine Fury](https://foreverdb.net/spell/18530) early, then a respec at 20 |

Icy Veins calls Wand Specialization and Spirit Tap the core of every Priest levelling build, and treats Twilight Focus as optional for players who draw aggro. Wowhead's Holy guide warns that two Wand Specialization points leave a level 30 Holy Priest one point short of Spirit of Redemption. ForeverDB's own levelling builds keep all 21 points in one tree.

### Endgame mixes (WoWSims, level 60)

The [WoWSims presets](https://github.com/wowsims/forever/blob/master/ui/specs/priest/healer/presets.ts) are projections for level 60 and have not been played:

- **Shadow (17/0/34):** Meditation, Inner Focus, Twin Disciplines, Silent Resolve, Mental Strength and Martyrdom from Discipline.
- **Discipline (32/19/0):** Holy's Improved Renew, Holy Specialization, Inspiration, Improved Healing and Binding Heal.
- **Holy (16/35/0):** Discipline's Meditation, Improved Power Word: Shield, Inner Focus and Twin Disciplines.
- **Smite (31/17/3):** see below.

### Smite: the Holy damage hybrid

WoWSims' "Smite" preset takes Discipline's [Penance](https://foreverdb.net/spell/402174), [Power in Light](https://foreverdb.net/spell/1309969), Wand Specialization, [Holy Precision](https://foreverdb.net/spell/1309957), Mental Agility, Meditation and Power Infusion. It adds Holy's Twilight Focus, Holy Specialization, Divine Fury, Holy Nova and [Searing Light](https://foreverdb.net/spell/14909), plus three points of Shadow Focus. Its [default rotation](https://github.com/wowsims/forever/blob/master/ui/specs/priest/dps/builds/smite_testing.build.json):

1. Power Infusion just before the pull.
2. Keep [Holy Fire](https://foreverdb.net/spell/14914) burning, dropping to a lower rank when mana is under 20%.
3. Spend a free Holy Nova on three or more targets.
4. Keep Shadow Word: Pain up.
5. Penance on cooldown.
6. [Smite](https://foreverdb.net/spell/585) as filler, again at a lower rank below 20% mana.
7. Wand below 10% mana.

Its stat weights rank mana per 5 highest (1.46), then spell power (1), Holy damage (0.81) and Intellect and Spirit (about 0.58). That shows how much mana limits the build.

For levelling, ForeverDB's Holy Smite builds use Divine Fury and Searing Light. Forever raised Smite's spell power scaling, so it grows with gear ([ForeverDB](https://foreverdb.net/guide/leveling-priest)). Icy Veins and Wowhead open with Holy Fire for the same Power in Light bonus.

### The hybrid tax

On episode 2 of the WoW: Forever Podcast (1 October), the developers set out their position ([ForeverDB's write-up](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)):

- **The target:** hybrid damage specs should do about 5% less damage than Hunters, Mages, Rogues and Warlocks. Every class that can fill more than one role counts as a hybrid, Priests included.
- **Healing counts:** a damage spec that heals while it fights, such as Shadow with Vampiric Embrace, has that healing counted as part of its output.
- **Not the old approach:** one developer said they don't believe in the original-style hybrid tax. The aim is for every role to be competitive, with hybrids missing some tools rather than lagging far behind.
- **An average:** 5% is a target across fights, so a hybrid can still top some fights.
- **Who it covers:** ForeverDB reads it as covering Shadow and, by the same rule, damage-focused Smite builds. The developers didn't list specs one by one.

It is a design target, not a number in the client, and nobody can measure level 60 damage yet. ForeverDB summarises forum reaction: Shadow players worry groups will prefer Mages and Warlocks, and some Smite players asked for a talent that gives up healing to avoid the tax.

### Healer and damage in one character

- **Early dungeons:** Wowhead says Discipline can fill a damage slot because its early talents resemble Shadow's. Its Shadow guide says Shadow can still heal dungeons at 30 with some healing gear. Icy Veins notes Shadow Priests often end up healing because healers are scarce.
- **Shadowform:** from level 40, Shadowform blocks healing spells, so a Shadow Priest's group healing then comes from Vampiric Embrace ([Wowhead](https://www.wowhead.com/forever/guide/classes/priest/shadow/overview-pve-dps)).
- **Switching roles:** respec at a class trainer in a major city. Dual Specialization at 40 lets you keep a healing build and a damage build.
- **By design:** the developers said on the podcast that they avoid giving hybrid damage specs strong healing, so groups still need a healer ([ForeverDB](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)).

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: The hybrid tax in WoW Forever](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): the developers' 5% target, who counts and player reaction
- [ForeverDB: Class Highlights part 3, checked](https://foreverdb.net/article/class-highlights-druid-warlock-priest): Blizzard's video on Priest talents, including the Meditation dip
- [ForeverDB: Levelling a Priest to 30](https://foreverdb.net/guide/leveling-priest): single-tree levelling builds to compare against the hybrids
- [Wowhead: Level 30 Shadow Priest](https://www.wowhead.com/forever/guide/classes/priest/shadow/level-30-dps-overview): the Wand Specialization dip and healing as Shadow
- [Wowhead: Level 30 Holy Priest](https://www.wowhead.com/forever/guide/classes/priest/holy/level-30-healer-overview): the Wand Specialization versus Spirit of Redemption trade-off
- [Blizzard: Class Deep Dives, Priest and Warrior](https://worldofwarcraft.blizzard.com/en-us/news/24301514): talent milestones, respecs and Dual Specialization at 40
- [WoWSims Forever: healer Priest presets](https://github.com/wowsims/forever/blob/master/ui/specs/priest/healer/presets.ts): level 60 Discipline and Holy talent strings
- [WoWSims Forever: Smite rotation build file](https://github.com/wowsims/forever/blob/master/ui/specs/priest/dps/builds/smite_testing.build.json): the Smite talents and priority list
