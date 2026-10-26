# WoW Forever Journal

Fares and Mike's shared notebook for World of Warcraft: Forever, published at
https://faresbn.github.io/FvrRepo/. It holds Auction House prices from Fares's
Auctionator scans, and the guides, builds and discoveries worth keeping. ChatGPT
reads it too: everything is in one plain-text file, `llms-full.txt`.

This repository is private; only the built site is public. Fares writes to it,
and Mike reads the site (directly or through ChatGPT).

## After a scan: add the prices

Scan the Auction House in game, then log out or `/reload` so WoW writes the
addon's file. Then, in this folder:

```sh
python3 scripts/ingest.py --push
```

That finds Forever's `Auctionator.lua` in `/Applications/World of Warcraft/_forever_`,
keeps only the market price records, refreshes item names, runs the tests,
builds and checks the site, commits, and pushes. Run it on `main`: a push to
`main` is what republishes the site, which takes a minute or two. If anything
fails, the import undoes itself and says which step stopped it.

- The first time, it asks which market to publish (`--market "Realm Faction"`)
  if the file holds more than one, then remembers the choice.
- `--list` shows the markets in the file; `--no-commit` stops before git.
- The original file never leaves the Mac. Settings, posting history, searches
  and shopping lists stay in it; the repo keeps only its fingerprint.

## Add a journal entry

Copy `journal/_template.md` to a new file in `journal/` (for example
`frost-mage-levelling.md`), fill in the header and write the entry in Markdown.
ChatGPT can draft it in this format. Commit and push, or ask Claude or Codex to
add it. Entries are added only when Fares asks.

The header's `type` is `guide`, `build` or `discovery`; `status` is `idea`,
`testing`, `tested` or `outdated`. Links to foreverdb.net items and spells get
tooltips on the site.

## How ChatGPT reads it

ChatGPT's web tool opens pages it finds through search; it refuses most pasted
links. So the site is open to search engines, and:

- `llms.txt` is a short index; `llms-full.txt` holds the reading guide, every
  journal entry, and each market's summary and price table.
- Each market has `prices.tsv` (every item: typical and latest price, last seen,
  units listed, weekly change) and `history.tsv` (daily lowest and highest
  price and units listed).
- `llms-full.txt` and `prices.tsv` also work as files uploaded to a ChatGPT
  project, for when search can't find the site.

## How prices work

Auctionator records, per item, the cheapest listing each time a scan sees it,
plus each day's cheapest and highest-cheapest listing and the most units
listed. The site's **typical price** is the median of each day's cheapest
listing over the item's last seven days of records, so one troll listing or
one-day spike doesn't set the price. **Latest** is the most recent cheapest
listing. Day numbers count from midnight on 1 January 2020, as in
Auctionator's `Constants/Main.lua`.

## Working on the site

Standard-library Python 3.10+ and nothing to install.

```sh
python3 -m unittest discover -s tests   # tests
python3 scripts/build.py                # build into dist/
python3 scripts/check_site.py           # check links, headings and data files
python3 scripts/item_names.py           # refresh item names from ForeverDB
```

To preview, serve `dist` under `/FvrRepo/` (see `.claude/launch.json`).
GitHub Actions runs the same three checks on every push and publishes `main`.

| Path | What it is |
|---|---|
| `data/captures.json` | One receipt per scan: fingerprints, environment, markets published |
| `data/captures/<environment>/` | Market-only extracts of each scan |
| `data/items.json` | Item names (Data from ForeverDB.net) |
| `journal/` | Journal entries in Markdown |
| `scripts/auctionator.py` | Reads SavedVariables and Auctionator's CBOR data without running Lua |
| `scripts/build.py`, `scripts/pages.py` | Builds the site; page templates |
| `site/assets/` | Styles, script, hero art |

The Forever Beta closed on 23 October 2026. Its three scans stay as a sample of
30 items; the full Beta catalogue is deliberately not published.

## Credits

Item names and tooltips: Data from ForeverDB.net (https://foreverdb.net), reused
under the terms in its addon's NOTICE. The hero map is an original illustration
generated for this project. World of Warcraft belongs to Blizzard Entertainment.
