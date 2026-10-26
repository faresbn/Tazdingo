# Forever Ledger

An unofficial journal for World of Warcraft: Forever, published at
https://faresbn.github.io/FvrRepo/. It holds Auction House prices from our
Auctionator scans, notes on classes, professions and the game's systems, and
lists of addons, macros and known issues. The repository is private; only the
built site is public, and the site never names the people behind it.

## Who writes what

| What | Written by | How |
|---|---|---|
| Prices | Fares's Mac | `python3 scripts/ingest.py --push` after an in-game scan |
| Notes (`content/`) | The shared ChatGPT project | Commits to `main`, following `docs/chatgpt/UPDATING.md` |
| Game data (`data/foreverdb.json`, `data/items.json`) | Scripts | `scripts/foreverdb_data.py`, `scripts/item_names.py` |
| Structure, design, checks | Claude or Codex | This README and AGENTS.md |

Every push to `main` runs the tests, builds the site and checks it. Only a
passing build is published, so a bad change leaves the previous site online.

## After a scan: add the prices

Scan the Auction House in game, then log out or `/reload` so WoW writes the
addon's file. Then, in this folder, on `main`:

```sh
python3 scripts/ingest.py --push
```

It finds Forever's `Auctionator.lua`, keeps only the market price records,
refreshes item names, runs the tests, builds, checks, commits and pushes. If
anything fails it undoes itself and says which step stopped it. The first time,
it asks which market to publish (`--market "Realm Faction"`), then remembers.
`--list` shows the file's markets. The original file never leaves the Mac.

## Keeping ChatGPT in the loop

- Paste `docs/chatgpt/PROJECT_INSTRUCTIONS.md` into the project's instructions.
- Upload `docs/chatgpt/UPDATING.md` as a project source file: where each kind of
  note goes, the file format, the commit-message rule and when to write.
- ChatGPT reads the site through `llms-full.txt` (everything in one file) and
  each market's `prices.tsv`.

## Refreshing game data

```sh
python3 scripts/foreverdb_data.py   # recipes, crates, camp items, other players' and vendor prices (~1 minute)
python3 scripts/item_names.py       # item names
```

Both fetch from ForeverDB, politely, with the credit "Data from ForeverDB.net"
shown on the site. Run them after launch to replace pre-launch data; the
Pre-launch labels clear once the data is fetched on or after 4 November.

## How prices work

- **Typical price:** the median of each day's cheapest listing over the item's
  last seven days of records, so a troll listing or one-day spike doesn't set it.
- **Latest:** the most recent cheapest listing.
- **Steadiness:** how far the daily price swings over two weeks, from the
  cheapest day to the 80th-percentile day, relative to the median (steady below
  25%, moving below 75%, volatile above).
- **Gold-making tables** use our price when it's current, traded and seen on at
  least three days, otherwise ForeverDB players' median when enough players saw
  it. Vendor-sold reagents use the vendor price.
- **Days** follow Auctionator's own counter, which starts on 1 January 2020.

## Working on the site

Standard-library Python 3.11+, nothing to install.

```sh
python3 -m unittest discover -s tests   # tests
python3 scripts/build.py                # build into dist/
python3 scripts/check_site.py           # links, headings, data files, no names
```

To preview, serve `dist` under `/FvrRepo/` (see `.claude/launch.json`).

| Path | What it is |
|---|---|
| `content/` | Notes, one Markdown file per spec, profession, world topic or list |
| `data/game.json` | Classes, specs, professions, world topics, source links, launch date |
| `data/captures.json`, `data/captures/` | Scan receipts and market-only extracts |
| `data/foreverdb.json`, `data/items.json` | ForeverDB-derived data and item names |
| `scripts/auctionator.py` | Reads SavedVariables and Auctionator's data without running Lua |
| `scripts/build.py`, `pages.py`, `sections.py` | Builds the site; page templates |
| `docs/chatgpt/` | Instructions for the ChatGPT project |

The Forever Beta closed on 23 October 2026. Its three scans stay as a reference
sample: the 975 items the gold-making tables need, labelled Beta.

## Credits

Item names, recipes, crates, camp items, tooltips and second-opinion prices:
Data from ForeverDB.net. The front-page map is an original illustration. World
of Warcraft belongs to Blizzard Entertainment; this project isn't affiliated
with or endorsed by Blizzard.
