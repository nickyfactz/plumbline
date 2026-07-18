# Router installation

The router is intentionally repository-local and tiny. Copy the stable activation shim in `templates/router/SKILL.md` to:

```text
.agents/skills/plumbline-router/SKILL.md
```

Only do this after explicit `$plumbline-init` approval. The plugin install itself must not create this path. The shim hands ordinary prompts to the installed `plumbline` front door, which owns phase selection and lifecycle doctrine; do not copy evolving phase rules into the repository. The same approved setup may create project-local `.codex/config.toml`, `.codex/agents/*.toml`, and an `AGENTS.md` delegation section. Keep the config, role TOMLs, and router untracked through `.git/info/exclude`; review and commit `AGENTS.md` as durable repository guidance when the team should reach future worktrees. Never use personal/global agent definitions as fallback.

When new Codex-managed worktrees need the team, approve and track the smallest `.worktreeinclude` manifest containing the ignored project paths. The manifest is the propagation mechanism; the config, agent TOMLs, and router remain ignored and untracked. Propagation is not retroactive to existing worktrees, and the manifest must be present in the starting commit for future worktrees to see it.

To use the supplied helper from a checkout of this plugin:

```text
python scripts/install_router.py --root <target-repository>
```

The helper writes only the router file and refuses to overwrite an existing file unless `--replace` is supplied. Agent-team audit reports router drift without overwriting it. The user remains responsible for approval and any ignore rule.
