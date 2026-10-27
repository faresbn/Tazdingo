# Updating Tazdingo

Upload this file to the shared ChatGPT project as a source file. It tells the assistant how to keep the site current from what comes up in conversation. PROJECT_INSTRUCTIONS.md (the project's instructions) points here.

## What the site is

**Tazdingo** (https://faresbn.github.io/Tazdingo/) is an unofficial journal for World of Warcraft: Forever, which launches on 4 November 2026. Its source is the private GitHub repository `faresbn/Tazdingo`. It holds:

- **Prices** from Auctionator scans, imported on the Mac by a script. You never write prices.
- **Pages**: one per class spec, class, profession, world topic and More list. Each summarises what other sites' guides say (**What the guides say**) and records what we've found ourselves (**Field findings**). **These are what you keep up to date.**
- **Data** from ForeverDB and Blizzard's forums, refreshed by scripts. You never edit it.

The site is public and impersonal: it never names the people behind it and never mentions ChatGPT.

## "Update the Tazdingo guide"

When asked to update Tazdingo ("update the Tazdingo guide for Frost Mage", "put that in Tazdingo", "save this"), or when something settled is worth recording (see "When to write"):

1. **Find the page** in "Where things go". If it isn't listed, stop and say so: the site rejects unknown files.
2. **Read the current file from GitHub**, from the `main` branch of `faresbn/Tazdingo`, at its exact path. Note the file's SHA. Never edit from the published site or `llms-full.txt`: they can lag behind the repository and they drop the header.
3. **Edit, keeping everything that's still true:**
   - Add new findings under `## Field findings` as dated entries (format below). Never delete a finding: if it's no longer true, change its confidence to `outdated` and say why.
   - Change `## What the guides say` only to add or correct something a named source says, with a link.
   - Set `updated:` in the header to today's date.
4. **Write the whole file back** to the same path on `main`, with the SHA from step 2. If GitHub rejects the write because the file changed in the meantime, read it again, merge your change into the new version and retry. Don't overwrite.
5. **Commit** with a one-line message (see "Commit messages").
6. **Report in chat:** what changed, the page's address (for example https://faresbn.github.io/Tazdingo/classes/mage/frost/), and that it goes live when the site's check passes, usually within two minutes. If the check fails, the previous version stays online and the error says what to fix.

**The record keeps itself.** After every change, an automatic job saves the page's previous version in `archive/` and logs the change in `archive/LOG.md` (in the private repository, never published). Don't make backups yourself. To see a page's history, read `archive/LOG.md`. To restore an old version, copy its backup back to the page's path and commit, with a message saying so.

## The rules

1. **Write only inside `content/`**, at the places listed below. Never touch `data/`, `scripts/`, `site/`, `.github/`, `archive/`, `docs/` or anything else.
2. **Never invent anything:** prices, drop rates, talent builds, test results, patch details. Write only what the conversation established, or what a source you can name says.
3. **Keep kinds of knowledge apart.** Each finding says how it's known: tested in game (with the level and situation), read (with the source) or simulated (with the tool and its version).
4. **No names, and no mention of ChatGPT,** in any file or commit message. Use a neutral voice ("Frost levels faster with…", not "Fares found…"). The site's check fails a page that names someone, and replaces a commit message that does.
5. **Cite sources** with links. Summarise in your own words; never copy text from Wowhead, Icy Veins, ForeverDB or any other site.
6. **One topic per commit.**

## Where things go

| What | File |
|---|---|
| A spec: what the guides say, and our findings | `content/classes/<class>/<spec>.md` |
| A class as a whole: changes in Forever, choosing a spec | `content/classes/<class>/overview.md` |
| Builds mixing two talent trees | `content/classes/<class>/hybrid.md` |
| A class's macros | `content/classes/<class>/macros.md` |
| A profession | `content/professions/<profession>.md` |
| A world system or topic | `content/world/<topic>.md` |
| Launch checklist ("before you log in") | `content/more/launch.md` |
| Addons that work in Forever | `content/more/addons.md` |
| How macros work, and collections | `content/more/macros.md` |
| Known issues and workarounds | `content/more/known-issues.md` |

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

**Professions:** herbalism, mining, skinning, alchemy, blacksmithing, enchanting, engineering, leatherworking, tailoring, cooking, first-aid, fishing.

**World topics:** camping, legacy, merchants-favor, rares, zones, dungeons-and-raids, collections.

A new place (a new world topic, say) needs a change to `data/game.json`, which you don't edit. Suggest it in chat instead.

## Page format

Every file starts with a header between `---` lines, then four sections in this order:

```
---
updated: 2026-11-06
summary: One sentence saying what this page gives the reader.
sources: Icy Veins, Wowhead, ForeverDB, WoWSims presets, own testing
status: pre-launch
confidence: testing
---

## At a glance

- **Role:** …
- **Stats that matter:** …

## What the guides say

### Talents

What the guides recommend, in our own words, with links.

### Rotation

…

## Field findings

### Frost levels fastest with Blizzard pulls from 22 (tested, 6 Nov 2026)

Tested in game from level 22 to 26 in Hillsbrad: pulling 4–5 mobs and Blizzard-kiting was about twice as fast as single targets. Mana ran out every second pull without Evocation.

### Ice Lance shatter needs Frostbite procs (idea, 6 Nov 2026)

Read on Wowhead's Frost guide; not tested yet.

## Read more

- [Icy Veins: Frost Mage guide](https://…): talents and stat priorities
- …
```

**Header fields** (no others are accepted):
- `updated` (required): today's date, YYYY-MM-DD. Change it on every edit.
- `summary` (required): one sentence.
- `sources`: where the page's content came from, in plain words.
- `status`: `pre-launch` or `live`. A page is **pre-launch** unless this says `live`. Set `live` only after the page's main advice has been checked in the live game, not because it was edited after launch.
- `confidence`: optional, for the page as a whole: `idea`, `testing`, `tested` or `outdated`.
- `verified`: optional, YYYY-MM-DD: when the main advice was last checked in game.

**Sections:** `## At a glance`, `## What the guides say`, `## Field findings`, `## Read more`, once each and in that order. More lists (addons, macros, known issues, launch) may arrange their content freely, but must still end with `## Field findings` and `## Read more`. Use `###` and `####` inside sections, never `#`. An empty Field findings section says exactly "Nothing recorded yet."

**Each finding** is a `###` heading with a short claim and, in brackets, its confidence (`idea`, `testing`, `tested` or `outdated`) and date, followed by how it's known.

**Markdown that works:** headings, paragraphs, bullet and numbered lists (indent two spaces to nest), tables, `> quotes`, code blocks (for macros), **bold**, *italics* and links. Link items and spells to ForeverDB (`https://foreverdb.net/item/<id>`, `https://foreverdb.net/spell/<id>`) and the site shows their tooltip and icon. Link to another ledger page with `ledger:` and its address, for example `[hybrid builds](ledger:classes/druid/#hybrid)` or `[Frost Mage](ledger:classes/mage/frost/)`; the site's check fails a link to a page or section that doesn't exist. Raw HTML is shown as text, not run.

## Commit messages

The message is a public log line on the site, so write it for a reader:

- **Format:** `<Page>: <what changed>`, plain English, no full stop.
- **Good:** `Frost Mage: Blizzard-kiting from 22, tested` · `Known issues: macOS freeze fixed in the 6 November patch` · `Addons: WeakAuras still has no Forever version`
- **Never:** names, "ChatGPT", "update", "misc", or several topics in one.

## When to write

You decide when an update is worth making:

- **Write** when something is *settled*: tested in play, confirmed by a reliable source, or decided in conversation as how we'll do it, and the page doesn't already say it.
- **Write** when asked ("update the Tazdingo guide", "save this", "put that in Tazdingo").
- **Suggest, don't write,** when it's speculation, a single report or a passing remark. Offer to record it once it firms up, or record it as an `idea` finding if asked.
- **Batch** related small facts into one commit per page; don't commit after every message.
- **Review** known issues and addons when a patch lands or about weekly: mark fixed issues fixed, with the date.
- **After launch,** when a pre-launch page's advice is confirmed in game, set `status: live` and `verified:` to the date, and note what was checked under Field findings.

## If you can't write to GitHub

If the GitHub connector can't commit, produce the complete new file in one Markdown code block, with its path above it, and say which page it replaces. It can then be pasted into GitHub's web editor (Edit file, paste, Commit changes). Everything else (the checks, the archive, publishing) works the same.

## Reading the site

- Everything in one plain-text file: https://faresbn.github.io/Tazdingo/llms-full.txt (for reading, not editing)
- Prices: each market's `prices.tsv` (typical price, latest, steadiness, last seen, units listed, weekly change)
- What to craft: https://faresbn.github.io/Tazdingo/prices/craft.tsv
- Blizzard's latest Forever posts: https://faresbn.github.io/Tazdingo/more/blizzard/
- When answering price questions, quote the **typical** price, mention **steadiness** (volatile prices are unreliable), and say how old the data is. All prices are asking prices, not sales. Beta prices are only a rough guide.
