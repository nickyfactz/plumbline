# Contributing

Plumbline is a prompt-and-reference plugin, so keep changes small and behavior-focused.

1. Run `python scripts/validate.py`.
2. Keep public skills explicit and short; put branch-specific detail in `references/`.
3. Do not add session-start hooks, global installers, plugin-owned worktrees, or mandatory TDD language.
4. Update the relevant skill, reference, and evaluation fixture together when behavior changes.
5. Keep `docs/architecture.md` aligned with shipped behavior and update `docs/evaluation.md` when validation or UAT behavior changes.
