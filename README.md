# FvrRepo — WoW Forever Repo

Private source repository for a small public Warcraft reference site.

The first publication uses market-only extracts of historical Forever Beta Auctionator captures. Original Lua files remain outside GitHub pending explicit upload approval.
Beta is a test dataset, not an ongoing supported game or release market.

## Build

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py --base-path /FvrRepo/
python3 scripts/check_site.py
```

Only `dist/` is published by GitHub Actions. Raw Lua, scripts and private notes
are excluded. No package installation or application server is required.

## New scan

Parse the supplied Lua locally with `scripts/auctionator.py`. Preserve the original privately. Commit only its market-only extraction and a receipt containing the original SHA-256, extraction SHA-256, environment, received date and selected market keys. Actions validates extraction fingerprints and schema; it does not claim to re-read unavailable Lua originals. Unknown formats stop publication; the prior
deployment remains available. Chat-to-repository transfer has been tested only
in the environments explicitly recorded in `docs/STATUS.md`.

## Character history

Write only on explicit user request. The assistant can suggest saving a useful
state that is missing from the repo. Do not infer that a comparison is finished
or save every discussion. No real character records have been supplied yet.

## Reading

`/data/manifest.json` lists market pages, complete current downloads, immutable
source snapshot URLs and small current/history partitions. Every record links
to its source hash and capture date. Daily source codes and unknown per-item quote
times remain explicit; do not treat retained quotes as fresh scans.

The site has six HTML pages. A targeted price query reads the manifest and the
one matching `partitions` entry's `json` file. Records point to a source in
`capture_sources`; history is downloaded separately only when requested.

Design reference: the official WoW Forever site, viewed 26 October 2026.
The decorative landscape is original SVG. No Blizzard artwork/logo is copied.
