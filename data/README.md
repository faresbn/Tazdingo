# data/

What the site and the feed are built from.

| File or folder | What it holds | Where it comes from |
|---|---|---|
| `captures/` | Original addon files (`*.lua`, kept unchanged) and the Beta market extracts | Our own game clients |
| `captures.json` | A receipt and fingerprint for every capture | `scripts/ingest.py` |
| `market/` | Auction House scan records and the daily archive | `scripts/market_store.py`, from our Auctionator scans |
| `items.json` | Item names | ForeverDB's companion addon |
| `foreverdb.json` | Recipes, camp kits, crates, other players' and vendor prices | ForeverDB's addon data and site |
| `foreverdb-api.json` | Trainers, recipe vendors, gathering, abilities, disenchanting, vendor prices, item categories | ForeverDB's API |
| `game.json` | Classes, specs, professions, world topics, links, market names | Written here |
| `blue.json`, `news-config.json` | Blizzard's Forever posts and how they're classified | Blizzard's forums |
| `art.json` | Sourced artwork and its credits | See each entry |

## ForeverDB

**Data from ForeverDB.net (https://foreverdb.net).** `items.json`, `foreverdb.json` and `foreverdb-api.json` hold data from ForeverDB, used with this credit wherever it appears:
- **Its addon data** (item names, recipes, camp kits and crates) is published under GPL-3.0, with the credit required by section 7(b) of its notice.
- **Its site and API data** is used on our own site with credit. It isn't ours, isn't offered for resale, and isn't relicensed by this repository.

Questions about reusing it belong with ForeverDB.

## Blizzard

World of Warcraft® and Blizzard Entertainment® are trademarks or registered trademarks of Blizzard Entertainment, Inc. Game data and names are Blizzard's. This project isn't affiliated with or endorsed by Blizzard.
