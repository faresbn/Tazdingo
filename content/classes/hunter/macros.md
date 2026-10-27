---
updated: 2026-10-27
summary: Hunter macros for WoW Forever collected from community guides, covering the pet, shots, Survival melee, aspects and traps, with notes on which ones need later levels.
sources: ForeverDB macros, Kami Labs macros, Wowhead macro guide
---

## At a glance

- **Where these come from:** ForeverDB's Hunter macro page, Kami Labs' macro tool and Wowhead's beginner macro guide. Each macro is credited to its source.
- **Not tested in the live game:** None of these has been tried in Forever's live game. ForeverDB checked spell names against the beta client but says it hasn't tested them in game.
- **No ranks needed:** Writing `/cast Spell Name` without a rank always casts your highest rank, so the button keeps up as you train (Wowhead, Kami Labs).
- **The `!` prefix:** `/cast !Auto Shot` or `/cast !Aspect of the Hawk` only ever turns the effect on, so a second press can't switch it off.
- **Pet commands are free:** In the client, pet commands and Auto Shot don't trigger the global cooldown, so they can share a key with a shot (ForeverDB).
- **Level checks:** Feign Death needs level 30 and Frost Trap 28. Bestial Wrath (40), Explosive Trap (34) and Flare (32) are above the beta cap.

## What the guides say

### Tazdingo recommendation

Prioritise separate pet-attack and pet-follow controls, a predictable shot key and a trap key. Keep an opener that sends the pet away from your crowd-control button. Automatic pet attacks can break traps or pull an unintended enemy. Combined cooldown macros may not activate every ability on one press if the client puts one on the global cooldown. Test each action separately before using the combined version; these are unverified community examples.

### Opening and shooting

Sends the pet and marks the target in one press (ForeverDB; Kami Labs has the same macro):

```
#showtooltip Hunter's Mark
/petattack
/cast Hunter's Mark
```

Sends the pet and starts Auto Shot without ever toggling it off (ForeverDB):

```
#showtooltip Auto Shot
/petattack
/cast !Auto Shot
```

Picks a living enemy if you have no valid target, then starts Auto Shot (Kami Labs):

```
#showtooltip
/targetenemy [noexists][dead][help]
/cast !Auto Shot
```

Fires Arcane Shot and makes sure Auto Shot keeps running. Kami Labs uses the same pattern for Serpent Sting and Multi-Shot:

```
#showtooltip Arcane Shot
/cast Arcane Shot
/cast !Auto Shot
```

Aimed Shot normally, Multi-Shot while holding Shift. In Forever the two share a 6-second cooldown (ForeverDB):

```
#showtooltip
/cast [mod:shift] Multi-Shot; Aimed Shot
```

Slows the enemy under your mouse, or your target, without changing target (ForeverDB):

```
#showtooltip Concussive Shot
/cast [@mouseover,harm,nodead][] Concussive Shot
```

Pulls a loose enemy off your healer with Distracting Shot and sends the pet after it (ForeverDB):

```
#showtooltip Distracting Shot
/petattack [@mouseover,harm,nodead][]
/cast [@mouseover,harm,nodead][] Distracting Shot
```

Attempts Rapid Fire, Bestial Wrath (if talented) and both trinkets' use effects; shared cooldowns can prevent all of them activating together (ForeverDB):

```
#showtooltip Rapid Fire
/cast Rapid Fire
/cast Bestial Wrath
/use 13
/use 14
```

### Pet control

Pet attacks your mouseover or target, follows with Shift and stays with Ctrl (ForeverDB):

```
/petfollow [mod:shift]
/petstay [mod:ctrl]
/petattack [nomod,@mouseover,harm,nodead][nomod]
```

Switches Growl's autocast on or off, for example before joining a group with a tank (ForeverDB):

```
#showtooltip Growl
/petautocasttoggle Growl
```

Calls the pet if none is out and mends it if it is; Shift revives it (ForeverDB):

```
#showtooltip
/cast [mod:shift] Revive Pet; [nopet] Call Pet; Mend Pet
```

Sends the pet in and uses its family ability. Replace `{PETSKILL}` with the ability's name, such as Web, Pinch or Dismember (ForeverDB):

```
#showtooltip {PETSKILL}
/petattack
/cast {PETSKILL}
```

Sends the pet in and casts Intimidation (the level 30 Beast Mastery talent) so its next hit stuns (ForeverDB):

```
#showtooltip Intimidation
/petattack
/cast Intimidation
```

Starts Feed Pet only when out of combat with a pet summoned; you must still select compatible food (Kami Labs):

```
#showtooltip Feed Pet
/cast [pet,nocombat] Feed Pet
```

### Melee and staying alive

Starts melee, uses Mongoose Bite after a dodge and queues Raptor Strike on the next swing, for Survival (ForeverDB):

```
#showtooltip Raptor Strike
/startattack
/cast Mongoose Bite
/cast Raptor Strike
```

Casts Deterrence and switches to Aspect of the Monkey when several enemies are on you (ForeverDB):

```
#showtooltip Deterrence
/cast Deterrence
/cast !Aspect of the Monkey
```

### Aspects, tracking, traps and escapes

Aspect of the Hawk normally, Cheetah with Shift, Monkey with Ctrl, never toggling one off (ForeverDB):

```
#showtooltip
/cast [mod:shift] !Aspect of the Cheetah; [mod:ctrl] !Aspect of the Monkey; !Aspect of the Hawk
```

Four tracking types on one key, which suits Survival's Improved Tracking (Kami Labs):

```
#showtooltip Track Humanoids
/cast [mod:shift] Track Beasts; [mod:ctrl] Track Undead; [mod:alt] Track Hidden; Track Humanoids
```

Freezing Trap normally, Immolation Trap with Shift, Frost Trap with Ctrl (ForeverDB):

```
#showtooltip
/cast [mod:shift] Immolation Trap; [mod:ctrl] Frost Trap; Freezing Trap
```

Stops attacking, calls the pet back and feigns death (ForeverDB):

```
#showtooltip Feign Death
/stopattack
/petfollow
/cast Feign Death
```

Sets the pet passive, feigns death in combat and drops a Freezing Trap, for trapping mid-fight (Kami Labs):

```
#showtooltip Freezing Trap
/petpassive
/petstay [@pettarget,harm]
/stopattack
/cast [combat] Feign Death
/cast Freezing Trap
```

Scares the beast set as your focus, under your mouse or targeted, so you can fight one beast at a time (ForeverDB):

```
#showtooltip Scare Beast
/cast [@focus,harm,nodead][@mouseover,harm,nodead][] Scare Beast
```

### Notes on the sources

- Kami Labs also lists an Aspect of the Viper macro. ForeverDB finds Aspect of the Viper only as an unused Season of Discovery leftover in the Forever client, so it's left out here.
- Kami Labs describes Disengage as a backwards leap. In Forever, Blizzard and the client describe it as a threat reduction that turns off your auto-attack, so restart Auto Shot after using it.
- Forever's trap tooltips no longer say traps work only out of combat, and Blizzard confirms traps work in combat. That makes the Feign Death trap trick optional.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: Hunter macros](https://foreverdb.net/class/Hunter/macros): 19 macros with levels, character counts and client notes
- [Kami Labs: WoW Forever macros](https://kami-labs.fr/en/macros-wow-forever/): 26 Hunter macros sorted by use, with an English and French client toggle
- [Kami Labs: 240 macros for nine classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): the rank trap and other common macro mistakes
- [Wowhead: Beginner's guide to writing macros in WoW Forever](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): how conditions and modifiers work
