"""File what arrives in inbox/: guide pages and addon files sent through the hidden form.

    python3 scripts/inbox.py           process the waiting submissions and commit (no push)
    python3 scripts/inbox.py --push    ... and push; GitHub Actions runs this (inbox.yml)

The inbox Site (inbox-site/) checks the key, removes it and commits each submission as
inbox/<id>/submission.json plus page.md or the addon's <Name>.lua. Everything else is decided
here, one submission at a time, oldest first, each with its own rollback:

- a page must be a known page, read at its current version, in the page format, and pass the
  provenance and change rules (scripts/provenance.py). It's applied, archived and published;
  or, if it needs the owner's eye (Live, a new recommendation, an outdated finding, a new site),
  sent as a pull request instead.
- an addon file is always kept (scripts/originals.py); Auctionator's is filed as a scan.
- anything that fails is moved to inbox/held/<id>/ with reason.txt. The workflow fails after
  pushing, so GitHub emails the owner.

The full tests, build and site check run before anything is committed. If main moved while this
ran, it starts again from the new main rather than rebasing, so a stale page can't slip through
and what's pushed is what was tested.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import build
import feed
import ingest
import originals
import provenance
from auctionator import InvalidCapture

ROOT = Path(__file__).resolve().parents[1]
INBOX = Path("inbox")
HELD = INBOX / "held"
FORMAT = 1
MAX_PAGE = 300_000
MAX_LUA = 25 * 1024 * 1024
LUA_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,60}\.lua")
TOP_LEVEL = re.compile(rb"^([A-Za-z_][A-Za-z0-9_]*)\s*=", re.M)
ID = re.compile(r"[0-9]{8}T[0-9]{6}Z-[a-z0-9]{6,12}")
# Addons whose files can be checked against their name: the tables only that addon writes.
KNOWN_TABLES = {"auctionator": b"AUCTIONATOR_PRICE_DATABASE"}
ENVIRONMENT = "forever"


class Held(Exception):
    """The submission can't be applied; the message says why, for the submitter."""


def git(root: Path, *args: str, check: bool = True) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=check).stdout.strip()


def waiting(root: Path) -> list[Path]:
    folders = [p for p in (root / INBOX).iterdir() if p.is_dir() and p.name != "held"] if (root / INBOX).is_dir() else []

    def order(folder: Path):
        try:
            return json.loads((folder / "submission.json").read_text())["received"], folder.name
        except (OSError, ValueError, KeyError, TypeError):
            return "", folder.name
    return sorted(folders, key=order)


def read_submission(folder: Path) -> dict:
    try:
        sub = json.loads((folder / "submission.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise Held(f"submission.json is missing or unreadable ({error})")
    if not isinstance(sub, dict) or sub.get("format") != FORMAT:
        raise Held(f"submission.json must be format {FORMAT}")
    if not ID.fullmatch(str(sub.get("id", ""))) or sub["id"] != folder.name:
        raise Held("the submission's id doesn't match its folder")
    if sub.get("kind") not in ("page", "lua"):
        raise Held("kind must be 'page' or 'lua'")
    try:
        datetime.fromisoformat(str(sub.get("received", "")).replace("Z", "+00:00"))
    except ValueError:
        raise Held("received must be a UTC time")
    if not isinstance(sub.get("key_label"), str) or not sub["key_label"]:
        raise Held("the submission has no key label")
    files = sorted(p.name for p in folder.iterdir() if p.name != "submission.json")
    if files != [sub.get("file")]:
        raise Held(f"the submission must hold exactly one file, named in submission.json (found: {', '.join(files) or 'none'})")
    return sub


def run_checks(root: Path) -> None:
    """The same checks GitHub runs before publishing; the first failure holds the submission."""
    for step, command in (("tests", ["-m", "unittest", "discover", "-s", "tests"]),
                          ("build", ["scripts/build.py", "--base-path", "/Tazdingo/"]),
                          ("site check", ["scripts/check_site.py"])):
        done = subprocess.run([sys.executable, *command], cwd=root, capture_output=True, text=True)
        if done.returncode:
            tail = "\n".join((done.stdout + done.stderr).strip().splitlines()[-12:])
            raise Held(f"the site's {step} failed with this change:\n{tail}")


def known_domains(root: Path) -> set[str]:
    return set().union(*(provenance.domains_in(p.read_text(encoding="utf-8")) for p in (root / "content").rglob("*.md")))


def item_ids(root: Path) -> set[int]:
    ids = set()
    for name, key in (("data/items.json", "names"), ("data/foreverdb-api.json", "items")):
        path = root / name
        if path.exists():
            ids |= {int(k) for k in json.loads(path.read_text()).get(key, {}) if str(k).isdigit()}
    return ids


def page_change(root: Path, sub: dict, folder: Path) -> tuple[Path, str, list[str]]:
    """Validate a page submission; returns (target, text, review reasons)."""
    path = str(sub.get("path", ""))
    game = json.loads((root / "data/game.json").read_text())
    key = path.removeprefix("content/").removesuffix(".md")
    if not path.startswith("content/") or not path.endswith(".md") or key not in build.content_places(game):
        raise Held(f"{path!r} isn't a page the site knows; see feed/guides.md for every page's path")
    raw = (folder / sub["file"]).read_bytes()
    if len(raw) > MAX_PAGE:
        raise Held("the page is too long")
    try:
        text = raw.decode("utf-8").replace("\r\n", "\n").strip() + "\n"
    except UnicodeDecodeError:
        raise Held("the page must be UTF-8 text")
    target = root / path
    current = target.read_text(encoding="utf-8") if target.exists() else None
    version = str(sub.get("version", "")).strip().lower()
    expected = feed.blob_id(target) if target.exists() else "new"
    if len(version) < 7 or not expected.startswith(version):
        raise Held(f"{path} changed since it was read (or no version was given): read it again from the repository, "
                   f"make the change on the current version and submit that, quoting its version from feed/guides.md")
    try:
        meta, body = build.front_matter(text, path)
        build.check_sections(path, key, body)
        old_meta, old_body = build.front_matter(current, path) if current else ({}, None)
    except ValueError as error:
        raise Held(str(error))
    problems, review = provenance.check(old_body, body, meta, old_meta, known_domains(root), item_ids(root),
                                        datetime.now(timezone.utc).date())
    problems += provenance.message_problems(str(sub.get("message", "")))
    if build.PRIVATE.search(text):
        problems.append("the page can't name anyone or mention the assistant")
    if text == current:
        problems.append("the page is unchanged")
    if problems:
        raise Held("; ".join(problems))
    return target, text, review


def identify_lua(sub: dict, folder: Path) -> tuple[str, bytes]:
    """Check an addon file is what its name says; returns (addon slug, contents)."""
    name = str(sub.get("file", ""))
    if not LUA_NAME.fullmatch(name):
        raise Held("the file must be an addon's saved-variables file, named after the addon (e.g. AllTheThings.lua)")
    raw = (folder / name).read_bytes()
    if len(raw) > MAX_LUA:
        raise Held(f"the file is over {MAX_LUA // 1024 // 1024} MB")
    if b"\0" in raw[:4096] or not TOP_LEVEL.search(raw[:65536]):
        raise Held("this isn't a saved-variables file: it should start with 'SomeAddonData = {'")
    addon = originals.addon_slug(name)
    for known, table in KNOWN_TABLES.items():
        if (addon == known) != (re.search(rb"^" + table + rb"\s*=", raw, re.M) is not None):
            raise Held(f"{name} doesn't match its contents: {table.decode()} is {known.title()}'s, and only its file has it")
    return addon, raw


def received_at(sub: dict) -> int:
    return int(datetime.fromisoformat(sub["received"].replace("Z", "+00:00")).timestamp())


def rollback(root: Path, base: str) -> None:
    git(root, "reset", "-q", "--hard", base)
    git(root, "clean", "-q", "-fd", "--", "content", "data", "feed", "archive")


def commit(root: Path, message: str, *paths: str) -> bool:
    git(root, "add", "-A", "--", *paths)
    if not git(root, "diff", "--cached", "--name-only"):
        return False
    git(root, "commit", "-q", "-m", message)
    return True


def hold(root: Path, folder: Path, sub_id: str, reason: str) -> None:
    target = root / HELD / folder.name
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(folder), target)
    (target / "reason.txt").write_text(reason.strip() + "\n", encoding="utf-8")
    commit(root, f"Inbox: hold {sub_id}", str(INBOX))


def apply_page(root: Path, sub: dict, folder: Path, base: str, push: bool) -> dict:
    target, text, review = page_change(root, sub, folder)
    message = sub["message"].strip()
    trailer = f"\n\nSubmitted through the inbox ({sub['key_label']}, {sub['id']})."
    if review:
        return send_for_review(root, sub, folder, target, text, review, base, push)
    target.write_text(text, encoding="utf-8")
    shutil.rmtree(folder)
    run_checks(root)  # rebuilds feed/ with the page's new version
    commit(root, message + trailer, "content", "feed", str(INBOX))
    archive = subprocess.run([sys.executable, "scripts/archive.py", "--before", base, "--after", "HEAD"], cwd=root,
                             capture_output=True, text=True)
    if archive.returncode:
        raise Held(f"the page change couldn't be archived: {archive.stderr.strip()[-300:]}")
    commit(root, f"Archive page changes up to {git(root, 'rev-parse', '--short', 'HEAD')}", "archive")
    return {"outcome": "applied", "detail": f"{sub['path']} updated"}


def send_for_review(root: Path, sub: dict, folder: Path, target: Path, text: str, review: list[str], base: str, push: bool) -> dict:
    """Put the change on its own branch with a pull request, then take it out of the inbox."""
    branch = f"review/{sub['id']}"
    here = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    git(root, "switch", "-q", "-C", branch, base)
    try:
        target.write_text(text, encoding="utf-8")
        run_checks(root)
        commit(root, sub["message"].strip() + f"\n\nSubmitted through the inbox ({sub['key_label']}, {sub['id']}).", "content", "feed")
        if push:
            git(root, "push", "-q", "--force", "origin", branch)
            existing = subprocess.run(["gh", "pr", "list", "--head", branch, "--json", "number", "--jq", ".[].number"],
                                      cwd=root, capture_output=True, text=True, check=True).stdout.strip()
            if not existing:  # a run started again after a push conflict finds its pull request already open
                body = ("A submission from the inbox that needs your eye before it goes live:\n\n"
                        + "\n".join(f"- {r}" for r in review)
                        + f"\n\nKey: {sub['key_label']}. Submission {sub['id']}. Every check passed on this branch; "
                          "merge to publish it, or close it to drop it.")
                subprocess.run(["gh", "pr", "create", "--base", "main", "--head", branch, "--title", sub["message"].strip(),
                                "--body", body], cwd=root, check=True, capture_output=True, text=True)
    finally:
        git(root, "switch", "-q", "-f", here)
    shutil.rmtree(folder)
    commit(root, f"Inbox: {sub['id']} sent for review", str(INBOX))
    return {"outcome": "review", "branch": branch, "detail": f"{sub['path']}: pull request from {branch} ({'; '.join(review)})"}


def refresh_names(root: Path) -> None:
    """New items get their names, as on the Mac; without ForeverDB they show their ID until the next refresh."""
    subprocess.run([sys.executable, "scripts/item_names.py"], cwd=root, capture_output=True)


def apply_lua(root: Path, sub: dict, folder: Path) -> dict:
    addon, _raw = identify_lua(sub, folder)
    source = folder / sub["file"]
    if addon == "auctionator":
        registry = json.loads((root / "data/captures.json").read_text())
        if sub.get("market") is not None and (not isinstance(sub["market"], str) or not 0 < len(sub["market"]) <= 80):
            raise Held("market must be a realm and faction, e.g. 'Realm Horde'")
        markets = [sub["market"]] if sub.get("market") else registry.get("default_markets", {}).get(ENVIRONMENT, [])
        if not markets:
            raise Held("say which market this scan is for (its realm and faction, e.g. 'Realm Horde') in the market field")
        try:
            result = ingest.ingest(source, ENVIRONMENT, markets, root=root)
        except (InvalidCapture, SystemExit) as error:
            raise Held(f"the Auctionator file couldn't be read: {error}")
        if result:
            refresh_names(root)
        stamp = result["original"][2] if result else received_at(sub)
        kept = originals.keep(root, source, ENVIRONMENT, addon, stamp)
        detail = (f"scan of {result['scanned']} filed ({', '.join(f'{m}: {n:,} items' for m, n in result['items'].items())})"
                  if result else "nothing new since the last scan; the file is kept")
        message = f"Auction House scan of {result['scanned']}" if result else f"Keep an Auctionator file of {datetime.fromtimestamp(stamp, timezone.utc):%Y-%m-%d %H:%M} UTC"
    else:
        kept = originals.keep(root, source, ENVIRONMENT, addon, received_at(sub))
        detail = f"stored as {kept.relative_to(root).as_posix()}; no processor for {sub['file']} yet"
        message = f"Keep {sub['file'].removesuffix('.lua')} saved variables of {datetime.fromtimestamp(received_at(sub), timezone.utc):%Y-%m-%d}"
    shutil.rmtree(folder)
    run_checks(root)
    commit(root, message + f"\n\nSubmitted through the inbox ({sub['key_label']}, {sub['id']}).", "data", "feed", str(INBOX))
    return {"outcome": "applied", "detail": detail}


def process_all(root: Path, push: bool) -> list[dict]:
    outcomes = []
    for folder in waiting(root):
        base = git(root, "rev-parse", "HEAD")
        sub_id = folder.name
        try:
            sub = read_submission(folder)
            outcome = apply_page(root, sub, folder, base, push) if sub["kind"] == "page" else apply_lua(root, sub, folder)
        except Held as reason:
            rollback(root, base)
            hold(root, root / INBOX / sub_id, sub_id, str(reason))
            outcome = {"outcome": "held", "detail": str(reason)}
        except Exception as error:  # anything unforeseen holds this one and the rest still run
            rollback(root, base)
            reason = f"the inbox couldn't process this ({type(error).__name__}: {error}); it needs a look"
            hold(root, root / INBOX / sub_id, sub_id, reason)
            outcome = {"outcome": "held", "detail": reason}
        outcomes.append({"id": sub_id, **outcome})
    return outcomes


def run(root: Path = ROOT, push: bool = False) -> list[dict]:
    """Process everything waiting; with push, push and, if main moved meanwhile, start again from it."""
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise SystemExit("The checkout has uncommitted changes; the inbox resets and commits, so it only runs on a clean one.")
    for _attempt in range(3):
        outcomes = process_all(root, push)
        if not push or not outcomes:
            return outcomes
        if subprocess.run(["git", "push", "-q", "origin", "HEAD:main"], cwd=root).returncode == 0:
            return outcomes
        git(root, "fetch", "-q", "origin", "main")
        if subprocess.run(["git", "merge-base", "--is-ancestor", "HEAD", "origin/main"], cwd=root).returncode == 0:
            return outcomes  # the push landed, only its acknowledgement was lost
        withdraw_reviews(root, outcomes)  # the redo decides afresh; a stale pull request mustn't stay open
        git(root, "reset", "-q", "--hard", "origin/main")
    raise SystemExit("Couldn't push the inbox's results after three attempts; the submissions are still waiting.")


def withdraw_reviews(root: Path, outcomes: list[dict]) -> None:
    for outcome in outcomes:
        if outcome["outcome"] == "review" and outcome.get("branch"):
            subprocess.run(["gh", "pr", "close", outcome["branch"], "--delete-branch", "--comment",
                            "Withdrawn: main moved while this was being filed; the inbox is checking it again."],
                           cwd=root, capture_output=True)


def report(outcomes: list[dict]) -> None:
    lines = ["| Submission | Outcome | Detail |", "|---|---|---|"]
    lines += [f"| {o['id']} | {o['outcome']} | {o['detail'].replace('|', '/').replace(chr(10), ' ')} |" for o in outcomes]
    text = "## Inbox\n\n" + ("\n".join(lines) if outcomes else "Nothing waiting.") + "\n"
    print(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
            summary.write(text)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"applied={sum(o['outcome'] == 'applied' for o in outcomes)}\n")
            output.write(f"held={sum(o['outcome'] == 'held' for o in outcomes)}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="File what arrives in inbox/.")
    parser.add_argument("--push", action="store_true", help="push the results (GitHub Actions)")
    args = parser.parse_args()
    report(run(ROOT, args.push))


if __name__ == "__main__":
    main()
