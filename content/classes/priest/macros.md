---
updated: 2026-10-27
summary: Useful Priest macros for WoW Forever collected from community guides, each with a one-line explanation.
sources: ForeverDB, Kami Labs, Wowhead
---

## Cheatsheet

- **Where these come from:** community guides ([ForeverDB](https://foreverdb.net/class/Priest/macros), [Kami Labs](https://kami-labs.fr/en/macros-wow-forever/) and [Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950)). None has been tested in the live game; ForeverDB says it checked spell names against the beta client only.
- **Mouseover healing:** most healing macros heal the friend under your mouse, then your friendly target, then you, so you never drop your enemy target.
- **Ranks:** a macro without a rank always casts your highest rank. You don't need to re-drag spells after each trainer visit.
- **Race spells:** 12 Priest spells belong to one race each. Those macros only work for that race.
- **Level gates:** several macros need talents or spells above level 30, such as Prayer of Mending at 40 and Shadow Word: Death at 32.
- **Language:** spell names must match your game client's language. Kami Labs offers English and French versions.

## What the guides say

### Tazdingo recommendation

Start with mouseover heals, a predictable dispel and a separate emergency key. A macro cannot decide whether to shield, dispel or save mana. Keep stopcasting deliberate: it can save a target, but repeated presses can cancel a useful heal. Test friendly-target, mouseover and modifier fallbacks separately, and never assume a multi-spell sequence bypasses the global cooldown. The examples have not been validated in the launch client.

### General tips

- Wowhead and Kami Labs both suggest writing `/cast Spell Name` without a rank. The macro then uses the highest rank you know, so it stays current as you level.
- To pin a lower rank on purpose, write it exactly as the spellbook does, with no space before the bracket: `Lesser Heal(Rank 2)` ([ForeverDB](https://foreverdb.net/class/Priest/macros)).
- Wowhead lists Shadowform and Spirit of Redemption as `[stance:1]` for Priests, for macros that check your form.

### Healing

Heal on your mouseover, or Flash Heal while holding Shift (ForeverDB, level 20):

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Flash Heal; [@mouseover,help,nodead][help,nodead][@player] Heal
```

Renew on your mouseover, your friendly target or yourself (ForeverDB, level 8):

```
#showtooltip Renew
/cast [@mouseover,help,nodead][help,nodead][@player] Renew
```

Power Word: Shield on your mouseover; hold Alt to shield yourself (Kami Labs, level 6):

```
#showtooltip
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Power Word: Shield
```

Inner Focus followed by a free Flash Heal on one press (ForeverDB, Discipline talent, level 20):

```
#showtooltip Inner Focus
/cast Inner Focus
/cast [@mouseover,help,nodead][help,nodead][@player] Flash Heal
```

Binding Heal on your mouseover, healing them and you together (Kami Labs, Holy talent, level 25):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Binding Heal
```

Prayer of Healing on the party of whoever you point at, since Forever's version heals the target's party (ForeverDB, level 30):

```
#showtooltip Prayer of Healing
/cast [@mouseover,help,nodead][help,nodead][@player] Prayer of Healing
```

Penance that heals a friend or hurts an enemy, depending on what is under your mouse (ForeverDB, Discipline talent, level 30):

```
#showtooltip Penance
/cast [@mouseover,help,nodead][@mouseover,harm,nodead][] Penance
```

Prayer of Mending on your mouseover, usually the tank (Kami Labs, Holy talent, level 40):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Prayer of Mending
```

### Dispels, buffs and resurrection

Dispel Magic that cleans a friend or strips an enemy, whichever is under your mouse (ForeverDB, level 18):

```
#showtooltip Dispel Magic
/cast [@mouseover,help,nodead][@mouseover,harm,nodead][help,nodead][harm,nodead][@player] Dispel Magic
```

Fear Ward on your mouseover, or on your focus if you set the tank as focus (ForeverDB, level 20):

```
#showtooltip Fear Ward
/cast [@mouseover,help,nodead][@focus,help,nodead][help,nodead][@player] Fear Ward
```

Fortitude on one key, with Divine Spirit on Shift and Shadow Protection on Ctrl (ForeverDB, full use at level 30):

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] Divine Spirit; [mod:ctrl,@mouseover,help,nodead][mod:ctrl,@player] Shadow Protection; [@mouseover,help,nodead][help,nodead][@player] Power Word: Fortitude
```

Resurrection that only fires on a dead friend, under your mouse or targeted (ForeverDB, level 10):

```
#showtooltip Resurrection
/cast [@mouseover,help,dead][help,dead] Resurrection
```

### Damage and control

Shadow Word: Pain on the enemy under your mouse, to spread it without changing target (Kami Labs, level 4):

```
#showtooltip
/cast [@mouseover,harm,nodead][harm,nodead] Shadow Word: Pain
```

Wand attack that a second press won't switch off (ForeverDB, level 1):

```
#showtooltip Shoot
/cast !Shoot
```

Shadow Word: Death that cancels your current cast to fire at once (Kami Labs, level 32):

```
#showtooltip
/stopcasting
/cast [harm][@target] Shadow Word: Death
```

Psychic Scream that cancels your current cast first (ForeverDB, level 14):

```
#showtooltip Psychic Scream
/stopcasting
/cast Psychic Scream
```

Shackle Undead on your focus, then your mouseover, then your target, for re-shackling without a target swap (ForeverDB, level 20):

```
#showtooltip Shackle Undead
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Shackle Undead
```

Silence on your focus, cancelling your own cast first (ForeverDB, Shadow talent, level 30):

```
#showtooltip Silence
/stopcasting
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Silence
```

### Race-only spells

Human: Divine Grace on your mouseover or friendly target. It can't target yourself (ForeverDB, level 10):

```
#showtooltip Divine Grace
/cast [@mouseover,help,nodead][help,nodead] Divine Grace
```

Dwarf: Desperate Prayer, cancelling your current cast for an instant self-heal (ForeverDB, level 10):

```
#showtooltip Desperate Prayer
/stopcasting
/cast Desperate Prayer
```

Gnome: Contingency Plan on your mouseover, else your focus, else your target (ForeverDB, level 20):

```
#showtooltip Contingency Plan
/cast [@mouseover,help,nodead][@focus,help,nodead][help,nodead][@player] Contingency Plan
```

### Cautions

- Kami Labs lists Desperate Prayer and Shadowguard with the other Priest macros. In Forever they belong to Dwarves and Trolls only ([ForeverDB](https://foreverdb.net/guide/leveling-priest)).
- ForeverDB notes that a macro can't read health bars. A mouseover heal goes to whoever you point at, not to the most injured player.
- Inner Focus has a 3 min cooldown and fires on every press of its macro, so don't use it as your everyday Flash Heal key (ForeverDB).

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Priest macros](https://foreverdb.net/class/Priest/macros): 20 macros with levels, spell checks and usage notes
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): copy-ready cards for all nine classes, in English or French
- [Kami Labs: 240 macros for 9 classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap and mouseover healing explained
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): macro syntax, conditions and stance numbers
