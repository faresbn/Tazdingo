# Hosted inbox proof, 31 October 2026

The receiver is deployed. Authenticated service delivery works; the public form stays closed pending approval for browser and public-endpoint tests.

## Verified

- PR #7 merged; 126 Python tests, 24 Node tests and 1,055 generated pages passed.
- Seven-case integration proof passed: https://github.com/faresbn/Tazdingo/actions/runs/41178145354
- Receiver https://tazdingo-inbox.fact-special-2007.chatgpt.site; project appgprj_6ae4fe3d837481918b7ef17082430eae; source 23ce0f69b88ef542af435bac05a85d824f237bde; deployment appgdep_6ae58fc0b1808191ae93cc2562f982c6; environment revision 2. Both secrets and DB are configured. The manifest uses the string `"d1": "DB"`.
- Authenticated hosted health returned 200. Wrong inbox key returned 403; a key pasted in content returned 400. D1 logs store only refusal metadata, never the key or content.
- Multipart page 20261031T065405Z-3ab34ce3 applied, advanced the feed version and archived its previous bytes. The harmless source-link wording remains.
- Multipart addon 20261031T065427Z-be1f3a4e was retained unchanged and appeared in the feed.
- Stale page 20261031T065427Z-fc1fbfb0 was held without overwriting the current page.
- Processing https://github.com/faresbn/Tazdingo/actions/runs/41178446781 applied valid work and published; its final failure intentionally notified the owner about the held stale test.
- Publication https://github.com/faresbn/Tazdingo/actions/runs/41178621202 succeeded after those submissions.
- Cleanup removes the temporary addon and held-test files; evidence remains in git history.

## Verification boundaries and remaining approval

Delivery tests used the documented Sites owner service credential as well as the personal inbox key. They do not establish anonymous browser usability. The intended public receiver audience is configured; the website form remains disabled.

An anonymous automated request got Cloudflare 1010 (browser signature blocked). Automatic review rejected opening the receiver in a browser as a potential workaround. A saved browser permission separately blocks faresbn.github.io. No alternate user agent, proxy, browser surface or indirect fetch was used to bypass these rejections.

After the endpoint became public, automatic review rejected sending the personal key for a protected-edit test without specific authorisation for that destination. It also rejected a key-free protected-edit record pushed directly to main as a consequential test publication. Neither protected test reached the public repository. Protected review routing remains proved locally, not through a hosted PR.

Needed next: explicit approval to send the personal inbox key and test page/file to this public receiver over HTTPS, to perform the normal-browser check after the automated-client rejection, and to publish the resulting temporary test record/review PR to the public repository. Browser access to faresbn.github.io must also be allowed. Keep inbox.open false until these checks pass.

No Beta Auctionator fixture was published as live data. Ingestion is proved in the disposable test; the first real scan remains a launch task. The preceding outside-review attempt was unavailable because Claude CLI was not logged in; no outside review is claimed.
