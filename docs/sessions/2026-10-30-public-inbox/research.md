# Research: a public repository, a ChatGPT feed and an inbox

30 October 2026. Fares asked for the repository to be reorganised around four parts (uploads from ChatGPT conversations, the public website, a plain folder ChatGPT reads, and an inbox that ChatGPT or a person posts into without a GitHub account) and for the repository to become public. This file records what's true today and what the design has to work with. `plan.md` turns it into steps.

Fares's brief, in short:
- **Inbox:** a form on the website, not linked anywhere, known only through a `TAZDINGO_INBOX.md` file in the ChatGPT project that holds a key and the rules a submission must follow. A GitHub Action processes what arrives. Three outcomes: right key and right structure → applied; right key, wrong structure → held and flagged to Fares by email; wrong key → a failed folder, reviewed now and then.
- **Feed:** a folder inside the published site, in markdown, holding what ChatGPT needs (above all, the market data processed from the Lua scans). Not linked for visitors, who get the Auction House pages.
- **Lua files:** game data, fine to publish. The repository keeps their history and turns them into the feed.
- **Who writes how:** ChatGPT (Fares, Mike, possibly Fares's brother, all on one ChatGPT Business plan) goes through the inbox. Codex keeps committing to `main`. Fares can override either on request.
- **Public repository:** no value in staying private; restructure for whatever is more efficient in public.
- **Hosting:** stay on GitHub Pages. No Vercel (paused; Fares doesn't want to pay for a hobby site) and no paid GitHub Copilot (Fares has GitHub Pro only).
- **ChatGPT's abilities:** Fares tests them in the app; build to his description. Route A (a person submits the form) is the fallback for route B (ChatGPT submits it in agent mode).

## 1. No LLM is needed on GitHub's side

**What it means:** the inbox can live entirely on free GitHub Actions, with no Copilot subscription and no move to Vercel.

**How:** everything the Action does is already deterministic code in this repository.
- A **Lua scan** becomes prices through `scripts/auctionator.py` and `scripts/market_store.py`, the same code `ingest.py` runs on the Mac. No judgement involved.
- A **guide edit** arrives already written: ChatGPT does the writing in the conversation and submits the finished markdown file. The Action only checks it (known page, header fields, the four sections, links, no names) and swaps it in. Those checks already exist in `scripts/build.py` (`load_content`, header and section rules) and `scripts/check_site.py`.

The one thing that would need an LLM is turning *raw notes* into a page. That stays in the ChatGPT conversation; the inbox never accepts loose notes.

## 2. Submit markdown, not HTML

**What it means:** a submission changes one file in `content/` and the site rebuilds itself. Nothing ChatGPT writes is ever placed on the site unchecked.

**How:** every HTML page is generated from `content/*.md` plus the data files on each build (`scripts/build.py`, `scripts/sections.py`). A replaced HTML file would be overwritten by the next build, about every two hours (the scheduled run in `pages.yml`) or on any push.

## 3. The form needs something behind it, and GitHub Pages can't be that

**What it means:** one small extra piece, a ChatGPT Site (the same hosting the news relay already uses, included in the Business plan), receives the form and hands the submission to GitHub.

**How:**
- GitHub Pages only serves files; a form posted to it goes nowhere.
- A form on a public page can't talk to GitHub directly either. Writing to GitHub needs a token, and a token in a public page can be copied by anyone. GitHub also scans public pages and repositories for tokens and revokes them.
- The news relay runs on **ChatGPT Sites** (`tazdingo-news-relay.fact-special-2007.chatgpt.site`, Sites project `appgprj_6ae0525843008191bea52b4b0dc0adeb`, `relay/README.md`). Sites run on Cloudflare's Workers runtime. They keep **secrets in the Site's settings** and have a **database (D1, up to 10 GB) and file storage (R2)** ([OpenAI help](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites); [guide](https://kingy.ai/news/openai-sites-a-detailed-guide-to-codexs-new-hosted-website-and-app-builder/); [explainer](https://playcode.io/blog/chatgpt-sites-explained)). That's exactly what an inbox needs: hold the key as a secret, log refused attempts in the database, pass good submissions on. Sites is in public beta, and one unconfirmed forum report says a removed secret kept working after a redeploy ([forum](https://community.openai.com/t/chatgpt-sites-removed-environment-secret-still-persists-in-production-runtime-after-redeploy/1397652)), so key rotation should be checked once.
- **Deploying a Site goes through Codex's Sites workflow** (`relay/README.md`: a short-lived source credential, a separate relay checkout, deploy from a pushed commit). Claude Code can write and test the Site's code here, but Codex deploys it.

## 4. The Site has to push to GitHub; GitHub can't fetch from the Site

**What it means:** the Site holds a GitHub token. That reopens a settled rule ("the relay never receives GitHub publishing credentials"), so the inbox should be its own Site, leaving the news relay exactly as decided.

**How:**
- The other direction (GitHub's Action checking the Site for new submissions, so the Site never holds a token) was ruled out by experience. On 27 October the Sites host's edge rejected automated command-line clients with a browser-signature policy, which is why scheduled news collection reads Blizzard directly (`docs/sessions/2026-10-27-tazdingo/revlog.md`, `relay/README.md`). An Action polling the Site would very likely hit the same wall.
- Telling GitHub "something arrived" (a `repository_dispatch` event) needs **Contents: read and write** on a fine-grained token ([step-security/repository-dispatch](https://github.com/step-security/repository-dispatch); [mirror of peter-evans/repository-dispatch](https://github.com/ftos-forks/repository-dispatch); GitHub's [permissions reference](https://docs.github.com/en/enterprise-server@3.12/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens) for the table). That's the same permission as committing a file, and a dispatch payload is far too small for a 1 MB Lua file. So committing the submission is no riskier than pinging, and simpler: **the Site commits the submission into an `inbox/` folder**, and an Action triggered by that push does the rest.
- **The token:** a fine-grained personal access token limited to `faresbn/Tazdingo`, with Contents read and write and nothing else, expiring after a year. Only Fares can create it (GitHub settings → Developer settings). It can write anywhere in this one repository, so the Site's code must only ever write to `inbox/`. That's a code rule, not something GitHub enforces: a token acting as the repository's owner bypasses branch rules.
- **The key never reaches GitHub.** The Site checks it and strips it before committing. In a public repository, anything committed is published.

## 5. Where each outcome lands, given the repository is public

**What it means:** the three outcomes Fares described all work. The wrong-key "failed folder" has to live in the Site's private database rather than the repository, or anyone could fill the public repository with junk.

| Submission | Where it goes | How Fares hears |
|---|---|---|
| Wrong or missing key | Refused at the Site; logged in the Site's database (time, size, kind, reason). Never committed | Reviewed on request. Site editors (Fares, Codex) can read the live database |
| Right key, fails a check | Moved to `inbox/held/` with a note of the reason | The Action fails on purpose, and GitHub emails the account that pushed. That's Fares, because the token is his. Failed-run emails are on by default for runs you trigger; worth checking once in his notification settings |
| Right key, passes | Applied to `main`, archived, published | The submitter sees the result on the Site's reply page; the site updates within minutes |

The held folder also catches healthy submissions that fail for reasons nobody anticipated, which was Fares's second reason for a failed folder. Its contents come only from key holders, so they're safe in public.

Failing the run on purpose is simpler than opening an issue or sending mail: it needs no extra permission, no mail service, and no email address anywhere in the public repository.

## 6. What today's workflows do, and what the inbox inherits

- **`ingest.yml`** files scan records from `data/market/inbox/` on a push to `main`: tests, build, check, commit, push, then starts the publish itself. A commit made with a workflow's own token doesn't start other workflows (GitHub's loop guard).
- **`archive.yml`** backs up changed `content/` pages on a push to `main`. Because of the loop guard, **a page applied by an inbox Action wouldn't be archived** unless the inbox Action runs `scripts/archive.py` itself. It must.
- **`pages.yml`** publishes on every push to `main`, every two hours and on request. Submissions arriving in `inbox/` shouldn't trigger a publish (`paths-ignore`).
- **One bad inbox record blocks later inbox runs** (HANDOVER watch item). The new design moves a bad submission to `held/` instead of leaving it in place, which removes that problem.
- **Two people editing the same page:** today ChatGPT writes back against the file's SHA, so GitHub refuses a stale write. Through the inbox the Action has to do that check itself: the feed shows each page's version, the submission quotes it, and the Action holds the submission if the page has changed since.

## 7. The feed folder

**What it means:** ChatGPT reads plain markdown at a stable address, e.g. `https://faresbn.github.io/Tazdingo/feed/`, with prices and pages and nothing else.

**How it stands:**
- ChatGPT reads `llms-full.txt` (every page in one file), each market's `prices.tsv` and `prices.json`, and `prices/craft.tsv`, all built by `scripts/build.py`. There's no markdown output.
- `build.py` refuses to publish any `.md` file (an allow-list of public file types) and any `.lua`. The feed needs `.md` added for `feed/` only; the Lua block stays, because Lua belongs in the repository, not the website.
- **Size:** a live market of ~4,200 items at roughly 80–100 characters a row is about 350–400 KB of markdown. Chat tools may truncate long pages. Splitting by item category keeps each file small, and an index lists them.
- **Hiding it from the world:** GitHub Pages can't send "don't index" headers, and a `robots.txt` only counts at the host's root (`faresbn.github.io/robots.txt`), which this repository doesn't control. In practice: not linked, not in `sitemap.xml`, not in `search.json`. Search engines rarely find unlinked files, but it isn't guaranteed.
- **Versions for the stale-edit check:** each page's copy in the feed carries its git blob ID (what `git hash-object` gives), which is also what the inbox Action compares.

## 8. Lua files in the repository

**What it means:** every scan's original file is kept and published in the repository, and the Mac and the inbox file scans the same way.

**What's in them** (checked on the three Beta files): Auctionator's settings, saved variables, shopping lists, price database, posting history (item, price, quantity, time), vendor price cache, recent searches and selling groups. The price database and saved variables are keyed by realm type ("PvP", "ClassicBetaPvP"). No character names turned up in those top-level tables. Fares has decided they're fine to publish.

**What changes:**
- AGENTS.md's data rule "never commit an original SavedVariables file" and `.gitignore`'s `data/captures/**/*.lua` block are reversed. That's a decided change, recorded in DECISIONS.
- `tests/test_ingestion.py` compares the originals and skips when they're absent; with the files committed it always runs.
- **Size:** the Beta files are 0.72, 0.88 and 1.19 MB (0.24, 0.30 and 0.42 MB compressed). Auctionator's file grows over time, and live markets will be larger than the Beta sample. At three or four a day, the history could grow by very roughly 0.5 GB or more a year, and git history never shrinks. GitHub recommends keeping repositories small. A size check in the handover, and a retention decision before 500 MB, keep this in hand.

## 9. Going public

**What it means:** the flip is safe to do. Two things become visible that Fares should decide on knowingly.

- **No secrets in the history.** All 80 commits, every branch, searched for GitHub, OpenAI and AWS token formats, private keys and API keys assigned in code: nothing. The ForeverDB key has only ever lived in the environment.
- **Fares's work email is on every commit.** 77 commits are authored and 70 committed as `Fares B <faresb@fact.qa>`. A public repository shows that address to anyone. Options: accept it; switch future commits to GitHub's private `…@users.noreply.github.com` address and leave history alone; or rewrite the history's author emails before the flip. Rewriting changes every commit ID, breaks the commit IDs quoted in `archive/LOG.md` and the session logs, and needs a force-push, which needs Fares's explicit approval.
- **Names in the repository.** "Mike" appears in AGENTS.md, DECISIONS.md, three session documents, and `build.py` and `check_site.py` (where the names are listed so the *site* never shows them). Fares appears throughout. ChatGPT and Codex are named in docs and scripts. The "public site is impersonal" rule is about the site and `check_site.py` keeps enforcing it; the repository itself would no longer be impersonal. The site's address already carries `faresbn`, so the added exposure is small, but Mike is a third party.
- **ForeverDB data.** `data/foreverdb.json`, `data/foreverdb-api.json` and `data/items.json` hold ForeverDB data. Earlier research (`docs/sessions/2026-10-27-site-plan/research.md`): use on our own site is allowed with the credit; reselling or presenting it as ours isn't; no formal licence is named. A public repository republishes the raw files. That's low risk with a visible credit file in `data/`. Asking ForeverDB is Fares's call.
- **Gains.** GitHub Actions on standard runners is free for public repositories, which settles the open "Actions minutes" question. ChatGPT can read any file at `raw.githubusercontent.com` without a connector.
- **Workflows stay safe.** A pull request from a fork runs `pages.yml` with read-only permissions and no secrets. `ingest.yml`, `archive.yml` and the new inbox workflow run only on pushes to `main`, which outsiders can't make.
- **Settled decisions this changes:** "a private repo" (AGENTS.md, DECISIONS), "never commit SavedVariables" (AGENTS.md), "ChatGPT commits directly" (DECISIONS: ChatGPT now posts to the inbox; Codex still commits), "the non-GitHub route is parked" (DECISIONS), and "the relay never receives GitHub credentials" (kept for the news relay; the inbox is a separate Site).

## 10. What ChatGPT is asked to do, and what Fares tests

From TAZDINGO_INBOX.md, ChatGPT needs to: read a page from the feed (with its version), write the complete new markdown, and submit it with the key, the kind, the page path and that version, or submit a Lua file with the key. Route B (agent mode filling the form) and route A (the person filling it) use the same form.

To test in the ChatGPT app once built: reading `feed/` pages and prices (size, truncation), submitting a page edit in agent mode, uploading a Lua file in agent mode, and whether the Sites host lets ChatGPT's browser through. The form must work without JavaScript and give a plain reply page, so a person or an agent can read the result.

## Sources

- [Creating and using ChatGPT Sites (OpenAI help)](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)
- [OpenAI Sites guide (2026)](https://kingy.ai/news/openai-sites-a-detailed-guide-to-codexs-new-hosted-website-and-app-builder/)
- [ChatGPT Sites explained](https://playcode.io/blog/chatgpt-sites-explained)
- [Forum report: removed Sites secret persists after redeploy](https://community.openai.com/t/chatgpt-sites-removed-environment-secret-still-persists-in-production-runtime-after-redeploy/1397652)
- [step-security/repository-dispatch (token permissions)](https://github.com/step-security/repository-dispatch)
- [repository-dispatch mirror (token options)](https://github.com/ftos-forks/repository-dispatch)
- [GitHub: permissions required for fine-grained tokens](https://docs.github.com/en/enterprise-server@3.12/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens)
- Repository: `relay/README.md`, `docs/sessions/2026-10-27-tazdingo/revlog.md`, `docs/sessions/2026-10-27-site-plan/research.md`, `.github/workflows/*.yml`, `scripts/build.py`, `scripts/check_site.py`, `scripts/ingest.py`, `scripts/scan_record.py`
