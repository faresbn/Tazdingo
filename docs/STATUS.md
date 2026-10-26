# Status

Updated 26 October 2026.

## Working

- **Site:** https://faresbn.github.io/FvrRepo/ is built and published by GitHub Actions on every push to `main`.
- **Scans:** `scripts/ingest.py` imported all three original Beta files end to end as if they were launch scans (4,238 items, about a second each), refused a duplicate, and undid itself cleanly when a check failed.
- **Parser:** reads every current Auctionator market on this Mac (Anniversary and Classic Era, up to 32,000 items), including random-suffix gear. Old markets that use Auctionator's earlier formats are refused with a reason and don't block the rest of the file.
- **Prices:** typical price (median of daily lows over the last seven days of records), latest price, last-seen date, units listed and weekly change, checked against real Beta data with troll listings and one-day spikes.
- **Names:** 4,234 of 4,238 Beta items named from ForeverDB's addon data.
- **Beta sample:** 30 items from three scans; the extracts match the original files record for record (the test runs whenever the originals are in `data/captures/forever-beta/`, which git ignores).

## Still to prove

- **ChatGPT finding the site through search.** The site is now open to search engines, but it isn't indexed yet. Until it is, upload `llms-full.txt` and `prices.tsv` to the ChatGPT project, or paste a link in a chat. Telling Bing about the site (IndexNow) is outward-facing, so it waits for Fares's go-ahead.
- **The first real Forever scan** after launch on 4 November: the `_forever_` folder has no Auctionator data yet.
- **The first journal entry**, written in ChatGPT and saved here.
