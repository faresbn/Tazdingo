# Initial public reading contract (schema 1)

1. Fetch `/data/manifest.json` and select the exact environment and market key.
2. For an item ID, select the market's `partitions` entry whose inclusive
   `first_item_id`–`last_item_id` range contains it. Fetch that entry's `json`.
3. Require its `revision` to match the manifest and match the exact `item_key`.
   Variants belonging to one item are kept in the same partition.
4. `unit_price_copper` is an integer. The record's `source` points to its full
   fingerprint, capture timestamp and received date in `capture_sources`.
5. `quote_observed_at: null` means unknown, not equal to the capture timestamp.
6. Fetch `history_json` only for capture-to-capture comparisons. Its records
   are cached snapshot rows, not sale events or independent fresh observations.
7. Use `latest_json`, `latest_tsv` or immutable source snapshots when a larger
   calculation requires complete relevant records and original daily fields.

Human browsing uses the same partitions. Six HTML pages provide navigation,
context, the first price rows and direct download links without JavaScript;
optional JavaScript supplies targeted search, pagination, capture selection, sorting and inline history. ForeverDB provides reference item tooltips without a copied item database.

This contract is a first implementation and awaits anonymous reading tests in
ChatGPT before it is used to write final shared-project instructions.

For a specific historical capture, select its `snapshots` entry and matching
`partitions` range, requiring that snapshot's `revision`. Current and historical
partitions are separate; never label an upload date as the quote observation.
