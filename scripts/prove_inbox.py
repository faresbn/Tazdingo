"""Prove the inbox locally, in a disposable clone, without real keys or public submissions.

python3 scripts/prove_inbox.py

Runs the production receiver on actual multipart bodies, then gives its exact GitHub payloads
to the production processor. Successful edits run the full Python tests, build, site check and
archive. GitHub's HTTP transport and the receiver's D1 binding use test adapters; review cases
create local review branches. This does not prove hosted secrets, D1, Actions, PRs or browser UI.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
KEY = "local-only-proof-key-00000001"
PAGE = "content/more/addons.md"


def command(root: Path, *args: str, input: str | None = None, timeout: int = 180) -> str:
    result = subprocess.run(args, cwd=root, input=input, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}):\n{(result.stdout + result.stderr)[-4000:]}")
    return result.stdout.strip()


def git(root: Path, *args: str) -> str:
    return command(root, "git", *args)


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def main() -> None:
    stamp = datetime.now(timezone.utc)
    results = []
    with tempfile.TemporaryDirectory(prefix="tazdingo-inbox-proof-") as temporary:
        base = Path(temporary)
        remote, root = base / "remote.git", base / "work"
        command(base, "git", "clone", "-q", "--bare", "--no-hardlinks", str(ROOT), str(remote))
        command(base, "git", "clone", "-q", str(remote), str(root))
        git(root, "switch", "-C", "main")
        git(root, "config", "user.name", "tazdingo-proof")
        git(root, "config", "user.email", "tazdingo-proof@users.noreply.github.com")

        def submit(fields: dict, file: tuple[str, bytes] | None = None) -> dict:
            response = json.loads(command(root, "node", "inbox-site/receive-proof.mjs", input=json.dumps({
                "fields": {"key": KEY, **fields},
                "file": {"name": file[0], "base64": base64.b64encode(file[1]).decode()} if file else None,
                "now": int(stamp.timestamp() * 1000) + len(results) * 1000,
            })))
            for entry in response["files"]:
                path = root / entry["path"]
                require(path.is_relative_to(root / "inbox"), "Receiver wrote outside the inbox")
                raw = base64.b64decode(entry["base64"])
                require(KEY.encode() not in raw, "A personal key reached the GitHub payload")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            if response["files"]:
                git(root, "add", "inbox")
                git(root, "commit", "-qm", "Inbox: local proof submission")
            return response

        def process(expected: str) -> dict:
            # The real processor runs its real tests/build/checks; only the optional name refresh
            # is omitted. The fixture's item names already exist and this proof is offline.
            script = ("import sys,json;sys.path.insert(0,'scripts');import inbox;"
                      "inbox.refresh_names=lambda root:None;"
                      "print(json.dumps(inbox.run()))")
            output = command(root, sys.executable, "-c", script)
            outcomes = json.loads(output.splitlines()[-1])
            require(len(outcomes) == 1 and outcomes[0]["outcome"] == expected, f"Expected {expected}: {outcomes}")
            require(not git(root, "status", "--porcelain", "--untracked-files=no"), "Processor left tracked changes")
            git(root, "push", "-q", "origin", "HEAD:main")
            require(git(root, "rev-parse", "HEAD") == git(base, "--git-dir", str(remote), "rev-parse", "main"),
                    "Processed result did not reach the local remote")
            return outcomes[0]

        def passed(name: str, **details) -> None:
            results.append({"case": name, "passed": True, **details})
            print(f"PASS {name}", flush=True)

        original = (root / PAGE).read_text()
        version = git(root, "hash-object", PAGE)[:12]
        edited = re.sub(r"^updated: .*$", f"updated: {stamp.date().isoformat()}", original, count=1, flags=re.M)
        edited = re.sub(r"^summary: (.*)$", r"summary: \1 Source links are included.", edited, count=1, flags=re.M)
        fields = {"kind": "page", "path": PAGE, "version": version,
                  "message": "Addons: source-link wording clarified", "page": edited}
        received = submit(fields)
        require(received["status"] == 202, f"Valid page refused: {received['reply']}")
        outcome = process("applied")
        require((root / PAGE).read_text() == edited, "Applied page differs from the submission")
        backups = root / "archive/more/addons"
        require(any(p.read_text() == original for p in backups.glob("*.md")), "Previous page was not archived")
        current_version = git(root, "hash-object", PAGE)[:12]
        require(f"version `{current_version}`" in (root / "feed/guides.md").read_text(), "Feed version did not advance")
        passed("valid page applied, archived, rebuilt and pushed", submission=outcome["id"])

        received = submit(fields)
        require(received["status"] == 202, "Stale page should reach the processor")
        outcome = process("held")
        require("changed since it was read" in outcome["detail"], "Stale edit was held for an unexpected reason")
        require((root / PAGE).read_text() == edited, "Stale edit overwrote the page")
        passed("stale version held without overwriting the page")

        # A rendering-equivalent whitespace change still changes the protected cheatsheet.
        protected = edited.replace("\n- **Addons show", "\n\n- **Addons show", 1)
        require(protected != edited, "The protected-section fixture needs refreshing")
        received = submit({**fields, "version": current_version, "page": protected})
        require(received["status"] == 202, "Protected edit refused by receiver")
        outcome = process("review")
        require("cheatsheet changed" in outcome["detail"], "Protected change was not sent to review")
        require((root / PAGE).read_text() == edited, "Protected edit reached main without review")
        require(git(root, "show", f"{outcome['branch']}:{PAGE}") == protected.strip(), "Review branch lost the edit")
        passed("cheatsheet change isolated on a review branch")

        raw = b"TazdingoInboxProof = { localOnly = true }\n"
        received = submit({"kind": "lua"}, ("InboxProof.lua", raw))
        require(received["status"] == 202, "Addon file refused")
        process("applied")
        require(any(p.read_bytes() == raw for p in (root / "data/captures/forever/inboxproof").glob("*.lua")),
                "Original addon bytes were changed")
        require("inboxproof" in (root / "feed/index.md").read_text(), "Addon is missing from the feed map")
        passed("addon original retained byte for byte and listed in the feed")

        # A historical Beta file is used solely inside this disposable proof repository.
        # No scan, market, content or generated output here is ever sent to the real repository.
        sys.path.insert(0, str(ROOT / "scripts"))
        import market_store
        fixture = root / "data/captures/forever-beta/FOREVER_BETA_Auctionator_2026-10-17.lua"
        market = next(iter(market_store.read_all_markets(fixture)["markets"]))
        scans_before = set((root / "data/market").glob("*/scans/*.json"))
        received = submit({"kind": "lua", "market": market}, ("Auctionator.lua", fixture.read_bytes()))
        require(received["status"] == 202, "Auctionator fixture refused")
        process("applied")
        new_scans = set((root / "data/market").glob("*/scans/*.json")) - scans_before
        require(bool(new_scans), "Auctionator produced no new scan records")
        require(any(p.read_bytes() == fixture.read_bytes() for p in (root / "data/captures/forever/auctionator").glob("*.lua")),
                "Original Auctionator bytes were changed")
        require(all(len(list((root / "dist/prices" / p.parents[1].name).rglob("index.html"))) > 10 for p in new_scans),
                "The imported market's item pages were not generated")
        passed("Auctionator fixture ingested, retained and built into item pages")

        before = git(root, "rev-parse", "HEAD")
        refused = submit({**fields, "key": "wrong-key"})
        require(refused["status"] == 403 and not refused["files"], "Wrong key reached GitHub")
        passed("wrong key refused before any GitHub write")
        refused = submit({**fields, "page": edited + f"\n{KEY}\n"})
        require(refused["status"] == 400 and not refused["files"], "Pasted key reached GitHub")
        require(git(root, "rev-parse", "HEAD") == before, "Refusals changed the repository")
        passed("pasted key refused before any GitHub write")

        print(json.dumps({"scope": "isolated-local", "passed": len(results), "cases": results,
                          "limits": ["GitHub HTTP and D1 use test adapters", "Review branches, not hosted pull requests",
                                     "No hosted receiver, Actions, credentials or browser proof", "Optional item-name refresh omitted"]}, indent=2))


if __name__ == "__main__":
    main()
