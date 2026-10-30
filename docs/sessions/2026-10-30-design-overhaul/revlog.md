# Review log: design overhaul (30 October)

## 1. Plan review (senior)

**What it changed:** cheatsheet edits from the inbox now go to review; the tab script handles later hash changes, Back/Forward and arrow keys, and has a "Show all" control and print styles; both section names count as one section; the cheatsheet brief requires each line to keep its level, scenario, source and projection qualifiers; the deals rule keeps the 90%-under low-confidence override; the vendor rule was fixed as (Rare or better, or a recipe) and at least 100 copper.

- **Why:** the plan was major work that changes a settled decision (the four sections) and the Auction House measures.
- **Model and route:** `gpt-6-astra`, effort high, ChatGPT plan (Codex's saved login). Thread `01a18cdd-c98b-7ae2-8196-2845236f6a82`.
- **Steps:** 7 items. It opened `scripts/provenance.py` (recommendation review), `scripts/check_site.py`, the market confidence code, the templates and `content/classes/warrior/fury.md` to check qualifiers. "Context I needed": the implemented tabs and rewritten cheatsheets (not yet written at the time).
- **Raised:** (1) cheatsheet advice would bypass the recommendation review; (2) tabs need explicit anchor, history, keyboard and no-JS behaviour; (3) accepting both headings needs one section identity; (4) standard labels could strip qualifiers. On the Auction House: the arithmetic is a sound historical screen; keep "recorded", times and the availability warning; "exceptional" means the spread test, not a stronger recommendation; keep the 90% override; specify the vendor rule exactly.
- **Accepted:** all four, and the Auction House points. Rejected: nothing.
- **Usage:** 140,337 input tokens (111,104 cached), 1,903 output (386 reasoning). ChatGPT plan, no per-token charge.

A later automated security review of the commit found that the build reads section names in any case while the checks compared exact names, so a second "## CHEATSHEET" could sit beside the reviewed one. Fixed: headings must be spelt exactly, and the review rule compares every cheatsheet-like section.
