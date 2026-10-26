# FvrRepo: launch-ready rebuild

26 October 2026. Forever launches 4 November. Approved in chat ("Fix it"). Checkboxes are the save state.

## What FvrRepo is for

You and Mike ask your shared ChatGPT project about WoW Forever. FvrRepo is what that project reads: Auction House prices from your Auctionator scans, plus the guides, builds and discoveries you choose to keep. You write; Mike reads through ChatGPT and the public site, because Mike has no GitHub account. Beta data stays as a small sample; full data starts with the first launch scan.

## What was wrong, and what changes

**1. ChatGPT couldn't read the site.** OpenAI's web tool, tested through Codex on 26 October, opened a page it found through its own search, but refused every pasted URL, even foreverdb.net. FvrRepo can't be found by search because every page says `noindex`.
- Remove `noindex`, add a sitemap, and give pages clear titles so search engines list them.
- Publish one plain-text file, `fvrrepo.md`, that holds everything ChatGPT needs in one read: what the site is, how to read prices, every journal entry and each market's summary, with the full price list beside it as `prices.tsv`. The same two files can go into the ChatGPT project directly, as a fallback that's never blocked.
- Telling Bing about the site (IndexNow) is outward-facing: ask Fares first.

**2. The first launch scan would have failed.** Every current Auctionator file on this Mac was rejected:
- Random-suffix gear ("…of the Boar") is stored as `gr:<item>:<suffix>` (Auctionator `DBKeyFromLink.lua:38`), and the parser refused these keys. They're most of the keys in current files.
- One unreadable old market anywhere in the file failed the whole file, even when it wasn't being published.
- Fix: accept every key form current Auctionator writes, and decode only the markets being published.

**3. Prices had no names and no dates.** Records said "Item 236" and "quote time unknown".
- Item names come from ForeverDB's addon name list (`SearchNames.lua`), which ForeverDB allows reusing with the credit "Data from ForeverDB.net". The names themselves come from the game client. They're fetched when a scan is added, not during the build, so the site never depends on ForeverDB being up.
- Day codes are now converted to dates. Auctionator's day 0 is local midnight, 1 January 2020 (`Constants/Main.lua:14`), and this matches all three Beta scans exactly. Each item then gets a last-seen date, the number of units listed that day, and daily low/high history (`Database/Mixin.lua`: `m` latest minimum, `h`/`l` daily high/low of the minimum, `a` most units seen that day).

**4. The site was over-built and hard to change.** Thirty prices sat in nine kinds of file behind a 7-step reading guide.
- One page per market with the whole table in plain HTML (readable without JavaScript, so ChatGPT can read it), plus search and sort in the browser.
- Data files per market: `prices.tsv` (latest), `history.tsv` (daily) and `prices.json`. A short `manifest.json` lists everything.
- Build code split into readable templates; page text generated from the data instead of hard-coded.

**5. Scans need a near-automatic route in.** A single command, `python3 scripts/ingest.py`, will:
- find Forever's Auctionator file in the WoW folder
- keep only the market data
- refresh item names
- run the tests and build
- commit, and with `--push`, publish

**6. The journal grows into guides, builds and discoveries.** Each entry is a Markdown file in `journal/`, with a short header (type, class, status, date, sources). It becomes its own page and part of `fvrrepo.md`. Entries are added only when Fares asks. Nothing is invented: the journal starts empty, with a template.

**7. A better-looking site.** New visual design, with hero art generated through Codex (Fares to approve the art).

## Decisions taken (reversible)

- Pages become searchable (`noindex` removed). The site was already public; this only lets search engines list it.
- Still no individual item pages, keeping the earlier decision. Search covers lookups.
- Random-suffix variants are listed as their own rows under the base item's name ("Raider's Shoulderpads of the Boar").
- Fares's Brew instruction files (AGENTS.md, WORKFLOW.md, REVIEWER.md, CLAUDE.md) stay uncommitted. An FvrRepo-specific AGENTS.md is proposed for approval at the end.

## Steps

- [x] Parser: current key forms; decode only selected markets; tests with real-format fixtures
- [x] Item names: fetch + verify ForeverDB names; `data/items.json`; credit
- [x] Ingest command written (`scripts/ingest.py`); end-to-end run still to do
- [x] Build rewrite: market pages, data files, `llms.txt` + `llms-full.txt` (replacing the planned `fvrrepo.md`: same idea, the name ChatGPT and other assistants already look for), sitemap, journal
- [x] Design + Codex hero art (day and night maps); hero reworked so the map dissolves into the page
- [ ] Checks: tests, build, site check, browser check (desktop + phone), launch-scale dry run on a real current file (not committed)
- [ ] Docs: README, STATUS; remove superseded BUILD_PLAN/DATA_CONTRACT
- [ ] Merge to main, push, verify the live site

## Review loop (added at Fares's request: "Continue going through the website until you're convinced it delivers well")

Each pass goes through every page at phone, tablet and desktop widths in light and dark, as each reader:
- **Fares after a scan:** can the scan get in with one command, and does the site show it correctly?
- **Mike via ChatGPT:** can ChatGPT answer "what does Linen Cloth cost?" and "what's our frost mage build?" from `llms-full.txt` alone?
- **Mike on a phone:** can a price be found in under 10 seconds?

Then fix what's found and go round again. A checkpoint is merged to `main` (and so published) every 25–40 minutes, but only when tests, build and site check pass.

## Checks for done

- `python3 -m unittest discover -s tests` passes
- `python3 scripts/build.py` and `python3 scripts/check_site.py` pass
- Ingest of a real current Auctionator file works end to end in a scratch copy, at launch scale
- Live site serves the new pages and `fvrrepo.md` after the merge
