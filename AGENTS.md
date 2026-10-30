# Tazdingo: agent instructions

This is AGENTS.md; CLAUDE.md is a symlink to it, so Claude Code and Codex read the same file. It holds what's true for every task here. **Start every session by reading docs/HANDOVER.md**: the current state, what's in flight and how to continue. README.md explains how the site works.

This repository builds **Tazdingo** (https://faresbn.github.io/Tazdingo/), an unofficial journal for World of Warcraft: Forever (launch 4 November 2026). It holds Auction House prices from Fares's Auctionator scans; a page per class, spec, profession and world topic that summarises other sites' guides and records our own findings; addons, macros, known issues, a launch checklist and Blizzard's latest posts. Fares directs (see `~/.claude/CLAUDE.md` if you have it). A shared ChatGPT project reads Tazdingo through the map in `feed/index.md` and sends page updates and addon files through the inbox (`docs/chatgpt/UPDATING.md`, `docs/chatgpt/TAZDINGO_INBOX.md`). Codex and Claude commit to `main` directly.

## Settled decisions (flag before reopening)

They're listed with their reasons in docs/DECISIONS.md. The ones most often got wrong:
- **The public site is impersonal.** It never names Fares or any co-player and never mentions ChatGPT or AI. `scripts/check_site.py` enforces this; don't weaken it.
- **Authentic Warcraft imagery.** Fares authorised official/publicly reusable Warcraft artwork and screenshots on 27 October, superseding the generated-only direction. Use official sources or a documented reuse licence; credit the owner. Register sourced assets in `data/art.json`, keep receipts, and distinguish Classic artwork from Forever captures. No copied website layouts or implied Blizzard endorsement.
- **Summaries in our own words, always cited, never copied.** Wowhead and Icy Veins forbid copying and scraping; read their pages to summarise them, and link to them.
- **Pre-launch is the default.** A page is Live only when someone marks it so after checking it in the live game.
- **Standard-library Python plus Node 20+, a static Pages website, a public repository** (public since 30 October 2026). The website is the only place for visitors; ChatGPT reads markdown from the repository (`feed/`, `content/`), never from the website. The news relay (`relay/`) never receives GitHub credentials; the inbox Site (`inbox-site/`) is separate and holds a token limited to this repository.
- **Inbox submissions are public on arrival, and the checks enforce provenance, not truth** (`scripts/provenance.py`). Changes needing judgement (Live, a recommendation, an outdated finding, a new site) go to Fares as pull requests. Don't loosen these rules to get a submission through.

## Everyday tasks

- **"Add the new scan":** `python3 scripts/ingest.py --push` on `main`, after every scan (three or four a day after launch). It finds the file, files a scan record, tests, builds, commits, pulls and pushes, and undoes itself if anything fails. Report its message if it stops; never edit data files by hand to get past it. Files uploaded to ChatGPT arrive through the inbox (`inbox/`, filed by `inbox.yml`). The older `data/market/inbox/` scan-record route (`ingest.yml`) still works but isn't documented for ChatGPT any more.
- **"Update the Tazdingo guide for X":** edit the page's file in `content/` exactly as docs/chatgpt/UPDATING.md describes. The archive Action backs up the old version automatically.
- **Held inbox submissions:** each is in `inbox/held/<id>/` with `reason.txt` (GitHub emails Fares when one is held). Fix the cause or tell Fares; once dealt with, delete the folder in a commit. Review pull requests (`review/<id>`) are Fares's to merge or close.
- **Refresh game data:** `python3 scripts/foreverdb_data.py` and `python3 scripts/item_names.py` (both fetch from ForeverDB, no key); `python3 scripts/foreverdb_api.py fetch` then `slim` (the ForeverDB API: trainers, recipe vendors, gathering, abilities, disenchanting, vendor prices and item categories; needs `FOREVERDB_API_KEY`, caches in `tmp/`, about 20 minutes the first time); `python3 scripts/blue_posts.py` (Blizzard's forums; the publish workflow also runs it every two hours). Re-run the API fetch at launch, once ForeverDB's build changes and its level cap reads 60: `fetch` notices the new build, moves the old cache aside and fetches everything again.

## Data rules

- Original saved-variables files (`*.lua`, any addon) are committed, unchanged, at `data/captures/<environment>/<addon>/<time UTC>.lua` (`scripts/originals.py`; decided 30 October 2026: they're game data). Never edit one by hand. The website never serves a `.lua`.
- Never edit an extract, a scan record (`data/market/*/scans/`), a daily archive (`data/market/*/daily/`) or their receipts in `data/captures.json` by hand: their fingerprints are checked on every build and before every import. Scan records are kept for the last 30 scans or 30 days, whichever reaches further back, then folded into the daily archive (`scripts/market_store.py`).
- The Auction House measures (`scripts/market.py`) have no sales data behind them: say "recorded" with the scan time (never "seen at" an exact moment: Auctionator keeps one latest price per item per file), call estimates estimates, and keep volatile items out of gold-making tables (settled).
- ForeverDB data needs the visible credit "Data from ForeverDB.net"; keep it wherever its data appears.
- Screenshots publish only when listed in `data/game.json` (`screenshots`), after checking they show no names or chat.

## Changing the site

- Before every push, run what GitHub Actions runs: `python3 -m unittest discover -s tests`, `python3 scripts/build.py`, `python3 scripts/check_site.py` (plus `node --test relay/news.test.mjs`, `node --test inbox-site/inbox.test.mjs` and `node --check site/assets/app.js`). A push to `main` publishes within about a minute.
- The build also rewrites `feed/` (the markdown map ChatGPT reads): commit its changes with yours. `feed.yml` catches any push that didn't. Never edit `feed/` by hand.
- Work on a branch for anything bigger than a scan or a page edit, push checkpoints as you go, merge into `main` when the checks pass, and delete the branch. Version control is part of the job, not an approval point. Ask before anything that rewrites shared history.
- Keep docs/HANDOVER.md current at each checkpoint: what changed, what's in flight, what's next. Record outside reviews in the session's `revlog.md`.
- Graphics: prefer authentic sourced Warcraft imagery, including small creatures and objects. Keep source/licence records in the session folder, register credited assets in `data/art.json`, and optimise delivery copies in `site/assets/art/`. Generation is a fallback, not the default.

## Approvals

Plan before substantial work and wait for Fares's approval, unless he has asked you to go ahead and build. Stop before anything outward-facing that the plan doesn't cover: submitting the site to search engines, changing repository settings or visibility, renaming the repository (that changes the address), buying a domain, or messaging anyone.

## Outside reviews

REVIEWER.md describes consultations with the other model family (Codex for Claude, Claude for Codex), with the reviewer rules to paste and the commands. Use them for plans for major work and at the end of major phases, and log each in the session's revlog.md.
