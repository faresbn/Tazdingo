# WORKFLOW.md — Brew's additions to the session phases

The shared phase skills (/wf-research, /wf-plan, /wf-implement, /wf-end) define how research, plan, build and close work. This file adds what is specific to Brew.

## Session files

Each session gets a folder, `docs/sessions/YYYY-MM-DD-task-name/`, holding:
- **research.md:** the knowledge foundation. You build the plan from it; Fares checks it to confirm you understood the system before anything is decided.
- **plan.md:** your instruction set for building, laid out where Fares can see your reasoning and change it. Its checkboxes are your save state while you build.
- **revlog.md:** created when a session has outside reviews (see REVIEWER.md). It records what each consultation changed and why.

Each file is written once, for both readers. You use it to work; Fares uses it to decide, annotate and learn how the system works. Lead each item with what it means for the product, then explain the mechanism, then give the specifics.

## Milestone consultations

Before you hand Fares a plan for major work, and when a major phase of building is complete, decide whether an outside review would catch something you'd otherwise ship (REVIEWER.md → When to open a consultation). If it would, open one. Its result goes into revlog.md, and any fixes go into the plan or the code before Fares sees them. If it wouldn't, tell Fares in one line that you skipped it.

## Where the task comes from

When the task comes from a tracker (a track's PRODUCT.md, an issue, a list), note in research.md where the code disagrees with what the tracker says, and update the tracker when you close.

## Checks for "done"

plan.md states the checks for its own task. The usual ones in Brew:
- typecheck passes for every touched package: `npx tsc --noEmit`, plus `cargo check` for Rust
- builds succeed for the touched apps
- deploys use the commands in the track's own documentation (first-generation deploys: `legacy/README.md`)

When Fares calls for an explicit QA pass, re-read the code itself, end to end and adversarially, rather than trusting the diff or an earlier pass. Such passes have caught real defects that had survived a clean typecheck.

## Closing

Propose updates to AGENTS.md, WORKFLOW.md, REVIEWER.md, PRODUCT.md, the tracks' PRODUCT.md files, COMPASS.md and docs/claude/engineering-lessons.md. Lead each proposal with why it matters, then what it changes, then the text, and follow AGENTS.md → Editing these instruction files. Fares approves each one before anything is written.

## Worktrees

Worktrees live outside the repo, so **ask Fares before creating one** (AGENTS.md: ask before working outside the repo). Once he agrees, create them outside iCloud-synced folders, under `~/.claude/worktrees/brew/`: `git worktree add ~/.claude/worktrees/brew/<name> -b <branch> main`. The repository lives in `~/Documents`, which iCloud syncs. A worktree removed from there was partly restored by iCloud minutes later, as a stray folder beside the repo (2026-10-09). Remove each worktree with `git worktree remove` once its branch is merged.

## Hygiene passes

The first generation's cleanup system is retired with it; its playbooks are in the `first-gen-final` tag. Between pieces of work, keep the root clean by hand: new work goes in a track, retired work goes in `legacy/`, and session material stays in `docs/sessions/`. After installing dependencies in any track, run `bash scripts/icloud-shield.sh`; it keeps `node_modules` and build output out of iCloud for every track. `bash scripts/icloud-janitor.sh` sweeps iCloud's bounced copies, but only in the legacy LocalBrew build folders. Each track handles its own build clean-up with its own tooling.
