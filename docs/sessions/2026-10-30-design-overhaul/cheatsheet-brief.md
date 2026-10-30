# Brief: rewrite "At a glance" as "Cheatsheet"

You're rewriting the first section of some Tazdingo guide pages (Markdown files in `content/`). Tazdingo is an unofficial, public guide site for World of Warcraft: Forever. Each page summarises other sites' guides in our own words and cites them.

## The job

In each file you're given, replace the whole `## At a glance` section (heading and body, up to the next `## ` heading) with a `## Cheatsheet` section, written as described below. Then set the header's `updated:` line to `2026-10-30`. Change nothing else in the file: not the other sections, the header's other fields, or any other file. Don't run git.

## Who it's for

A casual-serious player who already knows the class or profession's basics (armour, resource, which races can play it, what a profession makes in general). They open the page to look something up: the build, the priority, the stats, the levels where things change, the traps. The cheatsheet should answer that in seconds. Drop anything they'd already know.

## Rules (settled, don't bend them)

1. **Only what the page already says.** Every line must come from the page's own `What the guides say` (or its current At a glance). No new facts, no outside knowledge, no web lookups. If the page has nothing for a label, leave the label out, or write "not established yet" when its absence is itself useful (e.g. no level-60 build is known).
2. **Keep the qualifiers.** Compression must not turn a conditional source example into a universal recommendation. Each line says, where it applies: the level (30, 60), the scenario (levelling, dungeons, solo), whether it's a projection or a simulator default, and whose advice it is. Where the guides disagree, say so briefly ("Wowhead and Icy Veins: X; ForeverDB: Y") rather than picking a winner. Don't overrule the page's own `Tazdingo recommendation`; stay consistent with it.
3. **Cite.** Keep a link to the source for each substantive claim, reusing the links already in the page (Wowhead, Icy Veins, ForeverDB, WoWSims, Blizzard). One link per line is usually enough. ForeverDB spell and item links (`https://foreverdb.net/spell/<id>`) show an icon and tooltip on the site: use them for a few key abilities, not every name.
4. **Our own words.** Plain British English, short. No marketing tone. Never mention ChatGPT, AI, or any person.
5. **Format.** A Markdown list, one line per label, each `- **Label:** text`. Each line is at most about 45 words; most are 15–30. "Pick it for" is at most 25 words. Use the labels below, in this order, exactly as written (the site lifts "Pick it for" onto cards). Use `·` to separate short items within a line (e.g. key levels). No nested lists, no tables, no headings inside the section.

## Labels

**Spec pages** (`content/classes/<class>/<spec>.md`):
- **Pick it for:** when this spec is the right choice, in one line.
- **Levelling build:** the talent build at the beta cap (30) from the guides, naming the source; note alternatives briefly.
- **Build at 60:** the level-60 build, marked as a projection or simulator default, with its source; or "not established yet".
- **Priority:** what to press, in order, at the level the guides cover (say which level); for healers, what to cast when; for tanks, how threat and survival work. If level 30 and level 60 differ, give both briefly.
- **Stats:** the stat priority, naming the source; if sources disagree, say so.
- **Key levels:** the levels where the spec changes: talents, abilities, quests, dual-wield, mounts etc. (`20 X · 30 Y · 40 Z`).
- **Gear and consumables:** the few items, consumables and profession pairings the page names.
- **Watch out:** the traps: outdated guide text, changed mechanics, common mistakes.

**Class overview pages** (`content/classes/<class>/overview.md`):
- **Pick a spec:** which spec for levelling, for dungeons, for tanking or healing, from the page, with the reasons in a few words.
- **Key levels:** class-wide milestones (`10 X · 20 Y · 30 Z · 40 W`).
- **New in Forever:** the changes a returning Classic player must know, in one or two lines.
- **Professions:** the pairings the page names.
- **Race:** the race guidance the page gives (after the 26 October changes, if the page covers them).
- **Watch out:** traps and outdated guide text.

**Profession pages** (`content/professions/<slug>.md`):
- **Pick it for:** who should take it, in one line.
- **Pairs with:** the companion profession(s) and why, briefly.
- **Levelling route:** the route in skill brackets (`1–55 X · 55–150 Y · …`), naming the guide; mark untested brackets.
- **Money makers:** what the guides say sells, with the page's caveats (estimates, not proven demand).
- **Camp items:** the camp items and the skill they need.
- **Trainers and ranks:** rank thresholds and notable trainers or recipe vendors the page names.
- **Watch out:** traps and things that changed from Classic.

## A model (Fury Warrior)

```
## Cheatsheet

- **Pick it for:** dual-wield melee damage in groups once you have two good weapons; a slow solo leveller until Flurry (35) and Bloodthirst (40).
- **Levelling build:** at 30, Wowhead and Icy Veins take Cruelty 5, Unbridled Wrath 5, Furious Precision 3, Dual Wield Specialization 5, Lingering Rage and Death Wish ([Wowhead](https://www.wowhead.com/forever/guide/classes/warrior/fury/level-30-dps-overview)); ForeverDB's levelling build stays on a two-hander. Icy Veins suggests levelling another spec and switching at 35–40.
- **Build at 60:** projection only: WoWSims' default is 32 Fury (Flurry, Bloodthirst, Raging Blows) and 19 Arms (Anger Management, Deep Wounds, Impale), with no Enrage ([WoWSims](https://github.com/wowsims/forever/blob/master/ui/specs/warrior/dps/presets.ts)).
- **Priority:** at 30 (Wowhead), Overpower, Sunder above 70% health, Execute, then Heroic Strike or Cleave only with spare Rage. At 60 the WoWSims list runs Death Wish, Whirlwind on packs, Execute, Whirlwind, Bloodthirst.
- **Stats:** ForeverDB puts hit first, then Strength and crit; Icy Veins puts weapon damage first. Off-hand misses starve Rage.
- **Key levels:** 20 dual-wield · 30 Death Wish · 35 Flurry · 36 Whirlwind · 40 Bloodthirst and Dual Specialization.
- **Gear and consumables:** two current one-handers first. ForeverDB's sim ranks Bear Brisket and Scroll of Strength II as the best level-30 consumables. Wowhead favours Engineering.
- **Watch out:** Wowhead's Fury overview still says crits give no extra Rage and Dual Wield Specialization gives hit; both changed on 1–2 October. Bloodthirst no longer heals.
```

## When you're done

Reply with: the files changed, and for each file any label you left out or marked "not established yet" and why, plus anything in the page that looked contradictory. Keep the reply short.
