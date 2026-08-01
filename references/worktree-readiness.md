# Worktree readiness

Use the active host's managed worktree for scoped or designed feature work when available. Plumbline must not create, register, remove, or clean up worktrees itself.

Before work starts, inspect repository-owned setup: package managers, virtual environments, generated assets, local services, environment variables, caches, and test commands. Prefer absolute interpreter/tool paths and environment variables. Treat borrowed models, caches, and shared virtual environments as read-only; verify imports resolve to the current worktree source before trusting a result.

Safe symlinks are optional and platform-sensitive. Only borrow a target outside disposable worktree roots, never link a source tree or package tree, and ensure cleanup cannot follow the link into shared assets. Use `.worktreeinclude` only for small ignored local files when the host/repository workflow supports it. Do not use it to copy secrets, models, dependencies, or source trees. For the Plumbline team, list only the applicable host-local config/role files (`.codex/config.toml`, `.codex/agents/*.toml`, or `.claude/agents/*.md`) and the local router. The manifest itself must be in the starting commit for future managed worktrees to see it; its listed files remain ignored and untracked. `AGENTS.md` is durable guidance and should be reviewed and committed separately. Existing worktrees are not retroactive.

Hand UAT back to Local when the check is singleton, hardware-bound, exceptionally heavy, or materially cheaper in the user's normal environment. Record the exact command and expected observation.
