# Verification record

## Local integration

`python3 scripts/prove_inbox.py` completed successfully on 30 October 2026 after the test-fixture fix:

1. Valid multipart page submission: applied, previous bytes archived, feed version advanced, site rebuilt, result pushed to a disposable bare remote.
2. Stale version: held with its reason; current page unchanged.
3. Cheatsheet change: isolated on a review branch; main unchanged.
4. Addon upload: original bytes retained; the file appears in the feed map.
5. Historical Auctionator fixture: ingested inside the disposable clone, original retained, item pages built.
6. Wrong key: refused before GitHub writes.
7. A key pasted into content: refused before GitHub writes.

Successful processor paths ran the actual Python test suite, site build and output checks. GitHub HTTP and D1 used test adapters; protected edits made local branches rather than hosted PRs. The optional online item-name refresh was omitted. All generated gameplay content and market records were deleted with the temporary clone.

The Auctionator assertions were then strengthened to require a *new* scan record and generated pages for its specific market. A final local run with those stronger assertions also passed all seven cases. The proof workflow is prepared to check the committed revision on GitHub; pushing and running it are pending.

## Other checks

- 126 Python tests passed on the starting implementation; the full suite also passed inside the successful integration paths after fixture isolation.
- 14 receiver tests passed, including missing/malformed configuration and secret-free health output.
- 10 news-relay tests passed.
- Site build and check: 1,055 pages, two reference markets, 77 guide sources, 1,039 search entries.
- Browser-script syntax and diff whitespace checks passed.
- The Sites Worker bundle built and passed its ESM entrypoint validator.
- The built Worker, with no configuration: `GET /` 200; `GET /submit` 405; `GET /health` 503; `POST /submit` 503.

## Not yet proved

There is no hosted deployment. The receiver Site is an unpublished draft with personal keys configured, but no repository-scoped GitHub token. Source synchronization was blocked by source-host DNS failure. Hosted D1, real receiver-to-GitHub delivery, Actions processing, review PR creation, Pages publication after a submission, and the browser form remain unverified. `inbox.open` remains false.

The GitHub connector rejected tree creation with `MCP tool call requires approval, but approval policy is never`. No remote tree, commit, branch or pull request was created, and no GitHub proof workflow ran. All changes are committed in the local working branch.
