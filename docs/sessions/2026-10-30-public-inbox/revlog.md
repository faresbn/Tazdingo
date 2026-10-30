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
- **Commit email switched** to the GitHub private address in this repository's config; **"Mike" becomes "co-player"** in current docs, for inclusivity.
- **Receiver reconsidered:** the plan now compares a ChatGPT Site with a free Cloudflare Worker and recommends the Worker (deployable and testable from here). Calling the inbox as a tool from chats is phase 9, via an MCP tool on either host.
- Not re-reviewed yet: the truth-check layers and generic Lua add rules to `inbox.py` without changing the transaction the review checked. The receiver choice isn't a security change, since the code and token are the same on either host.

## Fares's third round (30 October 2026)

- **"For you and any co-player"** is the wording for who holds keys, replacing named people throughout.
- **Receiver: fewest services wins.** Fares questioned the Worker and asked about Vercel and Google Apps Script, noting that more third-party services make a simple system harder to track. The plan now recommends a second ChatGPT Site: Sites already runs the news relay, so it adds no service. A Worker, Apps Script or a move to Vercel would each add or swap one. The Worker stays as the fallback if Sites gets in the way. My earlier Worker recommendation weighted my ability to deploy and test above system simplicity; Fares's principle reverses that.
