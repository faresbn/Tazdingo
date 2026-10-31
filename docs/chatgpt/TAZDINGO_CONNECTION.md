# Connecting either Warcraft project to Tazdingo

Both projects use the same Tazdingo running record. Their conversations remain separate.

## Primary route: Tazdingo chat tools

Install/connect the canonical plugin created by the existing Tazdingo inbox Site. It supplies:

| Tool | Purpose |
|---|---|
| read_tazdingo | Read a map, price feed, complete guide or procedure with its current blob version |
| submit_tazdingo_page | Queue a complete guide edit through normal provenance and review checks |
| submit_tazdingo_addon | Queue exact original addon bytes supplied as base64 |
| tazdingo_submission_status | Read the durable processing receipt |

The Site verifies the connected ChatGPT account. Reads require a signed-in caller; writes also require an explicit writer grant. Keys remain server-side. Each participant needs their own plugin connection and writer grant; sharing a ChatGPT project does not grant another person's credentials.

The owner configures MCP_WRITERS in the existing Site's secrets: a JSON mapping from each verified email to that person's existing INBOX_KEYS label. Do not put the map or keys in the public repository. Readers can connect without a writer grant; an unrecognised writer receives an explicit refusal. Public site visibility does not make write tools anonymous.

Start with read_tazdingo(path="feed/index.md"). For a guide, follow feed/guides.md and read the complete content/ file. Use the blob version returned with that exact file. submit_tazdingo_page returns a receipt id; check it with tazdingo_submission_status. Outcomes are waiting, held, review or applied. An older submission can be unknown if it predates durable receipts. Applied means the repository changed; do not claim the static site was published without checking its publish run.

## Fallback: public repository and inbox form

Read through the connected GitHub app or https://raw.githubusercontent.com/faresbn/Tazdingo/main/feed/index.md. Send through https://faresbn.github.io/Tazdingo/inbox/ using a personal inbox key. Keep the key in a private, person-specific copy of TAZDINGO_INBOX.md, never in shared instructions or the repository. Browser permissions and agent/file-attachment capabilities are required for an assistant to operate the form; otherwise the person can send it.

For large addon files, attach the original file through the form. Do not encode or reconstruct a file from a prose summary, and do not silently truncate it to fit tool limits. Stored originals are public, including held submissions. Auctionator ingestion requires its realm/faction and correct environment; do not use a historical Beta capture to test Live data.

## Afternoon smoke test

1. In each project, read feed/index.md, then one actual guide and one correct market category. Confirm source, date/environment and guide version.
2. Submit one harmless source-wording edit to an existing page, preserving its gameplay claims. Check the receipt until applied. Confirm the new version by reading the page again.
3. Reuse the old version once: confirm held, with no overwrite.
4. Change a protected cheatsheet: confirm review and an owner PR, then close that temporary PR if it is only a test.
5. Upload an exact small original addon file: confirm stored bytes and receipt. Use the first real live Auctionator scan for the launch test.

For read-only prices, reports should never invent a new scan or imply listed quantities are sales. For writes, never call received/queued applied. Preserve the receipt id if processing is still running.
