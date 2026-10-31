# Connecting either Warcraft project to Tazdingo

Both projects use the same Tazdingo running record. Their conversations remain separate.

For testing today, use the already-connected GitHub route below. It has been exercised from this chat through the actual connector. The optional direct tools are deployed, but their per-account plugin connection still needs a native smoke test; publication alone does not install them.

## Optional direct Tazdingo chat tools

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

## Already-connected GitHub route (works without a new plugin connection)

An authenticated GitHub account with write access can send an inbox packet directly through the connected GitHub tools. This is an alternate inbox transport, not a direct edit to a guide. All existing validation, review and receipt handling still runs. Use this route when the Tazdingo chat tools are unavailable; it requires no inbox key.

1. Read the current complete content/ file and its actual Git blob SHA. Prepare the whole edited page under UPDATING.md.
2. Generate a fresh id in `YYYYMMDDTHHMMSSZ-<8 lowercase hexadecimal characters>` form and a UTC ISO timestamp.
3. Prepare `inbox/<id>/submission.json` with `format: 1`, `id`, `received`, `key_label: "github-connector"`, `kind: "page"`, `file: "page.md"`, `path`, `version` (at least the first 12 characters of the blob SHA), and `message`. Put the complete edited page in `inbox/<id>/page.md`.
4. Publish BOTH files atomically in ONE Git commit based on current main: create their blobs, create a tree using main's tree as base, create a commit with main as parent, then update main without force and with its expected head SHA. If main moved, reread it and retry the commit/ref update. Never create the two files with separate commits: the processor could see an incomplete packet.
5. Read `inbox/results/<id>.json` for applied, held or review; while the packet is still in inbox/<id>/ it is waiting. For review, find the owner PR from branch `review/<id>`. Only report what the receipt and PR establish.

Do not send keys or credentials in a packet. Do not modify content/, feed/, data/ or archive/ directly to make an update go through. If the connected GitHub tools cannot publish an atomic commit, use the Tazdingo tools or form instead; never pretend the write happened.

For an original addon, use the same atomic packet with kind: "lua", file: the original safe addon filename (for example Auctionator.lua), and the unchanged file bytes as the second blob. Omit page path/version. Add market with the actual realm and faction for Auctionator. Create the file blob from exact original bytes (base64 encoding if needed); never from a conversation summary. If the tools cannot access the exact original or handle its size, use the original-file form upload. The transport does not bypass the 25 MB or provenance limits.
