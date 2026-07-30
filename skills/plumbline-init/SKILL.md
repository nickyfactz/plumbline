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
- `.codex/config.toml`, `.codex/agents/`, `.gitignore`, `.git/info/exclude`, and `.worktreeinclude`;
- `git worktree list --porcelain` and whether the target is a normal checkout or worktree;
- installed local skills, workflow plugins, and competing automatic controllers.

Read the global Codex `config.toml` only to report host capability and the current model/reasoning candidate. It is not an agent source or fallback. Never read, select, copy, or inherit personal/global custom-agent files. Project-local `.codex/config.toml` and `.codex/agents/` are the only team configuration considered. Treat an installed workflow plugin as available, not active, unless the user explicitly selected it or repository-local runtime evidence shows it owns the task. Do not modify global settings or disable another plugin during initialization.

Adopt an established repository's terminology and document structure. Do not create a parallel docs taxonomy just because Plumbline is new. For a new project, ask only for a concise product baseline: purpose, users, important behavior, priority, constraints, and non-goals.

## Required proposal

Present one reviewable proposal and wait for explicit approval before writing anything. Show the proposed agent set in a table with one row per role and these columns:

`role | why it is needed | model slug | reasoning effort | sandbox | write access`

Use the current project/main model when available; otherwise show the global model only as a candidate to approve. Do not invent a model slug. The approved model and reasoning values become explicit fields in every generated TOML, rather than an implicit global fallback. Recommend `max_depth = 1`, `multi_agent = true`, and a small approved `max_threads` (six is the template default). Explain that workers never spawn children.

The same proposal must name every selected change:

- install `.agents/skills/plumbline-router/SKILL.md` from `templates/router/SKILL.md`;
- create or audit the selected project agents under `.codex/agents/`;
- create or patch project `.codex/config.toml` with `multi_agent`, `max_threads`, and `max_depth`;
- add or update the Plumbline section in `AGENTS.md` with delegation and no-child rules;
- add local `.git/info/exclude` entries so the agent/config/router files stay untracked;
- when propagation is approved, patch the root `.gitignore` with the exact local Plumbline ignore entries and add `.worktreeinclude`; the proposal must show both changes together rather than promising to keep `.gitignore` unchanged;
- repair documentation routing only if the repository already needs it;
- identify competing controllers and offer reversible conflict actions without applying them.

State whether each item is `Create`, `Keep`, `Patch`, or `Skip`, and show the exact model, reasoning, sandbox, config, ignore, and propagation values. Do not treat missing global agents as a reason to create or select them.

Before asking for approval, run the candidate installer commands with `--dry-run --format json` and include their file/operation/field manifest in the proposal. If a repository-local router already exists, the preview must state whether it matches the current template and whether `--replace` would be required; never overwrite it merely because it is stale. This is read-only and does not approve or apply anything.

## After approval

Apply only the approved items. Rerun the dry-run manifest after approval; if the target changed, refresh the proposal before writing. Then rerun `scripts/install_agent_team.py` without `--dry-run` using the approved roles, model, reasoning, thread cap, and explicit `--update-agents`/`--propagate` choices. Use the same dry-run/apply sequence with `scripts/install_router.py` for the approved router. For existing teams, run `--mode audit` first; it is read-only and does not need `--replace`. A normal `--mode retune` preserves existing model, reasoning, sandbox, custom fields, and instructions; use `--fill-missing` or the explicitly approved `--update-instructions` flag for narrow changes. `--replace` is reserved for an explicitly approved initialize replacement. The helper refuses a differing project config unless the approved command includes `--replace-config`. Never write global or personal agent files.

Validate Plumbline setup separately from repository product checks. Report Plumbline files/config/TOML/ignore/worktree validation as passed or failed; preflight repository commands for missing dependencies or executables; and label repository checks as passed, skipped, or blocked. Missing dependencies are a repository bootstrap blocker, not a Plumbline setup failure, and do not justify starting `npm ci` or another install without approval. Validate required model/reasoning/sandbox/no-child fields, `multi_agent=true`, `max_depth=1`, AGENTS guidance, local discovery paths, ignore rules, exact changed-field output, `git diff --check`, and the `.worktreeinclude` contents. Explain that propagation affects new Codex-managed worktrees only; the `.worktreeinclude` manifest must be committed for future worktrees to see it, and existing worktrees need explicit refresh or local copy. A delegation wave must report selected role names with configured model slugs and reasoning efforts in one compact line; otherwise report `Direct: <reason>` and continue on the main thread. End initialization and recommend a fresh task for feature work.

A writable parent is normal during a goal. For researcher, architect, and QA dispatches, require a report-only brief with no write set and describe `sandbox_mode = "read-only"` as intent rather than proof of effective child permissions. If the host cannot provide hard read-only isolation when it is required, use `Direct: delegation prohibited or effective read-only isolation unavailable`.
