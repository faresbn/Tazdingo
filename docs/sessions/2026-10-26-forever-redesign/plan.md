# Forever redesign: plan for approval

26 October 2026. Responds to Fares's four notes on the live draft. Note 4 (no ChatGPT, Fares or Mike on the public site) is already done and published, with a site check that fails the build if a mention returns. Notes 1–3 change the structure, so they wait for this plan's approval.

## 1. The user journey (note 2)

**Who comes, and why.** The site is public and impersonal; ChatGPT reads the plain-text files, not the pages. So the pages serve a person who comes with one of three intents, most frequent first:

1. **"What's X worth?"** A quick lookup mid-session: sell, buy or craft. Seconds matter, often on a phone.
2. **"What's new?"** A returning visitor catching up: what moved in the market, which builds or discoveries changed since last time.
3. **"How should I play my class / what's out there?"** Reference reading: a class's current build and guide, or what's been found about a zone, dungeon or system.

**The journey, and the rule we stick to:** every page answers "what is this, and how current is it?" first, then offers the next step.

```
Front page ──► one search box (items, classes, topics)  ──► the answer
     │
     ├─► Latest: a dated log of every change, newest first  ──► the changed page
     │
     └─► three doors, always in the same order:
           Auction House   →  market  →  item (row opens daily history)
           Classes         →  class   →  its living guide and builds, with change log
           World           →  topic   →  zone / dungeon / system notes, with change log
```

- The front page is the journal's front page: search first (intent 1), the latest changes second (intent 2), the three doors third (intent 3).
- The same three doors appear in the navigation on every page, in the same order. No other top-level sections; "About and sources" lives in the footer.
- Every detail page shows "Last updated" at the top and its change log at the bottom.

## 2. The content model (note 3)

**What changes:** there are no "journal entries". The whole site is the journal, made of **living pages** that get updated, plus a log of every change.

- `content/classes/<class>.md`: one living page per class (guide, builds, open questions), with a header recording status (idea / testing / tested) per section where it matters.
- `content/world/<topic>.md`: one living page per discovery topic (a zone, a dungeon, a profession, a system).
- Auction House pages stay generated from scans, as now.
- **The log writes itself.** Each update is a git commit. The build reads each page's commit history and turns it into that page's change log and the front page's Latest feed. The only rule for whoever writes an update: a one-line, plain-English commit message ("Mage: added a 40–50 frost build after testing"). Scan imports already write such messages.

**How updates arrive (Fares's note: ChatGPT decides how and when).** The site needs one documented way in, which ChatGPT's workflow can then use on whatever schedule it decides. `UPDATING.md` in the repo would define:
- where each kind of content goes, the page format, and what the build checks (header fields, links, no invented data)
- the commit message rule
- what never goes in (people's names, ChatGPT, private game files)

**Open question for Fares: which channel ChatGPT uses to write.** My recommendation is **Codex in ChatGPT, connected to the GitHub repo**: it's ChatGPT's own route to GitHub, it can edit the content files and open a pull request, and GitHub Actions checks the change before it publishes. The fallback, which needs no setup: ChatGPT writes the update as a file, and Claude or Codex on the Mac applies it with one command. Either way the site side is the same. Only Fares's ChatGPT would hold the GitHub connection; Mike's conversations reach the site through Fares.

## 3. The design (note 1, with Fares's follow-up: "inspired by, not infringing")

**The rule: borrow the mood, not the marks.** The official WoW Forever site (worldofwarcraft.blizzard.com/en-us/forever, read 26 October 2026) sets a mood: dusk and night, cream type on deep blue-green, warm parchment, a gold accent, painterly frontier landscapes. The journal takes that mood. It doesn't take the things that identify Blizzard's site (its trade dress): its exact colours, its typefaces or lookalikes, its ornaments, its navigation pattern or its logo treatment. A visitor should feel they're in the same world, and still never mistake the journal for an official page.

| | Official site (what makes it recognisably Blizzard's) | Journal (inspired, distinct) |
|---|---|---|
| Mood | Dusk sky, deep teal-blue sections, warm parchment, gold | **Kept:** dusk-to-night, deep blue-green, parchment warmth, a gold accent |
| Colours | `#F3EEE2` cream, `#114F72` / `#09344C` teal-blues, `#001845` navy, `#F7B90A` gold | **Our own values** in that family: shifted hues and lightness, never their hex codes |
| Type | Custom flared display face, Blizz Quadrata (WoW's signature lettering), Open Sans, Archivo | **Our own pairing**, with nothing Quadrata-like: IM Fell English (an old printed-book face, a field-journal voice) for headings, Alegreya Sans for text. Both are already on the site |
| Ornament | Cream filigree frames around images | **None of theirs.** The journal's own motif: surveyor's map lines, contour rules, a compass mark |
| Navigation | Floating dark-glass bar with logo and pill buttons | Plain masthead with a typographic wordmark; no logo, no badge |
| Imagery | Blizzard's game art and screenshots | **Original painterly art**, generated through Codex and approved by Fares, that never imitates Blizzard's characters, logos or compositions |
| Theme | Dark | Dark, matching the mood (the light theme goes) |
| Positioning | Official product site | "Unofficial fan project" in the footer and the About page, as now; World of Warcraft credited to Blizzard |

**The name.** "WoW Forever Journal" begins with Blizzard's product name, which is the strongest signal of affiliation the site carries. Fan sites usually use the game's name descriptively next to a name of their own (ForeverDB is one example). Options: keep the name with a clear "unofficial" line; or give the journal its own name and describe it as "an unofficial World of Warcraft: Forever journal". This is a brand call for Fares. Changing the repo name also changes the web address, so decide before asking search engines to index the site.

## 4. Also in this pass

- The hero map gets replaced by the new painterly art (drafts first, for approval).
- The web address still contains `faresbn` (github.io takes the account name). Removing it needs a custom domain or another GitHub account: a decision for later, flagged here only.
- `llms.txt`, `llms-full.txt` and the TSV/JSON files stay as the plain-text side of the site, rewritten for the new structure (classes, world, latest changes).

## Steps after approval

- [ ] `content/` model, `UPDATING.md`, build reads git history for change logs and Latest
- [ ] Pages: front page (search, Latest, three doors), Classes, World, Auction House restyled, footer About
- [ ] Design tokens: own colour values in the Forever mood, own type and ornament; dark only
- [ ] Hero art drafts through Codex, presented for approval before use
- [ ] Plain-text files restructured; checks updated
- [ ] Review loop at phone/tablet/desktop; checkpoints to GitHub every 25–40 minutes

## Decisions needed from Fares

1. **The journey** above: approve, or adjust the three intents and their order.
2. **The channel for ChatGPT's updates:** Codex connected to the repo (recommended), or ChatGPT writing a file for a local agent to apply.
3. **Dark only**, matching the mood: yes or no.
4. **Class pages for all nine classes from the start** (empty ones say "Nothing recorded yet"), or only classes that have content.
5. **The name:** keep "WoW Forever Journal" with an "unofficial" line, or choose a name of its own.
