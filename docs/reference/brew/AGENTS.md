# Brew — agent instructions

This is AGENTS.md. Claude Code reads it as well, through CLAUDE.md, which is a symlink to this file. It stays short on purpose: it holds what is true for every task in Brew and points to the document that covers each kind of work. Open a linked document when the task calls for it.

Brew is Fares's private workbench; products leave it under their own names. What is being built, and why, is in PRODUCT.md. Each track lives in its own folder under `tracks/`, with its own PRODUCT.md. The retired first generation is in `legacy/`.

## Sessions and checkpoints

Sessions use the shared phase skills: /wf-research, /wf-plan, /wf-implement and /wf-end in Claude Code, and $wf-research and the rest in Codex. WORKFLOW.md adds what is specific to Brew.

When a session goes through research and planning, two checkpoints need Fares's approval before you go further: research.md before you plan, and plan.md before you build. Get each document to a finished, reviewable state, then stop for his review. Also stop before anything destructive or outward-facing (deleting data, deploying, publishing, sending messages) unless the approved plan already covers it. **Exporting a product to its own public repository is the exception:** it needs Fares's explicit instruction at that moment, even if a plan mentions it. Until then all work stays inside Brew. **Ask Fares before working outside the Brew repo, even in Auto Mode** (other folders, `/tmp`, `~/Library`, `/Applications`, worktrees). He doesn't want access blocked, he wants to be asked. Build output stays inside the repo, gitignored; tools may keep their own caches elsewhere. Tell subagents the same, and have them use absolute paths, because a subagent's shell starts in the main checkout. Version control (branches, commits, pushes, merging finished work into main) and outside-review consultations within REVIEWER.md's budget are part of the job, not approval points. Everywhere else, make reversible in-scope decisions yourself, note them, and keep going.

## Evidence

If a claim can't be grounded in the code, a tool result or a primary source, say so and name what would verify it. When the detail is the decision (version pins, flags, schema fields, security boundaries), read the actual source; a summary is a pointer, not evidence.

## Where to look

| When you are… | Read |
|---|---|
| Running a session phase | The phase skill, plus WORKFLOW.md for Brew's additions |
| Making or questioning a product decision | PRODUCT.md, then the track's own `tracks/<track>/PRODUCT.md`. Their settled decisions are listed; flag it before you reopen one. |
| Working inside one track | That track's `PRODUCT.md`. Keep the track self-contained: it becomes its own repository, so don't import from other tracks or from `legacy/`; copy what you salvage. |
| Working on one portfolio app (mlx-bar, Reicon, WCL Exporter) | That app's own `tracks/portfolio/<app>/PRODUCT.md`: its status, decisions, next steps and how to build and test it. Each app is self-contained like a track. |
| Shaping a proposal to fit how Fares decides | COMPASS.md |
| Opening a consultation: stuck, holding a doubt no tool can settle, or at a milestone | REVIEWER.md. Reviewing someone else's work? Your rules are in the packet you received. |
| Reading or salvaging first-generation code | `legacy/README.md`. The old per-app reference docs, Supabase rules included, are in the `first-gen-final` tag (`git show first-gen-final:docs/claude/<file>`). |
| Debugging integrations, provider calls, database writes or builds | docs/claude/engineering-lessons.md |

## Images

When the work needs a graphic, generate it with OpenAI's Images API. Use `gpt-image-2.5-flare` by default. Use `gpt-image-2.5-sunburst` when editing an existing image whose composition must stay intact. Save drafts in the session folder; nothing goes into the product until Fares approves it.

## Keys

Outside reviews run on Fares's subscriptions: Codex on the ChatGPT plan, Claude on the Claude subscription. `LOCALBREW_OPENAI_KEY` is for images and is the Codex fallback; `LOCALBREW_CLAUDE_KEY` is the Claude fallback. Both are used only when a subscription is unavailable or at its limit (REVIEWER.md → Commands). `SUPABASE_ACCESS_TOKEN`, `VERCEL_ACCESS_TOKEN` and `GITHUB_ACCESS_TOKEN` are for operations. Pass keys inline to the command that needs them and never print their values.

## Editing these instruction files

Each line should be something a model would get wrong without it. State the rule plainly, with its reason. Name the scope it applies to: current models apply rules literally and don't extend them to cases you didn't mention. Put task-specific material in that task's document and link it from the table above. Propose changes when closing a session; Fares approves them.
