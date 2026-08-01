# Evaluation and UAT

## Automated checks

Run:

```bash
python scripts/validate.py
python scripts/test_install_agent_team.py
python scripts/test_install_claude_agent_team.py
```

It checks the manifests, both marketplaces, 18 skill manifests, public/engine invocation policies, reference set, router word budget, project-agent template fields, local multi-agent defaults, worktree patterns, and helper-script syntax. These are static configuration/workflow-intent checks; they do not prove effective permissions in a spawned session. The Codex and Claude installer smoke tests prove that approved setup creates host-local roles, guidance, ignore rules, and propagation manifests without touching global files; their dry-run paths prove the same manifests without writes. Router and AGENTS drift audits are report-only and never overwrite customized integration files.

## Platform smoke checks

- Root repo marketplace: passed with Codex CLI 0.144.0 and isolated `CODEX_HOME`.
- `codex plugin list`: discovered `plumbline@plumbline` at the repo root.
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
26. A delegation wave reports role names, host-native model and reasoning/effort values, and the report-only/no-write-set/no-child boundary in one compact line.
27. Phase entry resolves the current installed Plumbline root once; reference paths resolve from that root and no absolute versioned cache path is persisted.
28. The active plan's compact resume record is updated together when checkpoint status, owner, verified commit, or next action changes.
29. An unchanged resume emits a compact transition and skips repeated routing, doctrine, lifecycle, and broad-document narration.
30. Adjacent evidence-only or packaging work is batched into its parent checkpoint unless it has an independent acceptance, rollback, risk, contract, or ownership boundary.
31. A dry-run setup manifest lists `.gitignore`, `.worktreeinclude`, selected roles, and router changes without creating files; the approved apply matches that manifest.
32. A complete work order resumes at its latest safe phase without replaying settled shaping or planning, while new product decisions and failed gates still interrupt.
33. A contract-complete broad task may remain direct when no phase advancement is required.
34. Shape offers a throwaway prototype only for material behavioral uncertainty, after conversation/research is insufficient, and only after explicit approval to write.
35. A prototype uses one existing run command, no persistence by default, visible results, and no automatic production promotion or Git ceremony.
36. Worker briefs use anchored paths and existing evidence; successful command output is summarized rather than pasted into the main context.
37. Closeout selects light or full mode proportionally without skipping required UAT, documentation, or explicit transient cleanup boundaries.
38. Router dry-run previews an existing stale copy without writing and reports when `--replace` is required.

39. An unchanged resume fingerprint reuses the compact record and checkpoint evidence without rereading agent TOMLs, broad plan bodies, or delegation doctrine.
40. The first actual delegation loads the detailed orchestration reference, reports role names with host-native model and reasoning/effort values, states the report-only/no-write-set/no-child boundary, and inspects Git once after the wave.
41. Direct work with no delegation need does not emit routine lifecycle, Direct, or delegation doctrine ceremony.
42. A compact checkpoint card is sufficient for ordinary work; material security, schema, rollback, public-contract, ownership, or irreversible boundaries receive expanded detail.
43. A kickoff commit is required only for an explicit policy, recovery need, material contract, or auditable boundary; otherwise planning artifacts may remain uncommitted until a coherent recovery boundary.
44. Execute reaches Ready for Acceptance without deleting transient artifacts; accepted Closeout handles integration, retirement, and cleanup.
45. A supporting construction-policy skill may constrain implementation choices but does not add lifecycle ownership, checkpoints, or competing acceptance gates.
46. An accepted equivalent evidence path is reused before slice-specific packaging or receipt machinery is introduced.

47. An explicit phase skill accepts a sufficient external specification, plan, handoff, or work order in an uninitialized repository without requiring setup, Plumbline frontmatter, or generated paths.
48. A sufficient external specification with no separate plan receives a companion-plan recommendation but does not block execution when it contains execution topology, the next safe slice, and acceptance proof.
49. A sufficient external plan or work order can execute without a separate Plumbline specification; a material product ambiguity routes back to Shape.
50. Unrelated specifications or plans do not block the current task; competing artifacts for the same task produce one compact ambiguity report.
51. The front door offers setup for an ordinary unclassified request without a router but assesses a supplied sufficient artifact before making setup a prerequisite.
52. Plan and Execute reject inconsistent current-checkpoint/frontmatter state before advancement, while retained external artifacts are not rewritten merely for format compliance.
53. Rolling telemetry is recorded as timestamped sample evidence and does not force acceptance rewrites or evidence-only commits when stable assertions remain valid.
54. Closeout uses explicit acceptance or integration as its gate and does not require a Plumbline-generated specification or plan.
55. Execute traverses all remaining serial checkpoints through final plan completion without requiring `/goal` or a user prompt between checkpoints.
56. Explicit checkpoint-by-checkpoint wording pauses after the requested checkpoint and does not imply the default behavior.
57. An architect's in-scope product-question label is resolved by the main thread from the approved plan and a safe reversible default without automatically reopening Shape.
58. A named destructive or user-approval gate still pauses only at that gate while preserving the active plan.
59. Claude setup creates project-local `.claude/agents/*.md` roles with host-native model, effort, tools, and permission fields, without creating `.claude/settings.json` or enabling experimental Agent Teams.
60. Claude report-only roles omit the `Agent` tool, carry a `plan` permission intent, and preserve custom model, effort, frontmatter, and instructions during audit/retune.

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
14. Provide a complete work order with a ready checkpoint and confirm `$plumbline` resumes execution without recreating the settled plan.
15. During Shape, present a material state or UI uncertainty and confirm Plumbline offers a prototype only after explaining its transient boundary and waiting for approval.
16. Run `scripts/install_router.py --dry-run --format json` against an older local router and confirm it reports `modify`, preserves the file, and marks `requires_replace`.
17. In a Claude Code fixture, run `/plumbline:plumbline-init`, review the host-native role table and dry-run manifest, approve the project-local team, and confirm only `.claude/agents/*.md`, approved guidance, ignore rules, and optional propagation are created.
18. In the Claude fixture, confirm report-only roles cannot invoke `Agent`, Claude global settings remain unchanged, and `/reload-plugins` or a new session loads the updated plugin.
