# Codex brief: deploy the Tazdingo inbox Site

Paste everything below the line into Codex.

---

Deploy a new ChatGPT Site named **tazdingo-inbox**. It's a Cloudflare-style Worker (ES module) whose code is the single file `inbox-site/worker/index.js` in the public GitHub repository `faresbn/Tazdingo`, branch `main`. Read `inbox-site/README.md` there first.

1. **Keep it separate from the existing news relay Site** (`tazdingo-news-relay`, project `appgprj_6ae0525843008191bea52b4b0dc0adeb`). Don't change the relay.
2. **Code:** copy `inbox-site/worker/index.js` as the Worker's entry module, unchanged. It has no dependencies. Before deploying, run its tests from a checkout of the repository: `node --test inbox-site/inbox.test.mjs` (all must pass).
3. **Secrets, set in the Site's settings, never in code or in `.openai/hosting.json`:**
   - `GITHUB_TOKEN`: the owner pastes a fine-grained GitHub token (repository `faresbn/Tazdingo` only, Contents read and write only).
   - `INBOX_KEYS`: the owner pastes a JSON object of personal keys, e.g. `{"key-1": "...", "key-2": "...", "key-3": "..."}`.
4. **Database:** bind the Site's database as `DB`. The Worker creates its two tables (`refusals`, `accepted`) itself.
5. **Deploy**, then check it in a browser:
   - `GET /` shows "Tazdingo inbox";
   - `GET /submit` shows "Send the form" (405).
   
   Don't submit anything real: a submission with a valid key is committed to the public repository.
6. **Report back:** the Site's public address (e.g. `https://tazdingo-inbox.<workspace>.chatgpt.site`), the deployed commit, and that both secrets and the database binding are set. Don't print either secret.
