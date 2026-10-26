# Implementation status

Verified 26 October 2026.

## Working

- Private source repository: `faresbn/FvrRepo`.
- Public Pages site: https://faresbn.github.io/FvrRepo/.
- GitHub Actions validation, build and deployment succeeded in run 40367231848.
- Anonymous HTML and JSON reads return the deployed revision and source commit.
- Six HTML pages; 24 selected PvP item keys across three captures, plus six legacy-market keys. No complete beta catalogue or individual item pages.
- Inline history for item 236 matches the three original exports: 6700, 900 and 5000 copper.
- Browser checks confirm external ForeverDB names/icons and inline history. Keyboard/hover tooltip rendering is not yet independently verified.
- All 15 local ingestion tests passed. Actions skips the original-file comparison because original Lua files are deliberately absent; the remaining checks pass.
- PR validation and main-branch deployment are separated. Published output excludes original Lua, scripts and private notes.

## Still to prove

- ChatGPT's web reader cannot currently retrieve the new Pages URLs, although anonymous HTTP and browser reads work. No site-served bot block has been observed. The shared project's retrieval route remains unresolved.
- Scan updates from the ordinary shared-project chat mode, and Mike's independent retrieval.
- Invalid-update blocking, previous-site preservation and recovery in an actual GitHub deployment failure.
- Character save schema and an explicit-save/write/read-back example.

## Data limits

Per-item quote observation times are unavailable. Daily source codes remain unconverted; their calendar definition has not been independently verified. Field interpretation follows the supplied project workflow; the matching maintainer field implementation has not been inspected. Cached prices do not prove current stock, sales or demand. No release prices or character states have been invented.

## Original-file boundary

Automatic approval review rejected full SavedVariables uploads to this repository. No original Lua was uploaded through another route. The published sample contains only selected market records and source fingerprints; configuration, posting history, searches and other addon state are excluded. Original-to-sample equality was checked locally. Actions validates sample fingerprints and schema, and records that narrower validation scope.
