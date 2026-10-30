# Review log: public repository, feed and inbox

## plan.md: senior review, GPT-6 Astra (30 October 2026)

**What it changed:** the architecture stands; seven corrections went into plan.md and research.md before Fares sees them.
1. Keyed submissions are public on arrival, held ones included; the plan now says so plainly, and the Site refuses content that contains the key itself.
2. The key is described as permission to publish, not protected by the checks (they enforce format, not truth). The Site gets rate and queue limits (30 accepted an hour, 20 waiting).
3. A push conflict no longer rebases: the inbox run resets to the new `main` and redoes everything, version checks included, so a stale page can't slip through and the tested tree is the one pushed. The Site rebuilds its commit on the new tip.
4. Archiving runs after the content commit (`archive.py` reads committed history).
5. Submissions are handled one by one with their own rollback. Results are pushed and the site published before a final step fails for held items, so a bad one never blocks good ones or skips the push.
6. ChatGPT gets `/feed/index.md`, not `/feed/`: the site is published without Jekyll, so a folder address needs an HTML page.
7. The hidden form needs a narrow `noindex` exception in `check_site.py` (line 76 rejects `noindex` on every page).

It also confirmed that pushes made with a personal token do trigger workflows, and that `paths-ignore` fits `pages.yml`. It noted that failure emails depend on Fares's notification settings (added to "What I need"), that the token is repository-wide authority and can reach the scripts workflows run (risk wording updated), and that branch protection can apply to administrators (research corrected: it isn't used because it works per branch, not per folder). It found no materially simpler architecture.

- **Why opened:** a plan for major, partly one-way work (making the repository public) with a new security boundary, which is a senior-tier case under REVIEWER.md.
- **Model, effort, billing:** `gpt-6-astra`, high effort, live web search, ChatGPT plan (Codex login). Session `01a18b91-77e8-7050-974a-9ed63282775c`, one exchange.
- **Steps:** 12 items: 8 commands reading `build.py`, `ingest.py` and `check_site.py` excerpts, 3 web searches and 1 page read (GitHub docs on triggers, notifications, Pages 404s, branch protection). "Context I needed but didn't have: none."
- **Accepted:** all seven findings and the four notes, each checked against the code (`check_site.py:76`, `archive.py:47–61`, `ingest.yml:34–50`) before applying.
- **Rejected:** none.
- **Packet note:** the extraction of the reviewer rules dropped their last line ("Context I needed but didn't have"); the reviewer answered it anyway. Next time, take the block by line range.
- **Usage:** 249,684 input tokens (194,432 cached), 3,560 output (1,069 reasoning), on the ChatGPT plan; no per-token charge.

## Fares's annotations after the review (30 October 2026)

- **The feed's `index.md` is a map, not content:** it sends ChatGPT to each file as needed. The plan now gives it a "how to use this" and one line per file (address, what it answers, version for pages), and holds no prices or page text.
- **The feed lives in the repository; the website stays the only place visitors go.** Chosen by Fares from two options. Guide pages are read straight from `content/`, prices become small committed markdown files in `feed/`, refreshed by `ingest.yml`, `inbox.yml` and a new `feed.yml`. The website publishes no markdown. Review finding 6 (the `/feed/` folder address on Pages) no longer applies.
- Not re-reviewed: the change moves generated files into git and adds one regenerate-and-commit workflow on the same pattern the review already checked (reset and redo on conflict, a shared concurrency group).

## Fares's second round (30 October 2026)

- **Lua from any addon** (AllTheThings and future ones): the inbox identifies the addon from file name and contents, always stores the file, and runs a processor only where one exists (Auctionator today).
- **"How can we enforce truth, not just format?"** Answered in the plan's new section: code can't verify the game, so it enforces provenance and change rules, uses personal keys for attribution, and routes judgement calls to Fares as one-tap pull requests. A free GitHub Models comment is noted as optional.
- **Commit email switched** to the GitHub private address in this repository's config; **a co-player's first name becomes "co-player"** in current docs, for inclusivity.
- **Receiver reconsidered:** the plan now compares a ChatGPT Site with a free Cloudflare Worker and recommends the Worker (deployable and testable from here). Calling the inbox as a tool from chats is phase 9, via an MCP tool on either host.
- Not re-reviewed yet: the truth-check layers and generic Lua add rules to `inbox.py` without changing the transaction the review checked. The receiver choice isn't a security change, since the code and token are the same on either host.

## Fares's third round (30 October 2026)

- **"For you and any co-player"** is the wording for who holds keys, replacing named people throughout.
- **Receiver: fewest services wins.** Fares questioned the Worker and asked about Vercel and Google Apps Script, noting that more third-party services make a simple system harder to track. The plan now recommends a second ChatGPT Site: Sites already runs the news relay, so it adds no service. A Worker, Apps Script or a move to Vercel would each add or swap one. The Worker stays as the fallback if Sites gets in the way. My earlier Worker recommendation weighted my ability to deploy and test above system simplicity; Fares's principle reverses that.

## Build notes (30 October 2026)

Fares approved the plan ("Approve, build"). Phases 1–8 were built, each checked and merged to `main` in turn. Where the build departed from the plan, and why:
- **The feed is written by every build** (`build.py` calls `scripts/feed.py`), not by a separate run. Anything that builds (the Mac import, the inbox, Codex) refreshes it in the same commit; `feed.yml` catches pushes that didn't build.
- **The map has two levels.** `feed/index.md` came out at 16 KB with every guide page in it, so the pages moved to `feed/guides.md` and crafting to `feed/craft/`. The start file is now about 1.5 KB.
- **Workflows keep separate concurrency groups,** not one shared group. GitHub cancels pending runs in a shared group, which could silently drop a feed refresh. Each workflow already handles push conflicts by starting again from the new `main`.
- **The "links must answer" check was dropped.** Large sites (Wowhead, Icy Veins) refuse automated requests, so it would hold good edits. A link to a site no page has cited before goes to review instead.
- **"No money amounts" became "a cost needs its source".** Pages rightly cite trainer and mount costs (e.g. riding at 100 gold, with Method named). A cost with a link or a named source passes; one without is held.
- **Non-Auctionator Lua gets a structural check, not a full parse.** The existing reader only accepts upper-case global names (AllTheThings uses mixed case) and walks the file in ways too slow for large ones. Files are stored, never run, so the check confirms the file looks like saved variables and that a known addon's tables match its name.
- **The repository setting "Allow GitHub Actions to create and approve pull requests" was switched on** (needed for review pull requests). It was listed in the approved plan.
- **Automated security review, four rounds, all applied:**
  - any unexpected error holds only that submission;
  - links are read with the renderer's own patterns, and protocol-relative links are refused;
  - repeated headings are refused, so one copy can't hide a change;
  - link addresses must be plain (no backslashes, `@` or unusual characters, which browsers and Python read as different hosts);
  - the Site refuses a key in any field, not only in the file.
- **End-to-end on GitHub:** a deliberately stale test page was held with its reason, pushed and failed the run as designed (run 41026422969). The publish workflow didn't start for the submission (`paths-ignore`). The test folder was then removed.

## End-of-build review: inbox code, GPT-6 Astra (30 October 2026)

**What it changed:** the security boundary held. The reviewer found no way to write to GitHub without a valid key, and no request-controlled write outside `inbox/<id>/`. It found nine weaknesses in validation, limits and recovery, all real when checked against the code. Eight are fixed; the remaining risk of the ninth is noted below.
1. **Links are read from the rendered page** (`markup.render`'s anchors), not by imitating its patterns. A second link in a table cell is now seen; a link inside code no longer counts as a citation.
2. **Headings are read as the renderer reads them** (`###<tab>Title` is a heading). Text under Field findings that isn't under a finding heading is held.
3. **The Site refuses a body without a declared size,** before reading it. Refusal logging is bounded: kept 30 days, at most 200 an hour.
4. **The hourly limit reserves a place before writing,** so a burst can't pass it together, and a failed write still uses its place. The queue check stays approximate; acceptable for a handful of trusted key holders.
5. **When the inbox starts again after a push conflict, review pull requests it opened are closed** (with a comment) before the redo decides afresh. Not covered by a test, since it needs `gh`.
6. **A submission that reached GitHub is always reported as received,** even if the Site's log write fails. *Remaining risk:* a lost reply to the final ref update could still report "not sent" for a submission that landed. A retry would then create a duplicate, which the inbox's version check holds.
7. **A push whose acknowledgement was lost** is detected (the commit is already on `main`), so outcomes, publishing and the held-run failure aren't skipped.
8. **The inbox refuses to run on a checkout with uncommitted changes,** so a local run can't reset away someone's work.
9. **JSON uploads allow for base64's overhead** up to the decoded 25 MB limit.

- **Why opened:** the end of a major phase, with a security boundary (a token on a public repository) and automatic publication; a senior-tier case.
- **Model, effort, billing:** `gpt-6-astra`, high effort, web search disabled, ChatGPT plan. Session `01a18beb-83e0-79c1-8bd7-c97bd2bfafe0`, one exchange.
- **Steps:** 14 items, reading targeted parts of `build.py`, `feed.py`, the renderer, the tests, the plan, `originals.py`, `ingest.py` and `check_site.py`; four in-memory probes confirmed findings 1–2. "Context I needed but didn't have: none."
- **Usage:** 345,571 input tokens (296,448 cached), 10,194 output (7,037 reasoning), on the ChatGPT plan.
- **Also this round:**
  - Semgrep flagged the SHA-1 used for page versions. Versions must be git's own blob IDs, so `feed.py` now asks git (`git hash-object`) instead of hashing in Python.
  - The packet took the reviewer rules by line range this time (the first packet's lesson); the block arrived whole.
