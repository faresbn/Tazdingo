# Tazdingo

An unofficial field guide and market tracker for World of Warcraft: Forever, published at
https://faresbn.github.io/Tazdingo/. It holds Auction House prices from our
Auctionator scans, notes on classes, professions and the game's systems, and
lists of addons, macros and known issues. Not affiliated with or endorsed by
Blizzard Entertainment; World of Warcraft and Warcraft are trademarks of Blizzard
Entertainment, Inc.

This repository is public. The website is the place for people; this repository holds
what builds it, the original addon files our prices come from (`data/captures/`), and
`feed/`, the plain markdown map ChatGPT reads (start at `feed/index.md`). Data from
ForeverDB.net is used with credit (`data/README.md`).

## Who writes what

| What | Written by | How |
|---|---|---|
| Prices | The Mac, or anyone through the inbox | `python3 scripts/ingest.py --push` after an in-game scan; or an `Auctionator.lua` sent through the inbox, filed by `inbox.yml` |
| Notes (`content/`) | The shared ChatGPT project, or Codex and Claude | Through the inbox, following `docs/chatgpt/UPDATING.md` (checked by `scripts/inbox.py` and `scripts/provenance.py`); Codex and Claude commit to `main` |
| Other addons' files | Anyone through the inbox | Kept as uploaded in `data/captures/<environment>/<addon>/` until a processor exists |
| Game data (`data/foreverdb.json`, `data/items.json`, `data/foreverdb-api.json`) | Scripts | `scripts/foreverdb_data.py`, `scripts/item_names.py`, `scripts/foreverdb_api.py` |
| Structure, design, checks | Claude or Codex | This README and AGENTS.md |

Every push to `main` runs the tests, builds the site and checks it. Only a
passing build is published, so a bad change leaves the previous site online.

## After a scan: add the prices

Scan the Auction House in game, then log out or `/reload` so WoW writes the
addon's file. Then, in this folder, on `main`:

```sh
python3 scripts/ingest.py --push
```

It finds Forever's `Auctionator.lua`, turns it into a scan record (the scan's
time and every item's latest price, plus that day's low, high and most listed),
merges its daily history into the archive, refreshes item names, runs the tests,
builds, checks, commits and pushes. Run it after every scan: each upload is kept
for the last 30 scans or 30 days (whichever reaches further back), then folded
into the daily archive. Uploads that include a full scan, at different times of
day, are what the time-of-day patterns are built from. If
anything fails it undoes itself and says which step stopped it. The first time,
it asks which market to publish (`--market "Realm Faction"`), then remembers.
`--list` shows the file's markets. The original file never leaves the Mac.

## Keeping ChatGPT in the loop

- Paste `docs/chatgpt/PROJECT_INSTRUCTIONS.md` into the project's instructions.
- Upload `docs/chatgpt/UPDATING.md` (where each kind of note goes, the file format,
  the change-note rule and when to write) and `docs/chatgpt/TAZDINGO_INBOX.md` (how
  to read the map and use the inbox; each person adds their own key to their copy).
- ChatGPT reads the repository, starting at `feed/index.md`: a map to one small
  markdown file per market category, profession and guide page. The build writes
  `feed/`; nothing in it is edited by hand.

## The inbox

A hidden form at https://faresbn.github.io/Tazdingo/inbox/ (not in the menu, sitemap
or search) posts to a small ChatGPT Site (`inbox-site/`). The Site checks the personal
key, then commits the submission, key removed, to `inbox/<id>/`. `inbox.yml` runs
`scripts/inbox.py`:
- **Pages** must be a known page at its current version, in the page format, and pass
  the provenance rules (`scripts/provenance.py`). They're applied, archived and
  published, or sent to the owner as a pull request when they need judgement.
- **Addon files** are kept; Auctionator's is filed as a scan.
- **Failures** are held in `inbox/held/<id>/` with the reason, and the run fails so
  GitHub emails the owner.

Everything sent is public on arrival.

## Refreshing game data

```sh
python3 scripts/foreverdb_data.py   # recipes, crates, camp items, other players' and vendor prices (~1 minute)
python3 scripts/item_names.py       # item names
FOREVERDB_API_KEY=… python3 scripts/foreverdb_api.py fetch && python3 scripts/foreverdb_api.py slim
```

All three fetch from ForeverDB, politely, with the credit "Data from ForeverDB.net"
shown on the site. Run them after launch to replace pre-launch data; the
Pre-launch labels clear once the data is fetched on or after 4 November. The
API script needs `FOREVERDB_API_KEY` (never written anywhere) and caches its
answers in `tmp/foreverdb-api/`; when ForeverDB's build changes it moves that
cache aside and fetches everything again.

## How prices work

The Auction House overview and each market page list what was recorded unusually
low, items recorded below what a vendor pays, an investment watch, short supply,
movers over a day and a week, items always on the market, a market index and a
weekday × time-of-day grid; every item has its own page with a 30-day chart.
The methods and thresholds are in `scripts/market.py`. Auctionator records
prices and the most units listed each day, never sales, so none of this claims
what sold.

- **Typical price:** the median of each day's cheapest listing over the item's
  last seven days of records, so a troll listing or one-day spike doesn't set it.
- **Latest:** the most recent cheapest listing.
- **Usual price** (item pages and alerts): the median of the item's daily lows
  over its last 14 finished days. An item is a deal when its latest price is at
  least 20% under that, and exceptional when it's at least 30% under and far
  outside its normal spread; the confidence tier says how much history stands
  behind the flag. "Below vendor price" is flagged only for Rare or better items
  and recipes, at 1 silver a unit or more.
- **Steadiness:** how far the daily price swings over two weeks, from the
  cheapest day to the 80th-percentile day, relative to the median (steady below
  25%, moving below 75%, volatile above).
- **Gold-making tables** use our price when it's current, traded and seen on at
  least three days, otherwise ForeverDB players' median when enough players saw
  it. Vendor-sold reagents use the vendor price.
- **Days** follow Auctionator's own counter, which starts on 1 January 2020.

## Working on the site

Python 3.11+ and Node.js 20+; no package installation. Node runs the shared news classifier and its tests.

```sh
python3 -m unittest discover -s tests   # tests
python3 scripts/build.py                # build into dist/
python3 scripts/check_site.py           # links, headings, data files, no names
```

To preview, serve `dist` under `/Tazdingo/` (see `.claude/launch.json`).

| Path | What it is |
|---|---|
| `content/` | Notes, one Markdown file per spec, profession, world topic or list |
| `data/art.json`, `site/assets/art/` | Credited Warcraft artwork, publication allowlist and delivery copies |
| `data/game.json` | Classes, specs, professions, world topics, source links, launch date |
| `data/captures.json`, `data/captures/` | Scan receipts and market-only extracts |
| `data/foreverdb.json`, `data/items.json` | ForeverDB-derived data and item names |
| `scripts/auctionator.py` | Reads SavedVariables and Auctionator's data without running Lua |
| `data/market/` | Scan records and the daily archive per market (`scripts/market_store.py`); `inbox/` takes records committed from ChatGPT |
| `scripts/market.py`, `scripts/ah_pages.py` | Auction House measures; the tabbed board and item pages |
| `data/foreverdb-api.json` | Slimmed ForeverDB API data (`scripts/foreverdb_api.py`) |
| `scripts/build.py`, `pages.py`, `sections.py` | Builds the site; page templates |
| `docs/chatgpt/` | Instructions for the ChatGPT project |

The Forever Beta closed on 23 October 2026. Its three scans stay as a reference
sample: the 975 items the gold-making tables need, labelled Beta.

## Credits

Item names, recipes, crates, camp items, tooltips and second-opinion prices:
Data from ForeverDB.net. Scenery comes from Blizzard's Forever reveal press kit;
character cut-outs from its Classic fan-site kit. Sources, editions, delivery
changes and file fingerprints are recorded in `data/art.json`; the website
credits every image under Sources and credits (linked from every page's footer). World of Warcraft belongs to
Blizzard Entertainment; this project isn't affiliated
with or endorsed by Blizzard.

## News and visitor refresh

GitHub Actions reads Blizzard every two hours and classifies complete posts/articles using the same classifier as the read-only browser relay. Dedicated Forever news appears on the homepage. Mixed roundups appear only on the news page with a tag and a Forever-only excerpt. Ambiguous or unreadable articles are held back. `data/blue.json` records classifications, reasons, source hashes and the last successful check; `data/news.json` is its published snapshot.

The Refresh news button checks the separate public relay, sharing a five-minute cache. It does not grant visitors GitHub publishing access or rebuild Pages. The website remains on GitHub Pages; the relay source and deployment notes are in `relay/`. Existing browser views can show a newer relay result before the next static snapshot is published.

After pulling the rename into an existing local checkout: `git remote set-url origin https://github.com/faresbn/Tazdingo.git`.
