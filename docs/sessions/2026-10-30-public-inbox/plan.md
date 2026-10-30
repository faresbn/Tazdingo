# Plan: a public repository, a ChatGPT feed and an inbox

30 October 2026. Built on `research.md` (same folder), which has the reasons and sources. Fares asked for research and this plan without a stop in between; **implementation waits for his approval of this plan.**

## What changes for you

- **ChatGPT reads markdown from the repository; visitors get the website.** `faresbn.github.io/Tazdingo/` stays the visual site and serves no markdown. ChatGPT starts at `feed/index.md` in the public repository (`https://raw.githubusercontent.com/faresbn/Tazdingo/main/feed/index.md`). That file is a map, not content: it says which file answers which kind of question, so ChatGPT opens only the one or two files a request needs. Prices are small markdown files in `feed/`; guide pages are read straight from `content/`, so nothing is copied.
- **ChatGPT (or any of you) updates the site without GitHub.** A hidden form at `https://faresbn.github.io/Tazdingo/inbox/` takes a finished guide page or any addon's saved-variables `.lua` (Auctionator, AllTheThings, whatever you add later), plus your personal key from `TAZDINGO_INBOX.md`. A good submission is live within minutes. A keyed submission that fails a check is held, and GitHub emails you why. A submission with the wrong key is refused and logged, and never touches the repository.
- **The repository is public, Lua files included.** Every scan's original file is kept in its history. GitHub Actions becomes free.
- **Unchanged:** Codex commits to `main`; `ingest.py --push` on the Mac; the site's look and pages; the archive of every page change; Pages hosting. No Vercel, no Copilot, no LLM on GitHub's side.

## How the inbox works

```
ChatGPT (agent mode) or a person
        │  fills in the hidden form on the website: key, kind, page + version, text or any addon's Lua file
        ▼
Inbox Site (a second ChatGPT Site, separate from the news relay)
        │  wrong key → refused, logged in the Site's own database (private): the "failed folder"
        │  over the rate or queue limit, or the key pasted into the content → refused, logged
        │  right key → key removed, submission committed to inbox/<id>/ on main (public from here on)
        ▼
GitHub Action "inbox.yml" (free, deterministic, no LLM)
        │  each submission in turn: known page? version current? format, provenance and change rules? Lua readable, which addon?
        │  fails → moved to inbox/held/<id>/ with the reason
        │  needs your eye (see "Checking truth") → opened as a pull request you approve with one tap
        │  passes → page replaced in content/ (and archived), or Lua stored and processed if a processor exists; tested, built, checked
        │  results pushed and the site published; then, if anything was held, the run fails so GitHub emails Fares
        ▼
Published site, about two minutes later; feed/ in the repository updated in the same commit
```

Why it's built this way, briefly (research.md sections 3–5):
- **GitHub Pages can't receive a form,** so the form posts to a small ChatGPT Site, the same service the news relay already runs on (why, below).
- **The Site holds the GitHub token and pushes to GitHub.** GitHub can't collect from a Sites host, which blocked automated clients on 27 October.
- **The key never enters the public repository.**
- **Two consequences of a public repository, stated plainly:**
  - **A keyed submission is public the moment it arrives,** held ones included. Moving it to `held/` doesn't unpublish it, and it stays in history.
  - **The key is permission to publish guide content automatically.** The checks enforce format, not truth: a well-formed page from a key holder goes live without review. Hand a key only to a co-player you trust on that understanding.

## Decisions this records (reconsiderations, decided by Fares on 30 October)

These change settled lines in AGENTS.md and DECISIONS.md. Each one gets the date and the reason when it's written in.
1. **The repository becomes public** (was: private, only `dist/` published).
2. **Original Lua files are committed** (was: never commit SavedVariables). They're game data. The website still never serves a `.lua`; they live in the repository.
3. **ChatGPT writes through the inbox** (was: ChatGPT commits directly). Codex still commits to `main`; Fares can override either on request.
4. **A route for people without GitHub exists** (was: parked).
5. **The inbox Site holds a GitHub token limited to this repository.** The news relay keeps its rule of never holding GitHub credentials; the Site is separate from it so that rule stands.
6. **ChatGPT reads the repository, visitors read the website** (new). ChatGPT's markdown lives in the repository's `feed/` and `content/`, mapped by `feed/index.md`. The website stays the only destination for visitors and carries no markdown.

## Settled on 30 October

- **A. Commit email:** history stays as it is; this repository's commits now use the GitHub private address (`195290664+faresbn@users.noreply.github.com`, set in the repository's own git config on 30 October). The inbox's commits use it too. Old commits keep `faresb@fact.qa`.
- **B. "Mike" becomes "co-player"** in the current docs (AGENTS.md, DECISIONS.md, the session documents), for inclusivity rather than anonymity: the role can be anyone. The site's no-names guard in `build.py` and `check_site.py` keeps the specific names it blocks, because that's what makes it work.

## Which receiver: a ChatGPT Site (no new service)

**Recommendation: a second ChatGPT Site, next to the news relay.** Your rule decides it: every extra service is one more account, bill, dashboard and failure to keep track of. The system today is GitHub (repository, Actions, Pages) plus one ChatGPT Site (the news relay), on the Business plan you already pay for. A Site for the inbox adds nothing to that list.

| Option | New service to keep track of? | What it costs | Verdict |
|---|---|---|---|
| **ChatGPT Site** | No: Sites already runs the news relay | Codex deploys it (I write and test the code here and hand Codex a brief). Public beta | **Use this** |
| Cloudflare Worker | Yes, a new account | Free; I could deploy it myself | Only worth it if Sites gets in the way |
| Google Apps Script | Yes, Google | Free, but awkward: plain HTML forms can't send files to it without extra code, and POST replies come back as redirects | No |
| Move the site to Vercel | Swaps GitHub Pages for Vercel, while GitHub stays for the repository and Actions, and the relay stays on Sites | A full re-host, a new address (`*.vercel.app`) unless you buy a domain, and it reopens "stay on GitHub Pages". The free Hobby plan would cover it, so no payment | No: the most work for the same result |

**What choosing the Site gives up,** and how the plan handles it:
- **Codex deploys every change.** The Site's code is a single small file with its own tests. I run them here, and Codex deploys from a ready-to-paste brief, as the relay is deployed today.
- **I can't test it from the command line,** because the host blocked automated clients. The end-to-end check goes through the built-in browser instead, which is a real browser, the same way a person or agent mode reaches it.

It stays a separate Site from the relay, so the relay keeps its rule of never holding GitHub credentials. Both sit in the same Sites account; that's still one service.

**"Can it be called from inside a shared project?"** Not as a plain web address. ChatGPT reaches a web form through agent mode, which is route B, and that works from any chat, project or not. To be *called as a tool*, the Site also has to offer an MCP tool, published to your Business workspace as a plugin, which Sites supports. That's phase 9, after the form works, because the form remains the fallback. Whether a workspace plugin can be used inside a shared project is one to test in the app.

## Checking truth, not just format

**Code can't know whether a claim about the game is true.** Only play, a source or a person can. What the inbox can do is make every claim traceable, catch the mistakes that machines can catch, and send the changes that matter to you. Five layers, cheapest first; I recommend the first four:

1. **Provenance rules, enforced** (UPDATING.md's rules turned into checks).
   - Every new or changed Field finding needs a confidence, a date and how it's known: tested (level and situation), read (with a link) or simulated (tool and version).
   - Every source claim in "What the guides say" needs a link.
   - No money amounts in guide pages, because prices come only from scans.
2. **Change rules, checked against the previous version.**
   - Findings can't be deleted, only marked `outdated` with a reason.
   - A submission changes one page.
   - Item and spell links must point to IDs that exist in our ForeverDB data.
   - Cited links must answer, and come from a list of known sources (Wowhead, Icy Veins, ForeverDB, Blizzard and the rest UPDATING.md names), so an unknown site goes to review rather than straight onto the page.
3. **A personal key for you and any co-player,** each with a neutral label such as `key-2`. Every submission is attributable inside the repository without a name on the site, and one key can be revoked without touching the others.
4. **Your one-tap review for the changes that matter.** These become a pull request instead of being applied, and you approve or close it from the GitHub app. The inbox runs every check before opening it (GitHub doesn't re-run checks on a pull request an Action opened); merging publishes as usual:
   - setting a page `live`;
   - changing a "Tazdingo recommendation";
   - marking findings outdated;
   - links to unknown sites.
   
   Additive changes (a new finding, a new source) apply straight away.
5. **Optional, later: a free LLM second opinion.** GitHub Models is free inside Actions with the built-in token (`models: read`), with tight daily limits and a small input ceiling, and it's still a preview ([setup](https://agentpatterns.ai/tools/copilot/github-models-in-actions/); [limits, vendor-reported](https://fast.io/resources/github-models-rate-limit/)). It could comment on a pull request ("this contradicts the existing finding from 6 November"). It can't verify the game, and it shouldn't decide anything. Not in this plan unless you want it.

## Steps

Each phase is one branch checkpoint with the full check run (`unittest`, `build.py`, `check_site.py`, both `node` checks), merged to `main` when it passes. Phases 1, 2 and 3 can ship before the inbox exists. Rough times are for my work, not waiting on you.

### Phase 1: the feed, in the repository (about 1.5 hours)

- **New `scripts/feed.py`** writes the repository's `feed/` folder from the data already in it:
  - **`feed/index.md`: the map, and only the map.** No prices, no page text. It has:
    - a short "how to use this" (open only what the question needs; prices are asking prices with a scan time; Pre-launch means unverified);
    - one line per file: its address, what it answers and when to open it. For example: "`feed/prices/<market>/herbs.md`: herb prices on <market>, last scan <time>". For each guide page: "`content/classes/mage/frost.md`: Frost Mage, updated <date>, Pre-launch, version <id>";
    - the inbox's address and where its instructions are.
    
    The versions are what a page edit quotes back. Guide pages are listed, not copied: ChatGPT reads them from `content/`.
  - **`feed/prices/<market>/index.md`: a map of that market.** Its last scan time, and the category files with what each holds.
  - **`feed/prices/<market>/<category>.md`:** one small table per item category (latest recorded price, typical, usual, steadiness, days listed, units, weekly change, scan time).
  - **`feed/prices/<market>/alerts.md`:** unusually low, investment watch and movers, with the scan time each was recorded at, worded as `market.py`'s rules require ("recorded", estimates called estimates).
  - **`feed/craft.md`:** the gold-making table.
  - **The ForeverDB credit goes wherever its data appears.**
- **Who refreshes it:** the feed is generated, never edited by hand, and committed together with what changed it.
  - `ingest.yml` and the new `inbox.yml` run `feed.py` before their own commit. Workflow commits don't trigger other workflows, so they have to.
  - A small new `feed.yml` runs on any other push to `main` that touches `content/`, `data/` or `scripts/feed.py`: the Mac's `ingest.py --push` or Codex. It regenerates the feed and commits only if something changed, in the same concurrency group as `ingest.yml` and `inbox.yml` so the three never race. On a push conflict it resets to the new `main` and regenerates; generated output is always safe to redo.
- **The website is unchanged:** `build.py` keeps refusing to publish any `.md` or `.lua`. `llms-full.txt` and the `.tsv`/`.json` price files stay as they are (nothing removed); ChatGPT's instructions point to the map first.
- **Tests:** a new `tests/test_feed.py` checks:
  - the map lists every market, category file and `content/` page;
  - every address in the map exists;
  - the versions match `git hash-object`;
  - the map holds no prices or page text;
  - no names (the site's no-names rule applied to `feed/`);
  - `feed/` matches a fresh run of `feed.py`.

### Phase 2: Lua files in the repository (about 30 minutes)

- **`.gitignore`:** remove the `data/captures/**/*.lua` block.
- **Originals live at `data/captures/forever/<addon>/<time UTC>.lua`** (e.g. `auctionator/2026-11-05T1830.lua`, `allthethings/…`). One Auctionator file can hold several markets, so it's named by time, not market.
- **`ingest.py` (Mac):** copy the original into that path as part of the import commit; same undo-on-failure.
- **Commit the three Beta originals,** so the comparison test in `tests/test_ingestion.py` runs in CI instead of skipping.
- **AGENTS.md data rules:** the rule becomes "commit originals, never edit them by hand"; fingerprints are kept as for extracts.
- **Handover gets a size line** (`git count-objects -vH`). A retention decision is due before the repository reaches 500 MB. The committed price files add to that alongside the Lua files; small per-category files keep each scan's change compact.

### Phase 3: prepare and flip to public (about 45 minutes, then your go)

- **"Mike" becomes "co-player"** in AGENTS.md, DECISIONS.md and the session documents (B above). The commit email is already switched (A).
- **`data/README.md`:** credits ForeverDB.net, says the data is used with credit and not ours to relicense, and which files hold it.
- **`README.md`:** an opening paragraph for public readers (what this is, unofficial, not affiliated with Blizzard); the rest stays.
- **Re-runs the secret scan on the final history.**
- **Flip:** `gh repo edit faresbn/Tazdingo --visibility public --accept-visibility-change-consequences`. Then I check the site still publishes and Actions run. **This step is outward-facing and effectively one-way** (anyone can copy a public repo the moment it's public), so I do it only after you approve this plan.

### Phase 4: the inbox on GitHub's side (about 3 hours)

- **Submission layout,** written by the Site: `inbox/<id>/submission.json` plus one of `page.md` or the submitted `.lua` under its own file name. The JSON has:
  - `id`, `received` (UTC) and `key_label` (which personal key, never the key)
  - `kind` (`page` or `lua`)
  - for a page: `path` (e.g. `content/classes/mage/frost.md`) and `version` (from the map in `feed/index.md`)
  - `message` (the one-line public commit message, UPDATING.md's rules)
  - for Auctionator: optional `market`
- **New `scripts/inbox.py`** owns the whole transaction. It works through every waiting submission, oldest first, each with its own rollback, so a bad one never blocks the good ones behind it:
  - **Page:** the path must be a known page (`build.py`'s list); the version must match the current file, otherwise held as "the page changed since you read it, read it again". GitHub's raw file addresses can be cached for a few minutes, so a read just after a change can be stale; this check turns that into a hold, never an overwrite; the file must pass `load_content`'s header and section rules; the message must pass the no-names rule.
  - **Lua, any addon:**
    - The addon is identified from the file name (saved-variables files are named after their addon, e.g. `AllTheThings.lua`) and confirmed by the file's top-level tables (`AUCTIONATOR_…` and so on). A name that doesn't match its contents is held.
    - The file must parse as saved variables; one that doesn't is held.
    - Then it's always stored under `data/captures/forever/<addon>/`.
    - **If a processor exists** for that addon (`scripts/addons/<addon>.py`), it runs. Auctionator's is the current import code, filed through the same `ingest()` the Mac uses (market: `market` or the remembered default).
    - **If not,** the file is stored, not held: the map lists it as "stored, not processed yet", and the run summary says so. Writing a processor for a new addon (AllTheThings first, if you want it) is a later piece of work, chosen per addon. Processors keep character names out of the feed and the site, as the screenshot rule already does.
  - **Apply, in order:** write the file; regenerate `feed/`; run the full test, build and check (if any fails, undo and hold with the failing step's message); commit the content change; then run `scripts/archive.py --before <base> --after <that commit>` and commit its record. `archive.py` reads committed history, so it has to run after the content commit. Workflow commits don't start `archive.yml`, so this is the only archiving the change gets.
  - **Held:** moved to `inbox/held/<id>/` with `reason.txt`, and committed.
  - **Push:** if `main` moved meanwhile (Codex, the Mac, another submission), it never rebases on top. It resets to the new `main` and redoes the whole run from there, version checks included. That way a stale page can't slip through, and the combined result is always the one that was tested. Three attempts, then the run fails and the submissions stay waiting.
  - **Report:** writes each submission's id, outcome and reason to the run's summary page.
- **New `.github/workflows/inbox.yml`:** permissions `contents: write`, `pull-requests: write`, `actions: write`; triggered by a push to `main` under `inbox/` (not `inbox/held/`), with a concurrency group shared with `ingest.yml` and `feed.yml`. Steps: run `inbox.py` (which pushes), start `pages.yml` if anything was applied, and only then a final step that fails if anything was held. That failure is what makes GitHub email you.
- **`pages.yml`:** `paths-ignore: inbox/**`, so arriving submissions don't trigger a publish.
- **`ingest.yml` and the scan-record route stay working but undocumented for ChatGPT.** Retiring them is a later tidy-up.
- **Tests:** a new `tests/test_inbox.py` covers good page, stale version, unknown path, bad header, name in message, each provenance and change rule, a review-worthy change becoming a pull request, good Auctionator Lua, an unknown addon's Lua (stored, not held), a file name that doesn't match its contents, unreadable Lua, held move, a bad submission followed by a good one (both handled), and `main` moving mid-run with an edit to the same page (redone, then held as stale).

### Phase 5: the inbox Site (about 1 hour here, plus a Codex deploy)

- **Code in this repository at `inbox-site/worker/index.js`, tests in `inbox-site/inbox.test.mjs` (not under `inbox/`, which holds submissions and triggers the inbox workflow),** the same layout as `relay/`. No dependencies. Its tests run here with `node --test`, like the relay's.
- **`POST /submit`** accepts a plain HTML form (multipart) and the same fields as JSON, for a GPT or agent later:
  - **Checks only what must be checked before anything is public:**
    - the key, matched against the personal keys in the `INBOX_KEYS` secret (constant-time), which gives the key's label
    - a 25 MB size limit (saved-variables files from collection addons can be large; GitHub's limit is 100 MB per file)
    - `kind` is `page` or `lua`, and a `.lua` file name looks like an addon's
    - the key doesn't appear anywhere in the content
    - limits of 30 accepted submissions an hour and 20 waiting in `inbox/`
    
    Every other rule lives in one place, `inbox.py`, so a keyed but malformed submission still reaches `held/`, where you see it.
  - **Refused** (wrong key or a limit): a row in the Site's database (time, size, kind, reason, no content) and a plain "Refused" reply.
  - **Right key:** removes the key and commits `inbox/<id>/…` in one commit through GitHub's API (`GITHUB_TOKEN` secret). The commit is built on the latest `main`; if `main` moves before it lands, the commit is rebuilt on the new tip, so nothing pushed in between is lost. Then it replies with the id and where to watch.
- **The reply is a plain page,** readable by a person or an agent: "Received. If it passes its checks it's live at <address> in about two minutes."
- **The news relay is untouched.**
- **Deploy:** Codex deploys it as a new Site named `tazdingo-inbox` (two secrets, a database binding), from a ready-to-paste brief I write in this folder.

### Phase 6: the hidden form (about 30 minutes)

- **`inbox/index.html`, built by `build.py` in the site's design:** `noindex` meta tag, not in the menu, sitemap or search.
- **Fields:** key, kind (page or Lua), page path, version, message, a large text box for the page and a file picker for any addon's `.lua`. A plain HTML form posting to the Site, so it works with no JavaScript.
- **`check_site.py`:** whitelist the Site's address next to the relay's, and allow `noindex` on `inbox/index.html` only. Today the check fails any page carrying `noindex` (line 76), and it keeps doing that for every other page.

### Phase 7: ChatGPT's instructions (about 45 minutes)

- **New `docs/chatgpt/TAZDINGO_INBOX.md`,** the project file:
  - the form's address and every field;
  - start at the map (`feed/index.md`), open only the files the request needs, and take a page's version from the map;
  - "submit the whole file";
  - message rules;
  - what each reply means;
  - "if you can't submit, give the user the finished file and the form's address".
  
  **The committed copy holds `<KEY>` as a placeholder.** You paste the real key into the copy you upload to ChatGPT, because the repository is public.
- **`PROJECT_INSTRUCTIONS.md` and `UPDATING.md`:** read through the map in the repository (the website is for people); write through the inbox; any addon's saved-variables file is submitted as the `.lua` itself (no sandbox scripts any more); the provenance rules from "Checking truth" are spelled out so ChatGPT writes pages that pass them first time. Everything else in UPDATING.md (page format, findings, sources, no names) stays.

### Phase 8: records and an end-to-end check (about 30 minutes)

- **Docs:** AGENTS.md (settled decisions, data rules, everyday tasks), DECISIONS.md (the six decisions above, plus the Site and the truth-check layers), README.md, HANDOVER.md.
- **Review log:** the Codex review of this plan, in `revlog.md`.
- **End-to-end check** after the Site is deployed: a page edit through the form, a stale-version edit (held, email arrives), a wrong key (refused, logged), a Beta Lua (filed). I can drive the form in the built-in browser for the person route.

### Phase 9: call the inbox as a tool from chats (after the form works; about 1 hour)

- The Site also offers one MCP tool, `submit_to_tazdingo`, with the same fields and the same checks as the form.
- You publish it to the Business workspace as a plugin, and test whether it can be called from inside the shared project.
- If it can, TAZDINGO_INBOX.md says to call the tool first, then agent mode on the form, then hand the file to the person.

## What I need from you, and when

| When | What | Time for you |
|---|---|---|
| Now | Approve or annotate this plan; confirm the ChatGPT Site and truth-check layers 1–4 | — |
| Before phase 4 | Check GitHub → Settings → Notifications → Actions is set to email you, at least for failed runs. That email is how held submissions reach you | 1 minute |
| Before phase 4 | Allow the inbox workflow to open review pull requests: repository Settings → Actions → General → Workflow permissions → "Allow GitHub Actions to create and approve pull requests". A repository setting, so it's yours to switch on (or I do it with your go) | 1 minute |
| Before phase 5 deploys | Create the GitHub token: Settings → Developer settings → Fine-grained tokens → only `faresbn/Tazdingo`, Contents read and write only, one-year expiry. Paste it straight into the Site's secret prompt (the Site's settings, during Codex's deploy), never into chat or a file. I'll generate the personal keys into `tmp/` (ignored by git) | 3 minutes |
| Phase 5 | Run the Codex brief to deploy `tazdingo-inbox` | 10 minutes |
| Phase 7 | Paste the new project instructions; upload `TAZDINGO_INBOX.md`; each person puts their own key in their copy, or keeps it in their ChatGPT memory or instructions | 5 minutes |
| After | Test from the ChatGPT app: start at the map and read a price and a page from the repository; edit a page via agent mode; submit a Lua via agent mode; the person route | 15 minutes |

## Risks and how they're handled

- **The token is full write access to this repository's contents.** It isn't limited to the inbox. Whoever got hold of it could change the scripts that workflows then run, and history can't undo what compromised code has already done. Mitigations:
  - the Site's code is small, has no dependencies and writes only under `inbox/`;
  - the token covers one repository and expires after a year;
  - it lives only in the Site's secrets;
  - revoking it disables the inbox in seconds.
- **The key leaks** (it sits in a ChatGPT project file). Whoever has it can publish well-formed but wrong pages or unwanted links: the checks enforce format, not truth. The rate and queue limits bound the volume. With personal keys only the leaked one is revoked, in `INBOX_KEYS` and in that person's copy, then put any affected page back from `archive/`. Check once that rotation takes effect (research.md section 3 notes a beta bug report).
- **Keyed submissions are public on arrival,** held ones included. Accepted, because only you and the co-players you give keys to can submit. The Site refuses content containing the key itself, so a pasted key can't be published by accident.
- **Repository growth from Lua files and the committed price files.** Collection addons can write large files that change at every login. Watched in the handover; retention decided before 500 MB, possibly per addon (e.g. keep only the latest few files of a non-price addon).
- **ChatGPT can't do part of this in practice** (opening raw GitHub addresses, agent-mode file upload). The person route always works for writing. For reading, the GitHub connector can open the same public files. Feed files are split by category and the map holds no content, so each read stays small.
- **Going public is effectively one-way.** Everything is checked before the flip; nothing secret is in the history.

## Not in this plan

- No change to the site's design, pages or Auction House logic. Retiring `ingest.yml`'s scan-record route comes later.
- Not done in this plan: a GPT with an action, email from the Site, a Cloudflare Worker, Google Apps Script, Vercel, a custom domain, search-engine submission. Removing `llms-full.txt` isn't in it either.

## Order and checkpoints

The phases run in order 1 → 2 → 3 → 4 → 6 → 5 → 7 → 8, then 9, each merged to `main` on passing checks. The form (6) lands before the Site (5) is deployed, but points at the Site's address. Until the Site exists, it shows "inbox not open yet". Estimated total of my time: about 9 hours (phase 4 grows to about 3 hours with the truth checks and generic Lua; phase 9 adds 1), plus Codex's deploy and your four short steps.
