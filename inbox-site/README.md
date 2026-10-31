# Tazdingo inbox Site

Receives the hidden form at https://faresbn.github.io/Tazdingo/inbox/ (or the same fields as JSON) and commits each submission, with the key removed, to `inbox/<id>/` in this repository. `scripts/inbox.py`, run by `.github/workflows/inbox.yml`, then checks it and applies it, sends it for review or holds it. This Site only checks what must be checked before anything becomes public:

- the key, against the personal keys in `INBOX_KEYS` (constant-time), which gives the submission's label;
- the size (25 MB) and the kind (`page` or `lua`; a `.lua` named like an addon's file);
- that no key appears in the page or file;
- 30 accepted submissions an hour, and no more than 20 waiting in `inbox/`.

Refusals are logged in this Site's database (time, kind, size, reason; no content), never in the public repository.

It's a separate Site from the news relay (`relay/`), so the relay keeps its rule of never holding GitHub credentials.

## Current deployment checkpoint (31 October)

The receiver is deployed at https://tazdingo-inbox.fact-special-2007.chatgpt.site, project **appgprj_6ae4fe3d837481918b7ef17082430eae**. Reuse it. Both secrets and DB are configured (environment revision 3); the manifest declares `"d1": "DB"`.

Authenticated hosted tests proved multipart delivery, application, archiving, original-file storage, stale-version handling and publication. The owner authorised the remaining public tests: protected changes created an actual review PR. The form is enabled for testing, although its browser interaction remains unverified because a saved browser policy denies the Pages domain. The connected GitHub atomic-inbox route is available without a new plugin connection. See `docs/chatgpt/TAZDINGO_CONNECTION.md` and the afternoon session proof.

`GET /health` returns 200 only when the GitHub token, a valid personal-key map and the database binding are configured; otherwise 503. It exposes booleans only and disables caching. **This is a configuration check, not evidence that the token works or that a submission has been processed.** Unconfigured POSTs return 503 before contacting GitHub.

## Local integration proof

Run `python3 scripts/prove_inbox.py` from the repository root. Allow about five minutes. It sends multipart bodies through the production receiver and processes the resulting payloads in a disposable local clone, running the real Python tests, build, site checks and archive. It covers successful and stale edits, cheatsheet review, unchanged addon bytes, an Auctionator fixture, wrong keys and pasted keys.

GitHub HTTP and D1 use test adapters, review cases create local branches, and the optional item-name refresh is omitted. This does not prove the hosted Site, token, database, Actions, pull requests or browser form. The historical Auctionator fixture is used only in the disposable clone. No proof submissions are sent to the real repository. `.github/workflows/inbox-proof.yml` is prepared to run the same proof when inbox source changes. It passed on GitHub before PR #7 merged.

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

## Direct chat tools and receipts

The published Site declares MCP capability and exposes read_tazdingo, submit_tazdingo_page, submit_tazdingo_addon and tazdingo_submission_status. Sites supplies verified identity; reads require a signed-in caller, writes require a verified email mapped through the secret MCP_WRITERS to a configured INBOX_KEYS label. Tools never accept a key from chat. Publication provisions a canonical plugin; it does not install it into a conversation. Native sign-in/invocation still needs client testing.

The processor stores public outcomes in inbox/results/<id>.json. Waiting payloads and held reasons remain inspectable. Applied means committed; Pages publication is separate. Both chat tools and authenticated GitHub atomic packets use this same processing pipeline. Never bypass protected-edit review by writing a guide directly.
