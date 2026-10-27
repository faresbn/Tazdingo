# Plan: the Auction House module, plus the first ForeverDB and interface upgrades

27 October 2026, evening. Built from `research.md` (sections 1–6) and Fares's direction to "push the envelope on AH tracking" while enhancing the rest, working autonomously and consulting Sol. Everything here ships to the live site in stages, each one tested, built, checked and verified on the live site before the next.

## In short

1. **Every upload becomes a timestamped price observation.** A compact scan record per upload (latest price plus that day's low, high and most listed, for every item seen), kept for the last 30 scans or 30 days, whichever reaches further back; older records fold into a permanent daily archive. About 115 KB per full-market upload instead of ~1.9 MB.
2. **An analytics layer on top:** unusually low prices, items listed below what a vendor pays, an investment watch, movers from the first day, time-of-day and weekday patterns, listing reliability (the honest stand-in for sales), item categories and dated market events.
3. **An Auction House section to match:** a dashboard overview, upgraded market pages, a page per item with its price chart and patterns, Auction House alerts on the homepage, and item search that lands on the item page.
4. **Two ways in for uploads:** the Mac (`ingest.py`, as today, now keeping each scan) and a ChatGPT route (a script ChatGPT runs on the uploaded file, committing only the compact market record; a GitHub Action folds it in and publishes).
5. **First ForeverDB API wave:** where to learn and buy recipes (with Merchant's Favor costs), gathering zones by skill, disenchanting, class abilities by level; vendor sell prices and item categories feed the Auction House.
6. **Interface and copy:** "Auction House" replaces "Prices" in the menu (addresses unchanged), a new strapline without "Horde-side", search on every page, a More overview page, and the label fixes from research section 4.

## Decisions taken on Fares's behalf

Fares asked me to work autonomously. These are the calls the research left open; each is reversible, none reopens a settled decision.

| Question (research) | Decision | Why |
|---|---|---|
| 1. Menu names | **"Auction House"** replaces "Prices"; addresses stay `prices/`. Camping and Merchant's Favor stay under World | The module is now the site's centre and players search for the in-game term. Keeping addresses avoids redirects. Moving World topics wasn't asked |
| 2. More | Give it an **overview page** like the others | Smallest change that makes all five menu labels behave the same |
| 3. Market names | A **display-name rule**: a `market_names` map in `data/game.json` (raw Auctionator key → shown name), falling back to the raw key with "Beta" labelling | Live names aren't known yet; a map handles any split |
| 4. Homepage | The market block becomes an **Auction House block** (alerts, investments, movers); other rows unchanged | Fares's priority is the AH; the other homepage choices weren't asked |
| 5. Early movement | Answered by Fares: **per-scan tracking**. Movers use the median of the item's previous 24 hours of scans (three or more) as the baseline | Avoids single-scan noise and the unfinished-day bias |
| 6. Search | **On every page**, in the masthead | Item pages make search the main way into the AH |
| 7–10. Templates | **Not in this plan.** Template work belongs with the next phase on writing (guide length, PvP sections) | Fares put inner-page writing in the next phase |
| 11. Strapline | **"An unofficial field guide and market tracker for World of Warcraft: Forever"**; the greeting keeps "Loktar Ogar" | Fares dislikes "Horde-side field guide"; the game name stays spelled out (settled) |
| 12. Pre-launch labels | Unchanged | Touches a settled decision; not needed for the AH |
| 13. API scope | Wave 1 as research section 5 proposed, plus vendor sell prices and item categories for the AH | The AH needs both |
| 14. API run location | **The Mac**, like the other ForeverDB scripts | An Actions secret is a repository settings change, which needs Fares |
| 15. Actions minutes | **No new scheduled jobs.** The new ingest workflow runs only when a record is committed | Billing is unclear (research section 1) |
| 16. Analytics | None | Outward-facing; not asked |

## Phase A: scan records and retention

**What it means for Fares:** each upload is kept as its own observation, so the site can chart prices through the day; the repository stays small; history beyond Auctionator's 21 days is never lost.

**How it works.**
- **Scan record** (`data/market/<market-slug>/scans/<UTC time>.json`): format `scan-record-v1` with the source file's fingerprint, the scan time (newest `TimeOfLast…Scan`), the Auctionator day, and per item seen that day `[m, l, h, a]` (latest price; that day's low, high and most listed). Items not seen on the scan's day are left out (their `m` is stale).
- **Daily archive** (`data/market/<market-slug>/daily.json`): per item per day `[low, high, most listed, scans, median scan price]`, written when scan records age out. Days present in a newer upload's own 21-day history are taken from there.
- **Retention:** keep every record within 30 days of the newest, and the newest 30 if they reach further back; fold the rest into the archive and delete their files. Their receipts stay, marked `folded`.
- **Receipts:** `data/captures.json` gains a `scans` list (path, market, environment, scan time, source fingerprint, record fingerprint, status) and an `archives` map (path, fingerprint). The build verifies every kept record and every archive against its fingerprint, as it does for today's extracts. The three Beta extracts and their receipts stay exactly as they are; the build reads them as before and also treats each as one scan observation.
- **`ingest.py` (Mac):** after parsing, writes a scan record instead of a full extract, applies retention, then tests, builds, commits and pushes as today. A same-content upload is still skipped.
- **ChatGPT route:** `scripts/scan_record.py` (standard library only, imports `auctionator.py`) turns an uploaded `Auctionator.lua` into a scan record; ChatGPT commits it to `data/market/inbox/`. A new workflow `ingest.yml` (on pushes to the inbox only) runs `ingest.py --inbox`: validates, files the record, applies retention, refreshes item names, runs the tests, build and checks, commits with its own token, then starts `pages.yml` with `workflow_dispatch` (the default token can't trigger a push run). UPDATING.md gets the steps. Untested on ChatGPT's side until Fares tries it.

**Specifics:** new `scripts/market_store.py` (record format, validation, retention, archive fold); changes to `ingest.py`, `build.py` (`collect`, `build_markets`), `.github/workflows/ingest.yml`; tests for record round-trip, retention edges (quiet month, busy month), fold arithmetic, fingerprint failures, inbox validation.

## Phase B: the analytics layer

**What it means for Fares:** the site points at what's worth acting on now (cheap listings, vendor arbitrage, items worth buying to resell) and learns how the market moves through the day and week.

**How it works** (new `scripts/market.py`, pure functions over one market's observations):
- **Reference price** per item: median of its scan prices in the window when it has six or more on at least two days; otherwise the median daily low over 14 days (today's typical price).
- **Unusually low now:** seen in the newest scan; latest price at most 70% of the reference; a robust z-score of 3.5 or more (median absolute deviation) when the item's price varies; reference at least 1 silver; a confidence tier (high, medium, low) from the history behind the reference and how reliably the item is listed, with low hidden and counted; 90% or more under usual is treated as low confidence (probably one mispriced unit). Sorted by the gold saved per unit.
- **Below vendor price:** latest price below the vendor sell price (ForeverDB API). Certain profit if the listing is still there.
- **Investment watch:** buy at the latest price, resell at the reference less the 5% Auction House cut; positive expected margin only; listed on at least 60% of the window's days; shown with margin per unit, return on cost, steadiness and how often it's listed. Ranked by expected margin per unit, weighted by listing reliability and by steadiness (volatile items rank lower). Called "an estimate from the price spread, not proven demand".
- **Movers:** "last 24 hours" (latest against the median of the item's earlier scans in the previous 24 hours, three or more, baseline at least 50 copper, move at least 15%) alongside today's weekly rule.
- **Listing reliability** (the stand-in for "how well it sells"): share of window days and scans the item was listed, median most-listed per day, and how often its minimum price changes between consecutive scans. Labelled as listing activity, never sales.
- **Patterns:** each scan price divided by the item's window median; averaged per weekday and per four-hour band (UTC, shown in the visitor's time by the browser), for the market (median across items) and for an item with enough scans. Cells with too few observations show as "collecting".
- **Short supply:** priced at least 20% over usual while the last full day's most-listed fell to half its usual level or less (Saddlebag's shortage rule).
- **Good-buy price** per item: the usual price less half its usual swing, once it has eight or more prices.
- **Market index:** each finished full day, the median across items of their lowest price against their own usual level, times 100; for reading what an event did to the market.
- **Partial days:** days covering under half the usual number of items (a few searches, not a full scan) and the unfinished newest day are left out of stock and index comparisons.
- **Categories:** class and subclass from the ForeverDB item list (Consumable, Trade Goods, Recipe, Projectile…), for filtering and grouping.
- **Events:** a `market_events` list in `data/game.json` (launch 4 November 23:00 UTC; raids open 9 December), drawn on charts.

**Specifics:** thresholds live in one place at the top of `market.py`; tests with synthetic scans for each rule's guards (thin history, stale sighting, flat prices, a troll listing, a quiet month).

## Phase C: the Auction House section

**What it means for Fares:** an Auction House that answers "what's cheap now, what should I buy to resell, how is this item behaving, when is the best time to buy or sell".

- **Menu:** "Auction House" with Deals, Investments, Movers, What to craft, Waylaid Crates, Materials, and the markets.
- **Overview (`prices/`):** a dashboard per market: unusually low now, below vendor price, investment watch, movers (24 hours and week), most reliably listed, the market's weekday × time-of-day pattern grid, categories, and the gold-making links. Every list shows its scan time.
- **Market page:** the same blocks in full, the item table gains a category filter and links each item to its page; the "Reading these prices" notes explain every measure honestly (no sales data).
- **Item page (`prices/<market>/item/<id>/`)** for every item with data: latest, typical and reference prices; alert status; investment estimate; listing reliability; steadiness; a server-drawn chart of scan prices over the daily low–high band with event markers; the item's patterns when it has enough scans; the last 30 days and last 30 scans as tables; vendor price; ForeverDB players' median for comparison; recipes that make or use it; links to ForeverDB.
- **Homepage:** the market block becomes the Auction House block (top alerts, top investments, movers), Beta-labelled until live data arrives.
- **Search** sends items to their item page. **Exports:** TSV and JSON gain the new measures; `llms-full.txt` carries the alerts and investments.

**Specifics:** `scripts/pages.py` (market and overview templates, homepage block), a new `scripts/ah_pages.py` (item pages, charts), `site/assets/style.css`, `site/assets/app.js` (local-time labels; table links), `scripts/check_site.py` (item pages in the checks).

## Phase D: ForeverDB API wave 1

**What it means for Fares:** profession, class and gathering pages gain facts instead of more prose, and the AH gains categories and vendor prices.

- `scripts/foreverdb_api.py` fetches into a local cache (written; the first fetch ran on 27 October) and `slim` writes `data/foreverdb-api.json` (only what pages use).
- **Profession pages:** "Where to learn" (trainers by faction and zone, Forever-seen or Classic data) and "Recipes you buy" (vendor, price or Merchant's Favor cost, limited stock).
- **Gathering pages:** best zones by skill range. **Enchanting:** disenchant results by item level. **Class pages:** abilities by level and tree, new-in-Forever marked.
- Each table carries a linked "Data from ForeverDB.net" credit and the game build, Pre-launch labelled like today's data.

## Phase E: interface and copy

- Strapline and homepage title (above); hero description without "Horde-side" or promised discoveries.
- Masthead search on every page (the homepage search code, reused).
- More overview page; the More menu label points to it.
- Label fixes: "Market pulse", "Listing margins" lead-in, "From the data"/"In the data" → "In the game data", "Blizzard says" vs "Blizzard posts" → "Blizzard's posts" in both, "Last verified check" → relative time, the Classes overview promise, the 404 line, the footer build line moved to the Sources page.

## Phase F: documents, review, publication

- DECISIONS.md: today's decisions (per-scan tracking and retention, AH priority, PvP per class and spec, the strapline, the menu name). HANDOVER.md rewritten to current state (folding in STATUS.md). AGENTS.md and README.md: the new data layout and ingest routes. UPDATING.md: the ChatGPT scan route and the Auction House notes.
- Sol reviews the plan before building and the finished work before the final publish.
- Each phase: branch from main, tests, build, check, local preview, merge, push, live check.

## As built, after three review rounds

The final observation model is in research section 6 ("The observation model, as built"): recorded prices timed by uploads, usual prices from daily lows, time of day only from full scans, weekday from daily lows. The store keeps a journal so an import cut off mid-write is undone on the next run, verifies itself before every change, removes folded records only after the archive and registry are written, and cleans up folders a failed import created. Revlog has the detail.

## Out of scope

Guide prose (length, PvP sections, templates); a companion addon for sales data; search-engine submission; a custom domain; analytics; moving World topics.

## Changes during the build

- The tool survey (`sources/ah-tools.md`) added confidence tiers, short supply, the good-buy price, the market index and a volatility penalty, and moved the deal test to the published 3.5 threshold.
- The Beta catalogue stays a 975-item sample (settled): the full Beta files are not put through the new store, which is for live scans.
- Sol's review (revlog) changed the build in substance: uploads count as **sightings** only when an item is new to that day or changed; "fresh" means seen on the newest Auctionator day, and lists show when each item was seen; the store is verified before every import and folded records are deleted only after the archive and registry are written; uploads for already-folded days are refused; the inbox carries all 21 days of history; the investment watch excludes volatile, too-new and thinly listed items (settled rule); presence is measured against the market's full days (shown as "9 of 13"); the plan's "share of scans listed" is dropped (sightings aren't scans); patterns need ten items on two dates per cell and aggregate per item first.
- Item pages weigh about 39 KB, half of it the repeated menu; at a full live market (~4,200 items) the site is ~160 MB. Fine for Pages; trim if deploys slow down.
- Market display names come from `market_names` in `data/game.json`; the Beta markets read "Beta PvP realm" and "Beta Classic PvP realm".

## Risks

- **Launch-day ingest must keep working.** Phase A changes the path Fares uses on 4 November. Mitigation: end-to-end tests on the real Beta files, and the old extracts stay readable.
- **Beta data is thin** (three uploads, 975 items), so patterns and 24-hour movers will show "collecting" until live scans arrive. Deals and investments work from the Beta daily history.
- **The ChatGPT route is untested** on ChatGPT's side.
- **Thresholds are first guesses**; they live in one place so they're easy to tune once live data exists.
