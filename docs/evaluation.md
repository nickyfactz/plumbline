# Evaluation and UAT

## Automated checks

Run:

```bash
python scripts/validate.py
```

It checks the manifest, root marketplace, 18 skill manifests, public/engine invocation policies, reference set, router word budget, project-agent template fields, local multi-agent defaults, worktree patterns, and helper-script syntax. The installer smoke test also proves that an approved setup creates local config, all five roles, AGENTS guidance, ignore rules, and the propagation manifest without touching global files.

## Platform smoke checks

- Root repo marketplace: passed with Codex CLI 0.144.0 and isolated `CODEX_HOME`.
- `codex plugin list`: discovered `plumbline@plumbline-development` at the repo root.
- Plugin browser install/enable/disable: requires an interactive Codex app or `/plugins` session and is listed in the UAT below.

## Behavioral scenarios

The compact prompts in `evals/prompts/` cover the consent boundary and latest-safe-phase choices. The expected outcomes in `evals/expected/` are deliberately behavior-level so they do not freeze model wording.

1. Uninitialized config change stays direct.
2. Explicit shape works without a router.
3. A rough idea selects Shape.
4. A sufficient external design selects Plan.
5. An active spec and plan select Execute.
6. A bug selects Diagnose.
7. A review request is report-only.
8. Accepted work selects Closeout.
9. Router deletion stops automatic routing.
10. Plugin disable prevents the router's engine path.
11. Init proposal shows every selected role's model, reasoning effort, sandbox, config, AGENTS, ignore, and worktree changes before approval.
12. Approved setup creates only project-local `.codex/config.toml` and `.codex/agents/*.toml`, with `multi_agent=true`, `max_depth=1`, and explicit model/reasoning fields.
13. A project-local role is selected when available; a missing role reports `Direct` and never uses a personal/global fallback.
14. Workers cannot spawn children and the project stays at delegation depth one.
15. A committed `.worktreeinclude` manifest makes the ignored team files eligible for new managed worktrees while leaving them untracked; existing worktrees are not retroactive.
16. Audit is read-only and preserves deliberately different per-role model, reasoning, sandbox, and custom instruction values.
17. Retune without flags changes nothing; explicit instruction retune changes only `developer_instructions` and reports that field exactly.
18. Approved `--fill-missing` adds absent required fields without replacing present customized values.

## User UAT

1. Add the GitHub marketplace and install Plumbline from `/plugins`.
2. Start a new task and make a normal config request in an uninitialized fixture; confirm no automatic takeover.
3. Run `$plumbline-shape` in that fixture; confirm it works without creating the router.
4. Run `$plumbline-init`, approve only the router, then start a fresh task and try a rough feature prompt.
5. Delete `.agents/skills/plumbline-router/` and confirm automatic routing stops.
6. Disable Plumbline in the plugin browser and confirm no Plumbline skill runs.
7. In a disposable repository, run `$plumbline-init`, review the role/model/reasoning/sandbox table, and approve the full project-local team plus router.
8. Confirm `.codex/config.toml`, `.codex/agents/*.toml`, and the router are ignored/untracked. Review and commit `AGENTS.md`, `.gitignore`, and the optional `.worktreeinclude` manifest when the team should reach future worktrees.
9. Start a delegated feature task and confirm the main thread states `Delegated: <role>`; remove that local role and confirm it states `Direct` rather than selecting a global agent.
10. Run `$plumbline-agent-team --mode audit` against custom per-role TOMLs and confirm no file changes.
11. Run `$plumbline-agent-team --mode retune` without update flags, then with explicit `--update-instructions`; confirm only the instruction field changes and the custom model/reasoning/sandbox values survive.
12. Run `$plumbline-offboard` and confirm it proposes only Plumbline-owned integration for removal.
