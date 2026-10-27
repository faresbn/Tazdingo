# Review log: site plan

## research.md review loop (27 October 2026)

Fares asked for repeated review passes until two consecutive passes needed no edits.

| Pass | Method | Result |
|---|---|---|
| 1 | Every claim checked against the repo, the built site, the live site and GitHub | 13 corrections (scheduled-run count, homepage-only title, overview word counts, five not six "disagree" wordings, link-list overlap, ForeverDB footer credit already linked…) and 6 gaps filled (homepage-only search, no item pages, no analytics, no redirects, the ripple effects of template changes, real Actions numbers) |
| 2 | The claims pass 1 added | 3 clarity fixes |
| 3 | Full read | 4 precision fixes (77 sections across 59 pages; "most-used entry point" unsupported; Enterprise plan; "headings" → fixed text) |
| 4 | Independent fact-check by a fresh agent with no access to my reasoning; each finding re-verified before applying | 14 findings applied: the "four sections per page" decision flagged as a reconsideration; market movers need two weeks of scans; market facts and display names; ForeverDB scripts need no key; Onyxia is in the API; per-zone skinning calls; world data-block headings; analytics precedent (ForeverDB's tooltip script); quests and PvP in the API; questions expanded to cover every decision raised. Its point that ChatGPT's commits are unproven was answered by Fares's confirmation earlier the same day; the document now says so |
| 5 | Full read | 2 fixes (PvP coverage; settled decision named in the summary) |
| 6 | Every cited link and file path resolved | 1 consistency fix (content files vs published pages) |
| 7 | Full read | 3 fixes (no source for "server status"; steadiness vs movers timing; word counts were single pages, now medians and ranges across each type) |
| 8 | Full read | 2 timestamps on figures that change over time |
| 9 | Full read | 1 arithmetic fix (ten scheduled runs were due, not eleven) |
| 10 | Full read | Clean |
| 11 | Every number re-derived by script and compared with the text | Clean |

## Fares's corrections and the second review loop (27 October 2026)

Fares corrected three points: three or four scans a day are planned in the first days after launch; "ClassicBetaPvP" is a Beta name and its six items an incomplete set; PvP gets a dedicated section per class and spec, with no general PvP section yet. He asked for the review loop again, passing research.md to GPT-6.1 Sol at high effort at least once and at most three times.

Before writing, I checked how scans become price data: a day's scans merge into one daily record (`build_markets`), and each import keeps its own snapshot (`ingest.py`), so extra scans don't speed up the weekly movers rule by themselves.

### Consultation: GPT-6.1 Sol, high effort, three exchanges in one session

**What it changed:** the early-price-movement section was rebuilt and corrected (movers from about day 10, not two weeks; per-item sparklines already work; scans are kept only if each one is imported; the day-to-day bias explained, then corrected in direction), the Actions billing claim became an open question with GitHub's conflicting docs quoted, the Pre-launch badge idea now respects the per-page Live decision, the relay example is flagged as a reconsideration, the API call estimates separate bulk tables from per-item detail, and a question on the API rollout scope was added (16 questions now).

- **Why opened:** Fares asked for it. The new price-movement analysis also rests on code behaviour a second reader could check.
- **Route:** Codex CLI 0.164.0 on Fares's ChatGPT plan (`env -u CODEX_API_KEY`, "Logged in using ChatGPT"); no fallback. Session `01a17e69-b352-79b3-b16d-a827a47a2adb`; read-only sandbox; web search at the default.
- **Packet:** the reviewer rules, three questions (accuracy, faithfulness to Fares's directions and settled decisions, whether each question has what it depends on), Fares's directions quoted, DECISIONS.md, `build.py` (price merging and movers), `pages.yml`, `archive.yml`, the menu code, and the ForeverDB API notes. **Packet gap (mine, foreseeable):** research.md itself arrived empty because of a line-count bug in my packet script, so the reviewer opened it. Fixed in the follow-ups.
- **Exchange 1** (325 s, 12 steps): opened research.md; searched GitHub's Pages limits and billing docs (two web searches, one page fetch); read `ingest.py` 65–135, `auctionator.py` 270–391, `tests/test_ingestion.py` 185–240, `build.py` 42–72, `pages.py` 105–125, grepped `app.js`, `sections.py`, `UPDATING.md` and `relay/README.md`, and read two API samples. Raised 13 findings (no blockers; 10 should-fix, 3 minor). I verified each against the repo or GitHub's docs (both billing pages fetched; the sparkline threshold and the ingest snapshot logic read) and accepted all 13. "Context I needed": the account's actual billed Actions usage.
- **Exchange 2** (45 s, no file reads): checked the full revised file. Confirmed 12 fixes; found that my fix for the day-to-day bias had the direction backwards (an unfinished day's minimum tends to sit higher, so it exaggerates rises). Accepted and corrected.
- **Exchange 3** (15 s): confirmed the corrected passage and question 5. No findings.
- **Usage** (Codex `turn.completed`, cumulative for the session): 571,491 input tokens, of which 501,760 cached; 10,873 output tokens, of which 7,802 reasoning. By exchange: 388,887 / 9,397; then +90,577 / +1,200; then +92,027 / +276. ChatGPT plan, so no per-token charge.
- **Conclusion:** the reviewer's verdict moved from "useful, but its early-price framing, billing certainty and several decision premises need correction" to "both revised passages are accurate".

### Passes after the consultation

| Pass | Method | Result |
|---|---|---|
| Sol 3 | Confirmation of the bias fix | Clean |
| Own 1 | Market and PvP bullets, cross-references, numbers | 1 fix (a duplicated "isn't known yet" sentence in the market bullet); the count restarted |
| Own 2 | Full read | Clean |
| Own 3 | Re-derived today's figures by script: the build's own `summarise` on synthetic daily records (movers eligible from day 10, steadiness from day 3), quest paging (67), bulk API calls (~56), the two Beta markets | Clean |

## The Auction House build (27 October 2026, evening)

Fares asked for the Auction House module to be researched, planned, built and published autonomously, checking in with Sol as needed. A research agent surveyed other AH tools (`sources/ah-tools.md`); its ideas (confidence tiers, short supply, good-buy price, market index, the published 3.5 robust z-score) went into research section 6 and the plan.

### Consultation: GPT-6.1 Sol, high effort, plan and phases A–C

**What it changed:** three blockers and thirteen should-fix/minor findings, all but one accepted. The storage layer now verifies the whole store before any change, writes the archive and registry before deleting folded records, rejects uploads for already-folded days, and rolls back on any error during an import (verified end to end with a deliberately broken build). Uploads only count as sightings when an item is new to that day or changed, which removes carried-forward prices from references, freshness, movers and patterns. The investment watch excludes volatile, too-new and thinly listed items (the settled gold-making rule). Presence, short supply, partial-day detection, pattern readiness and aggregation, and chart day boundaries were corrected; public wording now says "seen at" with times.

- **Why opened:** the plan for major work and the data-safety of the launch-day import path (a mistake there is expensive to undo).
- **Route:** Codex CLI on Fares's ChatGPT plan; session `01a17eb0-e2c6-7af2-a706-1d499f47e992`; read-only.
- **Packet:** reviewer rules, three questions (storage/ingest safety, analytics correctness and honesty, settled decisions), plan.md, research section 6, DECISIONS.md, `market_store.py`, `market.py`, `ingest.py` (import path), `build.py` (market assembly), `scan_record.py`. 89 KB.
- **Exchange 1** (11 steps): read the parser's timestamp and day handling, ingest/build boundaries, tests, the name refresh, public templates, browser time handling, site checks and workflows. 17 findings. Accepted 16; finding 15 (inbox workflow missing) was a timing artefact: `ingest.yml` was written minutes after the packet was sent. "Context I needed": none.
- **Usage (exchange 1):** 501,877 input tokens (438,016 cached), 9,089 output (5,733 reasoning). ChatGPT plan.
