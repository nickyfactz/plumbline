# Router installation

The router is intentionally repository-local and tiny. Copy `templates/router/SKILL.md` to:

```text
.agents/skills/plumbline-router/SKILL.md
```

Only do this after explicit `$plumbline-init` approval. The plugin install itself must not create this path. Prefer adding the router directory to `.git/info/exclude` when the repository's managed worktrees do not need it. If worktrees need the router and local propagation is not supported, show the smallest tracked propagation change and wait for approval.

To use the supplied helper from a checkout of this plugin:

```text
python scripts/install_router.py --root <target-repository>
```

The helper writes only the router file and refuses to overwrite an existing file unless `--replace` is supplied. The user remains responsible for approval and any ignore rule.
