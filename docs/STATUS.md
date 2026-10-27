# Tazdingo update — 27 October 2026

Site/repo renamed; GitHub Pages retained. Full-text news classification, tagged inner-page roundups, Forever-only homepage and visitor refresh are live and browser-verified. Scheduled direct-Blizzard collection remains independent of the public relay. Final checks: 38 Python tests (one expected skip), ten Node tests, 72 generated pages. See HANDOVER.md and the 2026-10-27-tazdingo session for deployment evidence and limits.

# Status

Updated 26 October 2026, after the Tazdingo rebuild.

## Working

- **Site:** https://faresbn.github.io/Tazdingo/, published by GitHub Actions on every push to `main`, only after tests, build and checks pass.
- **Structure:** front page (countdown, site-wide search, Latest log, five doors), Prices (markets, What to craft, Waylaid Crates, Materials), Classes (9 classes, 27 specs, hybrid builds, macros), Professions (12), World (7 topics), More (addons, macros, known issues, sources).
- **Prices:** typical price, latest, steadiness, last seen, units listed and weekly change. The Beta reference sample holds 975 items, checked record for record against the original files.
- **Gold-making:** 382 priced recipes, the cheapest bundle for each of 30 Waylaid Crates, and materials by value. Built from ForeverDB data priced with our scans and ForeverDB players' prices.
- **Scans:** `scripts/ingest.py` imports, checks, commits and publishes, and undoes itself on failure (tested end to end on the original Beta files).
- **Notes:** `content/` files at known places; the build rejects anything else. Pre-launch labels are automatic.
- **Themes:** light and dark follow the device, with a toggle.

## Still to prove

- **ChatGPT writing to the repository** from the shared project. OpenAI documents the GitHub connector as read-only. If direct commits don't work, the fallback is a custom connector in the Business workspace (see `docs/sessions/2026-10-26-forever-redesign/plan.md`, section 3).
- **ChatGPT finding the site through search:** not indexed yet. Until it is, upload `llms-full.txt` and `prices.tsv` to the project.
- **The first live scan** after launch on 4 November, and a ForeverDB data refresh after launch to replace pre-launch data.
- **ForeverDB API key:** requested by Fares; would add disenchanting and Beta-versus-live changes.
