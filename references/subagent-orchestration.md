# Subagent orchestration

The main thread owns product intent, the active spec and plan, integration, and Git. Subagents are bounded workers or reviewers, not parallel project managers.

Give each worker:

- the checkpoint outcome and acceptance criteria;
- the exact read set and disjoint write set;
- relevant contract and repository paths;
- expected validation and report format;
- explicit limits: no Git operations, no active-plan edits, no unrelated cleanup.

Run independent work packages in parallel only after shared contracts are stable. Serialize any package that touches a shared file, public interface, schema, migration, or generated artifact. If a worker needs another file, pause and renegotiate ownership in the main thread.

Worker reports should name changed files, behavior, checks run, failures, residual risk, and follow-up. The main thread inspects and integrates the result, updates the plan, runs checkpoint verification, and commits. Do not let agents create recursive agent organizations or write commits behind the main thread.
