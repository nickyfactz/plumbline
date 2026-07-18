# Subagent orchestration

The main thread owns product intent, the active spec and plan, integration, and Git. Subagents are bounded workers or reviewers, not parallel project managers.

## Lifecycle ownership

Before phase execution, state one owner in a line such as `Lifecycle owner: Plumbline Execute` or `Lifecycle owner: <explicitly selected controller>`. Installed or enabled skills alone are not active ownership. One system owns checkpoint selection, plan advancement, review sequencing, and closeout for a task. If another explicitly selected orchestration loop already owns those responsibilities, do not stack a second lifecycle controller; use Plumbline only for the selected phase contract. When Plumbline owns the lifecycle, supporting skills may contribute bounded research, implementation, or review work but may not advance the plan or closeout independently.

## Selection and depth

Use only a matching project-local definition under `.codex/agents/` after checking project `.codex/config.toml`. The global config may explain host capability, but personal/global agent files are never selected or used as fallback. If no local role is available, keep the work on the main thread or report the missing capability. At a delegation wave, state the selected role names, configured model slugs, and reasoning efforts in one compact line; use `Direct: <reason>` when no local role is available.

Project `agents.max_depth = 1` is the recommended ceiling. The main thread may create direct workers; workers must never create children, delegate further, or form a second agent hierarchy.

## Capability versus assignment

A role has two separate boundaries:

- **Assignment:** researcher, architect, and QA roles are report-only and receive no write set. A brief asking them to edit source, tests, scripts, documentation, or Git state is invalid and returns to the main thread.
- **Capability:** `sandbox_mode = "read-only"` is the role's intent. The parent goal may remain writable; the host can apply the parent's live permission state to the child. Do not claim hard read-only isolation from the TOML alone.

At each delegation wave, emit one compact line such as `Delegated wave: researcher [model=<slug>, reasoning=<effort>] — Boundary: report-only; no write set; no child agents`; include each selected role, configured values, and effective model/reasoning/sandbox values when the host exposes them. Add the report-only/no-write-set/no-child boundary to the wave report. Do not invent effective values. After a child returns, inspect Git status and the diff; unexpected edits are not silently integrated. Use `Direct: delegation prohibited or effective read-only isolation unavailable` only when the task requires a hard read-only boundary that the host cannot provide.

Give each worker:

- the checkpoint outcome and acceptance criteria;
- the exact read set and disjoint write set;
- relevant contract and repository paths;
- expected validation and report format;
- explicit limits: no Git operations, no active-plan edits, no unrelated cleanup.

Run independent work packages in parallel only after shared contracts are stable. Serialize any package that touches a shared file, public interface, schema, migration, or generated artifact. If a worker needs another file, pause and renegotiate ownership in the main thread.

Worker reports should name changed files, behavior, checks run, failures, residual risk, and follow-up. The main thread inspects and integrates the result, updates the plan, runs checkpoint verification, and commits. Do not let agents create recursive agent organizations or write commits behind the main thread.
