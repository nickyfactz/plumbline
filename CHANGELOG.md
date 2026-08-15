# Changelog

## Unreleased

- Replace the legacy Codex v1 delegation workaround with current `agents.enabled` and `agents.max_concurrent_threads_per_session` settings; migrate old `features.multi_agent`, `agents.max_threads`, and `agents.max_depth` entries only after approval.
- Treat Luna and other legacy-compatible models as v2 leaf workers selected by their project-local role files, while keeping Plumbline's no-child rule as orchestration guidance rather than a host depth requirement.
- Add explicit `checkpoint_relay` execution mode with Git-backed plan readiness, fresh Codex tasks per checkpoint, host-local wake/recovery state, duplicate protection, and a final explicit Acceptance task.
- Preserve continuous Execute as the default and provide a manual fresh-conversation boundary for Claude Code and unsupported hosts without loading the Codex App Server adapter.
- Add deterministic relay, hook, adapter, restart, fingerprint, pause/stop, acceptance, and native two-checkpoint UAT coverage.
- Make useful bounded Execute delegation the default for available project-local roles across research, architecture, implementation, review, testing, and future capabilities while preserving direct main-thread ownership for lifecycle and tightly coupled work.
- Persist delegation roles/status in the active checkpoint resume record and restore the obligation after compaction or conversational resume.
- Align generated Codex/Claude guidance and the optional continuity reminder with approved project-local role selection and configured model/reasoning values.
- Add an explicit repeat-initialization refresh for the managed `AGENTS.md` section. Preview and apply it without replacing roles or config; require separate approval for legacy unmarked sections and preserve content outside the managed block.
- Restore non-terminal failure handling: `CHANGES_REQUIRED` reopens the same checkpoint, inconclusive/environment/harness failures block it for Diagnose, and unresolved checkpoints cannot complete Execute or Closeout.
- Require a minimum sufficient root-cause trace for blockers, regressions, repeated failures, and failed expensive gates before another correction cycle; keep trivial local fixes lightweight when their local cause is confirmed.

## 0.1.15 - 2026-08-12

- Add an optional Codex/Claude lifecycle hook that restores Plumbline awareness after resume or compaction only when the front door was explicitly invoked earlier in the same session and repository.
- Keep hook state host-local, avoid repository artifacts and global configuration, and preserve the inert-install/front-door-only boundary.
- Add validator and smoke-test coverage for explicit activation, session/repository isolation, and deactivation.

## 0.1.14 - 2026-08-08

- Allow Shape to batch two to four independent frontier questions with numbered `❓` prompts and `➡️ Recommendation` lines while preserving one-at-a-time handling for dependent or high-consequence decisions.
- Accept partial batch answers and recompute the frontier before the next shaping round.

## 0.1.13 - 2026-08-08

- Add a lightweight Shape decision frontier inspired by dependency-aware grilling: ask one highest-leverage product question at a time, defer dependent questions, and stop when only fog or non-blocking uncertainty remains.
- Keep grilling bounded and project-agnostic; no durable decision tree, exhaustive interview, or universal confirmation gate is introduced.

## 0.1.12 - 2026-08-08

- Add lightweight vertical-slice planning guidance with explicit checkpoint completion conditions and prerequisite handling.
- Add plain-language recovery guidance for confused users and single-owner guidance for deterministic build, deploy, restart, migration, and publication operations.
- Rewrite phase-engine instructions for progressive disclosure, anchored context reuse, explicit outcomes, and source-of-truth references without adding a new workflow or artifact type.
- Clarify agent-team and setup completion evidence while preserving main-thread dispatch, fresh-worker, parallel-wave, and user-owned host configuration boundaries.

## 0.1.11 - 2026-08-04

- Prefer fresh worker contexts for independent assignments and fresh QA for materially changed deltas.
- Batch same-seam corrective fixes before repeating expensive runtime gates.
- Add proportional runtime preflight, bounded observation, runtime-state capsule, and singleton-operation ownership guidance.

## 0.1.8 - 2026-08-01

- Add a Claude Code project-local agent-team adapter using shared role instructions and native Markdown subagent fields.
- Preserve Claude model, effort, permission, custom fields, and instructions during audit/retune; never edit global Claude settings or enable experimental Agent Teams.
- Document the Codex multi-agent compatibility setting and its role in dispatching explicit Luna-based project agents.

## 0.1.7 - 2026-08-01

- Make approved multi-checkpoint Execute runs complete the plan serially by default, while preserving explicit checkpoint-by-checkpoint control.
- Refresh the plugin icon and document the exact project-local Codex setup changes made by initialization.
- Clarify the architect-to-Shape product-question boundary and preserve active long-running goals during delegated escalation.
- Add conditional scenario-to-proof matrices, proportional QA ordering, and validation failure-origin classification.
- Add behavior fixtures for technical/product ambiguity, Fog, imported artifacts, environment failures, and checkpoint-local blocking.

## 0.1.3 - 2026-07-29

- Support convention-mode phase work without initialization or generated Plumbline artifacts.
- Adopt sufficient external specifications, plans, handoffs, and work orders without duplicate lifecycle files.
- Add conditional artifact-sufficiency preflight, ambiguity reporting, plan-state checks, open-item classifications, and timestamped rolling-evidence guidance.

## 0.1.2 - 2026-07-29

- Add fingerprint-based resume guidance so unchanged execution reuses prior evidence.
- Lazy-load detailed delegation doctrine while retaining one-line role/model/reasoning telemetry and worker boundaries.
- Add compact checkpoint cards, conditional kickoff commits, evidence-path reuse, and an explicit Execute/Closeout boundary.
- Add a ceremony budget so artifacts and announcements must serve recovery, validation, authorization, or ownership.

## 0.1.1 — 2026-07-26

- Adopt complete work orders without replaying settled planning.
- Add bounded worker-context guidance and quieter delegation reporting.
- Add an optional, explicitly approved Shape prototype probe for behavioral uncertainty.
- Add proportional light/full closeout guidance and safer existing-router dry-run previews.

## 0.1.0 — 2026-07-11

- Initial Plumbline v1 implementation.
- Added explicit phase skills, internal routing engines, shared references, and repository-local activation guidance.
- Added a repo marketplace, original branding, validation script, router installer, agent templates, and migration notes.
