"""Original saved-variables files, kept in the public repository as they arrived.

Every addon's file (Auctionator.lua, AllTheThings.lua, ...) is game data, published by decision
(30 October 2026). Each is kept at data/captures/<environment>/<addon>/<time UTC>.lua, never
edited. The website never serves a .lua (build.py refuses one); processors turn some of them into
prices and the feed.
"""
from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ORIGINALS = Path("data/captures")


def addon_slug(name: str) -> str:
    """'AllTheThings.lua' or 'AllTheThings' → 'allthethings'."""
    stem = name[:-4] if name.lower().endswith(".lua") else name
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    if not slug:
        raise ValueError(f"{name!r} isn't an addon's file name")
    return slug


def original_path(root: Path, environment: str, addon: str, timestamp: int) -> Path:
    moment = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    return root / ORIGINALS / environment / addon_slug(addon) / f"{moment}.lua"


def keep(root: Path, source: Path, environment: str, addon: str, timestamp: int) -> Path:
    """Copy `source` into the repository; a second, different file for the same minute gets a
    numbered name, and the same file twice is kept once."""
    target = original_path(root, environment, addon, timestamp)
    body = source.read_bytes()
    n = 1
    while target.exists():
        if target.read_bytes() == body:
            return target
        n += 1
        target = target.with_name(f"{target.stem.split('-v')[0]}-v{n}.lua")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target
