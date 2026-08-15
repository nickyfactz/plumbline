# Plumbline architecture

## Package boundary

The repository root is the plugin root. Codex and Claude Code each have a
native manifest and marketplace entry, while the shared workflow is expressed
as Markdown skills and references. Plugin installation exposes those skills;
it does not copy a runtime package into user repositories.

The public surface contains the front door, phase wrappers, agent-team setup,
and offboarding. Internal `*-engine` skills contain the detailed phase rules
and are selected only by a wrapper or the repository-local router.

## Invocation boundary

Public skills are explicit entry points. The front door classifies the task
and selects the latest safe phase: direct work, Shape, Specification, Plan,
Execute, Diagnose, Review, or Closeout. The phase wrappers keep the user-facing
command surface stable and load an internal engine only when that phase is
selected.

The only automatic controller Plumbline can install is the small,
repository-local router at `.agents/skills/plumbline-router/SKILL.md`. It is
created only after explicit initialization approval. Removing that directory
stops automatic routing while leaving explicit skills available.

## Durable state

Small work stays in conversation. Broad or multi-session work may use one
approved repository-local shaping handoff, one active specification, and one
live checkpoint plan. The plan's compact resume record holds the current
checkpoint, status, lifecycle owner, last verified commit, and next safe action.

Canonical repository documentation describes the current system. Transient
specifications, plans, imported source, and handoffs are removed only through
accepted Closeout. Plumbline does not treat a conversation transcript or a
historical implementation plan as current product truth.

Failure is corrective state, not automatic abandonment. Review changes reopen
the affected checkpoint; missing or inconclusive evidence blocks it for
Diagnose. Execute and Closeout require all required checkpoints to be complete,
and a new successor objective requires acceptance or explicit user-approved
defer/abandonment.

Plans may explicitly select `execution_mode: checkpoint_relay`. Missing mode
means `continuous`, preserving the existing full-plan Execute behavior. Relay
uses the same host-neutral checkpoint and evidence rules but stops after one
completed checkpoint and durable handoff. A host with automatic fresh-root
capability may start the successor; other hosts use a supported manual boundary.
Host transport details remain outside shared lifecycle skills and repository
plans.

Automatic Relay consumes only a normalized Relay Execution Contract. The
internal plan-adoption engine preserves a sufficient external source and adds
the smallest companion execution record when needed; it does not reopen
settled product intent. A dependency-free readiness validator checks the
normalized plan, checkpoint transition inputs, source references, and Git
recovery boundary. It does not parse arbitrary external prose or perform Git
integration.

The host-neutral relay core contains no model call or host transport. It
acquires one host-local controller lock, consumes a Relay Ready normalized
plan, asks a capability adapter to start and observe one checkpoint, rereads
durable state, validates the transition, and either exposes a handoff/acceptance
boundary or pauses. Ambiguity never triggers an automatic engineering retry.

The Codex adapter is the only module that knows App Server operations. It uses
the supported stdio JSONL handshake, creates and names one fresh root thread,
discovers and explicitly injects the installed Plumbline front door, starts one
bounded turn, observes its terminal notification, records thread/turn identity
in host-local state, and unsubscribes. It does not choose checkpoints or
interpret product semantics.

For a relay-owned Codex task, the bundled `Stop` hook writes only a host-local
wake marker containing the matching task and turn identity. It is inert for
ordinary sessions and cannot edit the repository, advance the plan, inject a
prompt, or dispatch a successor. The locked relay controller consumes the
marker and rereads durable plan state; unchanged state waits for another user
turn, while an invalid mutation pauses.

Relay recovery compares repository identity and a Git/source/plan fingerprint,
reconciles a recorded Codex task through `thread/read`, and refuses duplicate
dispatch when task state is active or unknown. Dead-process locks may be
reclaimed; malformed or live locks remain fail-closed. Host-local pause/stop
controls and App Server failures never alter repository lifecycle state or
trigger an automatic engineering retry.

The automatic runner serially dispatches each legal successor checkpoint. A
structured checkpoint marker prevents a dispatched task from starting a nested
controller. After the final transition, the adapter creates one fresh
Acceptance task. That task reports the normal acceptance boundary and waits for
explicit user acceptance; if accepted, it performs Closeout in the same task
instead of adding a cosmetic final task.

## Agent-team boundary

Agent teams are optional and project-local:

- Codex uses selected `.codex/agents/*.toml` files and an optional
  `.codex/config.toml`. Current Codex releases enable subagents by default;
  Plumbline recommends a user-owned concurrency value of 6 only when the
  project records an explicit cap.
- Claude Code uses selected `.claude/agents/*.md` files with Claude-native
  model, effort, tool, and permission fields. Plumbline does not edit global
  Claude settings or enable the separate experimental Agent Teams feature.

The shared role contracts keep report-only roles without write sets; each
approved write-capable role receives only a bounded write set. Every worker
returns to the main thread, worker recommendations are advisory, and only the
main thread selects and dispatches the next capability. Workers do not own
Git, edit the active specification or plan, or spawn children. Codex
`sandbox_mode = "read-only"` and Claude `permissionMode: plan` express intent,
not guaranteed isolation from a writable parent session.

The main thread may dispatch a dependency-aware parallel wave for independent
research, architecture, QA, or implementation work only after the shared
contract is stable, scopes are disjoint, no result dependency exists, and a
clear join condition is known. Shared files, public interfaces, schemas,
migrations, generated artifacts, unstable contracts, and moving review deltas
remain serial. Results are classified and integrated at the main thread before
downstream work is dispatched; this is guidance, not a scheduler or graph
runtime.

For an approved Execute checkpoint, delegation is the default whenever an
approved project-local role can own useful bounded research, architecture,
implementation, review, testing, or another capability with a clear boundary.
The main thread dispatches that role before duplicating the work and preserves
its configured model, reasoning/effort, and sandbox/permission intent. Product
decisions, lifecycle/plan state, joins, integration, Git, singleton operations,
and tiny coupled actions remain direct. The active checkpoint resume record
carries `delegation_roles` and `delegation_status` so compaction restores this
obligation. A missing local role is an explicit direct fallback, not a user
pause.

## Ownership and worktrees

The main thread owns product decisions, active artifacts, integration, and
Git. Plumbline uses the host's managed worktree or handoff mechanism when one
exists, but it does not create, register, remove, or clean up worktrees.

The project-local installer keeps role files and routers ignored and untracked
unless the user chooses otherwise. An approved `.worktreeinclude` manifest can
propagate small local setup files to future managed worktrees when the host and
repository workflow support it; existing worktrees are not updated
retroactively.

## Validation boundary

Static validation and installer smoke tests cover manifests, skill contracts,
role-file generation, preservation behavior, and dry-run safety:

```bash
python scripts/validate.py
python scripts/test_install_agent_team.py
python scripts/test_install_claude_agent_team.py
git diff --check
```

These checks prove repository and workflow intent. They do not claim to prove
effective child permissions in every host session; that remains a bounded
interactive UAT concern.

Initialization is repeatable without being destructive. An explicit repeat
initialization may refresh only the marked Plumbline section in `AGENTS.md`.
The installer previews this as a guidance-only change and leaves roles and host
config untouched. Older unmarked sections require a separate explicit
replacement approval; text outside the managed section is preserved.
