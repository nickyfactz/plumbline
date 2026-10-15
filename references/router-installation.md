# Router installation

The router is intentionally repository-local and tiny. Copy the stable activation shim in `templates/router/SKILL.md` to:

```text
.agents/skills/plumbline-router/SKILL.md
```

Only do this after explicit `$plumbline-init` approval. The plugin install itself must not create this path. The shim hands ordinary prompts to the installed `plumbline` front door, which owns phase selection and lifecycle doctrine; do not copy evolving phase rules into the repository. The same approved setup may create project-local `.codex/config.toml`, `.codex/agents/*.toml`, or `.claude/agents/*.md`, plus an `AGENTS.md` delegation section and, for Claude Code, a `CLAUDE.md` file importing it so Claude actually loads the shared guidance. Keep host-local config, role files, and router untracked through `.git/info/exclude`; review and commit the durable `AGENTS.md`/`CLAUDE.md` guidance when the team should reach future worktrees. Never use personal/global agent definitions as fallback.

When new managed worktrees need the team and the host/repository workflow supports `.worktreeinclude`, approve and track the smallest manifest containing the ignored project paths. The manifest is the propagation mechanism; host-local config, role files, and router remain ignored and untracked. Propagation is not retroactive to existing worktrees, and the manifest must be present in the starting commit for future worktrees to see it.

To use the supplied helper from a checkout of this plugin:

```text
python scripts/install_router.py --root <target-repository>
```

The helper installs the router, a marked conditional activation block in
`AGENTS.md`, and a router-only `.git/info/exclude` entry. This works independently
of agent-team setup. It preserves instructions outside its managed block and
refuses to overwrite a differing router without `--replace`. Deleting the router
still disables automatic routing; the activation block never recreates it.

Recommend `--propagate` for local Codex-managed worktrees. Preview the complete
transaction with `--dry-run --format json`; when approved, repeat without
`--dry-run`. Propagation also patches root `.gitignore` and `.worktreeinclude`.
Commit those two files and the reviewed `AGENTS.md` guidance; leave the router
untracked. `--host claude` also adds the supported `@AGENTS.md` import to
`CLAUDE.md`. Existing team files and model settings are unchanged.

`.worktreeinclude` applies to newly created local Codex-managed worktrees.
Existing, remote, and manually created worktrees, and new clones, need explicit
local initialization. Their tracked activation guidance remains inert until the
local router is present. A tracked shim is an explicit user choice, never the
default. Source symlinks are not a portable propagation mechanism.

## Front-door recovery

The local activation block reads the router even when the host omits it from
the skill list. The router first uses the host's advertised callable front door.
If unavailable, it resolves the front door from currently visible `plumbline:*`
skill paths with `scripts/resolve_front_door.py`, validates one installation's
manifest and front-door metadata, and reads that real `SKILL.md`. The selected
front door owns routing; this recovery adds no phase logic or workers.

Only live catalog paths establish the active installation. Never scan old cache
versions or infer an enabled plugin from files on disk. Missing, stale, invalid,
or ambiguous active paths produce `Blocked: Plumbline routing unavailable` with
an actionable repair: refresh/re-enable the plugin or explicitly refresh local
setup, then retry. Do not silently proceed with ordinary implementation. Resolve
once per task and again only when the installation changes or the path vanishes.
