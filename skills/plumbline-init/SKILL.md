---
name: plumbline-init
description: Initialize or reassess Plumbline for a repository through a read-only audit and one approved setup proposal.
---

# Initialize Plumbline

This skill is explicit only. It is the consent boundary for repository-local automatic behavior.

## Guard and assessment

Before inspecting files, check whether this conversation already contains unrelated active implementation work. If it does, recommend a fresh task and stop unless the user explicitly says `continue here`.

Start read-only. Determine whether the repository is new or established. Inspect only enough to understand:

- `AGENTS.md`, README files, documentation routing, and canonical document ownership;
- build, validation, UAT, and managed-worktree conventions;
- active specifications, plans, and current Git state;
- project and personal custom-agent locations and relevant Codex settings;
- existing local skills, workflow plugins, and competing automatic controllers.

Adopt an established repository's terminology and document structure. Do not create a parallel docs taxonomy just because Plumbline is new.

For a new project, ask only for a concise product baseline: purpose, users, important behavior, priority, constraints, and non-goals. Resolve the technical baseline autonomously.

## One proposal

Present one selectable proposal with each file or setting named:

- install `.agents/skills/plumbline-router/SKILL.md` from `templates/router/SKILL.md`;
- create or audit project agents under `.codex/agents/`;
- propose small ignored-file propagation for managed worktrees only when needed;
- repair documentation routing only if the repository already needs it;
- offer reversible conflict settings for overlapping workflow plugins.

Apply nothing before approval. Do not disable another plugin or rewrite project guidance silently.

## After approval

Create only the selected items. The router is the only automatic activation mechanism and its deletion is the kill switch. Prefer local-only `.git/info/exclude` entries for router files; if propagation needs a tracked file, show it and obtain approval. Validate discovery, paths, and `git diff --check`, then report the exact router path and how to remove it. End initialization and recommend a fresh task for feature work.
