#!/usr/bin/env bash
# icloud-shield.sh — keep regenerable output out of iCloud Drive sync.
#
# The repo lives in ~/Documents (iCloud-synced). Every build deletes and rewrites
# dist/ (72 pages and their assets) in about a second; iCloud's sync daemon
# races it and leaves "bounced" conflict copies ("file 2.ext", Apple TN2336).
# This moves each regenerable directory out of iCloud's view with the standard
# pattern: `dir` → `dir.nosync` + a relative symlink (iCloud skips anything
# named *.nosync; the symlink is per-machine, which is correct). Adapted from
# the Brew repo's script of the same name.
#
# Safety:
#   - macOS only; exits 0 silently elsewhere (GitHub Actions is never affected).
#   - Only acts when the repo is inside an iCloud-synced area.
#   - Idempotent: re-runs repair links that a clean-up or sync event broke.
#   - Never touches sources: only the fixed list of regenerable directories below.
#
# Usage: bash scripts/icloud-shield.sh [--quiet]

set -euo pipefail

QUIET=0
for arg in "$@"; do
  case "$arg" in
    --quiet) QUIET=1 ;;
    *) echo "[icloud-shield] unknown arg: $arg" >&2; exit 2 ;;
  esac
done
log() { [[ $QUIET -eq 1 ]] || echo "[icloud-shield] $*"; }

[[ "$(uname)" == "Darwin" ]] || exit 0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

case "$REPO_ROOT" in
  "$HOME/Documents/"* | "$HOME/Desktop/"* | "$HOME/Library/Mobile Documents/"*) ;;
  *) log "repo not under an iCloud-synced path — nothing to do"; exit 0 ;;
esac

# States handled: real dir (convert) · healthy link (no-op) · dangling link
# (repair or drop) · real dir AND stale .nosync sibling (the fresh dir wins) ·
# .nosync only (relink).
shield_dir() {
  local dir="$1"
  local nosync="${dir}.nosync"
  local link_target
  link_target="$(basename "$nosync")"

  if [[ -L "$dir" ]]; then
    if [[ -e "$dir" ]]; then
      return 0 # healthy
    fi
    rm "$dir"
    if [[ -d "$nosync" ]]; then
      ln -s "$link_target" "$dir"
      log "repaired dangling link: ${dir#$REPO_ROOT/}"
    else
      log "dropped dangling link (no target): ${dir#$REPO_ROOT/}"
    fi
    return 0
  fi

  if [[ -d "$dir" ]]; then
    if [[ -d "$nosync" ]]; then
      rm -rf "$nosync"
    fi
    mv "$dir" "$nosync"
    ln -s "$link_target" "$dir"
    log "shielded: ${dir#$REPO_ROOT/}"
    return 0
  fi

  if [[ -d "$nosync" && ! -e "$dir" ]]; then
    ln -s "$link_target" "$dir"
    log "relinked: ${dir#$REPO_ROOT/}"
  fi
}

# Regenerable only: the built site, the preview folder, the Blizzard-posts
# cache and Python's bytecode. scripts/build.py follows the dist link.
TARGETS=(
  "$REPO_ROOT/dist"
  "$REPO_ROOT/tmp"
  "$REPO_ROOT/.cache"
  "$REPO_ROOT/scripts/__pycache__"
  "$REPO_ROOT/tests/__pycache__"
)

for t in "${TARGETS[@]}"; do
  # Create the target first, so a folder made later by a build is already shielded.
  [[ -e "$t" || -L "$t" ]] || mkdir -p "${t}.nosync"
  shield_dir "$t"
done

log "done"
