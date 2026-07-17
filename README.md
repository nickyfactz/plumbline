# Plumbline

Plumbline is a Codex-native engineering workflow plugin for keeping product intent, implementation, verification, and canonical repository documentation aligned without forcing heavyweight process onto small changes.

It is a skills-only plugin: no MCP server, connector, session-start hook, global installer, issue-tracker integration, or plugin-owned Git worktree system.

## Install from GitHub

```bash
codex plugin marketplace add nickyfactz/plumbline --ref main
codex
/plugins
```

Choose the `plumbline-development` marketplace, install `Plumbline`, then start a new Codex session. The same marketplace can be added in the Codex desktop app or IDE plugin browser. The repo marketplace is intentionally checked in at `.agents/plugins/marketplace.json`, so a GitHub checkout is the only source a user needs.

For a local checkout:

```bash
codex plugin marketplace add .
codex
/plugins
```

The current Codex CLI was verified to discover the root plugin from this repo marketplace with `source.path: "./"`.

## How it behaves

Installation is inert. It does not inspect or modify a project. Use an explicit side door for one task:

```text
$plumbline
$plumbline-shape
$plumbline-spec
$plumbline-plan
$plumbline-execute
$plumbline-diagnose
$plumbline-review
$plumbline-closeout
$plumbline-agent-team
$plumbline-offboard
```

For ordinary automatic routing, run `$plumbline-init` in the target repository. It audits first, presents one selectable proposal, and creates the tiny `.agents/skills/plumbline-router/` skill only after approval. Delete that directory to stop automatic Plumbline routing. The plugin can also be disabled in the Codex plugin browser.

### Project-local agent team

`$plumbline-init` can include the complete agent-team setup in the same approval: a role-by-role table with the proposed model slug, reasoning effort, sandbox, and write access; project `.codex/config.toml` with `multi_agent = true` and `agents.max_depth = 1`; the Plumbline section in `AGENTS.md`; and local ignore/worktree propagation. The approved files under `.codex/` and the router stay untracked. A future managed worktree can receive them through an approved, committed `.worktreeinclude` manifest; existing worktrees are not retroactive.

Plumbline checks the global config only for host capability and a model candidate. It never selects personal/global custom-agent files as a fallback. A matching project-local role is reported as `Delegated: <role>`; otherwise the main thread reports `Direct: <reason>`. Researcher, architect, and QA roles are report-only and receive no write set. Their `read-only` TOML is intent, not proof of effective child permissions when the parent is writable; Plumbline reports the boundary when observable and inspects unexpected diffs. Only the approved implementer receives a write set. Workers never spawn children.

Plumbline keeps one feature outcome, one active specification, and one live checkpoint plan. It adopts an established repository's docs and agent conventions. Active specs and plans are transient execution memory; canonical project docs remain the long-lived current truth.

## Development

```bash
python scripts/validate.py
python scripts/install_router.py --root <target-repository>
python scripts/install_agent_team.py --root <target-repository> --mode initialize --model <approved-slug> --reasoning-effort <approved-effort> --update-agents
```

The installer commands are explicit post-approval helpers. Use `--mode audit` for a read-only report, or `--mode retune` with `--fill-missing` and/or the explicitly approved `--update-instructions`; retune preserves existing model, reasoning, sandbox, and custom fields without `--replace`. Add `--propagate` only when future managed worktrees need the ignored files. The validation script uses only the Python standard library. GitHub Actions runs it on pushes and pull requests. The approved specification and implementation plan remain available at [`docs/specs/plumbline-v1.md`](docs/specs/plumbline-v1.md) and [`docs/plans/plumbline-v1.md`](docs/plans/plumbline-v1.md) until explicit release acceptance.

## Repository map

- `.codex-plugin/plugin.json` — plugin manifest.
- `.agents/plugins/marketplace.json` — repo marketplace for GitHub/local installation.
- `skills/` — explicit public skills plus narrow internal routing engines.
- `references/` — progressive-disclosure workflow policy.
- `templates/router/` — the repository-local activation boundary.
- `templates/agents/` — project-owned role, config, and worktree templates.
- `scripts/` — validation and explicit router/agent-team installation helpers.
- `docs/` and `evals/` — design authority, migration guidance, and behavioral checks.

## Scope boundary

Plumbline v1 does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
