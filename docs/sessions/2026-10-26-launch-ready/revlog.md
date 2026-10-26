# Review log

## 1. Senior review of the data pipeline (26 October, 21:23)

**What it changed:** caught one real security hole I had missed (Markdown could inject an event handler through a code span inside a link address) and six real robustness gaps in imports and price ordering. All fixed; two of its findings I had already fixed in my own pass before it reported.

- **Why:** the parser, build and import are the foundation every launch scan goes through. A wrong price or a broken import after 4 November is expensive to find and undo.
- **Reviewer:** GPT-6 Astra (senior), effort high, on the ChatGPT plan through Codex (`codex exec`, read-only, web search off). Session `01a17974-4f0f-7f60-8209-58b9fe6d935d`.
- **Packet:** reviewer rules, three questions (wrong prices from realistic scan sequences; injection or private-data leaks; failed imports leaving a bad state), the decided requirements, and the full text of `auctionator.py`, `build.py`, `ingest.py`, `markup.py`, `pages.py` and `app.js`.
- **Steps:** 10 commands. It read `item_names.py`, the workflow and `check_site.py` (to judge failed refreshes, deployment and whether the site check would catch an injection), and ran three in-memory probes of `markup.inline` to confirm the injection. **Context it needed:** per-market scan timing and the source time zone. Not available in the data, and not a packet gap.
- **Usage:** 289,769 input tokens (235,648 cached), 8,147 output (5,359 reasoning). ChatGPT plan, so there's no per-token charge.

| # | Finding | Decision |
|---|---|---|
| 1 | Blocker: code span inside a link address breaks out of `href` | **Fixed.** Such links stay text; the site check now fails any page with an event-handler attribute; regression tests added. |
| 2 | Same-day files from two accounts overwrite each other | **Already fixed** before the report (lowest low, highest high, most listed). |
| 3 | A newer file can carry an older sighting and overwrite "latest" | **Fixed.** Latest comes from the scan that saw the item most recently. |
| 4 | Second market from an already imported file is lost | **Fixed** in ingest and build (dedupe per file and market). |
| 5 | Interrupted registry write can corrupt it | **Fixed** with whole-file writes. The suggested transaction log is more than this needs. |
| 6 | Rerun after interruption or failed push skips unfinished work | **Fixed.** A rerun finishes the commit or the push. Tested both. |
| 7 | Rollback leaves the local site built with the rejected scan | **Fixed.** The site is rebuilt after rollback. Publishing was never affected (CI builds fresh). |
| 8 | Scan dates in UTC vs Auctionator's local days | **Already fixed** (dates from day codes). Qatar has no daylight saving, so fixed-length days hold. |
| 9 | Non-ASCII realm names fail | **Fixed.** UTF-8 decoding, with a Cyrillic realm test. |
| 10 | TSV names could start spreadsheet formulas | **Fixed** for the name column (a `'` prefix). |
| 11 | Old sightings could appear as "Rising this week" | **Fixed.** Highlights need a sighting in the last three days. |
| 12 | Names could break tables in `llms-full.txt` | **Fixed.** Pipes, brackets and line breaks are neutralised. |

**Conclusion:** the reviewer found no route by which settings, posting history, searches or shopping lists could be published. After the fixes, all 29 tests pass, and the end-to-end import scenarios (three imports, a duplicate, a second market, an interrupted import, a failed push) behave correctly.
