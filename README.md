# Plumbline

Plumbline is a Codex-native engineering workflow plugin for keeping product intent, implementation, verification, and canonical repository documentation aligned without forcing heavyweight process onto small changes.

It is a skills-only plugin: no MCP server, connector, session-start hook, global installer, issue-tracker integration, or plugin-owned Git worktree system.

## Install from GitHub

After pushing this repository, replace `OWNER/REPOSITORY` with its GitHub shorthand:

```bash
codex plugin marketplace add OWNER/REPOSITORY --ref main
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

Plumbline keeps one feature outcome, one active specification, and one live checkpoint plan. It adopts an established repository's docs and agent conventions. Active specs and plans are transient execution memory; canonical project docs remain the long-lived current truth.

## Development

```bash
python scripts/validate.py
python scripts/install_router.py --root <target-repository>
```

The validation script uses only the Python standard library. GitHub Actions runs it on pushes and pull requests. The approved specification and implementation plan remain available at [`docs/specs/plumbline-v1.md`](docs/specs/plumbline-v1.md) and [`docs/plans/plumbline-v1.md`](docs/plans/plumbline-v1.md) until explicit release acceptance.

## Repository map

- `.codex-plugin/plugin.json` — plugin manifest.
- `.agents/plugins/marketplace.json` — repo marketplace for GitHub/local installation.
- `skills/` — explicit public skills plus narrow internal routing engines.
- `references/` — progressive-disclosure workflow policy.
- `templates/router/` — the repository-local activation boundary.
- `templates/agents/` — optional project-owned agent archetypes.
- `scripts/` — validation and explicit router installation helper.
- `docs/` and `evals/` — design authority, migration guidance, and behavioral checks.

## Scope boundary

Plumbline v1 does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
