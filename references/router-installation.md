# Router installation

The router is intentionally repository-local and tiny. Copy the stable activation shim in `templates/router/SKILL.md` to:

```text
.agents/skills/plumbline-router/SKILL.md
```

Only do this after explicit `$plumbline-init` approval. The plugin install itself must not create this path. The shim hands ordinary prompts to the installed `plumbline` front door, which owns phase selection and lifecycle doctrine; do not copy evolving phase rules into the repository. The same approved setup may create project-local `.codex/config.toml`, `.codex/agents/*.toml`, or `.claude/agents/*.md`, plus an `AGENTS.md` delegation section. Keep host-local config, role files, and router untracked through `.git/info/exclude`; review and commit `AGENTS.md` as durable repository guidance when the team should reach future worktrees. Never use personal/global agent definitions as fallback.

When new managed worktrees need the team and the host/repository workflow supports `.worktreeinclude`, approve and track the smallest manifest containing the ignored project paths. The manifest is the propagation mechanism; host-local config, role files, and router remain ignored and untracked. Propagation is not retroactive to existing worktrees, and the manifest must be present in the starting commit for future worktrees to see it.

To use the supplied helper from a checkout of this plugin:

```text
python scripts/install_router.py --root <target-repository>
```

The helper writes only the router file and refuses to overwrite an existing file unless `--replace` is supplied. `--dry-run` can preview an existing router without `--replace`; the JSON manifest reports whether replacement is required, and the apply command still needs explicit `--replace`. Agent-team audit reports router drift without overwriting it. The user remains responsible for approval and any ignore rule.
