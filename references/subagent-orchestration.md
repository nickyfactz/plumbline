# Subagent orchestration

Load this reference only when a delegation wave is materially useful. Execute keeps the dispatch invariant in its phase body and does not load this detailed doctrine for direct work.

## Lifecycle ownership

Record one owner in the active plan and report it only when ownership changes, a competing controller is selected, or the record is stale. Installed or enabled skills alone are not active ownership. One system owns checkpoint selection, plan advancement, review sequencing, and closeout for a task. If another explicitly selected orchestration loop already owns those responsibilities, do not stack a second lifecycle controller; use Plumbline only for the selected phase contract. When Plumbline owns the lifecycle, supporting skills may contribute bounded research, implementation, or review work but may not advance the plan or closeout independently.

## Selection and depth

Use only a matching project-local definition under .codex/agents/ after checking project .codex/config.toml. The global config may explain host capability, but personal/global agent files are never selected or used as fallback. If no local role is available, keep the work on the main thread and report Direct: <reason>. At a delegation wave, state the selected role names, configured model slugs, and reasoning efforts in one compact line.

Project agents.max_depth = 1 is the recommended ceiling. The main thread may create direct workers; workers must never create children, delegate further, or form a second agent hierarchy.

## Capability versus assignment

A role has two separate boundaries:

- Assignment: researcher, architect, and QA roles are report-only and receive no write set. A brief asking them to edit source, tests, scripts, documentation, or Git state is invalid and returns to the main thread.
- Capability: sandbox_mode = read-only is the role's intent. The parent goal may remain writable; the host can apply the parent's live permission state to the child. Do not claim hard read-only isolation from the TOML alone.

At each delegation wave, emit one compact line such as Delegated wave: researcher [model=<slug>, reasoning=<effort>] - Boundary: report-only; no write set; no child agents; include each selected role, configured values, and effective model/reasoning/sandbox values only when the host exposes a meaningful difference or the user asks. Add the report-only/no-write-set/no-child boundary to the wave report. Do not invent effective values. After a child returns, inspect Git status and the diff; unexpected edits are not silently integrated. Use Direct: delegation prohibited or effective read-only isolation unavailable when the task requires a hard read-only boundary that the host cannot provide.

## Worker briefs

Give each worker a context-bounded brief containing:

- the checkpoint outcome and acceptance criteria;
- the exact read set, anchored sections, and disjoint write set;
- relevant contract and repository paths;
- the current diff or last verified commit only when relevant;
- expected validation and report format;
- explicit limits: no Git operations, no active-plan edits, no unrelated cleanup.

Do not pass full conversation history or ask workers to reread entire instruction, plan, or documentation trees when the brief and unchanged artifacts already answer the question. Use the active plan's resume record and prior evidence first. A worker may widen its read set only when it identifies a concrete missing fact and reports why. Keep normal reasoning at the configured medium level; reserve high effort for a named ABI, security, persistence, concurrency, ownership, or other material risk, and never rewrite a project's approved TOML values at dispatch time.

For a checkpoint involving material state, persistence, concurrency, security, a public contract, or cross-language ownership transfer, give the applicable architect a compact risk-contract brief before implementation. Ask for only the relevant identities and ownership, state transitions and terminal precedence, failure/recovery/cancellation or shutdown behavior, compatibility constraints, proof seams, and unresolved assumptions. This is a conditional completeness check, not a universal checklist; do not dispatch an architect merely to fill it for mechanical or low-risk work.

Run independent work packages in parallel only after shared contracts are stable. Serialize any package that touches a shared file, public interface, schema, migration, or generated artifact. If a worker needs another file, pause and renegotiate ownership in the main thread.

Worker reports should name changed files, behavior, checks run, failures, residual risk, and follow-up without pasting large successful command logs. The main thread inspects and integrates the result, updates the plan, runs checkpoint verification, and summarizes evidence as command, outcome, counts or failure tail, and artifact path where applicable. Do not let agents create recursive agent organizations or write commits behind the main thread.

Review only after the implementer's bounded write set is integrated and the diff is stable. For a high-risk checkpoint, perform that first stable-delta review before the main thread makes material semantic repairs; return substantial corrections to the implementer or reopen the checkpoint instead of silently absorbing them. Classify a newly discovered issue as an implementation defect, contract gap, or environment/harness failure; a contract or ownership change reopens planning, while a small bounded defect may remain in Execute. Batch related evidence-only or packaging work into the parent checkpoint when it has no independent acceptance, rollback, risk, contract, or ownership boundary. Every process artifact, announcement, or receipt must support recovery, validation, authorization, or ownership; omit it otherwise.
