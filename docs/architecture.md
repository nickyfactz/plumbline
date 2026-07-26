# Plumbline architecture

## Package boundary

The repository root is the plugin root. `.codex-plugin/plugin.json` points at `./skills/`; `.agents/plugins/marketplace.json` exposes the root plugin for local or Git-backed marketplace installation. No runtime package is copied into user repositories.

## Invocation boundary

The public skills are explicit and have `allow_implicit_invocation: false` in `agents/openai.yaml`. Seven internal `*-engine` skills carry the phase bodies and allow model invocation only after the explicit wrapper or local router selects them. This keeps the public command surface stable while giving the router a narrow, model-invoked target.

`templates/router/SKILL.md` is the only repository-local automatic controller. It is not shipped into a target repository during plugin installation. `$plumbline-init` creates it only after approval; deleting its directory disables automatic routing.

## Durable state

Product intent lives in the active specification. Execution state lives in the active plan and Git history. Canonical repository docs describe the resulting current system. This separation lets a fresh task recover from files and Git without replaying the original conversation.

The active plan frontmatter also carries one compact resume record: current checkpoint, checkpoint status, lifecycle owner, last verified commit, and next safe action. Plumbline resolves the currently loaded plugin root once per phase entry or resume; repository artifacts never store absolute versioned cache paths.

A supplied work order is adopted when it already contains scope, non-goals, checkpoint, acceptance/proof, owner, and closeout boundaries. This lets Plumbline act as a thin safety rail for execution instead of replaying settled shaping or planning. Workers receive anchored, bounded briefs and reuse unchanged artifacts rather than inheriting or rereading full conversation and documentation history.

## Ownership

The main thread owns product decisions, active artifacts, integration, and Git. Agents are bounded researchers, architects, implementers, or report-only auditors. Report-only roles receive no write set; their `read-only` TOML is intent and may be affected by a writable parent session. Plumbline records the boundary when observable and inspects returned diffs instead of adding a permission daemon. Plumbline never owns a worktree registry or global agent installation.

Shape may offer an explicitly approved throwaway prototype when a behavioral question is cheaper to answer with a small runnable probe. It is not a new phase or artifact class and is not automatically promoted into production.

## Platform evidence

The root marketplace path was tested with Codex CLI 0.144.0 in an isolated `CODEX_HOME`: `codex plugin marketplace add E:\Plumbline --json` returned marketplace `plumbline-development`, and `codex plugin list` discovered `plumbline@plumbline-development` at the repository root. Browser enable/disable and a real fresh-task routing session remain part of user UAT.
