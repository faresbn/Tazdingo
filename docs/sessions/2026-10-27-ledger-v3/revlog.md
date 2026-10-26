# Review log: Ledger v3

## 1. Design direction (GPT-6.1 Sol, high effort, 26 Oct 23:20)

**What it changed:** the whole visual direction. The site moved from a navy, cream and gold palette (which sat close to the official WoW Forever combination) to a **quartermaster's field ledger kept at a roadside waystation**: a canvas work surface, ledger-paper sheets, spruce-ink links, an oxblood accent, gold kept for money, and Literata with Source Sans 3 instead of IM Fell and Alegreya. It also shaped the front-page dashboard layout, the spec page's reading column with an aside, the Classes mega-menu (all specs at once, no second hover level), the phone menu, and the image set with ready prompts.

- **Why:** Fares asked for "character and texture and flavour", in-game feel without infringing, and for Codex to be used for design ideas.
- **Route:** ChatGPT plan through Codex (`codex exec`, read-only, web search off), with four screenshots attached (front page desktop and phone, a class page, a market page).
- **Usage:** 23,348 input tokens, 8,991 output (3,269 reasoning). ChatGPT plan: no per-token charge.
- **Taken:** palette, type, materials, layouts, menu behaviour, image list and prompts (adjusted to look more like in-game screenshots, per Fares).
- **Adjusted:** the reviewer kept art "selective". Fares wants more in-game flavour, so the class emblems appear in the menus, the class picker and on page heads, and every section index has a banner.
- **Context it needed:** the profession list and a light-theme screenshot (headless dark mode didn't apply). Neither changed its advice.

## 2. Senior review of plan, update flow and code (GPT-6 Astra, high effort, 26 Oct 23:28)

**What it changed:** the update and archive design, page validation and the blue tracker's safety. It found one blocker and ten should-fix issues. All were accepted except one, where we chose a lighter version.

- **Why:** plan for major work plus the foundation later work builds on (senior tier per REVIEWER.md).
- **Route:** ChatGPT plan through Codex, read-only, web search off. Session `01a179ec-5244-7b02-a3fd-fd3b18be72ec`.
- **Packet:** reviewer rules, three questions (update and archive flow; build-time blue tracker; what to change before building), the owner's requirements, and plan.md, content-brief.md, UPDATING.md, pages.yml, build.py and check_site.py in full.
- **Steps:** read markup.py, pages.py, sections.py, ingest.py and app.js excerpts to check escaping, routes and concurrent writes; tried GitHub documentation online and failed (no network in the sandbox).
- **Usage:** 441,088 input tokens (377,984 cached), 7,644 output (3,517 reasoning). ChatGPT plan.

| # | Finding | Decision |
|---|---|---|
| 1 | Blocker: whole-file writes can silently overwrite newer work (ChatGPT editing from the lagging public text) | **Fixed in UPDATING.md:** read the exact file from GitHub `main`, keep its SHA, write back against it (GitHub rejects stale writes), and re-read and merge on conflict. Never edit from `llms-full.txt`. |
| 2 | The archive misses versions when runs are skipped or concurrent | **Fixed:** archive.py records everything since its own mark (`archive/.last-recorded`), is idempotent per commit, handles additions, deletions and renames, and retries the push with rebase. |
| 3 | Page structure and header fields are only instructed, not enforced | **Fixed:** allowed header fields only (no overriding title or address), the four sections once and in order, Markdown only in `content/`, `summary` required. Detecting large deletions of findings is left to the archive (recoverable) rather than blocking. |
| 4 | Editing Beta advice after launch would mark it Live | **Fixed:** Pre-launch by default; Live only via `status: live`; `verified:` date added; the plain-text export shows status for every page. |
| 5 | A commit subject naming someone would keep failing the build | **Fixed:** such log lines are replaced with "Page updated" on the public site; the original stays in git and the private archive. |
| 6 | Blue tracker fetching unbounded; failure cases unspecified | **Fixed:** 8 pages, 45-second budget, validated fields, any failure keeps the saved posts; the page shows when posts were checked and warns when they're over 12 hours old. Note: the 60-day schedule pause applies to public repositories. |
| 7 | The revision doesn't identify what was published | **Fixed:** the revision includes page metadata and the posts snapshot; the manifest records fetch time, snapshot hash and workflow run. |
| 8 | Excerpts are third-party text, not summaries | **Accepted in a lighter form:** excerpts stay short, plain text, quoted, attributed and linked only to Blizzard's forum; the front page shows titles only. |
| 9 | The site check would miss broken `#section` links after the spec-page move | **Fixed:** every promised page is checked, and every in-page link and search result must point to an existing section. Old `#spec` links on class pages still resolve. |
| 10 | Research fallbacks weaken evidence | **Accepted:** agents' source reports are kept in this folder (`sources/`), WoWSims presets are labelled as presets, and spot checks review the recommendations, not just the wording. |
| 11 | Screenshots would publish straight from a folder | **Fixed:** only screenshots listed in `data/game.json` publish; SVGs join the name check. |
| — | Scan import would be rejected after archive commits | **Fixed:** ingest.py pulls with rebase before pushing. |

**Conclusion:** keep the static design; the lost-update, archive, status and provenance contracts are now resolved in code and in UPDATING.md.

## 3. Peer code review of the finished build (GPT-6.1 Sol, high effort, 27 Oct 00:05)

**What it changed:** the menus now behave the same however they're opened, Blizzard's posts no longer vanish between site rebuilds, class pages have unique section links, and the archive copes with merges and simultaneous pushes. Eleven findings, all accepted and fixed.

- **Why:** peer review of the completed implementation before merging (REVIEWER.md: milestone).
- **Route:** ChatGPT plan through Codex, read-only, web search off. Session `01a17a05-be63-71f1-bcd0-a26b92833e89`.
- **Packet:** reviewer rules, the diff of `ledger-v3` against `main` (build, templates, scripts, workflows, site script), and three questions: correctness bugs; injection or private-data leaks; menu behaviour and accessibility for mouse, keyboard, touch and screen readers. Visual taste, copy, price maths and the parser were out of scope.
- **Usage:** 696,311 input tokens (610,048 cached), 12,526 output. ChatGPT plan.

| # | Finding | Fix |
|---|---|---|
| 1 | Moving the pointer from a menu tab to its panel crossed a gap and closed the panel | Leaving a menu closes it after 250 ms; re-entering (the panel included) cancels that |
| 2 | Posts fetched in one run were lost by the next, because CI publishes only `dist/` | The Pages job restores the previous snapshot from the Actions cache, merges it, and saves the new one (`blue_posts.py --merge`); a fetch failure still keeps both |
| 3 | The archive skipped merge commits and the first commit | `diff-tree -m --first-parent --root`, and `rev-list --first-parent` so a merged branch is recorded once (tested on a merge) |
| 4 | Class pages repeat the anchors of their embedded hybrid and macros notes | Those notes' sections and headings are prefixed `hybrid-` and `macros-`; the site check now fails duplicate ids |
| 5 | The embedded notes dropped their Read more sources | Rendered |
| 6 | Hover (CSS) and click (JS) kept separate state: wrong `aria-expanded`, two panels open, a clicked menu that hover kept open | One state in JS: hover opens and closes others; a keyboard user's open menu isn't closed by the pointer leaving |
| 7 | The archive job ran against the pushed commit, not current main, and pushed a stale record after a lost race | Checks out `main`, and on a rejected push resets to the new main and records again (up to three tries) |
| 8 | De-duplication merged different replies by the same author on the same day | Replies are kept by id; only opening posts cross-posted under the same title, author and day are merged |
| 9 | The phone menu ignored Escape and outside clicks | Both close it |
| 10 | Contents labels with links nested anchors | Labels are plain text |
| 11 | Checklist and issue labels on the front page were escaped twice | Decoded once after stripping tags, then escaped once |

**Conclusion:** no security issue in rendered content; the fixes are in commits `99b1fac` and `4e7fedd`.
