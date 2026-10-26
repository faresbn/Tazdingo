# Forever Ledger v3: depth, texture and a living front page

27 October 2026 (night of the 26th). Fares's brief, in his words: "Rebuild, push to main, and leave a running record of everything." This plan is the running record's starting point. Checkboxes are the save state.

## What changes for the reader

1. **The front page becomes a dashboard of what's happening.** It shows the launch countdown, Blizzard's latest Forever posts (a blue tracker that refreshes every two hours), a "before you log in" checklist, a class picker, the market's pulse and the latest ledger changes. It replaces the current static list of doors.
2. **Every class spec and profession gets its own page,** reached through hover menus in the top bar: Classes, then class, then spec; Professions by kind. Each page summarises what the best guides say, in our own words and cited. It links to the guides and tools (Wowhead, Icy Veins, ForeverDB, WoWSims and others), and keeps a **Ledger findings** section for our own discoveries.
3. **Texture and character.** Painted, game-like art made through Codex: a ledger-at-the-inn hero, a banner per section, wax seals for classes and professions, and parchment and leather textures. None of it uses Blizzard marks. Fares's own screenshots replace or join the art after launch: drop them into `site/assets/screens/` and the build uses them.
4. **Updates from ChatGPT leave a record.** "Update the Ledger guide for Frost Mage" means: ChatGPT reads the page from GitHub, edits it and commits it back. A GitHub Action then saves the old version to `archive/` and logs the change in `archive/LOG.md` automatically, so the record never depends on ChatGPT remembering to keep it. The archive lives in the private repo and is never published.

## Decisions taken (reversible)

- **No in-game screenshots exist yet.** None on this Mac, and the game can't be played until 4 November, so the art is original and generated. Blizzard's Legal FAQ allows the player's own screenshots for non-commercial use, which is why `site/assets/screens/` exists.
- **The blue tracker is fetched at build time.** `pages.yml` runs every two hours and refreshes the posts, using the committed `data/blue.json` if Blizzard is unreachable. There are no commits every two hours, so no clashes with Fares's or ChatGPT's pushes. Source: Blizzard's own forum feed (`/groups/blizzard-tracker/posts.json`), filtered to the WoW: Forever categories (346–349) and news posts that mention Forever. Each post shows a short excerpt and links to the original.
- **One file per page, with fixed sections:** At a glance · What the guides say · Ledger findings · Read more. The archive Action backs up every version, whoever edits it.
- **Standard guide links are generated from `data/game.json`,** with checked addresses for Wowhead, Icy Veins, ForeverDB, WoWSims and the talent calculators, so a page's file only lists extra sources.
- **Wowhead and Icy Veins block scripts.** Research subagents read them in a browser tab and summarise them. Nothing is copied; everything is cited.
- **AGENTS.md becomes FvrRepo's own.** Fares's Brew files move to `docs/reference/brew/` (kept, not deleted), so another LLM or machine starts from the right instructions.

## Work

- [x] Research subagents write the content files: classes (5 agents), professions (1), world and More (1)
- [x] Senior outside review (GPT-6 Astra) of this plan and the current code; design ideas from GPT-6.1 Sol
- [x] Art through Codex: hero (day and night), 5 section banners, 9 class seals, 12 profession seals, 2 textures, social card
- [x] Build: spec and profession pages, hover menus (desktop) and nested menu (phone), new front page, blue tracker, launch checklist, archive Action, 404 page, social card
- [x] UPDATING.md rewritten for the "Ledger guide" flow; AGENTS.md; HANDOVER.md; DECISIONS.md
- [x] Review loop: every page type at phone and desktop, light and dark; peer code review; fixes
- [ ] Merge to main, push, verify live; checkpoints every 25–40 minutes

## Checks for done

- Tests, build and site check pass, and the site check covers the new pages
- Every spec, profession and world page has sourced content or an honest "nothing yet"
- Hover menus work with mouse, keyboard and touch
- The blue tracker shows Forever posts; the archive Action is tested on a branch
- HANDOVER.md lets a new thread, LLM or machine continue without this conversation
