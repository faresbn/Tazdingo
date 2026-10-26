# Content brief for research agents (v3)

You're writing pages for **Forever Ledger** (https://faresbn.github.io/FvrRepo/), an unofficial journal for World of Warcraft: Forever. Forever launches on 4 November 2026 with a level cap of 60. The Beta closed on 23 October and was capped at level 30, so most guides only cover levels 1–30 and are tentative. Today is 27 October 2026.

Each page is one Markdown file in `/Users/faresb/Documents/Dev/FvrRepo/content/`. Write only the files you're assigned, at exactly the paths given. Don't edit anything else in the repository, and don't commit: the lead agent reviews and commits.

## Rules

1. **Summarise, never copy.** Write every sentence in your own words. No copied paragraphs, lists or tables from any site. Short quoted phrases (under 15 words, in quotation marks, credited) are allowed only when the exact wording matters. Talent names, ability names, item names and numbers are facts, so use them freely.
2. **Never invent.** Every claim must come from a source you read. If sources disagree, say so and name them. If something isn't known yet (anything above level 30 is mostly projection), say that plainly. Don't fill gaps with Classic knowledge unless you label it ("in Classic, …; not yet confirmed for Forever").
3. **Forever isn't Classic.** Specs, talents, abilities, professions and systems changed. Prefer Forever-specific sources, and say what changed from Classic when the sources say so.
4. **Neutral, impersonal voice.** Never name the people behind the site, never mention ChatGPT or AI, and don't write "I" or "we tested". Plain British English, short sentences, active voice.
5. **Cite as you go.** Link sources inline where a claim comes from one site, and list every source under "Read more", each with a few words on what it's best for.
6. **Diversify.** Use at least three independent sources per page where they exist. Good ones:
   - **Wowhead Forever guides:** `https://www.wowhead.com/forever/guide/classes/<class>/<spec>/overview-pve-<dps|tank|healer>`, plus the "Abilities", "Level 20 Overview" and "Level 30 Overview" pages linked from each.
   - **Icy Veins:** spec guides such as `https://www.icy-veins.com/wow-forever/frost-mage-ranged-dps-pve-guide`; the full list is at `https://www.icy-veins.com/wow-forever/all-class-guides`. Also professions-overview, camping, legacy-system and the dungeon guides.
   - **ForeverDB:** `https://foreverdb.net/class/<Class>/guide`, `/pve`, `/pvp`, `/talents`, `/macros`, `/profession/<slug>`, `/camping`, `/legacy`, `/rares`, `/launch`, `/veterans`, and its plain-text digest `https://foreverdb.net/llms-full.txt`. Plain `curl` works for ForeverDB.
   - **WoWSims Forever** (MIT-licensed code): `gh api repos/wowsims/forever/contents/ui/specs/<class>/<spec>/presets.ts` (default talents, gear and stat weights) and `.../apls/*.apl.json` (rotation priority lists). The simulators are at `https://www.wowsims.com/forever/<class>/<spec>/`.
   - **Also:** Method (`https://www.method.gg/wow-forever`), Warcraft Tavern (`https://www.warcrafttavern.com/forever/`), Mobalytics, wowtbc.gg's Forever section, Eternadex, The Forever Era, Kami Labs (macros), wow-professions.com (professions), Blizzard's forums (JSON works, for example `https://us.forums.blizzard.com/en/wow/c/wow-forever/346.json`).

## Reading sites that block scripts

Wowhead, Icy Veins, CurseForge and Mobalytics refuse plain `curl` and WebFetch. Read them in the built-in browser (the `mcp__Claude_Browser__*` tools):
- **Open your own tab** with `tabs_create` and pass its `tabId` on every call. Other agents share this browser, so never use or close another tab. Close yours when you're done.
- Read with `navigate` then `get_page_text`, or `javascript_tool` returning `document.querySelector('#guide-body, main, article').innerText.slice(0, 20000)`. On Wowhead, the guide body is `#guide-body`.
- Read only the pages you need, one at a time. This is reading to summarise, not crawling.
- If the browser tools aren't available to you, use WebSearch results plus the sources that `curl` can read, and say in your report which sites you couldn't read.

## File format

```
---
updated: 2026-10-27
summary: One sentence saying what this page gives the reader.
sources: Short plain list, e.g. Icy Veins, Wowhead, ForeverDB, WoWSims presets
---

## At a glance

…

## What the guides say

…

## Ledger findings

Nothing recorded yet.

## Read more

- [Site: page title](https://…): what it's best for
```

- The header needs `updated` (YYYY-MM-DD) and `summary`. Leave out `confidence` and `status`; they're for later.
- Use `##` for the four sections, in this order, with these exact names. Use `###` and `####` inside them. Never use `#`.
- **At a glance:** 5–8 bullets with bold labels.
- **What the guides say:** the substance. Aim for 400–900 words for a spec or profession, and less for small topics. Use tables where they help (talent order by level, stat priorities, profession skill brackets).
- **Ledger findings:** exactly "Nothing recorded yet." (Our own discoveries go here later.)
- **Read more:** every source you used. Don't repeat the standard links the site adds automatically to class and spec pages: the Wowhead overview, the Icy Veins spec guide, ForeverDB's class guide and talent calculator, and the WoWSims simulator. List them only if you cite a specific sub-page, such as Wowhead's "Level 30 Overview".
- **Markdown that works:** headings, paragraphs, bullet and numbered lists (nest by indenting two spaces), tables, `> quotes`, code blocks (for macros), **bold**, *italics* and links. Link items and spells to ForeverDB (`https://foreverdb.net/item/<id>`, `https://foreverdb.net/spell/<id>`) when you know the ID; the site shows their tooltips.

## Report back

When you're done, reply with:
- the files you wrote
- for each page, the sources you actually read (and which you couldn't)
- any claim you're unsure about
- anything that seemed wrong or contradictory between sources

Keep the report under 400 words.
