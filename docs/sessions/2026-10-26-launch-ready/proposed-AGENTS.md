# FvrRepo — agent instructions

This is AGENTS.md; CLAUDE.md is a symlink to it. It holds what's true for every task in this repository.

FvrRepo builds the **WoW Forever Journal** (https://faresbn.github.io/FvrRepo/): Auction House prices from Fares's Auctionator scans, and the guides, builds and discoveries Fares chooses to keep. Fares writes; Mike reads the site, directly or through their shared ChatGPT project. README.md explains how everything works; read it before changing anything.

## The two everyday tasks

- **"Add the new scan":** run `python3 scripts/ingest.py --push` on `main`. It finds the file, imports, tests, builds, commits and publishes, and undoes itself if a check fails. If it stops, report its message; don't edit data files by hand to get past it.
- **"Save this to the journal":** copy `journal/_template.md` to a new file and fill it in from what Fares gave you. Write an entry only when Fares asks, and only with content he or the conversation supplied. Never invent builds, prices, drop rates or discoveries, and keep tested, read and simulated claims distinct in the entry.

## Data rules

- Never commit an original SavedVariables file (`*.lua`). It holds settings, posting history, searches and shopping lists. Only the market-only extracts that `ingest.py` writes go into the repo; `.gitignore` already blocks `data/captures/**/*.lua`.
- Never edit an extract or its receipt in `data/captures.json` by hand: their fingerprints are checked on every build.
- Item names come from ForeverDB (`scripts/item_names.py`), whose reuse terms require the visible credit "Data from ForeverDB.net". Keep that credit wherever names appear.
- The Forever Beta closed on 23 October 2026. Its sample stays as 30 items; don't import the full Beta catalogue.

## Changing the site

- Standard-library Python only: no packages, no build tools, no server. The site must stay readable without JavaScript, because ChatGPT reads the HTML and `llms-full.txt` without running scripts.
- Before every push, run the three checks GitHub Actions runs: `python3 -m unittest discover -s tests`, `python3 scripts/build.py`, `python3 scripts/check_site.py`. A push to `main` publishes the site within a minute.
- Use a branch for anything bigger than a scan or a journal entry, and merge it into `main` when the checks pass. Version control is part of the job, not an approval point.
- Graphics: generate them through Codex on Fares's ChatGPT plan, keep drafts outside the repo, and put one into the site only once Fares approves it.

## Approvals

Plan before substantial work and wait for Fares's approval. Also stop before anything outward-facing that the approved plan doesn't cover: submitting the site to search engines, changing repository settings or visibility, renaming the repository (that changes the site's address), or messaging anyone.

## Outside reviews

REVIEWER.md describes consultations with the other model family; follow it for milestone reviews.
