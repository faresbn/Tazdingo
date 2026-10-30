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
