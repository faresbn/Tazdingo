# Handover

The running record of where Tazdingo stands, kept current at every checkpoint so another thread, model or machine can carry on. Read this first, then AGENTS.md and README.md.

**Last updated:** 27 October 2026, focused UX refinement (session folder `docs/sessions/2026-10-27-ux/`).

## Where things stand

- **Current work:** Focused UX pass complete and live, merged in PR #5 as `8fa0535b437c6254ac60ae1d4a5fedd1f2ce2354`; publish run 40480651338 succeeded. Homepage changelog removed; full-width class picker, keyboard search, reset/shareable price filters, mobile guide disclosure, active More marker and refresh feedback shipped. Live desktop interaction checks passed; phone layout is implemented and code-reviewed, but no phone-browser visual verification is claimed.

- **Live site:** https://faresbn.github.io/Tazdingo/ (published from `main` by `.github/workflows/pages.yml`, about a minute after each push, and every two hours to refresh Blizzard's posts).
- **Previous work:** Authentic Warcraft imagery merged in PR #4 and published successfully (run 40477656697). The live homepage and class cards were visually checked; all nine class images load and preserve transparency. Live checks in both colour themes verified the final class portrait bounds, all world icons and source credits. The camp scene uses a small complete sidebar image to avoid cropping characters. Pages remains on GitHub. The separate news relay is unchanged. Cleanup of the older merged `fix/visitor-news-cache` branch remains blocked pending explicit user permission.
- **Launch:** WoW Forever opens on 4 November 2026; level cap 60 (the Beta's was 30).

## What v3 is

- **Front page:** a dashboard with the countdown, the "Before you log in" checklist (from `content/more/launch.md`), the market pulse (steadiness meter, most listed, best crafts), Blizzard's latest posts, the full-width class picker, professions and world. Repository changes are not shown on the homepage; individual guide histories remain.
- **Menus:** hover mega-menus (Prices, Classes with every spec, Professions, World, More) that also open by click, tap and keyboard; a nested menu on phones.
- **Pages:** one per spec (27), class hub (9), profession (12), world topic (7), More list (launch, Blizzard posts, addons, macros, known issues). Each has At a glance · What the guides say · Field findings · Read more, plus a "Guides and tools" box with checked links (Wowhead, Icy Veins, ForeverDB, WoWSims).
- **Prices:** typical price, latest, steadiness, history; What to craft, Waylaid Crates, Materials worth gathering.
- **Design:** teal/blue field guide, authentic Forever Darkspear/Orgrimmar/camp scenery, Classic fan-site-kit character cut-outs, Blizzard game icons and small objects. Generated scenes, class/profession emblems and social-card artwork have been removed from active assets. The paper/canvas textures and original Tazdingo mark remain.
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
- All 34 local tests pass (one original-capture test skipped), build/check covers 72 pages, browser script syntax and PR validation pass. Deployment 40461966416 succeeded. Live desktop checks: More menu is 336px wide, opens on pointer click, and no broken game icons or horizontal overflow were observed. This earlier own-captures-only policy was superseded by Fares's explicit authorisation to use sourced authentic imagery on 27 October.

## Known gaps and small follow-ups

- Pages run long in places ("What the guides say" is 850–1,000 words on most spec pages, 1,900 on dungeons and raids). Trim when a page is next edited.
- The countdown counts calendar days to 4 November in the visitor's time zone, but servers open at 23:00 UTC (02:00 on 5 November in the Gulf), so east of UTC it says "opens today" on the 4th and "Day 2" at the moment servers open. A fix would count to the launch moment; not done, as it wasn't in the plan.
- **iCloud duplicates:** the repo sits in `~/Documents`, which iCloud Drive syncs. On 27 Oct it created byte-identical "… 2.md" / "… 2.webp" copies of about 240 recently written files (none inside `.git`). The build rejects an unknown page like `content/professions/alchemy 2.md`, so a scan import would stop. If `git status` shows "… 2" files, compare each with its original (`cmp`) and delete the identical ones. Moving the repo out of iCloud (or turning off Desktop & Documents sync) would end it; that's Fares's call.
- Screenshots: none yet. Take them after launch (see "After launch").

## Open decisions for Fares

1. **Can ChatGPT commit from the shared project?** OpenAI documents its GitHub connector as read-only. Test it with docs/chatgpt/UPDATING.md. If it can't, the fallbacks are a custom MCP connector in the Business workspace (docs/sessions/2026-10-26-forever-redesign/plan.md, section 3) or pasting ChatGPT's file into GitHub's web editor.
2. **Name:** Tazdingo was selected on 27 Oct. Custom domain remains undecided.
3. **The art:** authentic sourced imagery is now the default. Register files and attribution in `data/art.json`; keep receipts in the session folder.
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

## Artwork workflow

Prefer authentic official/publicly reusable Warcraft imagery, as Fares authorised. Larger assets live in `site/assets/art/` and publish only when listed in `data/art.json`; the build checks their fingerprints. Record the source URL, original filename, edition, credit, terms, delivery treatment and dimensions. The public Sources and credits page reads this registry. Original transparent character renders come from Blizzard's Classic fan-site kit; identify them as Classic artwork, never Forever equipment or gameplay evidence. Official Forever scenes retain their compositions, resized/encoded for delivery; CSS handles framing. The source kit's licence and required notices are kept in `docs/sessions/2026-10-27-authentic-art/`. Icons continue to use Blizzard's public renderer. Personal screenshots still require the separate `data/game.json` allowlist and privacy check.

## Session history

- **26 Oct:** repo connected to GitHub; parser fixed for current Auctionator files; site rebuilt (v1 → v2 "Tazdingo"); prices with typical price and steadiness; gold-making tables; ChatGPT instructions. Sessions: `2026-10-26-launch-ready`, `2026-10-26-forever-redesign`.
- **27 Oct (overnight):** v3 per Fares's brief ("Rebuild, push to main, and leave a running record of everything"): dashboard front page, mega-menus, a page per spec, profession, world topic and More list (77), painted art, Blizzard's posts, the archive and the Ledger guide flow. Three outside consultations: see the session's revlog.md.

## News relay and classifier

The Pages website remains on GitHub. `scripts/blue_posts.py` reads Blizzard directly during Actions runs and invokes `scripts/classify_news.mjs`, which imports the same classifier used by `relay/worker/index.js`. The relay serves visitor refreshes; its server deployment is a separate small public endpoint. Source is mirrored under `relay/`, while the deployed service is managed separately (deployment instructions in `relay/README.md`).

The initial live trial read ten complete posts/articles, retained seven distinct entries, tagged WoW Weekly as mixed, and quarantined a short podcast post. Failed reads keep prior verified records, and do not advance the successful timestamp. Each decision stores its reason and an article fingerprint. Ambiguous cases are rule-based classifications, not AI judgements.

The automated command-line client encountered the relay host's browser-signature block. Do not route the scheduled collector through that host; GitHub Actions fetches Blizzard directly. Browser-to-relay integration was verified on the live Pages site: Refresh news returned a verified snapshot and an explicit shared-cache status. The host forbids its default cache, so the relay now uses a named cache with isolate fallback and seeds cold instances from the published verified snapshot.

Local validation: 38 Python tests (one expected original-file skip), ten Node tests, 72 generated pages, and browser script syntax. Claude CLI is unavailable here; no independent outside-model review was claimed. Historical session documents and `ledger:` internal link aliases are preserved intentionally.

Final live verification: Pages is https://faresbn.github.io/Tazdingo/ and repo is https://github.com/faresbn/Tazdingo (private). PR #2 deployed in run 40469268994; cache-fix PR #3 deployed in run 40470166261. The browser showed a successful 08:01 UTC check newer than the published static snapshot, proving a refresh beyond the prior cache window. Mixed roundup tag verified on the full news page, absent on home. Repo description and homepage link are updated; the workspace remote points to the renamed repo.

The rebrand branch was removed. Automatic approval review twice rejected deleting the fully merged `fix/visitor-news-cache` branch, requiring explicit user authorisation despite its recoverability and AGENTS.md's cleanup instruction. The branch remains; no alternate deletion route was used.

## Authentic artwork rollout (27 Oct)

PR #4 replaces 29 generated active assets with twelve credited delivery images (402,170 bytes total). Three Forever scenes: Darkspear Islands, Orgrimmar and Horde camping. Nine Classic character cut-outs favour Trolls/Horde; a Human paladin keeps Alliance represented. Boar, crocolisk, crate, coin, sword, potion and fishing-pole icons add smaller in-world details. The social preview uses Darkspear. Every page carries the fan-site-kit notice; individual sources/editions appear under Sources and credits. `data/art.json` is an explicit publication allowlist with fingerprints; personal captures retain their separate privacy allowlist. Local build/check covers 72 pages, 38 Python tests (one expected skip), ten Node tests and script syntax. Live review found no horizontal overflow on the desktop class hub; no phone-browser verification is claimed in this environment.
