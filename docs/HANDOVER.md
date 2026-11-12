# Handover

Where Tazdingo stands, kept current at every checkpoint so another thread, model or machine can carry on. Read this first, then AGENTS.md and README.md. History lives in git and in `docs/sessions/`; this file describes the present.

**Last updated:** 5 November 2026, launch day (session `docs/sessions/2026-11-05-launch-data/`). The inbox went live on 31 October (`docs/sessions/2026-10-31-inbox-live/`); the ChatGPT projects now enter through `docs/chatgpt/START_HERE.md`. `main` is the whole state.

## In flight (7 November)

**Live data has started.** The first Live Auctionator scan is published: 78 items on CAMWOW EU5 Realm 2 PvP (Horde), market slug `forever-pvp`, scanned 01:09 UTC, two hours after launch. ForeverDB data is refreshed at the release build 1.60.1.70790 (level cap 60): recipes, trainers, abilities, 2,778 items with categories and vendor prices. Notes, including what ForeverDB.lua and OneForAll.lua hold: `docs/sessions/2026-11-05-launch-data/notes.md`.

- **Auctionator keys this realm `PvP`, like the Beta market,** so `market_names` in `data/game.json` is keyed by market slug now. `ingest.py` remembers `PvP` as the default Live market; later scans need no `--market`.
- **Keep scanning** three or four times a day and run `python3 scripts/ingest.py --push` after each. The market is tiny on day one; deals, usual prices and patterns need about two weeks of daily lows.
- **Updates run themselves (7 November).** A watcher on Fares's Mac (`tazdingo-update.sh`, kept in the WoW SavedVariables folder, not in this repository) runs Claude Code headless: on every save of Auctionator.lua it runs `ingest.py --push` and confirms the publish run and the homepage; at 06:00, 14:00 and 22:00 it refreshes ForeverDB (site data, item names, API with the key from the Keychain) and publishes after every check. Log: `~/Library/Logs/Tazdingo/update.log`. It needs this checkout clean and on `main`: do code work in a worktree, or its runs will refuse (safely) and notify. iCloud sync leaves `feed/… 2.md` copies (each build rewrites the feed), which blocked a timer run on 9 November; the watcher now runs `python3 scripts/icloud_janitor.py --delete` before every job, which removes any copy whose content is the current file or a version in git. It's Python because under launchd macOS lets python3 and git read ~/Documents, but not bash, find or cmp ("Operation not permitted").
- **Checked 9 November:** every scan save since 7 November imported or correctly found nothing new, and each confirmed live. The API refresh at the new build took about two hours (since 11 November a new build reuses the previous build's item details, so it takes minutes; `fetch --full` is the two-hour version; the item list is 6,277 items now), so the watcher allows two hours for the fetch; a fetch that runs over resumes from its cache next time. A connection reset mid-download, not caught before, is now retried (`item_names.fetch`).
- **Combat logs are filed on the `logs` branch (11 November).** The 8-hourly job runs `scripts/combat_logs.py "_forever_/Logs" ForeverDB.lua --out "~/Library/Application Support/Tazdingo/logs-branch"`: it updates that clone of the `logs` branch, files each game log unchanged for 30 minutes (`--now` files one still being written; it's refiled as it grows) (instance runs, meaning any zone whose instance ID isn't 0 or 1, or with a difficulty, or with a boss fight in it, since Forever logs Razorfen Kraul with Kalimdor's ID, as exact slices behind the log's header; open world as `-open-world.md` summaries of our character and pets), removes logs beyond the last 14 days or 10 per character below 60, rewrites `README.md` (guide + list) and each day's `index.md`, commits it all as one orphan commit and force-pushes `logs`, then deletes game logs over a week old that the pushed branch has. Level-60 characters are skipped and their game logs never deleted. A run over 95 MB stays in `combat-logs-large/` beside the clone. Its git work is in Python so it runs under launchd. `main` holds no logs; the evening's 76 MB in `main`'s history was left (Fares's call to purge, which means a force-push of `main`).
- **A co-player's Windows PC (12 November):** `docs/chatgpt/MIKE_CODEX_WOW_SCRIPTS.md` tells Codex how to install a PowerShell script and scheduled task that sends each new Auctionator scan through the inbox with the co-player's personal key (no GitHub account). It reads the scan time with `ingest.scan_time` from a read-only clone and sends only new scans; it was written on the Mac and hasn't been run on Windows yet. Characters and combat logs from a second player aren't possible yet: the inbox publishes files as sent and takes only pages and `.lua`, and `characters.py` and the `logs` branch assume one player. Fares to decide the route.
- **Characters are tracked (9 November).** The 8-hourly job runs `scripts/characters.py` on ForeverDB.lua: for each of the account's own characters (ForeverDB's `armory` snapshots whose IDs are in its levelling-coach tables) it keeps class, race, level, item level, gear, talents, professions and skills, reputations, stats, PvP and collection counts, under a race-and-class label, in `data/characters.json`; the build writes `feed/characters.md` for ChatGPT. Names, IDs, realms, other players and the bot-suspect list are never copied (`tests/test_characters.py`); the website shows none of it. OneForAll.lua (recipes per character) isn't read.
- **ForeverDB's Recipes.lua gained fields on 7 November** (Classic-trainer flag; fewest/most for random counts). `parse_recipes` now ignores any fields after `new`; `tests/test_foreverdb_data.py` covers all three layouts.
- **Next:** the design discussion Fares asked for after this update.
- **Fares's call:** commit `adbb82f` (the first scan) has the local file path, including the WoW account folder number, in its message. Changing it means rewriting pushed history.

## Picking this up

| You are | Read | Then |
|---|---|---|
| Claude Code or Codex in this repo | This file, AGENTS.md (= CLAUDE.md), README.md; docs/DECISIONS.md before changing anything settled | Branch from `main`, run the checks in "How to work on it", merge and delete the branch |
| The shared ChatGPT project | the appropriate WARCRAFT_DEEP_PROJECT_INSTRUCTIONS.md or WARCRAFT_PROJECT_INSTRUCTIONS.md, TAZDINGO_CONNECTION.md and UPDATING.md | Read through `feed/index.md` in the repository; send page edits and addon files through the inbox |
| Reviewing as the other model family | REVIEWER.md | Log the consultation in the session's `revlog.md` |

The latest plan, research and review log are in `docs/sessions/2026-10-30-public-inbox/` (`plan.md`, `research.md`, `revlog.md`, `codex-deploy-brief.md`).

## The site now

- **Design overhaul (30 October, afternoon):** guide pages are tabbed and open on a **Cheatsheet** (renamed from At a glance; standard labels in `docs/chatgpt/UPDATING.md`) and "Our take" (the Tazdingo recommendation, lifted from What the guides say). `app.js` makes the tabs; without it the page reads in order, and any `#anchor` opens its tab. Menus open under their word with one link per page; "Sources and credits" is in the footer. The Auction House overview is a tabbed board; Deals are now 20% under usual (exceptional = the old 30% + spread test); below-vendor only for Rare+ items and recipes worth 1s+. Market pages are the searchable list with views. Professions overview leads with the gold-making pages. `style.css` was rewritten as one system. 48 cheatsheets were rewritten from each page's own cited content; cheatsheet edits from the inbox go to review. Plan, brief and reviews: `docs/sessions/2026-10-30-design-overhaul/`.

- **Public repository, feed and inbox (30 October):**
  - **The repository is public.** Original Lua files are committed under `data/captures/`.
  - **`feed/` is ChatGPT's markdown,** read from the repository: a map (`feed/index.md`) to price files per market category, crafting per profession and the guide map with each page's version. Every build rewrites it; `feed.yml` refreshes it after other pushes.
  - **The hidden form** at `inbox/` (enabled for testing) posts to `inbox-site/`.
  - **`scripts/inbox.py` and `inbox.yml`** check, apply, review or hold each submission; `scripts/provenance.py` holds the truth rules.
  - **Commits** use the GitHub private address.

- **Final pass (27 October, late evening):** a fresh bug check of the Auction House code found and fixed five defects (a market nobody rescanned being filed again on every import, slug clashes for names in other alphabets, a latest price older than the item's last day, unclear refusals of badly typed inbox records, a one-copper wording slip) and one in the ForeverDB refresh (it would have missed live-scan items and re-used Beta answers at launch). Details in the session's revlog.md.
- **Published and checked live on 27 October, late evening** (publish run 40569733334): homepage Auction House card, the overview's eight blocks (unusually low, below vendor price, investment watch, short supply, movers, always on the market, market index, patterns), item pages, ForeverDB tables on profession and class pages, the More overview and masthead search all load on https://faresbn.github.io/Tazdingo/ with no console errors or sideways scrolling at desktop width; phone width was checked in local preview.

- **Live:** https://faresbn.github.io/Tazdingo/, published from `main` by `.github/workflows/pages.yml` about a minute after each push (returning visitors may see the old version for up to 10 minutes: the host caches pages). A failed test or check publishes nothing.
- **Auction House** (menu: "Auction House", addresses `prices/`): the overview and each market page show what was recorded unusually low (with confidence tiers), items recorded below what a vendor pays, an investment watch (steady and moving items only), short supply, movers over a day and a week, items always on the market, a market index and a weekday × time-of-day grid. Every item has its own page: latest recorded price, usual price, good-buy price, days listed, a 30-day chart (daily bands, recorded prices, typical price, quantity), patterns, recipes that make or use it, vendor price, other players' median. The homepage card shows the top alerts and investments. It now runs on the Live market (`forever-pvp`); the three Beta sample uploads stay as a historical market. Patterns and movers read "collecting" until enough scans build up.
- **Classes, professions, world:** 77 guide pages (four sections each), plus ForeverDB API tables: trainers and bought recipes (with Merchant's Favor costs) on profession pages, best zones by skill on gathering pages, disenchanting on Enchanting, abilities by level on class pages. Release-build data since 5 November (1.60.1.70790, level cap 60); guide pages stay Pre-launch until checked in game.
- **Other:** countdown counted in the browser to 23:00 UTC on 4 November, with a Pre-launch checklist tag; search box on every page; More has an overview page; Blizzard's posts collected every two hours (best-effort timer) and refreshable through the relay.

## How data arrives

| What | How | Notes |
|---|---|---|
| Prices | `python3 scripts/ingest.py --push` on the Mac after every scan (it also commits the original file); or an `Auctionator.lua` sent through the inbox, filed by `inbox.yml` | Each upload is a scan record; kept 30 scans or 30 days (whichever reaches further back), then folded into `data/market/<market>/daily/`. Store and receipts are fingerprinted. The inbox asks for the market until the first live import remembers it |
| Guide pages | Through the inbox (ChatGPT, anyone with a key), or Codex and Claude committing to `content/`; archived on every change | UPDATING.md and TAZDINGO_INBOX.md are ChatGPT's procedure; judgement calls arrive as pull requests for Fares |
| Other addons' files | Through the inbox, kept in `data/captures/forever/<addon>/` | No processor yet; listed in the feed map |
| ForeverDB data | `foreverdb_data.py`, `item_names.py` (no key); `foreverdb_api.py fetch` + `slim` (key in `FOREVERDB_API_KEY`) | Run on the Mac. Re-run the API fetch at launch |
| Blizzard posts | Scheduled Action + the read-only relay | |

## Launch checklist for the data (4 November)

1. First live scan: log out or `/reload`, then `python3 scripts/ingest.py --push` (first time: `--market "Realm Faction"`). Add the market's display name to `market_names` in `data/game.json`.
2. Scan three or four times a day and import after each; use Auctionator's full scan at different times of day, since only full scans feed the time-of-day patterns. Usual prices and confidence build up from daily lows over the first two weeks.
3. Re-run `foreverdb_data.py`, `item_names.py`, and `foreverdb_api.py fetch` + `slim` once ForeverDB's build changes (`fetch` notices the new build and starts a fresh cache); commit. Pre-launch labels on data clear then.
4. Pages stay Pre-launch until checked in game (`status: live`).
5. Screenshots: without the interface (Alt+Z), WebP, listed in `data/game.json`.

## Open items

- **Remaining client checks:** paste the prepared instructions into each ChatGPT project and test its own connected GitHub account. Optional MCP plugin sign-in and browser form/file attachment need client testing; the inbox backend and GitHub connector write path have live proof.
- **Repository size:** about 23 MB of git data on 30 October (`du -sh .git`; mostly loose objects before packing). Lua files and committed price files grow it with every scan. Decide a retention rule before 500 MB (perhaps keep only recent files of non-price addons). Check with `git count-objects -vH`.
- **Thresholds in `scripts/market.py` are first guesses**; tune them after a week of live scans.
- **Watch items from the final bug check** (none affects the site today): in the older `data/market/inbox/` route, one bad record blocks later runs until someone removes it (the new inbox holds bad submissions instead); if the market grows fast after launch, early full scans can count as partial days (the baseline is the median full-scan size); a full scan's time-of-day sample includes items whose price was recorded earlier that day; the Beta capture route credits full scans among published markets only.
- **Actions minutes:** settled. Standard runners are free for public repositories.
- **Site size:** item pages are ~39 KB (half of it the repeated menu); a full live market (~4,200 items) makes the site ~160 MB. Within limits; trim the item-page menu if publishing slows.
- **Next content phase** (Fares): guide length, per-type templates, PvP sections per class and spec, the empty Field findings.
- **Fares's calls:** custom domain (not yet), search engines (not a priority), analytics (none).
- **iCloud:** `scripts/icloud-shield.sh` keeps build output out of sync; `scripts/icloud-janitor.sh [--delete]` removes "name 2.ext" copies identical to the current file or to any version in git, and lists the rest (and any inside `.git`) for a person.

## How to work on it

- **Machine:** Python 3.11+, Node 20+, `git`, `gh` (logged in as faresbn), Codex CLI on the ChatGPT plan (for GPT-6.1 Sol reviews, see REVIEWER.md), `cwebp`.
- **Before any push:** `python3 -m unittest discover -s tests && python3 scripts/build.py && python3 scripts/check_site.py && node --test relay/news.test.mjs && node --test inbox-site/inbox.test.mjs && node --check site/assets/app.js`. Commit the `feed/` changes the build makes.
- **Preview:** `mkdir -p tmp/serve && ln -sfn ../../dist tmp/serve/Tazdingo && python3 -m http.server 8765 --directory tmp/serve` (or the `site` entry in `.claude/launch.json`), then http://localhost:8765/Tazdingo/.
- **Beta originals** are committed in `data/captures/forever-beta/*.lua`, so the comparison test always runs. The Beta stays a 975-item sample (settled): don't put the full Beta files through the new store.
- **Phone checks:** use a browser's device emulation (the built-in browser's mobile preset works).

## Session record

- 26 Oct: repository connected; parser fixed; site v1 → v2; prices with typical price and steadiness; ChatGPT instructions. (`2026-10-26-*`)
- 27 Oct: v3 rebuild (77 pages, menus, dashboard, archive); Tazdingo rebrand and news classification; authentic artwork; UX pass; guide recommendation review; hero checklist tag and browser countdown; iCloud shield; research and the Auction House module with ForeverDB API tables (`2026-10-27-*`). Outside reviews are logged in each session's `revlog.md`.
- 5 Nov: launch day: first Live scan, ForeverDB release-build refresh (`2026-11-05-launch-data`).
- 31 Oct: inbox deployed and proved; ChatGPT entry point and connected-GitHub route (`2026-10-31-inbox-live`).
- 30 Oct: public repository; Lua originals committed; the `feed/` map for ChatGPT; the inbox (hidden form, Site code, `inbox.py` with provenance checks and review pull requests); ChatGPT instructions rewritten (`2026-10-30-public-inbox`).
