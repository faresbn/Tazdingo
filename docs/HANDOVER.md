# Handover

The running record of where Tazdingo stands, kept current at every checkpoint so another thread, model or machine can carry on. Read this first, then AGENTS.md and README.md.

**Last updated:** 27 October 2026, Tazdingo rebrand and news refresh (session folder `docs/sessions/2026-10-27-tazdingo/`).

## Where things stand

- **Live site:** https://faresbn.github.io/Tazdingo/ (published from `main` by `.github/workflows/pages.yml`, about a minute after each push, and every two hours to refresh Blizzard's posts).
- **Current work:** `feature/tazdingo-news`: Tazdingo branding/repo rename and full-text news classifier with visitor refresh. Local tests pass; renamed Pages deployment and browser refresh verification pending.
- **Launch:** WoW Forever opens on 4 November 2026; level cap 60 (the Beta's was 30).

## What v3 is

- **Front page:** a dashboard with the countdown, the "Before you log in" checklist (from `content/more/launch.md`), the market pulse (steadiness meter, most listed, best crafts), Blizzard's latest posts, the class picker, the latest ledger changes, professions and world.
- **Menus:** hover mega-menus (Prices, Classes with every spec, Professions, World, More) that also open by click, tap and keyboard; a nested menu on phones.
- **Pages:** one per spec (27), class hub (9), profession (12), world topic (7), More list (launch, Blizzard posts, addons, macros, known issues). Each has At a glance · What the guides say · Field findings · Read more, plus a "Guides and tools" box with checked links (Wowhead, Icy Veins, ForeverDB, WoWSims).
- **Prices:** typical price, latest, steadiness, history; What to craft, Waylaid Crates, Materials worth gathering.
- **Design:** a quartermaster's field ledger (see docs/DECISIONS.md). Painted art generated through Codex: a hero pair (day and night), five section banners, nine class emblems, twelve profession emblems, paper and canvas textures, and the social card. Originals are in the session folder's `art/`.
- **Records:** the archive Action keeps a backup of every changed page and a log in `archive/LOG.md`.

## v3 status (done, 27 Oct)

- [x] Infrastructure, templates, design, all art, blue tracker, archive, `ledger:` links
- [x] All 77 pages written by research agents, checked by the build, spot-checked, committed. Each agent's sources, doubts and source contradictions are in the session's `sources/`.
- [x] Three outside consultations: design (GPT-6.1 Sol), senior review (GPT-6 Astra), peer code review (GPT-6.1 Sol). Every finding fixed; see the session's `revlog.md`.
- [x] Browser review: menus (hover, click, keyboard, Escape) at desktop; the phone menu; light and dark; no horizontal overflow on any of the 72 pages at phone width.
- [x] Merged into `main` and live.

## Cosmetic refinement (27 Oct)

- Dropdown widths vary by content; panels scroll within the desktop viewport. Mobile menus remain nested.
- Class/spec/profession icons use Blizzard's public icon renderer (48 unique URLs checked). Text labels remain present and the footer credits Blizzard. This is an intentional small-icon exception to the generated-art direction, requested by Fares; large scenes are still generated illustrations, not screenshots.
- Teal links/accent, blue-toned dark surfaces and reduced paper/canvas texture. No content structure, market data or guide advice changed.
- Home crafting heading says "Listing margins", to distinguish listing arithmetic from realised profit. Beta content is temporary and will be replaced at launch; do not treat its current prominence as a permanent hierarchy problem.
- All 34 local tests pass (one original-capture test skipped), build/check covers 72 pages, browser script syntax and PR validation pass. Deployment 40461966416 succeeded. Live desktop checks: More menu is 336px wide, opens on pointer click, and no broken game icons or horizontal overflow were observed. Full screenshot replacement awaits the user's own captures under the existing policy.

## Known gaps and small follow-ups

- Pages run long in places ("What the guides say" is 850–1,000 words on most spec pages, 1,900 on dungeons and raids). Trim when a page is next edited.
- The countdown counts calendar days to 4 November in the visitor's time zone, but servers open at 23:00 UTC (02:00 on 5 November in the Gulf), so east of UTC it says "opens today" on the 4th and "Day 2" at the moment servers open. A fix would count to the launch moment; not done, as it wasn't in the plan.
- **iCloud duplicates:** the repo sits in `~/Documents`, which iCloud Drive syncs. On 27 Oct it created byte-identical "… 2.md" / "… 2.webp" copies of about 240 recently written files (none inside `.git`). The build rejects an unknown page like `content/professions/alchemy 2.md`, so a scan import would stop. If `git status` shows "… 2" files, compare each with its original (`cmp`) and delete the identical ones. Moving the repo out of iCloud (or turning off Desktop & Documents sync) would end it; that's Fares's call.
- Screenshots: none yet. Take them after launch (see "After launch").

## Open decisions for Fares

1. **Can ChatGPT commit from the shared project?** OpenAI documents its GitHub connector as read-only. Test it with docs/chatgpt/UPDATING.md. If it can't, the fallbacks are a custom MCP connector in the Business workspace (docs/sessions/2026-10-26-forever-redesign/plan.md, section 3) or pasting ChatGPT's file into GitHub's web editor.
2. **Name:** Tazdingo was selected on 27 Oct. Custom domain remains undecided.
3. **The art:** generated for v3 and live with it. Swap any image by replacing its file in `site/assets/` (see "Making art").
4. **Search engines:** the site isn't submitted to Bing or Google yet. That's outward-facing, so it waits for Fares.
5. **ForeverDB API key:** requested by Fares; it would add disenchanting and Beta-versus-live changes.

## After launch (4 November)

1. Scan the Auction House, log out, run `python3 scripts/ingest.py --push` (first time: `--market "Realm Faction"`).
2. Run `python3 scripts/foreverdb_data.py` and `python3 scripts/item_names.py`, then commit: the data's Pre-launch labels clear.
3. Pages stay Pre-launch until someone checks their advice in game and sets `status: live` (UPDATING.md explains).
4. Take screenshots without the interface (Alt+Z), convert to WebP, put them in `site/assets/screens/` and list them in `data/game.json`.

## How to work on it

- **Machine setup:** Python 3.11+, `git`, `gh` (logged in as faresbn), Node (to syntax-check the script), `cwebp` (Homebrew `webp`), Google Chrome (headless screenshots), Codex CLI logged in with the ChatGPT plan. Nothing to install for the site itself.
- **Checks before any push:** `python3 -m unittest discover -s tests && python3 scripts/build.py && python3 scripts/check_site.py && node --check site/assets/app.js`
- **Preview:** serve `dist/` under `/Tazdingo/`: `mkdir -p tmp/serve && ln -sfn ../../dist tmp/serve/Tazdingo && python3 -m http.server 8765 --directory tmp/serve`, then open http://localhost:8765/Tazdingo/.
- **Original scans:** the three Beta `.lua` files are not in git. They were in `~/Downloads/FOREVER_BETA_AH_PROJECT_FILES_2026-10-17/`; copy them into `data/captures/forever-beta/` to run the comparison test (it skips without them).
- **Phone checks:** headless Chrome can't go narrower than about 500px, so check phones in a real browser's device emulation.

## Making art (the recipe that works)

1. Write a brief: one subject per numbered item; in-game scene or item-icon style; "Horde races and landmarks are welcome; no copied logos, key art, frames or text"; transparent background for emblems.
2. Run it on the ChatGPT plan: `env -u CODEX_API_KEY codex exec --skip-git-repo-check -C <folder> -m gpt-6.1-sol -c model_reasoning_effort=low --disable memories -s read-only - < prompt.md`. Tell it to make **one separate image call per item** and to leave files where the tool saves them. Asking it to save files, or giving several items without that rule, produces contact sheets or nothing.
3. Images land in `~/.codex/generated_images/<thread id>/` in generation order. Check them on a contact sheet, then convert with `cwebp` (emblems `-resize 192 192 -q 82 -alpha_q 90`; scenes `-q 72`) into `site/assets/`.
4. Every image must look like it's from inside the game. Reject abstract or obviously off-world results.

## Session history

- **26 Oct:** repo connected to GitHub; parser fixed for current Auctionator files; site rebuilt (v1 → v2 "Tazdingo"); prices with typical price and steadiness; gold-making tables; ChatGPT instructions. Sessions: `2026-10-26-launch-ready`, `2026-10-26-forever-redesign`.
- **27 Oct (overnight):** v3 per Fares's brief ("Rebuild, push to main, and leave a running record of everything"): dashboard front page, mega-menus, a page per spec, profession, world topic and More list (77), painted art, Blizzard's posts, the archive and the Ledger guide flow. Three outside consultations: see the session's revlog.md.

## News relay and classifier

The Pages website remains on GitHub. `scripts/blue_posts.py` reads Blizzard directly during Actions runs and invokes `scripts/classify_news.mjs`, which imports the same classifier used by `relay/worker/index.js`. The relay serves visitor refreshes; its server deployment is a separate small public endpoint. Source is mirrored under `relay/`, while the deployed service is managed separately (deployment instructions in `relay/README.md`).

The initial live trial read ten complete posts/articles, retained seven distinct entries, tagged WoW Weekly as mixed, and quarantined a short podcast post. Failed reads keep prior verified records, and do not advance the successful timestamp. Each decision stores its reason and an article fingerprint. Ambiguous cases are rule-based classifications, not AI judgements.

The automated command-line client encountered the relay host's browser-signature block. Do not route the scheduled collector through that host; GitHub Actions fetches Blizzard directly. Browser-to-relay integration still needs live verification before calling manual refresh complete.

Local validation: 37 Python tests (one expected original-file skip), ten Node tests, 72 generated pages, and browser script syntax. Claude CLI is unavailable here; no independent outside-model review was claimed. Historical session documents and `ledger:` internal link aliases are preserved intentionally.
