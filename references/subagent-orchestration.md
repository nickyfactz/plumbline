# Subagent orchestration

The main thread owns product intent, the active spec and plan, integration, and Git. Subagents are bounded workers or reviewers, not parallel project managers.

## Selection and depth

Use only a matching project-local definition under `.codex/agents/` after checking project `.codex/config.toml`. The global config may explain host capability, but personal/global agent files are never selected or used as fallback. If no local role is available, keep the work on the main thread or report the missing capability. State `Delegated: <role>` or `Direct: <reason>`.

Project `agents.max_depth = 1` is the recommended ceiling. The main thread may create direct workers; workers must never create children, delegate further, or form a second agent hierarchy.

Give each worker:

- the checkpoint outcome and acceptance criteria;
- the exact read set and disjoint write set;
- relevant contract and repository paths;
- expected validation and report format;
- explicit limits: no Git operations, no active-plan edits, no unrelated cleanup.

Run independent work packages in parallel only after shared contracts are stable. Serialize any package that touches a shared file, public interface, schema, migration, or generated artifact. If a worker needs another file, pause and renegotiate ownership in the main thread.

Worker reports should name changed files, behavior, checks run, failures, residual risk, and follow-up. The main thread inspects and integrates the result, updates the plan, runs checkpoint verification, and commits. Do not let agents create recursive agent organizations or write commits behind the main thread.
