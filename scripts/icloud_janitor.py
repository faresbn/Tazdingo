"""Find iCloud's "bounced" copies ("name 2.md", "name 3.webp") in the repository and remove the safe ones.

iCloud resolves a sync conflict by keeping both versions and renaming one. A copy is safe to delete
when it is identical to its original, or when its exact content is already stored in git: the build
rewrites every feed file, so a copy is usually of the version before, and git keeps every version it
committed. Anything else (a copy that differs and isn't in git, or has no original) is only listed:
a person decides which to keep. Copies inside .git are listed and never touched (a copied ref can
break `git fetch`).

Python, not shell, because the Mac's update watcher runs under launchd, where macOS lets python3 and
git read ~/Documents but not bash, find or cmp. scripts/icloud-janitor.sh runs this.

Usage: python3 scripts/icloud_janitor.py [--delete]   (dry run without --delete)
"""
from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COPY = re.compile(r"^(.*) [2-9](\.[^.]+)?$")  # "alchemy 2.md" → ("alchemy", ".md"); "screens 2" → ("screens", None)
SKIP = {".git", "node_modules"}


def original_of(path: Path) -> Path | None:
    match = COPY.match(path.name)
    return path.with_name(match.group(1) + (match.group(2) or "")) if match else None


def in_git(root: Path, path: Path) -> bool:
    """Is this file's exact content stored in the repository (any commit, any path)?"""
    digest = subprocess.run(["git", "-C", str(root), "hash-object", str(path)], capture_output=True, text=True)
    return digest.returncode == 0 and subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", digest.stdout.strip()], capture_output=True).returncode == 0


def safe(root: Path, copy: Path, original: Path) -> bool:
    if copy.is_file():
        return (original.is_file() and filecmp.cmp(copy, original, shallow=False)) or in_git(root, copy)
    if copy.is_dir() and original.is_dir():
        compared = filecmp.dircmp(copy, original)
        return not (compared.left_only or compared.right_only or compared.diff_files or compared.funny_files)
    return False


def find(root: Path) -> tuple[list[Path], list[Path]]:
    """(safe to delete, for a person) under root, not descending into .git, node_modules or *.nosync."""
    deletable, review = [], []
    stack = [root]
    while stack:
        folder = stack.pop()
        for entry in sorted(folder.iterdir()):
            if entry.name in SKIP or entry.name.endswith(".nosync") or entry.is_symlink():
                continue
            original = original_of(entry)
            if original is not None:
                (deletable if safe(root, entry, original) else review).append(entry)
            elif entry.is_dir():
                stack.append(entry)
    git_dir = root / ".git"
    if git_dir.is_dir():
        review += [p for p in sorted(git_dir.rglob("*")) if original_of(p) is not None]
    return deletable, review


def main(root: Path = ROOT, delete: bool = False) -> int:
    deletable, review = find(root)
    if not deletable and not review:
        print("[icloud-janitor] clean — no bounced copies found")
        return 0
    if review:
        print(f"[icloud-janitor] {len(review)} copy/copies differ from the original or have none; compare and keep the right one by hand:")
        print("\n".join(f"  {p.relative_to(root)}" for p in review))
    if deletable:
        print(f"[icloud-janitor] {len(deletable)} copy/copies identical to the original or to a version in git:")
        print("\n".join(f"  {p.relative_to(root)}" for p in deletable))
        if delete:
            for p in deletable:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
            print(f"[icloud-janitor] deleted {len(deletable)} identical copy/copies")
        else:
            print("[icloud-janitor] dry-run — re-run with --delete to remove them")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--delete", action="store_true", help="remove the safe copies (default: only list)")
    raise SystemExit(main(delete=parser.parse_args().delete))
