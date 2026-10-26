# Implementation status

## Implemented locally

- Private source/public generated-output boundary.
- Data-only Lua reader and bounded CBOR decoder; no Lua execution.
- Original-file fingerprints and complete counts from all three beta exports.
- Separate PvP and ClassicBetaPvP markets, cached-payload deduplication.
- Dated snapshots, full downloads and small current/history partitions.
- Six static HTML pages and optional search, date selection, sorting and inline history.
- Validation/build/deploy workflow; PRs validate without publishing.

## Still to verify

- Authenticated repository transfer and the actual GitHub Actions deployment.
- Anonymous ChatGPT web retrieval of HTML and structured records.
- Ordinary shared-project Chat upload route and Mike's independent reading.
- Invalid-update blocking, previous-site preservation and recovery on GitHub.

## Deliberately incomplete

- Item names/tooltips use the documented ForeverDB embed; no item database is mirrored.
- Actual browser behaviour of the external tooltip still needs verification.
- Per-item quote observation timestamps are unavailable in `m`.
- Calendar conversion of raw daily codes awaits the matching addon definition.
- Field interpretation follows the supplied project workflow; the matching
  maintainer field implementation has not yet been inspected.
- Character save schema and write/read-back flow follow after AH retrieval.
- Final shared-project instructions have not been written or installed.
- No release market or character state has been invented from beta data.

The website is an initial historical test publication, not a completed market
or character recommendation system. Deployment claims require public readback.

## Upload review boundary

Automatic approval review rejected full SavedVariables uploads to `faresbn/FvrRepo`. No original Lua has been uploaded through another route. Market-only JSON excludes configuration, posting history, searches and other personal addon state. Original-to-extraction equality is checked locally; Actions checks the extraction and records that narrower scope. Raw archival awaits explicit authorisation.

## Current prototype scope

Only 24 selected PvP items across three dated scans and six legacy-market items are included. Complete beta catalogue migration is intentionally deferred. Original-to-sample values and original row counts were checked locally.
