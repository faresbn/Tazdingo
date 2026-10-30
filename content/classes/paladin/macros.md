---
updated: 2026-10-27
summary: A selection of community Paladin macros for WoW Forever from ForeverDB, Kami Labs, Icy Veins and Wowhead, each with what it does; none tested in the live game.
sources: ForeverDB Paladin macros, Kami Labs, Icy Veins levelling guide, Wowhead
---

## Cheatsheet

- **Where these come from:** a selection of useful macros from four community guides (ForeverDB, Kami Labs, Icy Veins and Wowhead), credited to each. None has been tested in the live game. ForeverDB checked its spell names against the beta client, but hasn't tried them in play.
- **Heal without losing your target:** most healing macros here use the "mouseover, then friendly target, then yourself" pattern, so you can heal between swings ([ForeverDB](https://foreverdb.net/class/Paladin/macros)).
- **Judgement is off the global cooldown:** it can share a key with Holy Strike or Repentance and fire on the same press (ForeverDB, [Icy Veins](https://www.icy-veins.com/wow-forever/retribution-paladin-leveling)).
- **Ranks:** leave the rank off to always cast your highest. ForeverDB notes that a lower Holy Light rank costs far less Mana, so healers may want a ranked key too ([Kami Labs](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/), ForeverDB).
- **Forbearance:** Divine Protection, Blessing of Protection and Templar's Bulwark share a one-minute lockout, so keep them on separate, deliberate keys.

## What the guides say

### Tazdingo recommendation

Keep emergency protection, taunt/Judgement and ordinary damage keys distinct enough to use deliberately. A damage sequence cannot decide whether Judgement must be saved for a loose enemy. Multi-spell macros still obey global and shared cooldowns; item, target and modifier branches need separate testing. Confirm spell names and equipped shield requirements in the current client before relying on these community examples.

This is a short list, not a full library; each source's page has more. Level requirements come from ForeverDB. Anything above level 30 couldn't be used in the beta.

### Healing and cleansing

**Holy Light, Shift for Flash of Light** (ForeverDB): heals your mouseover, friendly target or yourself with Holy Light, or with Flash of Light while Shift is held. Flash of Light comes at 20.

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,help,nodead][mod:shift,@player] Flash of Light; [@mouseover,help,nodead][help,nodead][@player] Holy Light
```

**Mouseover Purify** (Wowhead): removes poisons and diseases from the friend under your cursor, or your target.

```
/cast [@mouseover, help,nodead] [] purify
```

**Mouseover Cleanse** (Kami Labs): the same pattern for Cleanse, which replaces Purify at 42 and also removes magic.

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Cleanse
```

**Lay on Hands, Alt for yourself** (ForeverDB): puts Lay on Hands on your mouseover or target, or always on you with Alt. It drains your Mana, so keep it for emergencies.

```
#showtooltip Lay on Hands
/cast [mod:alt,@player][@mouseover,help,nodead][help,nodead][@player] Lay on Hands
```

**Holy Shock on friend or foe, Shift for Light's Vigil** (ForeverDB): Holy Shock heals or hurts whoever you point at. Shift places Light's Vigil (level 40) first. Holy Shock is a level 30 talent.

```
#showtooltip
/cast [mod:shift,@mouseover,exists,nodead][mod:shift] Light's Vigil; [@mouseover,help,nodead][@mouseover,harm,nodead][] Holy Shock
```

**Mouseover Redemption** (Kami Labs): resurrects the dead player under your cursor without clicking the body.

```
#showtooltip
/cast [@mouseover,dead][target=targettarget,dead] Redemption
```

### Blessings

**Might, Wisdom or Kings on one key** (ForeverDB): Might by default, Wisdom with Shift and Kings with Ctrl, on your mouseover or yourself. Kings comes at 20.

```
#showtooltip
/cast [mod:shift,@mouseover,help,nodead][mod:shift,@player] Blessing of Wisdom; [mod:ctrl,@mouseover,help,nodead][mod:ctrl,@player] Blessing of Kings; [@mouseover,help,nodead][@player] Blessing of Might
```

**Mouseover Blessing of Freedom** (Kami Labs): frees the friend under your cursor, your target or you from slows and roots.

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Blessing of Freedom
```

### Seals, Judgement and damage

**Seal that follows your shield** (ForeverDB): casts Seal of Fury with a shield equipped and Seal of Righteousness without one.

```
#showtooltip
/cast [equipped:Shields] Seal of Fury; Seal of Righteousness
```

**Holy Strike with Judgement** (ForeverDB): starts swinging, Judges if ready, and Holy Strikes. Hold Shift to save Judgement.

```
#showtooltip Holy Strike
/startattack
/cast [nomod:shift] Judgement
/cast Holy Strike
```

**Tank taunt: mouseover Judgement, Shift for Swift Judgement** (ForeverDB): with Seal of Fury up, Judges the enemy under your cursor to taunt it. Shift resets the cooldown first for a second taunt (Swift Judgement is a level 25 talent).

```
#showtooltip Judgement
/cast [mod:shift] Swift Judgement
/cast [@mouseover,harm,nodead][] Judgement
```

**Repentance and Judgement** (Icy Veins): incapacitates the target and Judges it in the same press. Icy Veins says the Judgement doesn't break the incapacitate and gains Seal of Command's bonus against incapacitated targets.

```
#showtooltip
/cast Repentance
/cast Judgement
```

**Exorcism** (Kami Labs): Exorcism on your hostile target. It only works on Undead and Demons.

```
#showtooltip
/cast [harm][@target] Exorcism
```

**Hammer of Wrath** (Kami Labs): the execute spell for low-health enemies, trained at 44.

```
#showtooltip
/cast [harm][@target] Hammer of Wrath
```

### Stuns and cooldowns

**Hammer of Justice on focus, mouseover or target** (ForeverDB): stops your own cast, then stuns your focus, mouseover or target. The stun stops a cast only when the enemy is susceptible; it is not a conventional interrupt against stun-immune bosses.

```
#showtooltip Hammer of Justice
/stopcasting
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Hammer of Justice
```

**Both trinkets** (Kami Labs): fires both trinkets' on-use effects on one key.

```
/use 13
/use 14
```

### Where the guides differ

- **Healing ranks:** Kami Labs and Wowhead recommend leaving ranks off so bars stay current. ForeverDB adds a deliberately ranked Holy Light key, because rank 2 costs a fraction of your top rank for small top-ups. Both can be right: unranked for damage, a ranked key for cheap heals.
- **Lay on Hands:** Kami Labs describes a full heal. ForeverDB's client tooltip heals for your maximum health and drains all your Mana. In practice that is a full heal on most targets, but plan to drink afterwards.
- **Repentance and Judgement:** Icy Veins' claim that the Judgement doesn't break Repentance comes from beta play and is worth checking at launch.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Paladin macros](https://foreverdb.net/class/Paladin/macros): 19 macros with how to use them and the client values behind each.
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): copy-ready macros for every class, in English and French.
- [Kami Labs: 240 macros for 9 classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap, `/startattack` and mouseover healing.
- [Icy Veins: Retribution Paladin Leveling](https://www.icy-veins.com/wow-forever/retribution-paladin-leveling): the Repentance and Judgement macro.
- [Wowhead: Level 30 Protection Paladin](https://www.wowhead.com/forever/guide/classes/paladin/protection/level-30-tank-overview): the mouseover Purify macro.
- [Wowhead: Beginner's guide to writing macros](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): macro syntax and the highest-rank trick.
