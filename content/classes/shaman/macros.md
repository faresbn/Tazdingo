---
updated: 2026-10-27
summary: Useful Shaman macros for WoW Forever collected from community guides, each with a one-line explanation.
sources: ForeverDB, Kami Labs, Wowhead
---

## Cheatsheet

- **Where these come from:** community guides ([ForeverDB](https://foreverdb.net/class/Shaman/macros), [Kami Labs](https://kami-labs.fr/en/macros-wow-forever/) and [Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950)). None has been tested in the live game; ForeverDB says it checked spell names against the beta client only.
- **Totem bar first:** Forever's Call of the Elements drops four chosen totems in one 3 sec cast, so many old totem macros are no longer needed.
- **One totem per press:** every totem is on the global cooldown, so a macro can't drop two at once (ForeverDB).
- **Totem items:** totem spells still need the matching Earth, Fire, Water or Air Totem in your bags. A macro does nothing without it.
- **Ranks:** a macro without a rank always casts your highest rank.
- **Level gates:** several macros need spells above level 30, such as Chain Heal and Riptide at 40.

## What the guides say

### Tazdingo recommendation

Start with separate, predictable keys for interrupts, totem sets and mouseover healing. Modifier keys save space but can conflict with existing bindings; test each branch on a harmless target. A cast sequence advances once per successful press and can stall on an unavailable spell. It does not choose the right totem or healing target for the situation. These community examples have not been validated in the launch client.

### General tips

- Wowhead's guide uses Lightning Bolt to show the rank trick: write `/cast Lightning Bolt` without a rank and the macro always uses your best rank. Kami Labs gives the same advice.
- Wowhead lists Ghost Wolf as `[stance:1]` for Shamans, for macros that check your form.
- To pin a cheaper rank, write it as the spellbook does, with no space before the bracket, such as `Earth Shock(Rank 1)` ([ForeverDB](https://foreverdb.net/class/Shaman/macros)).

### Totems

Call of the Elements; Shift for Totemic Recall; Ctrl for your second set, Call of the Ancestors (ForeverDB, level 20, Ctrl at 30):

```
#showtooltip
/cast [mod:shift] Totemic Recall; [mod:ctrl] Call of the Ancestors; Call of the Elements
```

Three totems one press at a time, for the levels before Call of the Elements (ForeverDB, level 10):

```
#showtooltip
/castsequence reset=combat Strength of Earth Totem, Searing Totem, Healing Stream Totem
```

Every Earth totem on one key: Strength of Earth, or Stoneskin with Shift, Earthbind with Ctrl and Tremor with Alt (ForeverDB, level 10):

```
#showtooltip
/cast [mod:shift] Stoneskin Totem; [mod:ctrl] Earthbind Totem; [mod:alt] Tremor Totem; Strength of Earth Totem
```

Fire Nova, or a Searing Totem with Shift to give it somewhere to erupt from (ForeverDB, level 12):

```
#showtooltip
/cast [mod:shift] Searing Totem; Fire Nova
```

Searing Totem then Magma Totem on two presses (Kami Labs, level 26):

```
#showtooltip
/castsequence reset=combat Searing Totem, Magma Totem
```

Grounding Totem that cancels your current cast to go down at once (ForeverDB, level 30):

```
#showtooltip Grounding Totem
/stopcasting
/cast Grounding Totem
```

### Shocks, interrupts and Purge

Earth Shock on your focus, then mouseover, then target, cancelling your own cast first (ForeverDB, level 4):

```
#showtooltip Earth Shock
/stopcasting
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Earth Shock
```

All three shocks on one key: Earth Shock, Frost Shock with Shift, Flame Shock with Ctrl (ForeverDB, level 4):

```
#showtooltip
/cast [mod:shift] Frost Shock; [mod:ctrl] Flame Shock; Earth Shock
```

Purge on your mouseover, then focus, then target (ForeverDB, level 12):

```
#showtooltip Purge
/cast [@mouseover,harm,nodead][@focus,harm,nodead][] Purge
```

### Healing, cures and resurrection

Healing Wave on your mouseover, friendly target or yourself; Alt always heals you (ForeverDB, level 1):

```
#showtooltip Healing Wave
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Healing Wave
```

Lesser Healing Wave the same way, for when speed matters more than mana (ForeverDB, level 20):

```
#showtooltip Lesser Healing Wave
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Lesser Healing Wave
```

A cheap low-rank Healing Wave for small top-ups (ForeverDB, level 6):

```
#showtooltip Healing Wave
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Healing Wave(Rank 2)
```

Nature's Swiftness into an instant Healing Wave on one press (ForeverDB, Restoration talent, level 30):

```
#showtooltip Nature's Swiftness
/cast Nature's Swiftness
/cast [@mouseover,help,nodead][help,nodead][@player] Healing Wave
```

Chain Heal starting on your mouseover (Kami Labs, level 40):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Chain Heal
```

Riptide on your mouseover, which also strengthens Chain Heal on that target (Kami Labs, Restoration talent, level 40):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Riptide
```

Cure Poison on your mouseover, or Cure Disease with Shift (ForeverDB, level 16, Shift at 22):

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Cure Disease; [@mouseover,help,nodead][help,nodead][@player] Cure Poison
```

Ancestral Spirit that only fires on a dead friend (ForeverDB, level 12):

```
#showtooltip Ancestral Spirit
/cast [@mouseover,help,dead][help,dead] Ancestral Spirit
```

### Shields, weapons and travel

Lightning Shield, or Water Shield with Shift (ForeverDB, level 8; Water Shield is a level 20 Restoration talent):

```
#showtooltip
/cast [mod:shift] Water Shield; Lightning Shield
```

Every weapon imbue on one key: Rockbiter, Flametongue with Shift, Frostbrand with Ctrl, Windfury with Alt (ForeverDB, full use at level 30):

```
#showtooltip
/cast [mod:shift] Flametongue Weapon; [mod:ctrl] Frostbrand Weapon; [mod:alt] Windfury Weapon; Rockbiter Weapon
```

Stormstrike that also starts your auto attack (ForeverDB, Enhancement talent, level 25):

```
#showtooltip Stormstrike
/startattack
/cast Stormstrike
```

Ghost Wolf that a second press won't cancel (ForeverDB, level 20):

```
#showtooltip Ghost Wolf
/cast !Ghost Wolf
```

Both trinkets on one key (Kami Labs):

```
/use 13
/use 14
```

### Cautions

Some Kami Labs descriptions don't match Forever's versions of these spells:

- Its Flame Shock card says Flame Shock guarantees a Lava Burst critical hit. In Forever, Lava Burst deals 20% more damage with your Flame Shock up instead ([ForeverDB](https://foreverdb.net/class/Shaman/talents)).
- Its Fire Nova card describes a burst around the Shaman. Forever's Fire Nova erupts from your active Fire totem.
- It calls Lesser Healing Wave mana-efficient. ForeverDB says it heals less per point of mana than Healing Wave.
- Its four-totem sequence includes both Windfury and Flametongue Totems. Blizzard says a party can't benefit from both at once ([deep dive](https://worldofwarcraft.blizzard.com/en-us/news/24302097)), so it isn't listed here.

ForeverDB adds that a cast sequence only moves on when a step succeeds. Without mana or the right totem item, it waits on that step.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Shaman macros](https://foreverdb.net/class/Shaman/macros): 19 macros with levels, totem notes and usage tips
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): copy-ready cards for all nine classes, in English or French
- [Kami Labs: 240 macros for 9 classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap and how the macro tool works
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): macro syntax, conditions and stance numbers
- [Blizzard: Class Deep Dives, Mage and Shaman](https://worldofwarcraft.blizzard.com/en-us/news/24302097): how totems, the totem bar and Call spells work in Forever
