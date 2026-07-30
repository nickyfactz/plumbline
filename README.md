# Plumbline

Plumbline is a skills-only engineering workflow plugin for Codex and Claude Code. It keeps product intent, implementation, verification, and canonical repository documentation aligned without forcing heavyweight process onto small changes.

It is a skills-only plugin: no MCP server, connector, session-start hook, global installer, issue-tracker integration, or plugin-owned Git worktree system.

## Install for Codex

Codex has a direct CLI path and a plugin-browser path. Both use the checked-in repo marketplace at `.agents/plugins/marketplace.json`.

### Direct CLI install from GitHub

```bash
codex plugin marketplace add nickyfactz/plumbline@main
codex plugin add plumbline@plumbline
```

Start a new Codex session after installation. The first command registers the GitHub marketplace; the second installs the `plumbline` plugin from it.

### Plugin browser

```bash
codex plugin marketplace add nickyfactz/plumbline@main
codex
/plugins
```

Select the `plumbline` marketplace, install `Plumbline`, and start a new Codex session. The browser path is available in Codex CLI and the Codex desktop app.

### Local checkout

```bash
codex plugin marketplace add .
codex plugin add plumbline@plumbline
```

The root plugin is intentionally addressed by the marketplace with `source.path: "./"`, so no nested package or copy step is required.

## Install for Claude Code

Claude Code uses the same platform-neutral `SKILL.md` workflows through the Claude plugin manifest and marketplace at `.claude-plugin/`. From GitHub:

```bash
claude plugin marketplace add nickyfactz/plumbline@main
claude plugin install plumbline@plumbline
```

For a local checkout while developing:

```bash
claude plugin marketplace add .
claude plugin install plumbline@plumbline
```

Reload the current Claude Code session with `/reload-plugins`. The explicit entry skills are available as `/plumbline:plumbline`, `/plumbline:plumbline-shape`, `/plumbline:plumbline-spec`, `/plumbline:plumbline-plan`, `/plumbline:plumbline-execute`, `/plumbline:plumbline-diagnose`, `/plumbline:plumbline-review`, `/plumbline:plumbline-closeout`, `/plumbline:plumbline-agent-team`, `/plumbline:plumbline-init`, and `/plumbline:plumbline-offboard`. The plugin exposes only these public entry skills; internal phase engines remain package-local guidance so they do not add menu or automatic-invocation noise.

Validate before sharing or installing:

```bash
claude plugin validate .
```

Claude Code uses the repository's Git credentials for a private GitHub marketplace. The plugin adds no Claude hooks, agents, MCP servers, project settings, or global files. Codex-specific `agents/openai.yaml` metadata remains alongside the shared skills and is ignored by Claude Code.

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

Invoke `$plumbline` in a new repository and the front door offers the read-only setup proposal for an ordinary unclassified request. When the request includes a sufficient external specification, plan, handoff, or work order, it can instead adopt that artifact and continue in convention mode. Setup remains read-only until it presents one selectable proposal and receives approval. `$plumbline-init` can also be invoked directly. It creates the tiny `.agents/skills/plumbline-router/` skill only after approval. Delete that directory to stop automatic Plumbline routing. The plugin can also be disabled in the Codex plugin browser.

Explicit phase skills also support convention mode in an uninitialized repository. A user-supplied specification, plan, handoff, or work order can be adopted without Plumbline frontmatter or generated paths; initialization and a project-local agent team are optional enhancements. Plumbline recommends companion artifacts when they improve recovery, but does not block a sufficient external artifact merely because its companion is absent.

### Project-local agent team

`$plumbline-init` can include the complete agent-team setup in the same approval: a role-by-role table with the proposed model slug, reasoning effort, sandbox, and write access; project `.codex/config.toml` with `multi_agent = true` and `agents.max_depth = 1`; the Plumbline section in `AGENTS.md`; and local ignore/worktree propagation. When `--propagate` is approved, the installer patches `.gitignore`, `.git/info/exclude`, and `.worktreeinclude` with the exact local Plumbline paths. Preview the same change set with `--dry-run --format json` before applying it. The approved files under `.codex/` and the router stay untracked. A future managed worktree can receive them through an approved, committed `.worktreeinclude` manifest; existing worktrees are not retroactive.

Plumbline checks the global config only for host capability and a model candidate. It never selects personal/global custom-agent files as a fallback. Before phase work, it states one lifecycle owner; installed workflow plugins are available capabilities, not active controllers unless explicitly selected. Each delegation wave reports the selected project-local roles with their configured model slugs and reasoning efforts in one compact line; effective values are included when the host exposes them. If no local role is available, the main thread reports `Direct: <reason>`. Researcher, architect, and QA roles are report-only and receive no write set. Their `read-only` TOML is intent, not proof of effective child permissions when the parent is writable; Plumbline reports the boundary when observable and inspects unexpected diffs. Only the approved implementer receives a write set. Workers never spawn children.

Plumbline keeps one feature outcome, one active specification, and one live checkpoint plan. It adopts an established repository's docs and agent conventions. A complete work order can be adopted as the lifecycle contract, so Plumbline does not replay settled shaping or planning when only execution remains. The plan frontmatter carries the compact resume record: active checkpoint, status, lifecycle owner, last verified commit, and next safe action. Resumed execution reuses unchanged evidence and avoids repeating routing or doctrine unless a material trigger changes the work. Active specs and plans are transient execution memory; canonical project docs remain the long-lived current truth.

Execution uses a resume fingerprint of the checkout, plan record, and relevant local agent configuration. An unchanged resume reuses the exact checkpoint evidence instead of rereading broad documents or repeating lifecycle narration. Checkpoints use a compact card by default and expand only for material boundaries. Execute ends at Ready for Acceptance; accepted-work Closeout handles integration and transient cleanup. Every process artifact or announcement must earn its space by serving recovery, validation, authorization, or ownership.

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
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — Claude Code plugin and marketplace manifests.
- `skills/` — explicit public skills plus narrow internal routing engines.
- `references/` — progressive-disclosure workflow policy.
- `templates/router/` — the stable repository-local activation shim.
- `templates/agents/` — project-owned role, config, and worktree templates.
- `scripts/` — validation and explicit router/agent-team installation helpers.
- `docs/` and `evals/` — design authority, migration guidance, and behavioral checks.

## Scope boundary

Plumbline v1 does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
