---
updated: 2026-10-27
summary: Shaman builds that mix talent trees in WoW Forever, Blizzard's "hybrid tax" on Elemental and Enhancement, and off-healing or off-tanking alongside your main role.
sources: Wowhead, ForeverDB, WoWSims presets, Blizzard class deep dive and podcast
---

## Cheatsheet

- **Why mixing is common:** one talent point per level from 10, and each row needs five more points in its own tree. Blizzard also moved some talents up on purpose so other specs can reach them.
- **Designed dips:** Blizzard placed Elemental Devastation to tempt Enhancement into Elemental. It placed Mindfulness and Natural Grace so Elemental can reach them in Restoration.
- **Levelling mixes:** Wowhead's "Mana Management" Elemental build and "Solo Levelling" Restoration build both spend points outside their own tree.
- **Endgame mixes:** WoWSims' level 60 Elemental preset is 32/11/8 and its Enhancement preset 19/32/0.
- **Hybrid tax:** Blizzard's target is about 5% less damage for hybrid damage specs than for pure classes. Shamans count as hybrids.
- **Dual roles:** every spec can off-heal with Healing Wave. Enhancement can hold threat briefly in small groups. Dual Specialization unlocks at level 40.

## What the guides say

### Tazdingo recommendation

Use the mana-focused hybrid when **downtime or occasional healing is costing more than an earlier damage talent would gain**. Use a deep tree when reaching its key talent is the priority. Compare builds at the same level and Legacy-point allowance: 21 ordinary points and 26 points are not equivalent. The [level-30 guides](https://www.wowhead.com/forever/guide/classes/shaman/elemental/level-30-dps-overview) support those different jobs; a level-60 preset is a separate projection. The hybrid damage target applies to class design, not an extra penalty for spending points in a second tree. Emergency Shaman tanking also lacks a taunt and is not a substitute for an agreed dungeon tank.

### Blizzard built the trees for it

Blizzard's [Mage and Shaman deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24302097) explains several placements in terms of other specs:

- [Elemental Devastation](https://foreverdb.net/spell/30160) moved to row 2 mainly to give Enhancement a reason to spend points in Elemental.
- [Mindfulness](https://foreverdb.net/spell/1223033) sits in Restoration's row 2 so Elemental can reach it for mana regeneration while casting.
- [Natural Grace](https://foreverdb.net/spell/29187) moved up to row 2 for the same reason. It now lowers threat from all spells.
- [Thundering Strikes](https://foreverdb.net/spell/16255) now raises critical chance with spells as well as weapon attacks. WoWSims' Elemental preset takes all five ranks.

Talents can be reset at a class trainer in a major city, and Dual Specialization unlocks at level 40 ([Blizzard](https://worldofwarcraft.blizzard.com/en-us/news/24301514)).

### Levelling hybrids

| Build | Source | Split at 30 | What it does |
|---|---|---|---|
| Elemental "Mana Management" | [Wowhead](https://www.wowhead.com/forever/guide/classes/shaman/elemental/level-30-dps-overview) | 0/10/11 | Enhancement's Thundering Strikes, [Mental Dexterity](https://foreverdb.net/spell/415140) and Improved Ghost Wolf; Restoration's [Tidal Focus](https://foreverdb.net/spell/16179), Mindfulness and [Water Shield](https://foreverdb.net/spell/408510) |
| Restoration "Solo Levelling" | [Wowhead](https://www.wowhead.com/forever/guide/classes/shaman/restoration/level-30-healer-overview) | 10/0/11 | Mindfulness and Water Shield first, then Elemental's Concussion, Elemental Alacrity and Convection for damage while questing |
| Enhancement with a Restoration point | [Wowhead](https://www.wowhead.com/forever/guide/classes/shaman/enhancement/level-30-dps-overview) | 0/25/1 (26 points) | the Legacy build adds one point of Tidal Focus |

Wowhead describes the Mana Management build as playing like a melee and caster hybrid. You fight in melee with an imbued weapon, use shocks and Fire Nova, and lean on Restoration's mana talents. It suggests switching to Deep Elemental once Lava Burst or Elemental Mastery are within reach, then working back to Mindfulness and Water Shield. With Legacy points it adds [Shamanistic Focus](https://foreverdb.net/spell/1223030) and Elemental Weapons. Wowhead's Enhancement guide also mentions putting points into Restoration to afford more Fire Nova in dungeons and to heal when needed.

### Endgame mixes (WoWSims, level 60)

These presets are simulator projections for level 60 and have not been played:

- **Elemental (32/11/8):** Thundering Strikes 5, Ancestral Knowledge 3, Improved Ghost Wolf 2 and Shamanistic Focus in Enhancement. Tidal Focus 5 (for hit) and Mindfulness 3 in Restoration ([build file](https://github.com/wowsims/forever/blob/master/ui/specs/shaman/elemental/builds/testing.build.json)).
- **Enhancement (19/32/0):** Concussion 5, Elemental Devastation 3, Reverberation 5, Call of Flame 3, Elemental Focus and Trial by Fire 2 in Elemental ([presets](https://github.com/wowsims/forever/blob/master/ui/specs/shaman/enhancement/presets.ts)). That is the cross-tree path Blizzard said Elemental Devastation was moved for.
- **Restoration:** no default talents yet.

### The hybrid tax

On episode 2 of the WoW: Forever Podcast (1 October), the developers set out their position ([ForeverDB's write-up](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids)):

- **The target:** hybrid damage specs should do about 5% less damage than Hunters, Mages, Rogues and Warlocks. Any class that can fill more than one role counts as a hybrid. ForeverDB reads that as covering Elemental and Enhancement; the team didn't list specs one by one.
- **An average:** it is a target across fights, so a hybrid can still lead on some.
- **Missing tools, not a big gap:** the team wants every role competitive, with hybrids lacking some tools pure classes have.
- **Trade-offs:** each class has a damage budget, so a buff to a hybrid will likely be balanced by a cut elsewhere.

The same episode explains why Enhancement can't heal much mid-fight. The developers said they deliberately avoid giving hybrid damage specs strong healing. That is why [Maelstrom Weapon](https://foreverdb.net/spell/408498) speeds up only Lightning Bolt, which the client confirms ([ForeverDB](https://foreverdb.net/article/wow-forever-podcast-2-class-design)). They also said Shamans cleave only by spending mana, unlike Warriors.

The 5% is a design target, not a number in the client, and level 60 damage can't be measured yet.

### Healer, damage and tank in one character

- **Off-healing:** ForeverDB notes every spec can heal in an emergency with Healing Wave and resurrect with Ancestral Spirit ([ForeverDB](https://foreverdb.net/class/Shaman/pve)). Wowhead says an Elemental with the mana build heals levelling groups nearly as well as a dedicated healer at 30. Its Enhancement guide suggests using heals to support the healer or to turn spare mana into health.
- **Off-tanking:** Blizzard designed [Spirit Weapons](https://foreverdb.net/spell/16268) to cut threat normally but raise it by 30% with Rockbiter Weapon. [Improved Stormstrike](https://foreverdb.net/spell/1223031) can reset Stormstrike on a dodge or parry. Together they let Enhancement act as a temporary tank in small groups. Shamans still have no taunt; [Stoneclaw Totem](https://foreverdb.net/spell/5730) can only pull nearby enemies onto itself for 15 sec ([ForeverDB](https://foreverdb.net/article/marcelian-flame-most-fun-classes)).
- **Totems belong to the class:** Wowhead notes the totems are the same in every spec, so a raid can take whichever Shaman spec performs best.
- **Switching roles:** Wowhead's Restoration guide treats Restoration as a Dual Specialization pick at 40, with Enhancement for levelling.

## Field findings

Nothing recorded yet.

## Read more

- [Blizzard: Class Deep Dives, Mage and Shaman](https://worldofwarcraft.blizzard.com/en-us/news/24302097): the talent placements Blizzard made for cross-spec builds
- [ForeverDB: The hybrid tax in WoW Forever](https://foreverdb.net/article/blizzard-hybrid-tax-5-percent-warriors-count-as-hybrids): the 5% target, who counts and player reaction
- [ForeverDB: Podcast episode 2, class design](https://foreverdb.net/article/wow-forever-podcast-2-class-design): Maelstrom Weapon, healing in damage specs and cleave
- [ForeverDB: Marcelian&Flame's fun classes, checked](https://foreverdb.net/article/marcelian-flame-most-fun-classes): Enhancement off-tanking and its threat tools
- [Wowhead: Level 30 Elemental Shaman](https://www.wowhead.com/forever/guide/classes/shaman/elemental/level-30-dps-overview): the Mana Management hybrid and off-healing
- [Wowhead: Level 30 Restoration Shaman](https://www.wowhead.com/forever/guide/classes/shaman/restoration/level-30-healer-overview): the Solo Levelling hybrid
- [Wowhead: Level 30 Enhancement Shaman](https://www.wowhead.com/forever/guide/classes/shaman/enhancement/level-30-dps-overview): Restoration points for Fire Nova and healing
- [WoWSims Forever: Enhancement presets](https://github.com/wowsims/forever/blob/master/ui/specs/shaman/enhancement/presets.ts): the 19/32/0 level 60 talent string
- [WoWSims Forever: Elemental build file](https://github.com/wowsims/forever/blob/master/ui/specs/shaman/elemental/builds/testing.build.json): the 32/11/8 level 60 talent string
