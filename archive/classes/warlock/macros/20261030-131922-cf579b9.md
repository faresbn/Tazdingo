---
updated: 2026-10-27
summary: Useful Warlock macros for WoW Forever collected from ForeverDB and Kami Labs, covering demons, curses, stones and Soul Shards; none has been tested in the live game.
sources: ForeverDB Warlock macros, Kami Labs macro tool, Wowhead macro guide
---

## At a glance

- **Where these come from:** Community guides, namely [ForeverDB](https://foreverdb.net/class/Warlock/macros), [Kami Labs](https://kami-labs.fr/en/macros-wow-forever/) and [Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950). They have not been tested in the live game, which opens on 4 November.
- **Demon spells:** Your demon casts them, so they don't use your global cooldown (ForeverDB).
- **Demon names:** `[pet:...]` conditions use the client's names: Imp, Voidwalker, Succubus, Incubus and Felhunter (ForeverDB).
- **Curses and Banes:** One Curse and one Bane per Warlock can share a target, so swapping Curses never removes your Bane of Agony.
- **Rank trick:** A `/cast` line without a rank casts the highest rank you know (Wowhead, Kami Labs).
- **Client language:** Spell names must match your game client's language (Kami Labs). A macro holds up to 255 characters.

## What the guides say

### Tazdingo recommendation

**Start with separate keys for pet attack/follow, your main filler and emergency control.** The [source collection](https://foreverdb.net/class/Warlock/macros) labels its macros as untested in game; matching a spell name is not runtime validation. Keep a normal spell button available while checking a macro.

Use mouseover or focus control when it prevents a harmful target swap. Avoid fixed DoT sequences as a default rotation: short-lived targets, an unfinished DoT or movement can change the next useful spell. Use `/stopcasting` only for an ability whose urgency justifies losing the current cast. Ground-target shortcuts and modifier keys should be checked in a safe setting before relying on them in a dungeon.

ForeverDB checked every spell name and command against the beta client but tested none of its macros in the beta. Kami Labs flags some "to confirm in-game".

### Your demon

Send your demon in with its opener: Torment, Lash of Pain or Firebolt (ForeverDB):

```
#showtooltip
/petattack
/cast [pet:Voidwalker] Torment; [pet:Succubus/Incubus] Lash of Pain; [pet:Imp] Firebolt
```

Attack your mouseover or target; Shift calls the demon back and sets it to passive, Ctrl sets it to defensive (ForeverDB):

```
/petattack [nomod,@mouseover,harm,nodead][nomod]
/petfollow [mod:shift]
/petpassive [mod:shift]
/petdefensive [mod:ctrl]
```

Summon any demon by modifier, with Fel Domination first if you are in combat (ForeverDB):

```
#showtooltip
/cast [combat] Fel Domination
/cast [mod:shift] Summon Voidwalker; [mod:ctrl] Summon Succubus; [mod:alt] Summon Felhunter; Summon Imp
```

Consume Shadows out of combat with the Voidwalker out, otherwise Health Funnel (ForeverDB):

```
#showtooltip
/cast [nocombat,pet:Voidwalker] Consume Shadows; Health Funnel
```

Sacrifice the Voidwalker for a shield, then start Drain Life (ForeverDB):

```
#showtooltip Sacrifice
/cast [pet:Voidwalker] Sacrifice
/cast Drain Life
```

Demonic Sacrifice your demon, or summon the Imp (Voidwalker with Shift) if none is out (ForeverDB):

```
#showtooltip
/cast [pet] Demonic Sacrifice; [mod:shift] Summon Voidwalker; Summon Imp
```

Seduction on your focus, mouseover or target, from level 26 (ForeverDB):

```
#showtooltip Seduction
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Seduction
```

Felhunter Spell Lock on your mouseover or target, keeping the Felhunter passive and bringing it back afterwards; Spell Lock arrives at 36 (Kami Labs):

```
#showtooltip Spell Lock
/petpassive
/cast [@mouseover,exists,harm][harm,nodead][] Spell Lock
/petfollow
```

Devour Magic on a friend or enemy under your mouse, or your target (ForeverDB):

```
#showtooltip Devour Magic
/cast [@mouseover,help,nodead][@mouseover,harm,nodead][] Devour Magic
```

### Fear, Banish and curses

Fear your focus, mouseover or target (ForeverDB):

```
#showtooltip Fear
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Fear
```

Banish your focus, mouseover or target, from level 28 (ForeverDB):

```
#showtooltip Banish
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Banish
```

Curse of Weakness, with Curse of Recklessness on Shift and Curse of the Elements on Ctrl, on your mouseover or target (ForeverDB):

```
#showtooltip
/cast [mod:shift,@mouseover,harm,nodead][mod:shift] Curse of Recklessness; [mod:ctrl,@mouseover,harm,nodead][mod:ctrl] Curse of the Elements; [@mouseover,harm,nodead][] Curse of Weakness
```

Bane of Agony, with Amplify Curse first when you hold Shift (ForeverDB):

```
#showtooltip Bane of Agony
/cast [mod:shift] Amplify Curse
/cast Bane of Agony
```

Bane of Agony, then Immolate on the next press; it resets on a new target or out of combat (ForeverDB):

```
#showtooltip
/castsequence reset=target/combat Bane of Agony, Immolate
```

### Damage and Soul Shards

Send your demon in and cast Shadow Bolt in one press (Kami Labs):

```
#showtooltip Shadow Bolt
/petattack [harm,nodead]
/cast Shadow Bolt
```

Corruption on the enemy under your mouse without changing target (Kami Labs):

```
#showtooltip Corruption
/cast [@mouseover,exists,harm][] Corruption
```

Drop your current cast and Shadowburn at once (ForeverDB):

```
#showtooltip Shadowburn
/stopcasting
/cast Shadowburn
```

Rain of Fire where your mouse points (ForeverDB):

```
#showtooltip Rain of Fire
/cast [@cursor] Rain of Fire
```

Rank 1 Drain Soul, a cheap way to collect shards (ForeverDB):

```
#showtooltip Drain Soul
/cast Drain Soul(Rank 1)
```

### Stones

Create a Healthstone, with Soulstone on Shift, Spellstone on Ctrl and Firestone on Alt (Kami Labs):

```
#showtooltip Create Healthstone
/cast [mod:shift] Create Soulstone; [mod:ctrl] Create Spellstone; [mod:alt] Create Firestone; Create Healthstone
```

Use your best Healthstone, or Drain Life with Shift (adapted from Kami Labs). The Healthstone lines are explicitly disabled while Shift is held, so the modifier does not also consume the stone:

```
#showtooltip
/use [nomod:shift] Major Healthstone
/use [nomod:shift] Greater Healthstone
/use [nomod:shift] Healthstone
/use [nomod:shift] Lesser Healthstone
/use [nomod:shift] Minor Healthstone
/cast [mod:shift] Drain Life
```

Put your best Soulstone on the friend under your mouse, or your target (Kami Labs):

```
#showtooltip
/use [@mouseover,help][] Major Soulstone
/use [@mouseover,help][] Greater Soulstone
/use [@mouseover,help][] Soulstone
/use [@mouseover,help][] Lesser Soulstone
/use [@mouseover,help][] Minor Soulstone
```

ForeverDB notes that in the client Healthstones share a 2 minute cooldown with Mage mana gems, and Soulstones share a 30 minute cooldown.

### Where the sources differ

- **Corruption in cast sequences:** Kami Labs offers a levelling sequence of Immolate, Bane of Agony, Corruption and wand. ForeverDB deliberately leaves Corruption out of its sequence, because the client also has a sword named Corruption and `/castsequence` may try to use the item instead and get stuck. Test before relying on any sequence that names Corruption.
- **Shard costs:** Neither macro source confirms which spells consume Soul Shards in Forever; ForeverDB says the client's tooltips don't list reagents.
- **Rank spelling:** ForeverDB writes `Drain Soul(Rank 1)` with no space, as the spellbook pastes it; Wowhead's guide shows a space. Shift-click the spell into the macro window rather than typing it.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Warlock macros](https://foreverdb.net/class/Warlock/macros): 19 macros with usage notes and spell details
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): a copy-to-clipboard tool with English and French spell names
- [Kami Labs: 240 macros for nine classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): how the tool works and common macro traps
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): syntax and the highest-rank trick
