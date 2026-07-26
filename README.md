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

Invoke `$plumbline` in a new repository and the front door detects the missing project-local router, then hands off to `$plumbline-init`. Setup remains read-only until it presents one selectable proposal and receives approval. `$plumbline-init` can also be invoked directly. It creates the tiny `.agents/skills/plumbline-router/` skill only after approval. Delete that directory to stop automatic Plumbline routing. The plugin can also be disabled in the Codex plugin browser.

### Project-local agent team

`$plumbline-init` can include the complete agent-team setup in the same approval: a role-by-role table with the proposed model slug, reasoning effort, sandbox, and write access; project `.codex/config.toml` with `multi_agent = true` and `agents.max_depth = 1`; the Plumbline section in `AGENTS.md`; and local ignore/worktree propagation. When `--propagate` is approved, the installer patches `.gitignore`, `.git/info/exclude`, and `.worktreeinclude` with the exact local Plumbline paths. Preview the same change set with `--dry-run --format json` before applying it. The approved files under `.codex/` and the router stay untracked. A future managed worktree can receive them through an approved, committed `.worktreeinclude` manifest; existing worktrees are not retroactive.

Plumbline checks the global config only for host capability and a model candidate. It never selects personal/global custom-agent files as a fallback. Before phase work, it states one lifecycle owner; installed workflow plugins are available capabilities, not active controllers unless explicitly selected. Each delegation wave reports the selected project-local roles with their configured model slugs and reasoning efforts in one compact line; effective values are included when the host exposes them. If no local role is available, the main thread reports `Direct: <reason>`. Researcher, architect, and QA roles are report-only and receive no write set. Their `read-only` TOML is intent, not proof of effective child permissions when the parent is writable; Plumbline reports the boundary when observable and inspects unexpected diffs. Only the approved implementer receives a write set. Workers never spawn children.

Plumbline keeps one feature outcome, one active specification, and one live checkpoint plan. It adopts an established repository's docs and agent conventions. A complete work order can be adopted as the lifecycle contract, so Plumbline does not replay settled shaping or planning when only execution remains. The plan frontmatter carries the compact resume record: active checkpoint, status, lifecycle owner, last verified commit, and next safe action. Resumed execution reuses unchanged evidence and avoids repeating routing or doctrine unless a material trigger changes the work. Active specs and plans are transient execution memory; canonical project docs remain the long-lived current truth.

During Shape, Plumbline researches external capability and design options when the request leaves the option space open, then presents concise cited findings before asking the user to choose. If the remaining uncertainty is behavioral, Shape may offer an explicitly approved throwaway prototype instead of another planning round; it uses the smallest existing scratch/run convention, no persistence by default, and no automatic branch, tracker, dependency, or production promotion. For clearly long-running work, it may offer one transient in-repository shaping handoff containing decisions, research implications, open questions, fog, and non-goals. Small work stays conversation-only; Plumbline does not create a handoff for every question or use an external issue tracker.

## Development

```bash
python scripts/validate.py
python scripts/install_router.py --root <target-repository> --dry-run --format json
python scripts/install_agent_team.py --root <target-repository> --mode initialize --model <approved-slug> --reasoning-effort <approved-effort> --update-agents
```

The installer commands are explicit proposal/apply helpers. Run `--dry-run --format json` while preparing the proposal and again after approval to preview every file, operation, and changed field without writing. Existing router previews identify stale copies and whether `--replace` is required. Use `--mode audit` for a read-only report; it also detects stale router and `AGENTS.md` guidance without overwriting either. Use `--mode retune` with `--fill-missing` and/or the explicitly approved `--update-instructions`; retune preserves existing model, reasoning, sandbox, and custom fields without `--replace`. Add `--propagate` only when future managed worktrees need the ignored files; it includes the root `.gitignore` patch. Execution commits only after focused validation and when a coherent recovery boundary or repository policy calls for it; adjacent evidence-only work may stay with its parent checkpoint. Review and closeout are risk-proportional rather than mandatory ceremonies for trivial work. The validation script uses only the Python standard library. GitHub Actions runs it on pushes and pull requests. The approved specification and implementation plan remain available at [`docs/specs/plumbline-v1.md`](docs/specs/plumbline-v1.md) and [`docs/plans/plumbline-v1.md`](docs/plans/plumbline-v1.md) until explicit release acceptance.

## Repository map

- `.codex-plugin/plugin.json` — plugin manifest.
- `.agents/plugins/marketplace.json` — repo marketplace for GitHub/local installation.
- `skills/` — explicit public skills plus narrow internal routing engines.
- `references/` — progressive-disclosure workflow policy.
- `templates/router/` — the stable repository-local activation shim.
- `templates/agents/` — project-owned role, config, and worktree templates.
- `scripts/` — validation and explicit router/agent-team installation helpers.
- `docs/` and `evals/` — design authority, migration guidance, and behavioral checks.

## Scope boundary

Plumbline v1 does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
