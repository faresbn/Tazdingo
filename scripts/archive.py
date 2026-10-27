"""Record changes to Tazdingo's pages: a backup of each page's previous version and a log line.

Run by .github/workflows/archive.yml after every push to main that touches content/. For each
commit in the push (oldest first) and each content file it changed, the version before the
change is saved to archive/<page>/<UTC time>-<commit>.md and a line is added to archive/LOG.md.
The archive is in the private repository and is never published. Git history holds the same
information; this keeps it readable for anyone (or any assistant) reading files, not git.
"""
from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_HEADER = """# Tazdingo change log

Every change to a page in `content/`, oldest first. **Backup** is the page as it was before the change
(empty for new pages). Written automatically by `.github/workflows/archive.yml`; don't edit by hand.
To restore a page, copy its backup back to `content/` and commit.

| When (UTC) | Page | Change | Commit | Message | Backup |
|---|---|---|---|---|---|
"""
KINDS = {"A": "added", "M": "edited", "D": "deleted", "R": "renamed"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


MARK = ROOT / "archive/.last-recorded"


def usable(sha: str, after: str) -> bool:
    """A start point we can count from: a real commit that `after` descends from."""
    if not sha or set(sha) == {"0"}:
        return False
    try:
        git("merge-base", "--is-ancestor", sha, after)
        return True
    except subprocess.CalledProcessError:
        return False


def commits(before: str, after: str) -> list[str]:
    """Every commit that touched content/ since the last one recorded, oldest first. Counting
    from the archive's own mark (not just this push) means a run that was skipped or failed is
    caught up by the next. Without a usable start, only `after` is recorded."""
    start = MARK.read_text().strip() if MARK.exists() else ""
    start = start if usable(start, after) else before if usable(before, after) else ""
    if start:
        return git("rev-list", "--reverse", "--first-parent", f"{start}..{after}", "--", "content").split()
    return [after] if changes(after, "--name-only").strip() else []


def changes(sha: str, *options: str) -> str:
    """Files a commit changed in content/. A merge is compared with its first parent (main as it
    was), so a merged branch is recorded once; the first commit is compared with nothing."""
    return git("diff-tree", "--no-commit-id", "-r", "-m", "--first-parent", "--root", *options, sha, "--", "content")


def cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def record(sha: str) -> list[str]:
    when_iso, subject = git("show", "-s", "--format=%cI%x1f%s", sha).strip().split("\x1f", 1)
    when = datetime.fromisoformat(when_iso).astimezone(timezone.utc)
    stamp = when.strftime("%Y%m%d-%H%M%S")
    rows = []
    parent = f"{sha}^" if len(git("rev-list", "--parents", "-n", "1", sha).split()) > 1 else None
    for line in changes(sha, "-M", "--name-status").splitlines():
        status, *paths = line.split("\t")
        kind = KINDS.get(status[0], status)
        old_path = paths[0]
        page = paths[-1]
        backup = ""
        if parent and status[0] in "MDR":
            previous = git("show", f"{parent}:{old_path}")
            target = ROOT / "archive" / Path(old_path).relative_to("content").with_suffix("") / f"{stamp}-{sha[:7]}.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(previous, encoding="utf-8")
            backup = f"[{target.relative_to(ROOT / 'archive').as_posix()}]({target.relative_to(ROOT / 'archive').as_posix()})"
        rename = f" (from `{old_path}`)" if status[0] == "R" else ""
        rows.append(f"| {when:%Y-%m-%d %H:%M} | `{page}`{rename} | {kind} | `{sha[:7]}` | {cell(subject)} | {backup} |")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    args = parser.parse_args()
    after = git("rev-parse", args.after).strip()
    log = ROOT / "archive/LOG.md"
    log.parent.mkdir(exist_ok=True)
    existing = log.read_text(encoding="utf-8") if log.exists() else LOG_HEADER
    # Idempotent: a commit already in the log isn't recorded twice.
    rows = [row for sha in commits(args.before, after) if f"`{sha[:7]}`" not in existing for row in record(sha)]
    MARK.write_text(after + "\n")
    if rows:
        log.write_text(existing + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"Recorded {len(rows)} change(s).")


if __name__ == "__main__":
    main()
