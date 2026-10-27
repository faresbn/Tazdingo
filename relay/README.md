# Tazdingo news relay

The website stays on GitHub Pages. This read-only Worker serves `/news` for browser refreshes, with a five-minute edge cache, coalesced refreshes and per-isolate request throttling. The cache/throttle is per edge location/isolate, not a guaranteed global quota. It never triggers GitHub publishing or accepts user-supplied upstream URLs.

Canonical classifier source: `worker/index.js`. Its classification function is shared by the Python scheduled collector through `scripts/classify_news.mjs`. Run `node --test relay/news.test.mjs` from the repo root. Deploy changes to the relay as well as the Pages site; changing the mirror alone does not update the service.

Current public endpoint: https://tazdingo-news-relay.fact-special-2007.chatgpt.site/news
Sites project: appgprj_6ae0525843008191bea52b4b0dc0adeb

Deployment uses the Sites Worker ESM workflow, separately from GitHub Pages. Preserve the project identity, recover a short-lived source credential, open the relay checkout, copy this Worker into `worker/index.js`, run the tests/build/validation, then save and deploy the pushed commit. Never put source credentials in this repo. The endpoint contains public Blizzard data only.

GitHub Actions intentionally reads Blizzard directly: this environment's automated HTTP client was blocked by the relay host, and scheduled collection must remain independent of visitor hosting. Readable articles are inspected by section; this is a conservative rule-based classifier. A mixed roundup needs substantive identifiable Forever coverage; ambiguous/unreadable pages are not promoted. Both views use the same classified records; only the inner news page includes mixed posts.
