---
name: plumbline-init
description: Initialize or reassess Plumbline for a repository through a read-only audit and one approved setup proposal.
disable-model-invocation: true
---

# Initialize Plumbline

This skill is explicit only. It is the consent boundary for repository-local routing and the project-local agent team. Treat initialization as one guarded setup transaction, not as background bootstrap.

## Guard and assessment

Before inspecting files, check whether this conversation already contains unrelated active implementation work. If it does, recommend a fresh task and stop unless the user explicitly says `continue here`.

Start read-only and keep discovery targeted. Begin with repository guidance, README files, manifests, validation scripts, and only the config and paths that determine Plumbline integration. Do not dump a broad recursive file listing or start dependency installation.

Inspect enough to understand:

- `AGENTS.md`, README files, documentation routing, and canonical document ownership;
- build, validation, UAT, Git, and managed-worktree conventions;
- Codex `.codex/config.toml` and `.codex/agents/` when Codex is the host;
- Claude `.claude/agents/` and relevant project `.claude/settings.json` entries when Claude Code is the host;
- `.gitignore`, `.git/info/exclude`, and `.worktreeinclude`;
- `git worktree list --porcelain` and whether the target is a normal checkout or worktree;
- installed local skills, workflow plugins, and competing automatic controllers.

For Codex, read the global `config.toml` only to report host capability and the current model/reasoning candidate. It is not an agent source or fallback. For Claude Code, inspect project-local capability only; never read or modify global Claude settings as part of initialization. Never read, select, copy, or inherit personal/global custom-agent files. Treat an installed workflow plugin as available, not active, unless the user explicitly selected it or repository-local runtime evidence shows it owns the task. Do not modify global settings or disable another plugin during initialization.

Adopt an established repository's terminology and document structure. Do not create a parallel docs taxonomy just because Plumbline is new. For a new project, ask only for a concise product baseline: purpose, users, important behavior, priority, constraints, and non-goals.

## Required proposal

Present one reviewable proposal and wait for explicit approval before writing anything. Show the proposed agent set in a table with one row per role and these columns:

`role | why it is needed | host-native model value | reasoning/effort | sandbox/permission intent | write access`

Use the current project/main model when available; otherwise show a host model only as a candidate to approve. Do not invent a model slug or alias. Treat the table as a recommended, role-aware starting profile aimed at the cheapest effective model and reasoning/effort: lower-cost settings for bounded research or mechanical work, higher settings only for material architecture, persistence, concurrency, security, ownership, or acceptance risk. These values are adjustable and hotswappable after setup.

For Codex, recommend `features.multi_agent = true`, `agents.max_depth = 1`, and a small approved `agents.max_threads` (six is the template default). Explain that this keeps the main parent able to dispatch explicit project roles, including a selected `gpt-5.6-luna` role when Luna is not shown on the standard v2 model choice card; the feature flag keeps collaboration available, while the role's explicit `model` field selects Luna. It does not make Luna mandatory. For Claude Code, recommend project `.claude/agents/*.md` definitions with `model: inherit` unless the user approves a host-native alias/full ID, a suitable `effort`, restricted tools and `permissionMode: plan` for report-only roles, and no `Agent` tool for any generated role. Do not enable Claude's experimental Agent Teams or edit global settings.

The same proposal must name every selected change and state `Create`, `Keep`, `Patch`, or `Skip`:

- install `.agents/skills/plumbline-router/SKILL.md` from `templates/router/SKILL.md`;
- create or audit the selected project agents using the host adapter: `.codex/agents/*.toml` for Codex or `.claude/agents/*.md` for Claude Code;
- for Codex, create or patch project `.codex/config.toml` with `multi_agent`, `max_threads`, and `max_depth`;
- add or update the Plumbline section in `AGENTS.md` with delegation and no-child rules;
- add local `.git/info/exclude` entries so the host agent files and router stay untracked;
- when propagation is approved, patch the root `.gitignore` with the exact host-local ignore entries and add `.worktreeinclude` for the selected host paths; the proposal must show both changes together rather than promising to keep `.gitignore` unchanged;
- repair documentation routing only if the repository already needs it;
- identify competing controllers and offer reversible conflict actions without applying them.

Before asking for approval, run the host-specific candidate installer with `--dry-run --format json` and include its file/operation/field manifest in the proposal: `scripts/install_agent_team.py` for Codex or `scripts/install_claude_agent_team.py` for Claude Code. If a repository-local router already exists, the preview must state whether it matches the current template and whether `--replace` would be required; never overwrite it merely because it is stale. This is read-only and does not approve or apply anything.

## After approval

Apply only the approved items. Rerun the dry-run manifest; if the target changed, refresh the proposal before writing. Then rerun the host-specific installer without `--dry-run` using the approved roles, host-native model, reasoning/effort, thread cap where applicable, and explicit `--update-agents`/`--propagate` choices. Use the same dry-run/apply sequence with `scripts/install_router.py` for the approved router. For existing teams, run `--mode audit` first; it is read-only and does not need `--replace`. A normal `--mode retune` preserves existing model, reasoning/effort, sandbox/permission, custom fields, and instructions; use `--fill-missing` or the explicitly approved `--update-instructions` flag for narrow changes. `--replace` is reserved for an explicitly approved initialize replacement. Never write global or personal agent files.

Validate Plumbline setup separately from repository product checks. Report Plumbline files/config/TOML-or-Markdown/ignore/worktree validation as passed or failed; preflight repository commands for missing dependencies or executables; and label repository checks as passed, skipped, or blocked. Missing dependencies are a repository bootstrap blocker, not a Plumbline setup failure, and do not justify starting `npm ci` or another install without approval. Validate required host fields, Codex `multi_agent=true` and `max_depth=1` where applicable, AGENTS guidance, local discovery paths, ignore rules, exact changed-field output, `git diff --check`, and the `.worktreeinclude` contents. Explain that propagation affects new managed worktrees only when the host/repository workflow supports it; the `.worktreeinclude` manifest must be committed for future worktrees to see it, and existing worktrees need explicit refresh or local copy. A delegation wave must report selected role names with host-native model and reasoning/effort values in one compact line; otherwise report `Direct: <reason>` and continue on the main thread. End initialization and recommend a fresh task for feature work.

A writable parent is normal during a goal. For researcher, architect, and QA dispatches, require a report-only brief with no write set. Codex `sandbox_mode = "read-only"` and Claude `permissionMode: plan` are intent rather than proof of hard isolation when a parent is writable or permissive. If the host cannot provide hard read-only isolation when it is required, use `Direct: delegation prohibited or effective read-only isolation unavailable`.
