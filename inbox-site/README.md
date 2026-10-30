# Tazdingo inbox Site

Receives the hidden form at https://faresbn.github.io/Tazdingo/inbox/ (or the same fields as JSON) and commits each submission, with the key removed, to `inbox/<id>/` in this repository. `scripts/inbox.py`, run by `.github/workflows/inbox.yml`, then checks it and applies it, sends it for review or holds it. This Site only checks what must be checked before anything becomes public:

- the key, against the personal keys in `INBOX_KEYS` (constant-time), which gives the submission's label;
- the size (25 MB) and the kind (`page` or `lua`; a `.lua` named like an addon's file);
- that no key appears in the page or file;
- 30 accepted submissions an hour, and no more than 20 waiting in `inbox/`.

Refusals are logged in this Site's database (time, kind, size, reason; no content), never in the public repository.

It's a separate Site from the news relay (`relay/`), so the relay keeps its rule of never holding GitHub credentials.

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
