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

## 2. End-of-phase review (senior)

**What it changed:** old section anchors (`#glance`, `#guides`, `#more`, `#hybrid-…`, `#where-to-learn`, `#best-zones`, `#from-the-data`, `#vendor`, `#index`, and `#findings` where no findings tab exists) are kept as aliases that open the right tab; rare below-vendor items with a low-confidence deal no longer fall out of both tables; printed tab headings show; "Show all" mode keeps arrow-key order and the address; the cheatsheet grid is used only when the section is a single list (anything else shows whole); the investment list folds; empty-state wording names the threshold; two Holy Paladin cheatsheet lines regained their qualifiers ("projected"; "if talented").

- **Why:** the final review of a major phase before it reaches Fares.
- **Model and route:** `gpt-6-astra`, effort high, ChatGPT plan. Thread `01a18cf1-fcc3-76b3-bd52-562108a051d2`.
- **Steps:** 8 items: section-id generation, the prices.json fields, menu CSS and handlers, and a content search for mixed cheatsheets (none found). "Context I needed": a rendered browser session for keyboard and screen-reader checks (done here instead with Playwright: deep links, hash changes, Back, arrow keys, show-all).
- **Raised:** seven should-fix and two minor findings, listed above. It confirmed the deal, exceptional, vendor-quality and minimum-profit rules match the agreement, and found no fidelity issue in the Enchanting sample.
- **Accepted:** all nine. Rejected: nothing.
- **Usage:** 360,972 input tokens (296,960 cached), 3,521 output (1,571 reasoning). ChatGPT plan, no per-token charge.
