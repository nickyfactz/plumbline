# Evaluation and UAT

## Automated checks

Run:

```bash
python scripts/validate.py
```

It checks the manifest, root marketplace, 18 skill manifests, public/engine invocation policies, reference set, router word budget, project-agent template fields, local multi-agent defaults, worktree patterns, and helper-script syntax. These are static configuration/workflow-intent checks; they do not prove effective permissions in a spawned session. The installer smoke test also proves that an approved setup creates local config, selected roles, AGENTS guidance, ignore rules, and the propagation manifest without touching global files; its dry-run JSON path proves the same manifest without writes. Router and AGENTS drift audits are report-only and never overwrite customized integration files.

## Platform smoke checks

- Root repo marketplace: passed with Codex CLI 0.144.0 and isolated `CODEX_HOME`.
- `codex plugin list`: discovered `plumbline@plumbline-development` at the repo root.
- Plugin browser install/enable/disable: requires an interactive Codex app or `/plugins` session and is listed in the UAT below.

## Behavioral scenarios

The compact prompts in `evals/prompts/` cover the consent boundary and latest-safe-phase choices. The expected outcomes in `evals/expected/` are deliberately behavior-level so they do not freeze model wording.

1. An ordinary uninitialized config change stays direct; an explicit `$plumbline` invocation hands off to `$plumbline-init` for a read-only proposal.
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
19. A writable parent may delegate report-only roles without switching the whole goal to read-only; the dispatch states `report-only; no write set` and does not claim hard isolation from TOML alone.
20. A report-only role receives no implementation-shaped brief; unexpected child edits are detected by the main thread's post-dispatch status/diff inspection rather than silently integrated.
21. When a task requires hard read-only isolation but the host cannot provide it, the workflow reports `Direct: delegation prohibited or effective read-only isolation unavailable`.
22. A resume with unchanged checkout and referenced contracts reuses checkpoint evidence instead of rereading whole documents or rerunning broad checks.
23. A resume after relevant source drift invalidates only affected evidence and reassesses it before advancement.
24. A stale repository-local router or AGENTS guidance section is reported with a proposed refresh and no automatic overwrite.
25. An explicitly selected competing orchestration loop is named as lifecycle owner; Plumbline does not stack or advance it.
26. A delegation wave reports role names, model slugs, reasoning efforts, and the report-only/no-write-set/no-child boundary in one compact line.
27. Phase entry resolves the current installed Plumbline root once; reference paths resolve from that root and no absolute versioned cache path is persisted.
28. The active plan's compact resume record is updated together when checkpoint status, owner, verified commit, or next action changes.
29. An unchanged resume emits a compact transition and skips repeated routing, doctrine, lifecycle, and broad-document narration.
30. Adjacent evidence-only or packaging work is batched into its parent checkpoint unless it has an independent acceptance, rollback, risk, contract, or ownership boundary.
31. A dry-run setup manifest lists `.gitignore`, `.worktreeinclude`, selected roles, and router changes without creating files; the approved apply matches that manifest.

## User UAT

1. Add the GitHub marketplace and install Plumbline from `/plugins`.
2. Start a new task and make a normal config request in an uninitialized fixture; confirm no automatic takeover.
3. Invoke `$plumbline` in that fixture; confirm it hands off to `$plumbline-init` without writing before approval.
4. Run `$plumbline-shape` in that fixture; confirm it works without creating the router.
5. Run `$plumbline-init`, approve only the router, then start a fresh task and try a rough feature prompt.
6. Delete `.agents/skills/plumbline-router/` and confirm automatic routing stops.
7. Disable Plumbline in the plugin browser and confirm no Plumbline skill runs.
8. In a disposable repository, run `$plumbline-init`, review the role/model/reasoning/sandbox table and dry-run manifest, and approve the full project-local team plus router.
9. Confirm `.codex/config.toml`, `.codex/agents/*.toml`, and the router are ignored/untracked. Review and commit `AGENTS.md`, `.gitignore`, and the optional `.worktreeinclude` manifest when the team should reach future worktrees.
10. Start a delegated feature task and confirm the main thread reports one compact delegation-wave line with the selected role, configured model slug, and reasoning effort; remove that local role and confirm it states `Direct` rather than selecting a global agent.
11. Run `$plumbline-agent-team --mode audit` against custom per-role TOMLs and confirm no file changes.
12. Run `$plumbline-agent-team --mode retune` without update flags, then with explicit `--update-instructions`; confirm only the instruction field changes and the custom model/reasoning/sandbox values survive.
13. Run `$plumbline-offboard` and confirm it proposes only Plumbline-owned integration for removal.
