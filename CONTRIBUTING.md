# Contributing

Plumbline is a prompt-and-reference plugin, so keep changes small and behavior-focused.

1. Run `python scripts/validate.py`.
2. Keep public skills explicit and short; put branch-specific detail in `references/`.
3. Do not add session-start hooks, global installers, plugin-owned worktrees, or mandatory TDD language.
4. Update the relevant skill, reference, and evaluation fixture together when behavior changes.
5. Keep `docs/architecture.md` aligned with shipped behavior and update `docs/evaluation.md` when validation or UAT behavior changes.

For router changes, run `python scripts/test_router.py` in addition to the two
agent-team installer smokes. The tests exercise filesystem and resolver behavior
without model calls; `evals/prompts/router-recovery.md` covers fresh-session
activation expectations.

Format and lint the router's Python surface with the pinned development tool:

```text
uvx --from ruff==0.14.0 ruff format --check scripts/install_router.py scripts/resolve_front_door.py scripts/test_router.py
uvx --from ruff==0.14.0 ruff check scripts/install_router.py scripts/resolve_front_door.py scripts/test_router.py
```

Omit `--check` from the formatter to apply formatting. This development tool is
not a plugin runtime dependency.
