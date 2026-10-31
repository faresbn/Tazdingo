# Tazdingo inbox Site

Receives the hidden form at https://faresbn.github.io/Tazdingo/inbox/ (or the same fields as JSON) and commits each submission, with the key removed, to `inbox/<id>/` in this repository. `scripts/inbox.py`, run by `.github/workflows/inbox.yml`, then checks it and applies it, sends it for review or holds it. This Site only checks what must be checked before anything becomes public:

- the key, against the personal keys in `INBOX_KEYS` (constant-time), which gives the submission's label;
- the size (25 MB) and the kind (`page` or `lua`; a `.lua` named like an addon's file);
- that no key appears in the page or file;
- 30 accepted submissions an hour, and no more than 20 waiting in `inbox/`.

Refusals are logged in this Site's database (time, kind, size, reason; no content), never in the public repository.

It's a separate Site from the news relay (`relay/`), so the relay keeps its rule of never holding GitHub credentials.

## Current deployment checkpoint (30 October)

The separate receiver Site has been created: **appgprj_6ae4fe3d837481918b7ef17082430eae**, slug `tazdingo-inbox`. Reuse this identity; do not create another Site. It is an unpublished owner-private draft. The three prepared personal keys are configured as the `INBOX_KEYS` secret (environment revision 1). The repository-scoped `GITHUB_TOKEN` is still missing.

GitHub writes were also rejected because this session requires tool approval but has an approval policy of never. Changes are committed locally and have not been pushed.

The source-host connection failed to resolve `git.chatgpt-team.site` in the implementing session, so source synchronization and hosted deployment could not be completed. The Worker bundle was built and validated locally. `data/game.json` deliberately remains `inbox.open: false`.

`GET /health` returns 200 only when the GitHub token, a valid personal-key map and the database binding are configured; otherwise 503. It exposes booleans only and disables caching. **This is a configuration check, not evidence that the token works or that a submission has been processed.** Unconfigured POSTs return 503 before contacting GitHub.

## Local integration proof

Run `python3 scripts/prove_inbox.py` from the repository root. Allow about five minutes. It sends multipart bodies through the production receiver and processes the resulting payloads in a disposable local clone, running the real Python tests, build, site checks and archive. It covers successful and stale edits, cheatsheet review, unchanged addon bytes, an Auctionator fixture, wrong keys and pasted keys.

GitHub HTTP and D1 use test adapters, review cases create local branches, and the optional item-name refresh is omitted. This does not prove the hosted Site, token, database, Actions, pull requests or browser form. The historical Auctionator fixture is used only in the disposable clone. No proof submissions are sent to the real repository. `.github/workflows/inbox-proof.yml` is prepared to run the same proof when inbox source changes. It has not yet been pushed or run on GitHub.

## Deploying

Deploy it through ChatGPT Sites (Codex), as a Worker (ES module) from `inbox-site/worker/index.js`, with:

| Setting | Value |
|---|---|
| `GITHUB_TOKEN` (secret) | A fine-grained token for `faresbn/Tazdingo` only, with **Contents: read and write** and nothing else; one-year expiry |
| `INBOX_KEYS` (secret) | JSON of personal keys by label: `{"key-1": "…", "key-2": "…"}` |
| `DB` (database binding) | The Site's database, for the refusal log and the hourly limit |
| `REPO` (optional) | Defaults to `faresbn/Tazdingo` |

The ready-to-paste brief is `docs/sessions/2026-10-30-public-inbox/codex-deploy-brief.md`. Once it's deployed, put its address in `data/game.json` (`inbox.endpoint`, ending `/submit`) and set `inbox.open` to `true`.

Run the tests from the repository root: `node --test inbox-site/inbox.test.mjs`.

**To revoke:** delete the token on GitHub (the inbox stops at once), or remove one person's key from `INBOX_KEYS`.
