---
updated: 2026-10-27
summary: How macros work in Forever's modern client (conditionals, mouseover and focus targeting, cast sequences and their limits), with links to ready-made collections.
sources: ForeverDB, Wowhead, Kami Labs, Blizzard forums, Icy Veins, CurseForge
---

## At a glance

- **Modern client:** Forever runs on the current game client, so it has a focus target, mouseover and focus casting options, and modern macro conditionals ([ForeverDB](https://foreverdb.net/macros)).
- **No rank, best rank:** `/cast` without a rank uses the highest rank you know. Spells dragged from the spellbook don't upgrade on your bar when you train a new rank.
- **255 characters:** the macro length limit is unchanged.
- **One spell per press:** a macro can fire only one ability that triggers the global cooldown per key press; `/castsequence` steps through several, one press at a time.
- **Addons can't play for you:** the modern addon rules limit what addons see and do in combat.
- **Use your client's language:** spell and item names must match your game's language.
- **Class macros** are on each [class page](ledger:classes/).

## What the guides say

### Tazdingo recommendation

**Use built-in targeting options for simple needs and macros for a specific repeated action.** Test each target and modifier branch separately. A macro that is syntactically valid can still be wrong for the character's level, equipment or situation. Fixed sequences stall when a step cannot succeed and cannot adapt to procs, health or mana. Keep emergency actions predictable and avoid cancelling a useful cast by accident. None of the community examples establishes launch-client behaviour without an in-game check.

### Making a macro

Type `/macro`, choose the General or Character Specific tab, press **New**, give it a name and pick an icon, then type or paste the text and drag the icon to your bar. The question-mark icon lets `#showtooltip` show the spell the macro will cast ([Kami Labs](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/)). Some beta players found macros wouldn't save; see [Known issues](ledger:more/known-issues/).

Shift-clicking a spell from the spellbook while the macro box is open inserts its name with a rank, such as "(Rank 1)". Delete the rank and the macro always casts your best rank ([Wowhead](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950)). Kami Labs calls this the most common levelling trap: a spell placed straight on the bar keeps casting its old rank after you train a new one. Keep the rank only when you want a cheap rank on purpose; players have [asked Blizzard](https://us.forums.blizzard.com/en/wow/t/macro-auto-downrank-tag/2386249) for automatic downranking, so it isn't there.

### The building blocks

- **Lines starting with `#`** change how the button looks. `#showtooltip` shows the spell that will be used, with its cooldown; `#showtooltip Spell Name` forces one icon.
- **Lines starting with `/`** are commands: `/cast`, `/use`, `/castsequence`, `/target`, `/focus`, `/assist`, `/startattack`, `/stopcasting`, `/cancelform`, `/equipslot` and `/tm` (raid markers) among them.
- **Conditions in square brackets** decide whether an option runs: `[combat]`, `[mod:shift]`, `[stance:2]`, `[worn:Bows]`, `[harm]`, `[help]`, `[dead]`, `[exists]`. Put "no" in front to reverse one, for example `[nocombat]`.
- **Semicolons** separate options. The game uses the first option whose conditions are all true; empty brackets `[]` always match.
- **A `!` before a spell** stops a second press from switching it off, which matters for forms (Kami Labs). With `/tm`, the `!` stops a second press removing the marker (ForeverDB).

Stance and form numbers follow the order your character has them. Wowhead lists Warrior stances as 1 Battle, 2 Defensive and 3 Berserker; Kami Labs warns that Druid form numbers depend on which forms you've learned, so try another number if a form macro does nothing.

### Targeting without changing target

The `@` condition picks who an option affects:

- `@mouseover`: the unit under your mouse, including on party and raid frames.
- `@focus`: your focus target. Forever has focus key bindings (Focus Target and Target Focus) and focus-cast and mouseover-cast options in its settings. A focus clears when that unit dies or you leave the area (ForeverDB).
- `@player`: yourself. `@cursor`: drop a ground-targeted spell where your mouse points.

A heal that tries your mouseover, then a friendly target, then yourself (replace the spell name with your own):

```
#showtooltip
/cast [@mouseover,help,nodead][help,nodead][@player] Your Heal
```

Set your focus from the mouse, or clear it with Shift:

```
/clearfocus [mod:shift]
/stopmacro [mod:shift]
/focus [@mouseover,exists,nodead][]
```

Target what the tank is hitting, once the tank is your focus:

```
/assist [@focus,help,nodead]
```

Put the skull on your mouseover or target. You need to be in a group, and in a raid you need assist or lead (ForeverDB):

```
/tm [@mouseover,exists][] !8
```

### Cast sequences

`/castsequence` casts the first spell in its list, then the next one on the next press, and so on. `reset=` sets when it starts over: a number of seconds, `target`, `combat`, or a modifier such as `shift`. A timed reset counts inactivity since the last press, not a fixed combat rotation timer. A step only advances when it succeeds, so a step that keeps failing (an item you don't have, for example) blocks the rest until the sequence resets (ForeverDB). Players on Blizzard's forums confirm cast sequences work in Forever and use them for totems and caster rotations.

An illustrative Healthstone-then-potion sequence, reset on a combat-state change. Use the exact names of items in your bags; a missing first item blocks the potion:

```
#showtooltip
/castsequence reset=combat Healthstone, Healing Potion
```

### Consumables and shared cooldowns

ForeverDB checked the client's cooldown groups. All healing, mana and rejuvenation potions share one two-minute cooldown, Forever's new Discolored and Perishable potions included. Healthstones share a separate two-minute cooldown with a Mage's mana gems. Bandages have no shared cooldown, but Recently Bandaged blocks a second one. So a list of `/use` lines, best item first, drinks your best potion and skips the rest:

```
#showtooltip
/use Greater Healing Potion
/use Healing Potion
/use Lesser Healing Potion
/use Minor Healing Potion
```

Trinkets (`/use 13` and `/use 14` for the two slots) and most racials don't trigger the global cooldown, so they can share a press with a spell.

### The limits

- **One global-cooldown ability per press.** Everything else in the macro must be off the global cooldown. A macro can't decide for you based on information you couldn't see yourself.
- **255 characters.** Players [asked Blizzard](https://us.forums.blizzard.com/en/wow/t/can-we-finally-increase-the-255-character-macro-limit/2351343) to raise it for Forever; it hasn't changed. ForeverDB and Kami Labs show a character count for each macro.
- **Addons are display-only in combat.** Forever uses the modern game's addon rules ([Icy Veins](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/)), and ForeverDB notes that addons can't see cooldowns and damage-over-time effects in combat. Addons can build or place macros, but the macro still does the work. See [Addons](ledger:more/addons/).
- **Language.** Macros using English spell or item names need those names translated for a French client, and vice versa; command syntax and numeric item IDs are separate (Kami Labs).

### Collections and tools

- [ForeverDB macros](https://foreverdb.net/macros): 188 macros for every class plus general ones, checked against the client but not tested in game.
- [Kami Labs](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): 240 macros for the nine classes, with an English or French client switch and a character counter.
- [Wowhead's beginner's guide](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): a gentle introduction to the syntax; it was first written for Classic, so its author warns some details may differ.
- Addons: [ZMacros](https://www.curseforge.com/wow/addons/zmacros) places ready-made class macros on your keys; [Macro Bench](https://www.curseforge.com/wow/addons/macro-bench) builds and checks macros from blocks; [MacroSearch](https://www.curseforge.com/wow/addons/macrosearch) finds macros you've saved.

## Field findings

Nothing recorded yet.

## Read more

- [ForeverDB: WoW Forever macros](https://foreverdb.net/macros): ready-made macros with explanations, and the client's cooldown groups
- [Kami Labs: 240 macros for nine classes](https://kami-labs.fr/en/wow-forever/macros-wow-forever-9-classes/): common traps, healer and Druid examples, and a copy tool
- [Wowhead: Writing macros in WoW Forever](https://www.wowhead.com/forever/guide/beginners-guide-to-writing-macros-in-wow-forever-34950): the basics of commands and conditions
- [Icy Veins: Addons in WoW Forever](https://www.icy-veins.com/wow-forever/news/addons-in-wow-forever-blizzard-devs-just-addressed-the-big-question/): the addon rules that shape what tools can do
- [Blizzard forums: The 255-character limit](https://us.forums.blizzard.com/en/wow/t/can-we-finally-increase-the-255-character-macro-limit/2351343): players asking for longer macros
