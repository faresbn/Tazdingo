# FvrRepo: agent instructions

This is AGENTS.md; CLAUDE.md is a symlink to it, so Claude Code and Codex read the same file. It holds what's true for every task here. **Start every session by reading docs/HANDOVER.md**: the current state, what's in flight and how to continue. README.md explains how the site works.

FvrRepo builds **Forever Ledger** (https://faresbn.github.io/FvrRepo/), an unofficial journal for World of Warcraft: Forever (launch 4 November 2026). It holds Auction House prices from Fares's Auctionator scans; a page per class, spec, profession and world topic that summarises other sites' guides and records our own findings; addons, macros, known issues, a launch checklist and Blizzard's latest posts. Fares directs (see `~/.claude/CLAUDE.md` if you have it); a shared ChatGPT project writes page updates following `docs/chatgpt/UPDATING.md`.

## Settled decisions (flag before reopening)

They're listed with their reasons in docs/DECISIONS.md. The ones most often got wrong:
- **The public site is impersonal.** It never names Fares or Mike and never mentions ChatGPT or AI. `scripts/check_site.py` enforces this; don't weaken it.
- **Inspired by WoW Forever, never its marks.** No Blizzard logos, key art, screenshots we didn't take, the game's typefaces (Friz Quadrata, Morpheus) or lookalikes, official frames or copied layouts. Images must look like they come from inside the game (in-game scenes and item-like objects), never abstract art.
- **Summaries in our own words, always cited, never copied.** Wowhead and Icy Veins forbid copying and scraping; read their pages to summarise them, and link to them.
- **Pre-launch is the default.** A page is Live only when someone marks it so after checking it in the live game.
- **Standard-library Python, a static site, a private repo.** Only `dist/` is published.

## Everyday tasks

- **"Add the new scan":** `python3 scripts/ingest.py --push` on `main`. It finds the file, imports, tests, builds, commits, pulls and pushes, and undoes itself if a check fails. Report its message if it stops; never edit data files by hand to get past it.
- **"Update the Ledger guide for X":** edit the page's file in `content/` exactly as docs/chatgpt/UPDATING.md describes. The archive Action backs up the old version automatically.
- **Refresh game data:** `python3 scripts/foreverdb_data.py` and `python3 scripts/item_names.py` (both fetch from ForeverDB); `python3 scripts/blue_posts.py` (Blizzard's forums; the publish workflow also runs it every two hours).

## Data rules

- Never commit an original SavedVariables file (`*.lua`): it holds settings, posting history and searches. `.gitignore` blocks `data/captures/**/*.lua`. The originals live outside the repo (Fares's Downloads folder); the test that compares them skips when they're absent.
- Never edit an extract or its receipt in `data/captures.json` by hand: their fingerprints are checked on every build.
- ForeverDB data needs the visible credit "Data from ForeverDB.net"; keep it wherever its data appears.
- Screenshots publish only when listed in `data/game.json` (`screenshots`), after checking they show no names or chat.

## Changing the site

- Before every push, run what GitHub Actions runs: `python3 -m unittest discover -s tests`, `python3 scripts/build.py`, `python3 scripts/check_site.py` (and `node --check site/assets/app.js`). A push to `main` publishes within about a minute.
- Work on a branch for anything bigger than a scan or a page edit, push checkpoints as you go, merge into `main` when the checks pass, and delete the branch. Version control is part of the job, not an approval point. Ask before anything that rewrites shared history.
- Keep docs/HANDOVER.md current at each checkpoint: what changed, what's in flight, what's next. Record outside reviews in the session's `revlog.md`.
- Graphics: generate them through Codex on the ChatGPT plan (`codex exec`, see docs/HANDOVER.md for the working recipe), keep the originals in the session folder, and convert to WebP for `site/assets/`.

## Approvals

Plan before substantial work and wait for Fares's approval, unless he has asked you to go ahead and build. Stop before anything outward-facing that the plan doesn't cover: submitting the site to search engines, changing repository settings or visibility, renaming the repository (that changes the address), buying a domain, or messaging anyone.

## Outside reviews

REVIEWER.md describes consultations with the other model family (Codex for Claude, Claude for Codex), with the reviewer rules to paste and the commands. Use them for plans for major work and at the end of major phases, and log each in the session's revlog.md.
