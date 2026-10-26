# Updating Forever Ledger

Upload this file to the shared ChatGPT project as a source file. It tells the assistant how to keep the site current from what comes up in conversation. The short instructions block (PROJECT_INSTRUCTIONS.md) points here.

## What the site is

**Forever Ledger** (https://faresbn.github.io/FvrRepo/) is an unofficial journal for World of Warcraft: Forever, which launches on 4 November 2026. It holds:

- **Prices** from Auctionator scans: imported on the Mac with `scripts/ingest.py`. You never write prices.
- **Notes**: what we've learned about classes and specs, professions, the world's systems, addons, macros and known issues. **This is what you keep up to date.**
- **Data** derived from ForeverDB (recipes, crates, camp items): refreshed by a script. You never edit it.

The site is public and impersonal. It never names the people behind it, and never mentions ChatGPT.

## The rules

1. **Write only inside `content/`**, and only at the places listed below. Never touch `data/`, `scripts/`, `site/`, `.github/`, `docs/` or anything else. If something belongs somewhere that doesn't exist yet, say so in chat instead of inventing a place: the build rejects unknown files.
2. **Never invent anything:** prices, drop rates, talent builds, test results, patch details. Write only what the conversation established, or what a source you can name says.
3. **Keep the kinds of knowledge apart.** Say whether something was *tested in game*, *read* (with the source), or *simulated* (with the tool and version). Use the `confidence` field for the page as a whole, and say it in the text for individual points.
4. **No names, and no mention of ChatGPT,** in any file or commit message. Write in a neutral voice ("Frost works well for levelling", not "Fares found that…"). A site check fails the build if a name appears.
5. **Cite sources** with links. Summarise in your own words; never copy text from Wowhead, Icy Veins, ForeverDB or any other site.
6. **One topic per commit.** Its message is a single plain-English line that appears in the site's public log (see "Commit messages").

## Where things go

Each file is one living page section. Update it in place as knowledge grows; don't create dated copies.

| What | File | Valid names |
|---|---|---|
| A spec's notes, build, rotation | `content/classes/<class>/<spec>.md` | see the class list below |
| Builds mixing two talent trees | `content/classes/<class>/hybrid.md` | |
| A class's macros | `content/classes/<class>/macros.md` | |
| Notes on the class as a whole | `content/classes/<class>/overview.md` | |
| A profession | `content/professions/<profession>.md` | herbalism, mining, skinning, alchemy, blacksmithing, enchanting, engineering, leatherworking, tailoring, cooking, first-aid, fishing |
| A world system or topic | `content/world/<topic>.md` | camping, legacy, merchants-favor, rares, zones, dungeons-and-raids, collections |
| Addons that work in Forever | `content/more/addons.md` | |
| Macro collections and general macro tips | `content/more/macros.md` | |
| Known issues and workarounds | `content/more/known-issues.md` | |

**Classes and specs** (use these exact names):

- warrior: arms, fury, protection
- paladin: holy, protection, retribution
- hunter: beast-mastery, marksmanship, survival
- rogue: assassination, combat, subtlety
- priest: discipline, holy, shadow
- shaman: elemental, enhancement, restoration
- mage: arcane, fire, frost
- warlock: affliction, demonology, destruction
- druid: balance, feral, restoration

A new place (a new world topic, say) needs a change to `data/game.json`, which you don't edit. Suggest it in chat instead.

## File format

Every file starts with a header between `---` lines, then Markdown:

```
---
updated: 2026-11-06
confidence: testing
summary: One sentence saying what this page gives the reader.
sources: Own testing (levels 10–24); Wowhead Frost Mage guide; ForeverDB talent data
---

## Levelling build

What it is, who it's for, and why.

| Level | Talent | Why |
|---|---|---|
| 10–14 | Improved Frostbolt 5/5 | Faster casts while levelling |

## Rotation

- Point one
- Point two

## Still open

What we haven't tested yet, or where sources disagree.
```

- **updated** (required): today's date as YYYY-MM-DD. Change it every time you edit the page.
- **confidence** (optional): `idea` (not tried), `testing` (being tried), `tested` (confirmed in play), `outdated` (no longer true; keep the page so readers see why).
- **summary** (optional, recommended): one sentence.
- **sources** (optional, recommended): where it came from, in plain words.
- **status** (optional): `pre-launch` or `live`. Leave it out: pages dated before 4 November show as Pre-launch automatically, and later ones as Live. Set `status: pre-launch` only when you write after launch about something not yet confirmed in the live game.

**Markdown that works:** `##` and `###` headings (the page title already exists, so don't use `#`), paragraphs, bullet and numbered lists (indent two spaces to nest), tables, `> quotes`, code blocks, **bold**, *italics* and links. Link items and spells to ForeverDB, `https://foreverdb.net/item/<id>` or `https://foreverdb.net/spell/<id>`, and the site shows their tooltip and icon. Raw HTML is shown as text, not run.

### Examples of entries in the shared lists

A known issue, in `content/more/known-issues.md`:

```
## Quest tracker disappears after a loading screen

- **Who:** all platforms.
- **What:** the objective tracker empties after zoning; a /reload brings it back.
- **Status:** reported by players on 6 November; no Blizzard reply yet. [Forum thread](https://us.forums.blizzard.com/...)
- **Workaround:** /reload.
```

An addon, in `content/more/addons.md`: add a row to the table, with what it's for, its Forever status and a source link.

A class macro, in `content/classes/mage/macros.md`:

````
## Polymorph the focus target

```
#showtooltip Polymorph
/cast [@focus,harm,nodead] Polymorph
```

Tested in game on 7 November.
````

## How to make a change

1. **Read the current file first.** Use the GitHub connector on `faresbn/FvrRepo`, or the site's `llms-full.txt`. Keep what's still true, merge in what's new, and mark what's no longer true.
2. **Write the whole file back** at its exact path on the `main` branch, with `updated` set to today.
3. **Commit** with a one-line message (below).
4. **Say in chat what changed,** with a link to the page (for example https://faresbn.github.io/FvrRepo/classes/mage/#frost). The site republishes about a minute after the commit.

If the commit breaks a rule (an unknown file, a missing date, a bad confidence value, a name), the site's automatic check fails and the **previous version stays online**. The error says what to fix. Correct the file and commit again.

## Commit messages

The message is a public log line, so write it for a reader of the site:

- **Format:** `<Page>: <what changed>`, in plain English, without a full stop.
- **Good:** `Frost Mage: levelling build for 10–24, tested` · `Known issues: macOS freeze fixed in the 6 November patch` · `Addons: WeakAuras still has no Forever version`
- **Never:** names, "ChatGPT", "update", "misc", or several topics at once.

## When to write

You decide when an update is worth making. Use these signals:

- **Write** when something is *settled*: tested in play, confirmed by a reliable source, or decided in conversation as how we'll do it, and the page doesn't already say it.
- **Write** when Fares asks ("save this", "put that in the ledger", "update the ledger").
- **Suggest, don't write** when it's still speculation, a single report, or a passing remark. Offer to record it once it firms up.
- **Batch** related small facts into one commit per page. Don't commit after every message.
- **Review** the known issues and addons pages when a patch lands or after about a week. Remove fixed issues, or mark them fixed with the date.
- **Before launch** (until 4 November), everything is pre-launch: write freely, and the page shows its label.

## Reading the site

- Everything in one plain-text file: https://faresbn.github.io/FvrRepo/llms-full.txt
- Prices: each market's `prices.tsv` (typical price, latest, steadiness, last seen, units listed, weekly change). The main market's file is linked from `llms-full.txt`.
- What to craft: https://faresbn.github.io/FvrRepo/prices/craft.tsv
- When answering price questions, quote the **typical** price, mention **steadiness** (volatile prices are unreliable), and say how old the data is. All prices are asking prices, not sales. Beta prices are a rough guide only.
