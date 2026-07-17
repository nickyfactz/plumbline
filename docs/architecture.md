# Plumbline architecture

## Package boundary

The repository root is the plugin root. `.codex-plugin/plugin.json` points at `./skills/`; `.agents/plugins/marketplace.json` exposes the root plugin for local or Git-backed marketplace installation. No runtime package is copied into user repositories.

## Invocation boundary

The public skills are explicit and have `allow_implicit_invocation: false` in `agents/openai.yaml`. Seven internal `*-engine` skills carry the phase bodies and allow model invocation only after the explicit wrapper or local router selects them. This keeps the public command surface stable while giving the router a narrow, model-invoked target.

`templates/router/SKILL.md` is the only repository-local automatic controller. It is not shipped into a target repository during plugin installation. `$plumbline-init` creates it only after approval; deleting its directory disables automatic routing.

## Durable state

Product intent lives in the active specification. Execution state lives in the active plan and Git history. Canonical repository docs describe the resulting current system. This separation lets a fresh task recover from files and Git without replaying the original conversation.

## Ownership

The main thread owns product decisions, active artifacts, integration, and Git. Agents are bounded researchers, architects, implementers, or report-only auditors. Report-only roles receive no write set; their `read-only` TOML is intent and may be affected by a writable parent session. Plumbline records the boundary when observable and inspects returned diffs instead of adding a permission daemon. Plumbline never owns a worktree registry or global agent installation.

## Platform evidence

The root marketplace path was tested with Codex CLI 0.144.0 in an isolated `CODEX_HOME`: `codex plugin marketplace add E:\Plumbline --json` returned marketplace `plumbline-development`, and `codex plugin list` discovered `plumbline@plumbline-development` at the repository root. Browser enable/disable and a real fresh-task routing session remain part of user UAT.
