# Worktree readiness

Use the Codex host's managed worktree for scoped or designed feature work when available. Plumbline must not create, register, remove, or clean up worktrees itself.

Before work starts, inspect repository-owned setup: package managers, virtual environments, generated assets, local services, environment variables, caches, and test commands. Prefer absolute interpreter/tool paths and environment variables. Treat borrowed models, caches, and shared virtual environments as read-only; verify imports resolve to the current worktree source before trusting a result.

Safe symlinks are optional and platform-sensitive. Only borrow a target outside disposable worktree roots, never link a source tree or package tree, and ensure cleanup cannot follow the link into shared assets. Use `.worktreeinclude` only for small ignored local files. Do not use it to copy secrets, models, dependencies, or source trees.

Hand UAT back to Local when the check is singleton, hardware-bound, exceptionally heavy, or materially cheaper in the user's normal environment. Record the exact command and expected observation.
