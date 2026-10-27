---
updated: 2026-10-27
summary: Druid macros for WoW Forever gathered from community guides, from form-shifting and Prowl openers to mouseover heals, each with a line on what it does.
sources: ForeverDB macros page, Kami Labs macro tool and guide, Wowhead's macro guide
---

## At a glance

- **Status:** every macro here comes from a community guide and none has been tested in the live game. ForeverDB checked its spell names against the beta client but says none was tried in the beta.
- **Highest rank by default:** `/cast` with no rank always uses the best rank you know. A spell dragged to your bar doesn't update when you train a new rank (Kami Labs, Wowhead).
- **Form numbers:** in `[form:N]`, Bear Form (or Dire Bear Form) is always 1. Cat Form is 3 if you know Aquatic Form and 2 if you don't, and Travel Form comes after ([ForeverDB](https://foreverdb.net/class/Druid/macros)). Wowhead's list adds Moonkin Form as 5.
- **The `!` prefix:** stops a second press from cancelling a form or Prowl.
- **`/cancelform`:** drops your form on the same press, so a caster spell can follow.
- **Cost:** shifting into Bear or Cat Form costs 55% of your base mana and triggers the global cooldown, so form macros aren't free.
- **Powershifting:** Forever's Furor only gives back the Energy you'd have had anyway, so old powershift macros no longer gain Energy.
- **Above the beta cap:** anything using Ravage (32), Pounce (36), Dire Bear Form or Innervate (40), or Gift of the Wild (50) couldn't be tried before launch.

## What the guides say

### Forms and movement

**Escape a root in Cat Form** ([ForeverDB](https://foreverdb.net/class/Druid/macros)): leaves your current form and re-enters Cat Form on one press, since shifting clears roots and slows.

```
#showtooltip Cat Form
/cancelform
/cast Cat Form
```

**One travel key** (ForeverDB): Aquatic Form in water, Cat Form on land, and Travel Form with Shift held outdoors from level 30.

```
#showtooltip
/cast [swimming] Aquatic Form; [mod:shift,outdoors] Travel Form; Cat Form
```

**Dash with an automatic Cat Form** ([Kami Labs](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/)): shifts to Cat Form first, then Dashes on the next press. Change 3 to 2 if you don't have Aquatic Form.

```
#showtooltip Dash
/cast [noform:3] !Cat Form
/cast [form:3] Dash
```

**Forced form** ([Kami Labs](https://kami-labs.fr/en/macros-wow-forever/)): enters Cat Form without ever toggling you back out. The same works with Bear, Dire Bear, Travel and Aquatic Form.

```
#showtooltip
/cast !Cat Form
```

**"Powershift" re-shift** (Kami Labs): dismounts, stands, drops your form and shifts into Cat Form. Kami Labs says this grants Energy, but ForeverDB and Blizzard say the reworked Furor only restores the Energy you'd have had anyway, so treat it as a clean re-shift.

```
#showtooltip Cat Form
/dismount
/cancelform
/stand
/cast Cat Form
```

**Dire Bear Form with tank rings** ([Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950)): leaves any other form, shifts into Dire Bear Form and swaps in two rings. Replace the ring names with your own, and use Bear Form before 40.

```
#showtooltip Dire Bear Form
/cancelform [stance:2][stance:3][stance:4]
/cast Dire Bear Form
/equipslot 11 Ring of Protection
/equipslot 12 Naglering
```

### Cat and Bear

**Bear Form, then Maul or Swipe** (ForeverDB): shifts into Bear Form, then starts attacking with Maul, or Swipe while holding Shift.

```
#showtooltip
/startattack [form:1,harm,nodead]
/cast [form:1,mod:shift] Swipe; [form:1] Maul; Bear Form
```

**Cat Form, then Prowl** (ForeverDB): the first press puts you in Cat Form, the second Prowls, and a third press won't break stealth.

```
#showtooltip Prowl
/cast [noform][form:1] Cat Form; !Prowl
```

**Ravage from stealth, Shred otherwise** (Kami Labs): opens with Ravage while prowling and becomes Shred afterwards. Ravage needs level 32.

```
#showtooltip
/startattack
/cast [stealth] Ravage; Shred
```

**Feral Charge and attack** (ForeverDB): charges your target from 8 to 25 yards and starts swinging. Feral Charge is off the global cooldown, so both lines fire.

```
#showtooltip Feral Charge
/cast Feral Charge
/startattack
```

**Growl on mouseover** (ForeverDB): taunts the enemy under your cursor without changing target, or your target if you aren't pointing at one.

```
#showtooltip Growl
/cast [@mouseover,harm,nodead][] Growl
```

### Healing, cures and resurrection

**Leave form and heal yourself** (ForeverDB): drops Bear or Cat Form and casts Rejuvenation on you, or Regrowth with Shift.

```
#showtooltip
/cancelform
/cast [mod:shift,@player] Regrowth; [@player] Rejuvenation
```

**Rejuvenation or Regrowth on mouseover** (ForeverDB): heals the friend under your cursor, then your friendly target, then you; Shift switches to Regrowth.

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Regrowth; [@mouseover,help,nodead][help,nodead][@player] Rejuvenation
```

**Instant Healing Touch** (ForeverDB): fires Nature's Swiftness and a Healing Touch together for an emergency save. It needs the level 30 Restoration talent.

```
#showtooltip Nature's Swiftness
/cast Nature's Swiftness
/cast [@mouseover,help,nodead][help,nodead][@player] Healing Touch
```

**Rebirth in combat, Revive after** (ForeverDB): picks Rebirth on a dead friend during a fight and the new Revive outside one, saving Rebirth's long cooldown.

```
#showtooltip
/cast [combat,@mouseover,help,dead][combat,help,dead] Rebirth; [@mouseover,help,dead][help,dead] Revive
```

**Mouseover Innervate** (Kami Labs): leaves your form and casts Innervate on the friend under your cursor, or your target. Innervate needs level 40.

```
#showtooltip Innervate
/cancelform
/cast [@mouseover,help][] Innervate
```

### Buffs and crowd control

**Buff in two presses** (Wowhead): leaves your form, then casts Mark of the Wild and Thorns on consecutive presses, or Gift of the Wild (level 50) with Shift. The sequence resets after 10 seconds or on a new target.

```
/cancelform
/cast [mod:shift]Gift of the Wild
/castsequence reset=10/target Mark of the Wild, Thorns
```

**Entangling Roots on focus or mouseover** (ForeverDB): roots your focus, else the enemy under your cursor, else your target, so you can hold an add while fighting.

```
#showtooltip Entangling Roots
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Entangling Roots
```

**Moonfire from any form** (Kami Labs): drops your form and casts Moonfire in one press, useful for pulling or tagging at range.

```
#showtooltip
/cancelform
/cast Moonfire
```

### Notes from the sources

- ForeverDB writes each macro to fit the 255-character limit and marks the ones above the level 30 cap as speculation.
- Kami Labs' tool can switch between English and French spell names; a macro only works in your game client's language.
- Wowhead's guide is mainly a lesson in writing macros. It explains `#showtooltip`, conditions in square brackets and `/castsequence`, so you can adapt any of these.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Druid macros](https://foreverdb.net/class/Druid/macros): 19 Druid macros checked against the client, with notes on each spell
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): a copy-to-clipboard tool with 34 Druid macros, filterable by role
- [Kami Labs: 240 ready-made macros for 9 classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the common macro traps, including the Druid `!` trick
- [Wowhead: Beginners guide to writing macros in WoW Forever](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): how macro syntax and form numbers work
