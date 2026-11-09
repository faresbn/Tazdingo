#!/usr/bin/env bash
# icloud-janitor.sh — remove iCloud's "name 2.ext" copies that are identical to their original or to a
# version in git, and list the rest. The work is in scripts/icloud_janitor.py (see why there).
# Dry-run by default; pass --delete to remove them.
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/icloud_janitor.py" "$@"
