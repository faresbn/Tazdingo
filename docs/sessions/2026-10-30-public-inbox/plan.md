# Plan: a public repository, a ChatGPT feed and an inbox

30 October 2026. Built on `research.md` (same folder), which has the reasons and sources. Fares asked for research and this plan without a stop in between; **implementation waits for his approval of this plan.**

## What changes for you

- **ChatGPT reads one plain folder.** `https://faresbn.github.io/Tazdingo/feed/index.md` lists every market's prices and every guide page as markdown files. It isn't linked anywhere on the site. The address names `index.md` itself: this site is published without Jekyll, so a folder address only works when there's an HTML page in it.
- **ChatGPT (or any of you) updates the site without GitHub.** A hidden form at `https://faresbn.github.io/Tazdingo/inbox/` takes a finished guide page or an `Auctionator.lua`, plus the key from `TAZDINGO_INBOX.md`. A good submission is live within minutes. A keyed submission that fails a check is held, and GitHub emails you why. A submission with the wrong key is refused and logged, and never touches the repository.
- **The repository is public, Lua files included.** Every scan's original file is kept in its history. GitHub Actions becomes free.
- **Unchanged:** Codex commits to `main`; `ingest.py --push` on the Mac; the site's look and pages; the archive of every page change; Pages hosting. No Vercel, no Copilot, no LLM on GitHub's side.

## How the inbox works

```
ChatGPT (agent mode) or a person
        │  fills in the hidden form on the website: key, kind, page + version, text or Lua file
        ▼
Inbox Site (a new ChatGPT Site, separate from the news relay)
        │  wrong key → refused, logged in the Site's own database (private): the "failed folder"
        │  over the rate or queue limit, or the key pasted into the content → refused, logged
        │  right key → key removed, submission committed to inbox/<id>/ on main (public from here on)
        ▼
GitHub Action "inbox.yml" (free, deterministic, no LLM)
        │  each submission in turn: known page? version current? header, sections, links, no names? Lua readable?
        │  fails → moved to inbox/held/<id>/ with the reason
        │  passes → page replaced in content/ (and archived) or scan filed; tested, built, checked
        │  results pushed and the site published; then, if anything was held, the run fails so GitHub emails Fares
        ▼
Published site + feed, about two minutes later
```

Why it's built this way, briefly (research.md sections 3–5):
- **GitHub Pages can't receive a form,** so the form posts to a small ChatGPT Site, the same hosting the news relay already uses on the Business plan.
- **The Site holds the GitHub token,** because GitHub can't fetch from the Sites host: it blocked automated clients on 27 October.
- **The key never enters the public repository.**
- **Two consequences of a public repository, stated plainly:**
  - **A keyed submission is public the moment it arrives,** held ones included. Moving it to `held/` doesn't unpublish it, and it stays in history.
  - **The key is permission to publish guide content automatically.** The checks enforce format, not truth: a well-formed page from a key holder goes live without review. That's fine for the three of you. Hand the key out only on that understanding.

## Decisions this records (reconsiderations, decided by Fares on 30 October)

These change settled lines in AGENTS.md and DECISIONS.md. Each one gets the date and the reason when it's written in.
1. **The repository becomes public** (was: private, only `dist/` published).
2. **Original Lua files are committed** (was: never commit SavedVariables). They're game data. The website still never serves a `.lua`; they live in the repository.
3. **ChatGPT writes through the inbox** (was: ChatGPT commits directly). Codex still commits to `main`; Fares can override either on request.
4. **A route for people without GitHub exists** (was: parked).
5. **The inbox Site holds a GitHub token limited to this repository.** The news relay keeps its rule of never holding GitHub credentials; the inbox is a separate Site so that rule stands.

## Two calls I need from you before the flip

**A. Your work email on every commit.** 77 commits carry `faresb@fact.qa`; a public repository shows it. Options:
- **(Recommended) Keep history; switch future commits to your GitHub private address** (`<id>+faresbn@users.noreply.github.com`). Simple, nothing rewritten. The old address stays visible in old commits.
- Rewrite history before the flip. Removes the address everywhere, but changes every commit ID (breaking those quoted in `archive/LOG.md` and the session logs) and needs a force-push. You'd approve that explicitly.
- Accept it as is.

**B. Mike's name in the docs.** He's named in AGENTS.md, DECISIONS.md and three session documents. Keep it (my default, if he's fine with it), or I neutralise the current files ("a co-player"). Old commits would still have it either way, short of a rewrite.

## Steps

Each phase is one branch checkpoint with the full check run (`unittest`, `build.py`, `check_site.py`, both `node` checks), merged to `main` when it passes. Phases 1, 2 and 3 can ship before the inbox exists. Rough times are for my work, not waiting on you.

### Phase 1: the feed (about 1 hour)

- **New `scripts/feed.py`, called from `build.py`,** writes into `dist/feed/`:
  - `index.md`: what's here, when it was built, the scan time per market, and the Pre-launch or Live status. This is the address ChatGPT is given; `feed/` has no HTML page.
  - `prices/<market>/index.md` plus one file per item category (latest recorded price, typical, usual, steadiness, days listed, units, weekly change). Then alerts, investment watch and movers with their scan times, worded as `market.py`'s rules require: "recorded", estimates called estimates.
  - `craft.md` (the gold-making table).
  - `pages/<section>/<page>.md`: a copy of each `content/` file with two lines added at the top, its public address and its `version` (the file's git blob ID), which the inbox checks against.
- **`build.py`:** allow `.md` inside `feed/` only; keep refusing `.lua` on the site. The feed stays out of `sitemap.xml` and `search.json`, and the ForeverDB credit goes wherever its data appears.
- **`check_site.py`:** the no-names check covers the feed. It already reads every text file it lists; `.md` gets added.
- **Kept as they are:** `llms-full.txt` and the `.tsv`/`.json` files (nothing removed; ChatGPT's docs point to the feed first).
- **Tests:** a new `tests/test_feed.py` (versions match `git hash-object`, every market and page present, no `.md` outside `feed/`).

### Phase 2: Lua files in the repository (about 30 minutes)

- **`.gitignore`:** remove the `data/captures/**/*.lua` block.
- **Originals live at `data/captures/forever/<scan time UTC>.lua`.** One file can hold several markets, so it's named by scan time.
- **`ingest.py` (Mac):** copy the original into that path as part of the import commit; same undo-on-failure.
- **Commit the three Beta originals,** so the comparison test in `tests/test_ingestion.py` runs in CI instead of skipping.
- **AGENTS.md data rules:** the rule becomes "commit originals, never edit them by hand"; fingerprints are kept as for extracts.
- **Handover gets a size line** (`git count-objects -vH`). A retention decision is due before the repository reaches 500 MB.

### Phase 3: prepare and flip to public (about 45 minutes, then your go)

- **Applies your calls A and B,** then sets this repository's commit email to the noreply address if you choose that.
- **`data/README.md`:** credits ForeverDB.net, says the data is used with credit and not ours to relicense, and which files hold it.
- **`README.md`:** an opening paragraph for public readers (what this is, unofficial, not affiliated with Blizzard); the rest stays.
- **Re-runs the secret scan on the final history.**
- **Flip:** `gh repo edit faresbn/Tazdingo --visibility public --accept-visibility-change-consequences`. Then I check the site still publishes and Actions run. **This step is outward-facing and effectively one-way** (anyone can copy a public repo the moment it's public), so I do it only after you approve this plan.

### Phase 4: the inbox on GitHub's side (about 1.5 hours)

- **Submission layout,** written by the Site: `inbox/<id>/submission.json` plus one of `page.md` or `Auctionator.lua`. The JSON has:
  - `id` and `received` (UTC)
  - `kind` (`page` or `scan`)
  - for a page: `path` (e.g. `content/classes/mage/frost.md`) and `version` (from the feed)
  - `message` (the one-line public commit message, UPDATING.md's rules)
  - for a scan: optional `market`
- **New `scripts/inbox.py`** owns the whole transaction. It works through every waiting submission, oldest first, each with its own rollback, so a bad one never blocks the good ones behind it:
  - **Page:** the path must be a known page (`build.py`'s list); the version must match the current file, otherwise held as "the page changed since you read it, read it again"; the file must pass `load_content`'s header and section rules; the message must pass the no-names rule.
  - **Scan:** the Lua is stored under `data/captures/forever/` and filed through the same `ingest()` the Mac uses; the market is `market` or the remembered default.
  - **Apply, in order:** write the file; run the full test, build and check (if any fails, undo and hold with the failing step's message); commit the content change; then run `scripts/archive.py --before <base> --after <that commit>` and commit its record. `archive.py` reads committed history, so it has to run after the content commit. Workflow commits don't start `archive.yml`, so this is the only archiving the change gets.
  - **Held:** moved to `inbox/held/<id>/` with `reason.txt`, and committed.
  - **Push:** if `main` moved meanwhile (Codex, the Mac, another submission), it never rebases on top. It resets to the new `main` and redoes the whole run from there, version checks included. That way a stale page can't slip through, and the combined result is always the one that was tested. Three attempts, then the run fails and the submissions stay waiting.
  - **Report:** writes each submission's id, outcome and reason to the run's summary page.
- **New `.github/workflows/inbox.yml`:** triggered by a push to `main` under `inbox/` (not `inbox/held/`), with a concurrency group shared with `ingest.yml`. Steps: run `inbox.py` (which pushes), start `pages.yml` if anything was applied, and only then a final step that fails if anything was held. That failure is what makes GitHub email you.
- **`pages.yml`:** `paths-ignore: inbox/**`, so arriving submissions don't trigger a publish.
- **`ingest.yml` and the scan-record route stay working but undocumented for ChatGPT.** Retiring them is a later tidy-up.
- **Tests:** a new `tests/test_inbox.py` covers good page, stale version, unknown path, bad header, name in message, good Lua, unreadable Lua, held move, a bad submission followed by a good one (both handled), and `main` moving mid-run with an edit to the same page (redone, then held as stale).

### Phase 5: the inbox Site (about 1 hour here, plus a Codex deploy)

- **Code in this repository at `inbox-site/worker/index.js`, tests in `inbox-site/inbox.test.mjs`,** the same layout as `relay/`. No dependencies.
- **`POST /submit`** accepts a plain HTML form (multipart) and the same fields as JSON, for a GPT or agent later:
  - **Checks only what must be checked before anything is public:**
    - the key (constant-time compare against the `INBOX_KEY` secret)
    - a 5 MB size limit
    - `kind` is `page` or `scan`
    - the key doesn't appear anywhere in the content
    - limits of 30 accepted submissions an hour and 20 waiting in `inbox/`
    
    Every other rule lives in one place, `inbox.py`, so a keyed but malformed submission still reaches `held/`, where you see it.
  - **Refused** (wrong key or a limit): a row in the Site's database (time, size, kind, reason, no content) and a plain "Refused" reply.
  - **Right key:** removes the key and commits `inbox/<id>/…` in one commit through GitHub's API (`GITHUB_TOKEN` secret). The commit is built on the latest `main`; if `main` moves before it lands, the commit is rebuilt on the new tip, so nothing pushed in between is lost. Then it replies with the id and where to watch.
- **The reply is a plain page,** readable by a person or an agent: "Received. If it passes its checks it's live at <address> in about two minutes."
- **The news relay is untouched.**
- **Deploy:** Codex, as a new Site named `tazdingo-inbox`, with two secrets and a database binding. I write a ready-to-paste Codex brief in this folder.

### Phase 6: the hidden form (about 30 minutes)

- **`inbox/index.html`, built by `build.py` in the site's design:** `noindex` meta tag, not in the menu, sitemap or search.
- **Fields:** key, kind (page or scan), page path, version, message, a large text box for the page and a file picker for the Lua. A plain HTML form posting to the Site, so it works with no JavaScript.
- **`check_site.py`:** whitelist the inbox Site's address next to the relay's, and allow `noindex` on `inbox/index.html` only. Today the check fails any page carrying `noindex` (line 76), and it keeps doing that for every other page.

### Phase 7: ChatGPT's instructions (about 45 minutes)

- **New `docs/chatgpt/TAZDINGO_INBOX.md`,** the project file:
  - the form's address and every field;
  - how to read a page and its version from the feed;
  - "submit the whole file";
  - message rules;
  - what each reply means;
  - "if you can't submit, give the user the finished file and the form's address".
  
  **The committed copy holds `<KEY>` as a placeholder.** You paste the real key into the copy you upload to ChatGPT, because the repository is public.
- **`PROJECT_INSTRUCTIONS.md` and `UPDATING.md`:** read from the feed; write through the inbox; scans are submitted as the Lua itself (no sandbox scripts any more). Everything else in UPDATING.md (page format, findings, sources, no names) stays.

### Phase 8: records and an end-to-end check (about 30 minutes)

- **Docs:** AGENTS.md (settled decisions, data rules, everyday tasks), DECISIONS.md (the five decisions above), README.md, HANDOVER.md.
- **Review log:** the Codex review of this plan, in `revlog.md`.
- **End-to-end check** after the Site is deployed: a page edit through the form, a stale-version edit (held, email arrives), a wrong key (refused, logged), a Beta Lua (filed). I can drive the form in the built-in browser for the person route.

## What I need from you, and when

| When | What | Time for you |
|---|---|---|
| Now | Approve or annotate this plan; calls A and B | — |
| Before phase 4 | Check GitHub → Settings → Notifications → Actions is set to email you, at least for failed runs. That email is how held submissions reach you | 1 minute |
| Before phase 5 deploys | Create the GitHub token: Settings → Developer settings → Fine-grained tokens → only `faresbn/Tazdingo`, Contents read and write, one-year expiry. Give it to Codex for the Site's secrets, never to chat or a file. I'll generate the inbox key into `tmp/` (ignored by git) | 3 minutes |
| Phase 5 | Run the Codex brief to deploy `tazdingo-inbox` | 10 minutes |
| Phase 7 | Paste the new project instructions; upload `TAZDINGO_INBOX.md` with the real key in place | 5 minutes |
| After | Test from the ChatGPT app: read prices from the feed; edit a page via agent mode; submit a Lua via agent mode; the person route | 15 minutes |

## Risks and how they're handled

- **The token is full write access to this repository.** It isn't limited to the inbox. Whoever got hold of it could change the scripts that workflows then run, and history can't undo what compromised code has already done. Mitigations:
  - the Site's code is small, has no dependencies and writes only under `inbox/`;
  - the token covers one repository and expires after a year;
  - it lives only in the Site's secrets;
  - revoking it disables the inbox in seconds.
- **The key leaks** (it sits in a ChatGPT project file). Whoever has it can publish well-formed but wrong pages or unwanted links: the checks enforce format, not truth. The rate and queue limits bound the volume. The fix is to change `INBOX_KEY` in the Site and in TAZDINGO_INBOX.md, then put any affected page back from `archive/`. Check once that rotation takes effect (research.md section 3 notes a beta bug report).
- **Keyed submissions are public on arrival,** held ones included. Accepted, because only the three of you hold the key. The Site refuses content containing the key itself, so a pasted key can't be published by accident.
- **Repository growth from Lua files.** Watched in the handover; retention decided before 500 MB.
- **ChatGPT can't do part of this in practice** (reading long feed files, agent-mode file upload). The person route always works. Feed files are split by category, so each stays small.
- **Going public is effectively one-way.** Everything is checked before the flip; nothing secret is in the history.

## Not in this plan

- No change to the site's design, pages or Auction House logic. Retiring `ingest.yml`'s scan-record route comes later.
- Not done in this plan: a GPT with an action, email from the Site, Vercel, a custom domain, search-engine submission. Removing `llms-full.txt` isn't in it either.

## Order and checkpoints

The phases run in order 1 → 2 → 3 → 4 → 6 → 5 → 7 → 8, each merged to `main` on passing checks. The form (6) lands before the Site (5) is deployed, but points at the Site's address. Until the Site exists, it shows "inbox not open yet". Estimated total of my time: about 6 hours, plus Codex's deploy and your four short steps.
