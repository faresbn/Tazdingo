---
updated: 2026-10-27
summary: Useful Mage macros for WoW Forever collected from ForeverDB, Kami Labs and Wowhead, each with a line on what it does; none has been tested in the live game.
sources: ForeverDB Mage macros, Kami Labs macro tool, Wowhead macro guide
---

## At a glance

- **Where these come from:** Community guides, namely [ForeverDB](https://foreverdb.net/class/Mage/macros), [Kami Labs](https://kami-labs.fr/en/macros-wow-forever/) and [Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950). They have not been tested in the live game, which opens on 4 November.
- **Rank trick:** A `/cast` line without a rank always casts the highest rank you know, so you never keep an old rank on your bar (Wowhead, Kami Labs).
- **Focus and mouseover:** Polymorph and Counterspell work best on a focus, so you can keep casting at the kill target.
- **Cast now:** `/stopcasting` in front of Frost Nova, Blink or Counterspell drops your current cast so the escape or interrupt goes off at once.
- **Cursor casting:** `[@cursor]` drops Flamestrike or Blizzard where your mouse points.
- **Client language:** Spell names must match your game client's language, not your browser's (Kami Labs).
- **Length:** A macro holds up to 255 characters.

## What the guides say

### Tazdingo recommendation

Use clear keys for Counterspell, Polymorph and emergency defences before combining damage spells. Stopcasting can make an interrupt immediate but also discards the spell already in progress. Treat cast sequences as manual button sequences, not adaptive rotations; procs, movement and spell ranks can make a fixed order inappropriate. Check names and every modifier branch in the client before relying on these community examples.

ForeverDB checked every spell name and command in its macros against the beta client, but notes that none was tested in the beta. Kami Labs flags some macros "to confirm in-game". To make one, type /macro, click New, pick the question-mark icon so #showtooltip shows the spell, paste the text and drag the icon to your bar (Kami Labs).

### Crowd control and interrupts

Polymorph your focus, or the enemy under your mouse, or your target (ForeverDB):

```
#showtooltip Polymorph
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Polymorph
```

Hold Shift to make the enemy under your mouse your focus and sheep it in one press (ForeverDB):

```
#showtooltip Polymorph
/focus [mod:shift,@mouseover,harm,nodead][mod:shift]
/cast [@focus,harm,nodead][] Polymorph
```

Drop your current cast and Counterspell your focus, mouseover or target (ForeverDB):

```
#showtooltip Counterspell
/stopcasting
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Counterspell
```

### Staying alive

Cancel your cast and Frost Nova straight away (ForeverDB and Kami Labs):

```
#showtooltip Frost Nova
/stopcasting
/cast Frost Nova
```

Cancel your cast and Blink straight away (ForeverDB and Kami Labs):

```
#showtooltip Blink
/stopcasting
/cast Blink
```

Ice Block; hold Shift to cancel it deliberately (adapted from ForeverDB). Ordinary repeated presses no longer cancel the protection:

```
#showtooltip Ice Block
/stopcasting
/cancelaura [mod:shift] Ice Block
/stopmacro [mod:shift]
/cast Ice Block
```

Mana Shield, with Fire Ward on Shift and Frost Ward on Ctrl (ForeverDB):

```
#showtooltip
/cast [mod:shift] Fire Ward; [mod:ctrl] Frost Ward; Mana Shield
```

### Damage

Flamestrike where your mouse points, with no targeting circle (ForeverDB):

```
#showtooltip Flamestrike
/cast [@cursor] Flamestrike
```

Blizzard where your mouse points (ForeverDB):

```
#showtooltip Blizzard
/cast [@cursor] Blizzard
```

Presence of Mind followed by an instant Fireball, or Frostbolt with Shift (ForeverDB):

```
#showtooltip Presence of Mind
/cast Presence of Mind
/cast [mod:shift] Frostbolt; Fireball
```

Scorch the enemy under your mouse, or your target (Kami Labs):

```
#showtooltip Scorch
/cast [@mouseover,harm,nodead][] Scorch
```

Rank 1 Frostbolt, for a cheap slow while kiting (ForeverDB):

```
#showtooltip Frostbolt
/cast Frostbolt(Rank 1)
```

Wand that doesn't switch off if you press it twice (ForeverDB and Kami Labs):

```
#showtooltip Shoot
/cast !Shoot
```

### Buffs, curses and conjuring

Arcane Intellect on the friend under your mouse, a friendly target or yourself; Alt forces it onto you (Kami Labs):

```
#showtooltip Arcane Intellect
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Arcane Intellect
```

Remove Lesser Curse, which also clears Banes in Forever, on your mouseover, friendly target or yourself (ForeverDB):

```
#showtooltip Remove Lesser Curse
/cast [@mouseover,help,nodead][help,nodead][@player] Remove Lesser Curse
```

Amplify Magic on a friend, or Dampen Magic with Shift (ForeverDB):

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift] Dampen Magic; [@mouseover,help,nodead][] Amplify Magic
```

Ice Armor, with Mage Armor on Shift and Frost Armor on Ctrl (Kami Labs):

```
#showtooltip Ice Armor
/cast [mod:shift] Mage Armor; [mod:ctrl] Frost Armor; Ice Armor
```

Conjure water, food with Shift, or a Mana Agate with Ctrl (ForeverDB):

```
#showtooltip
/cast [mod:shift] Conjure Food; [mod:ctrl] Conjure Mana Agate; Conjure Water
```

Use your Mana Agate, or the best mana potion in your bags with Shift (ForeverDB):

```
#showtooltip
/use [nomod] Mana Agate
/use [mod:shift] Mana Potion
/use [mod:shift] Lesser Mana Potion
/use [mod:shift] Minor Mana Potion
```

ForeverDB notes that in the client a mana gem shares its 2 minute cooldown with Warlock Healthstones.

### Travel

Every Alliance teleport on one key: Stormwind, Ironforge on Shift, Darnassus on Alt, Dalaran on Ctrl (ForeverDB):

```
#showtooltip
/cast [mod:alt] Teleport: Darnassus; [mod:shift] Teleport: Ironforge; [mod:ctrl] Teleport: Dalaran; Teleport: Stormwind
```

Every Horde teleport on one key: Orgrimmar, Undercity on Shift, Thunder Bluff on Alt (ForeverDB):

```
#showtooltip
/cast [mod:alt] Teleport: Thunder Bluff; [mod:shift] Teleport: Undercity; Teleport: Orgrimmar
```

Alliance portals on one key, from level 40 (Kami Labs):

```
#showtooltip Portal: Stormwind
/cast [mod:shift] Portal: Ironforge; [mod:ctrl] Portal: Darnassus; Portal: Stormwind
```

Horde portals on one key, from level 40 (Kami Labs):

```
#showtooltip Portal: Orgrimmar
/cast [mod:shift] Portal: Undercity; [mod:ctrl] Portal: Thunder Bluff; Portal: Orgrimmar
```

### Where the sources differ

- **Teleport: Dalaran:** Kami Labs puts it in its Horde teleport macro too, but ForeverDB says the client teaches it only to Alliance Mages, at level 50.
- **Rank spelling:** ForeverDB writes rank macros the way the spellbook pastes them, as `Frostbolt(Rank 1)` with no space. Wowhead's guide shows a space before the bracket. Shift-click the spell into the macro window rather than typing it.
- **Mana gems:** Kami Labs offers a macro that tries every gem from Mana Ruby down to Mana Agate, flagged "to confirm in-game"; only Mana Agate exists below level 38.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Mage macros](https://foreverdb.net/class/Mage/macros): 19 macros with how to use each and the level it needs
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): a copy-to-clipboard tool with English and French spell names
- [Kami Labs: 240 macros for nine classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap and how the tool works
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): macro syntax and the highest-rank trick
