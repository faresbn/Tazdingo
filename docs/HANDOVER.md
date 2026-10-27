# Handover

Where Tazdingo stands, kept current at every checkpoint so another thread, model or machine can carry on. Read this first, then AGENTS.md and README.md. History lives in git and in `docs/sessions/`; this file describes the present.

**Last updated:** 27 October 2026, late evening, after the Auction House module (session `docs/sessions/2026-10-27-site-plan/`).

## The site now

- **Live:** https://faresbn.github.io/Tazdingo/, published from `main` by `.github/workflows/pages.yml` about a minute after each push (returning visitors may see the old version for up to 10 minutes: the host caches pages). A failed test or check publishes nothing.
- **Auction House** (menu: "Auction House", addresses `prices/`): the overview and each market page show what was seen unusually low (with confidence tiers), items seen below what a vendor pays, an investment watch (steady and moving items only), short supply, movers over a day and a week, items always on the market, a market index and a weekday × time-of-day grid. Every item has its own page: latest sighting, usual price, good-buy price, days listed, a 30-day chart (daily bands, sightings, typical price, quantity), patterns, recipes that make or use it, vendor price, other players' median. The homepage card shows the top alerts and investments. Until live scans arrive it runs on the three Beta sample uploads, so patterns and day movers read "collecting".
- **Classes, professions, world:** 77 guide pages (four sections each), plus ForeverDB API tables: trainers and bought recipes (with Merchant's Favor costs) on profession pages, best zones by skill on gathering pages, disenchanting on Enchanting, abilities by level on class pages. All still Beta-build data (1.60.1.70532, level cap 30), labelled Pre-launch.
- **Other:** countdown counted in the browser to 23:00 UTC on 4 November, with a Pre-launch checklist tag; search box on every page; More has an overview page; Blizzard's posts collected every two hours (best-effort timer) and refreshable through the relay.

## How data arrives

| What | How | Notes |
|---|---|---|
| Prices | `python3 scripts/ingest.py --push` on the Mac after every scan; or an `Auctionator.lua` uploaded to ChatGPT, which commits a scan record to `data/market/inbox/` for the `ingest.yml` Action to file | Each upload is a scan record; kept 30 scans or 30 days (whichever reaches further back), then folded into `data/market/<market>/daily/`. Store and receipts are fingerprinted |
| Guide pages | ChatGPT commits to `content/` (confirmed working); the archive Action backs up every change | UPDATING.md is ChatGPT's procedure |
| ForeverDB data | `foreverdb_data.py`, `item_names.py` (no key); `foreverdb_api.py fetch` + `slim` (key in `FOREVERDB_API_KEY`) | Run on the Mac. Re-run the API fetch at launch |
| Blizzard posts | Scheduled Action + the read-only relay | |

## Launch checklist for the data (4 November)

1. First live scan: log out or `/reload`, then `python3 scripts/ingest.py --push` (first time: `--market "Realm Faction"`). Add the market's display name to `market_names` in `data/game.json`.
2. Scan three or four times a day and import after each: that's what fills movers, patterns and confidence.
3. Re-run `foreverdb_data.py`, `item_names.py`, and `foreverdb_api.py fetch` + `slim` once ForeverDB's build changes; commit. Pre-launch labels on data clear then.
4. Pages stay Pre-launch until checked in game (`status: live`).
5. Screenshots: without the interface (Alt+Z), WebP, listed in `data/game.json`.

## Open items

- **The ChatGPT scan route is untested on ChatGPT's side** (running the repository's scripts in its sandbox and committing a record of up to ~1–2 MB). The Action side is tested here only through `ingest.py --inbox`.
- **Thresholds in `scripts/market.py` are first guesses**; tune them after a week of live scans.
- **Actions minutes:** GitHub's docs conflict on whether Pages runs count; only the billing page settles it (Fares). No new scheduled jobs were added.
- **Masthead strapline** wraps to three lines between about 860 and 1,240 px wide; worth a polish.
- **Next content phase** (Fares): guide length, per-type templates, PvP sections per class and spec, the empty Field findings.
- **Parked:** a route for someone without a GitHub account to send content through ChatGPT.
- **Cleanup waiting for Fares's OK:** merged remote branches `fix/visitor-news-cache`, `design/authentic-warcraft-art`, `design/focused-ux-pass`, `content/recommendation-review`, `research/site-plan`.
- **Fares's calls:** custom domain (not yet), search engines (not a priority), analytics (none).
- **iCloud:** `scripts/icloud-shield.sh` keeps build output out of sync; `scripts/icloud-janitor.sh [--delete]` removes identical "name 2.ext" copies.

## How to work on it

- **Machine:** Python 3.11+, Node 20+, `git`, `gh` (logged in as faresbn), Codex CLI on the ChatGPT plan (for GPT-6.1 Sol reviews, see REVIEWER.md), `cwebp`.
- **Before any push:** `python3 -m unittest discover -s tests && python3 scripts/build.py && python3 scripts/check_site.py && node --test relay/news.test.mjs && node --check site/assets/app.js`.
- **Preview:** `mkdir -p tmp/serve && ln -sfn ../../dist tmp/serve/Tazdingo && python3 -m http.server 8765 --directory tmp/serve` (or the `site` entry in `.claude/launch.json`), then http://localhost:8765/Tazdingo/.
- **Beta originals** (not in git) sit in `data/captures/forever-beta/*.lua` on this Mac; the comparison test skips without them. The Beta stays a 975-item sample (settled): don't put the full Beta files through the new store.
- **Phone checks:** use a browser's device emulation (the built-in browser's mobile preset works).

## Session record

- 26 Oct: repository connected; parser fixed; site v1 → v2; prices with typical price and steadiness; ChatGPT instructions. (`2026-10-26-*`)
- 27 Oct: v3 rebuild (77 pages, menus, dashboard, archive); Tazdingo rebrand and news classification; authentic artwork; UX pass; guide recommendation review; hero checklist tag and browser countdown; iCloud shield; research and the Auction House module with ForeverDB API tables (`2026-10-27-*`). Outside reviews are logged in each session's `revlog.md`.
