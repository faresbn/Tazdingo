---
updated: 2026-10-27
summary: Rogue macros for WoW Forever collected from community guides, covering openers, crowd control, escapes, finishers, poisons and weapon swaps, with notes on levels and known mistakes.
sources: ForeverDB macros, Kami Labs macros, Wowhead macro guide, Icy Veins Subtlety guide
---

## At a glance

- **Where these come from:** ForeverDB's Rogue macro page, Kami Labs' macro tool, Wowhead's beginner macro guide and the weapon-swap macros in Icy Veins' Subtlety guide. Each macro is credited to its source.
- **Not tested in the live game:** None of these has been tried in Forever's live game. ForeverDB checked spell names against the beta client but says it hasn't tested them in game.
- **No ranks needed:** `/cast Eviscerate` without a rank always uses your highest rank, so the button keeps up as you train (Wowhead, Kami Labs).
- **Stealth conditions:** `[stealth]` and `[nostealth]` let one key open from Stealth and attack normally out of it. The `!` in `/cast !Stealth` stops a second press from dropping you out of Stealth.
- **Free presses:** In the client's data, Premeditation, Pick Pocket, Cold Blood, Vanish, Evasion and Sprint don't trigger the global cooldown, so they can share a press with another ability (ForeverDB).
- **Level checks:** Cheap Shot needs 26, Kidney Shot 30, Blade Flurry 30 (Combat talent) and Cold Blood 25 (Assassination talent). Blind (34) and Adrenaline Rush (40) are above the beta cap.

## What the guides say

### Tazdingo recommendation

Keep Kick, crowd control and Vanish predictable. Damage-over-time effects and automatic attacks can break Gouge or Sap, so a combined attack button is not always a safe control button. Weapon-swap examples need the exact item names and enough bag space; test their combat behaviour before relying on them. A cast sequence neither chooses a finisher intelligently nor runs several global-cooldown abilities on one press.

### Openers and builders

Ambush from Stealth, Garrote with Ctrl, Cheap Shot with Shift; out of Stealth the same key is Sinister Strike (ForeverDB):

```
#showtooltip
/cast [stealth,mod:shift] Cheap Shot; [stealth,mod:ctrl] Garrote; [stealth] Ambush; Sinister Strike
/startattack [nostealth]
```

Picks the target's pocket and then Ambushes it in one press (ForeverDB):

```
#showtooltip
/cast [stealth] Pick Pocket
/cast [stealth] Ambush; Sinister Strike
```

Uses Premeditation for two free combo points and Ambushes on the same press (ForeverDB):

```
#showtooltip
/cast [stealth] Premeditation
/cast [stealth] Ambush; Sinister Strike
```

Enters Stealth without ever switching it off on a second press (ForeverDB):

```
#showtooltip Stealth
/cast !Stealth
```

Uses Backstab with a dagger equipped, otherwise Sinister Strike, and keeps auto attack going (Kami Labs):

```
#showtooltip
/startattack
/cast [equipped:Daggers] Backstab; Sinister Strike
```

### Sap, Kick, Gouge and Distract

Enters Stealth if needed, then Saps your mouseover, focus or target (ForeverDB):

```
#showtooltip Sap
/cast [nostealth] !Stealth; [@mouseover,harm,nodead][@focus,harm,nodead][] Sap
```

Kicks your focus, mouseover or target without switching target (ForeverDB):

```
#showtooltip Kick
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Kick
```

Gouges first, then Backstabs on the next press once you're behind the target (ForeverDB):

```
#showtooltip
/castsequence reset=target/5 Gouge, Backstab
```

Throws Distract where your mouse points, with no targeting circle (ForeverDB and Kami Labs):

```
#showtooltip Distract
/cast [@cursor] Distract
```

Blinds your target after stopping your attack, or your focus with Shift. It needs level 34, above the beta cap (ForeverDB):

```
#showtooltip Blind
/stopattack [nomod]
/cast [mod:shift,@focus,harm,nodead][nomod] Blind
```

### Staying alive

Stops auto attack before Vanishing, so a late swing can't pull you back out (ForeverDB):

```
#showtooltip Vanish
/stopattack
/cast Vanish
```

Evasion normally, Sprint with Shift, and stop attacking then Vanish with Ctrl (ForeverDB):

```
#showtooltip
/stopattack [mod:ctrl]
/cast [mod:shift] Sprint; [mod:ctrl] Vanish; Evasion
```

Feints on the enemy under your mouse, or your target (ForeverDB):

```
#showtooltip Feint
/cast [@mouseover,harm,nodead][] Feint
```

### Finishers, poisons and cooldowns

Eviscerate normally, Slice and Dice with Shift, Rupture with Ctrl and Expose Armor with Alt (ForeverDB):

```
#showtooltip
/cast [mod:shift] Slice and Dice; [mod:ctrl] Rupture; [mod:alt] Expose Armor; Eviscerate
```

Applies Instant Poison to the main hand, or Crippling Poison to the off hand with Shift. Change the names as you buy new poisons (ForeverDB):

```
#showtooltip
/use [nomod] Instant Poison; [mod:shift] Crippling Poison
/use [nomod] 16; [mod:shift] 17
```

Activates Cold Blood and follows it with a guaranteed critical Eviscerate (ForeverDB):

```
#showtooltip Cold Blood
/cast Cold Blood
/cast Eviscerate
```

Uses both trinkets with Blade Flurry, or with Adrenaline Rush when you hold Shift (ForeverDB):

```
#showtooltip
/use 13
/use 14
/cast [mod:shift] Adrenaline Rush; Blade Flurry
```

### Weapons

Fires whichever ranged weapon you have equipped, for pulling (Wowhead):

```
#showtooltip
/cast [worn:Bows] Shoot Bow; [worn:Crossbows] Shoot Crossbow; [worn:Guns] Shoot Gun; [worn:Thrown] Throw
```

Swaps a slow weapon into the main hand and uses Sinister Strike, for dagger openers before Hemorrhage. Put your own weapon names in (Icy Veins):

```
#showtooltip Sinister Strike
/startattack
/equipslot 16 Slow Weapon Name
/equipslot 17 Dagger Weapon Name
/cast Sinister Strike
```

Swaps the dagger back into the main hand for Ambush (Icy Veins):

```
#showtooltip Ambush
/equipslot 16 Dagger Weapon Name
/equipslot 17 Slow Weapon Name
/cast Ambush
```

Icy Veins notes that a weapon swap triggers the global cooldown and resets your swing timer, so each of these takes two presses: one to swap and one to attack.

### Notes on the sources

- Kami Labs describes Mutilate as a level 60 ability. In Forever it's a tier 5 Assassination talent you can take at level 30, and it needs a dagger in each hand.
- Kami Labs' poison macro names Instant Poison VI, a level 60 rank. Use the rank you actually have.
- Wowhead's guide lists `[stance:1]` as Stealth and `[stance:2]` as Vanish for Rogues, but says the guide was first written for Classic and the syntax may have changed.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Rogue macros](https://foreverdb.net/class/Rogue/macros): 16 macros with levels, character counts and client notes
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): 24 Rogue macros sorted by use, with an English and French client toggle
- [Kami Labs: 240 macros for nine classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): why /startattack and rank-free macros help
- [Wowhead: Beginner's guide to writing macros in WoW Forever](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): conditions, modifiers and stance numbers
- [Icy Veins: Subtlety Rogue levelling](https://www.icy-veins.com/wow-forever/subtlety-rogue-leveling): the weapon-swap macros in context
