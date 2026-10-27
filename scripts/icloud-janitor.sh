#!/usr/bin/env bash
# icloud-janitor.sh — find iCloud's "bounced" copies ("name 2.md", "name 3.webp")
# anywhere in the repo and remove the ones that are byte-identical to their
# original. iCloud resolves sync conflicts by keeping both versions and renaming
# one; on 27 October it made about 240 such copies of freshly written content
# and art, and the build refuses unknown pages like "content/professions/alchemy 2.md",
# which would stop a scan import. Adapted from the Brew repo's script of the
# same name, widened to sources because an identical copy is safe to delete
# wherever it is.
#
# A copy that differs from its original, or has no original, is only listed:
# a person decides which version to keep.
#
# Dry-run by default. Pass --delete to remove the identical copies.

set -euo pipefail

DELETE=0
[[ "${1:-}" == "--delete" ]] && DELETE=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

identical=()
review=()
while IFS= read -r -d '' copy; do
  name="$(basename "$copy")"
  # "alchemy 2.md" → "alchemy.md"; "screens 2" → "screens"
  original="$(dirname "$copy")/$(sed -E 's/ [2-9](\.[^.]+)?$/\1/' <<<"$name")"
  if [[ -f "$copy" && -f "$original" ]] && cmp -s "$copy" "$original"; then
    identical+=("$copy")
  elif [[ -d "$copy" && -d "$original" ]] && diff -rq "$copy" "$original" >/dev/null 2>&1; then
    identical+=("$copy")
  else
    review+=("$copy")
  fi
done < <(find "$REPO_ROOT" \( -name .git -o -name '*.nosync' -o -name node_modules \) -prune \
  -o \( -name '* [2-9].*' -o -name '* [2-9]' \) -print0 2>/dev/null)

if [[ ${#identical[@]} -eq 0 && ${#review[@]} -eq 0 ]]; then
  echo "[icloud-janitor] clean — no bounced copies found"
  exit 0
fi

if [[ ${#review[@]} -gt 0 ]]; then
  echo "[icloud-janitor] ${#review[@]} copy/copies differ from the original or have none; compare and keep the right one by hand:"
  for p in "${review[@]}"; do echo "  ${p#$REPO_ROOT/}"; done
fi

if [[ ${#identical[@]} -gt 0 ]]; then
  echo "[icloud-janitor] ${#identical[@]} identical copy/copies:"
  for p in "${identical[@]}"; do echo "  ${p#$REPO_ROOT/}"; done
  if [[ $DELETE -eq 1 ]]; then
    for p in "${identical[@]}"; do rm -rf "$p"; done
    echo "[icloud-janitor] deleted ${#identical[@]} identical copy/copies"
  else
    echo "[icloud-janitor] dry-run — re-run with --delete to remove them"
  fi
fi
