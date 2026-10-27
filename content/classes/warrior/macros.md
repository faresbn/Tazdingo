---
updated: 2026-10-27
summary: Community Warrior macros for WoW Forever from ForeverDB, Kami Labs, Wowhead and Icy Veins, each with what it does; none tested in the live game.
sources: ForeverDB Warrior macros, Kami Labs, Wowhead macro guide, Icy Veins levelling guides
---

## At a glance

- **Where these come from:** a selection of the most useful macros from four community guides (ForeverDB, Kami Labs, Wowhead and Icy Veins), credited to each. None has been tested in the live game. ForeverDB checked its spell names against the beta client, but says it hasn't tried them in play.
- **Stance numbers:** `[stance:1]` is Battle Stance, `[stance:2]` Defensive Stance and `[stance:3]` Berserker Stance ([Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950)).
- **Two presses to change stance:** in a stance-changing macro, the first press changes stance and the second uses the ability. Tactical Mastery keeps 10 Rage through the switch ([ForeverDB](https://foreverdb.net/class/Warrior/macros)).
- **Leave ranks off:** `/cast Heroic Strike` always uses your highest rank, so new ranks from the trainer work without editing your bars (Wowhead, [Kami Labs](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/)).
- **`/startattack`:** most melee macros start with it so your swings never stop (Kami Labs).
- **Vanguard catch:** the Protection talent Vanguard adds a separate Charge spell. Icy Veins says to shift-click that Charge from your spellbook into the macro, because `/cast Charge` won't find it.

## What the guides say

This is a short list, not a full library: each source's page has more. Level requirements come from ForeverDB. Anything above level 30 couldn't be used in the beta.

### Stances and openers

**Charge out of combat, Intercept in combat** (ForeverDB): charges from Battle Stance before a fight and Intercepts from Berserker Stance during one, fixing your stance first if needed. Intercept needs 30.

```
#showtooltip
/cast [nocombat,stance:1] Charge; [combat,stance:3] Intercept; [nocombat] Battle Stance; Berserker Stance
```

**Charge into Rend** (Kami Labs): a solo opener that Charges out of combat and applies Rend once the fight starts.

```
#showtooltip
/startattack
/cast [nocombat,nostance:1] Battle Stance
/cast [nocombat,stance:1] Charge
/cast [combat] Rend
```

**Battle and Defensive toggle** (Wowhead): flips between Battle and Defensive Stance on one key.

```
#showtooltip
/cast [stance:1] Defensive Stance; [stance:2] Battle Stance
```

**Charge, then Execute or Taunt** (Wowhead): Charges out of combat, then Executes in Battle Stance or Taunts in Defensive Stance.

```
#showtooltip
/cast [nocombat] Charge
/cast [stance:1]Execute; [stance:2] Taunt
```

**Overpower from any stance** (ForeverDB): moves you to Battle Stance if needed, then Overpowers on the next press.

```
#showtooltip Overpower
/startattack
/cast [stance:1] Overpower; Battle Stance
```

**Berserker Rage from any stance** (ForeverDB): moves you to Berserker Stance and casts Berserker Rage. Press it before a fear lands.

```
#showtooltip Berserker Rage
/cast [stance:3] Berserker Rage; Berserker Stance
```

**Whirlwind with a stance swap** (Kami Labs): enters Berserker Stance and Whirlwinds. Whirlwind is trained at 36.

```
#showtooltip
/cast [nostance:3] Berserker Stance
/cast Whirlwind
```

### Tanking

**Mouseover Taunt, Shift for Mocking Blow** (ForeverDB): taunts the enemy under your cursor (or your target), with Mocking Blow as a backup on Shift.

```
#showtooltip
/cast [mod:shift,stance:1,@mouseover,harm,nodead][mod:shift,stance:1] Mocking Blow; [mod:shift] Battle Stance; [stance:2,@mouseover,harm,nodead][stance:2] Taunt; Defensive Stance
```

**Mouseover Sunder Armor** (Kami Labs): stacks Sunder on the enemy under your cursor without changing target.

```
#showtooltip
/startattack
/cast [@mouseover,harm,nodead][] Sunder Armor
```

**Revenge and Shield Block together** (ForeverDB): Revenge plus Shield Block on one press. Hold Shift to skip the block and save Rage.

```
#showtooltip Revenge
/startattack
/cast Revenge
/cast [nomod:shift] Shield Block
```

**Shield Slam into Revenge** (Kami Labs): tries Shield Slam, then Revenge, from Defensive Stance. Shield Slam is a level 40 talent.

```
#showtooltip
/cast [nostance:2] Defensive Stance
/cast Shield Slam
/cast Revenge
```

**Shield Wall, Shift for Last Stand** (ForeverDB): both emergency buttons on one key, with Defensive Stance enforced for Shield Wall.

```
#showtooltip Shield Wall
/cast [mod:shift] Last Stand; [stance:2] Shield Wall; Defensive Stance
```

### Interrupts and weapons

**Focus interrupt** (ForeverDB): Shield Bash on your focus or target, or Pummel in Berserker Stance (Pummel needs 38).

```
#showtooltip
/cast [stance:3,@focus,harm,nodead][stance:3] Pummel; [@focus,harm,nodead][] Shield Bash
```

**Mouseover Shield Bash** (Icy Veins): interrupts the enemy under your cursor, or your target. Needs a shield and Battle or Defensive Stance.

```
#showtooltip Shield Bash
/cast [@mouseover,harm,nodead][] Shield Bash
```

**Mouseover Pummel** (Icy Veins): the Berserker Stance version.

```
#showtooltip Pummel
/cast [@mouseover,harm,nodead][] Pummel
```

**Sword and board, Shift for two-hander** (ForeverDB): equips one-hander and shield, or your two-hander with Shift. Replace the braces with your own item names; ForeverDB's page fills them in for you.

```
#showtooltip
/equip [mod:shift] {TWOHAND}
/equipslot [nomod] 16 {ONEHAND}
/equipslot [nomod] 17 {SHIELD}
```

**One ranged key** (Wowhead): uses whichever ranged weapon you have equipped for pulling.

```
#showtooltip
/cast [worn:Bows] Shoot Bow; [worn:Crossbows] Shoot Crossbow; [worn:Guns] Shoot Gun; [worn:Thrown] Throw
```

### Damage and Rage

**Heroic Strike, Shift for Cleave** (ForeverDB): queues Heroic Strike, or Cleave with Shift, and makes sure you are swinging.

```
#showtooltip
/startattack
/cast [mod:shift] Cleave; Heroic Strike
```

**Victory Rush** (Kami Labs): starts swinging and uses Victory Rush after a kill, from level 20.

```
#showtooltip
/startattack
/cast Victory Rush
```

### Where the guides differ

- **Charging with Vanguard:** ForeverDB suggests changing `stance:1` to `stance:1/2` in its Charge macro. [Icy Veins](https://www.icy-veins.com/wow-forever/protection-warrior-leveling) says Vanguard's Charge is a separate spell, which must be shift-clicked into the macro and re-added with each new rank. Which works won't be known until launch.
- **Berserker Rage:** Kami Labs says it breaks fear. ForeverDB says the tooltip only promises immunity, so use it before the fear.
- **Raging Blows:** ForeverDB's macro notes say it cuts Cleave by 2 Rage; the current talent tooltip says 3.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Warrior macros](https://foreverdb.net/class/Warrior/macros): the full set of 17, with how to use each and the client values behind it.
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): copy-ready macros for every class, in English and French.
- [Kami Labs: 240 macros for 9 classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap, `/startattack` and how to use the tool.
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): syntax, stance numbers and Warrior examples.
- [Icy Veins: Fury Warrior Leveling](https://www.icy-veins.com/wow-forever/fury-warrior-leveling): the mouseover Shield Bash and Pummel macros.
- [Icy Veins: Protection Warrior Leveling](https://www.icy-veins.com/wow-forever/protection-warrior-leveling): the Vanguard Charge macro tip.
