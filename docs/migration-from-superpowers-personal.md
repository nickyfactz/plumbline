# Migration from `superpowers-personal`

Plumbline is a lighter replacement, not a renamed copy. Do not run both as automatic controllers for the same repository.

| Predecessor | Plumbline treatment |
| --- | --- |
| universal bootstrap | removed; installation is inert |
| agent routing skill | folded into the router and `references/subagent-orchestration.md` |
| brainstorming | replaced by `plumbline-shape` and `plumbline-spec` |
| writing plans | replaced by `plumbline-plan` and `references/plan-schema.md` |
| universal TDD | removed; use `references/runtime-value-testing.md` |
| systematic debugging | replaced by `plumbline-diagnose` |
| parallel-agent and subagent-driven skills | folded into `plumbline-execute` and orchestration reference |
| code-review and verification gates | replaced by `plumbline-review` and checkpoint evidence |
| custom worktree workflow | removed; use Codex-managed worktrees |
| finishing branch workflow | replaced by `plumbline-closeout` |
| global agent installers | removed; optional project-owned templates live under `templates/agents/` |

Keep useful repository docs, agents, tests, and history. Remove old automatic bootstraps before enabling Plumbline if both could respond to the same ordinary prompt. Use the conflict audit to propose reversible settings rather than silently changing another plugin.
