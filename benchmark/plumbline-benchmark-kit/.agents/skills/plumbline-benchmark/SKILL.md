---
name: plumbline-benchmark
description: Run the compact Plumbline-versus-stock Codex execution benchmark from this controller repository, using isolated fresh sessions and evidence-based cost reports.
---

# Plumbline benchmark controller

You own the campaign, not the candidate implementations. Use `bench.py`; do not become an additional Plumbline orchestrator and do not solve the fixtures in this conversation.

## Read only the required controller guidance

Locate the kit root from this file. Read `START_HERE.md`, `docs/HOST_SETUP.md`, `config.example.json`, and `docs/TELEMETRY.md`. Use `docs/METHODOLOGY.md` when interpreting results. Do not preload reference solutions, grader source, or candidate solution transcripts into evaluation prompts.

## Prepare without asking routine setup questions

1. Run `python bench.py selftest`. Resolve a working Python 3.11+ executable and installed Codex executable locally. Run `python bench.py init-config`, preserving an existing local config. The user request selects pilot/full, root subset, repeat count, and whether a new or existing campaign is intended; default to the two-run pilot when no scope was selected. An explicit full-suite request means the 24-run full matrix, not an additional pilot campaign.
2. Perform HOST_SETUP's read-only discovery. Resolve exact current model IDs, native plugin installation, profile permissions, saved authentication, and the actual Ponytail implementer-only hook. Never invent model IDs, flatten all role efforts to medium, silently remove Ponytail, or copy the user's whole global agent configuration. Discover before asking. Native login/trust may require one user interaction; report the exact blocker and do not start paid work while it remains.
3. Configure only the dedicated benchmark state, auth source reference, and minimal Ponytail seed. For the current default comparison use `baseline_mode: stock`, continuous Execute, Standard speed, unchanged plugin-recommended workers, and the actual implementer-only hook. Validate the native hook receipt and negative controls. Never enable `audited-bypass` without the user's explicit approval of the exact audited hooks.
4. Confirm the user-visible configured limits once. Treat these as observed-spend guards, not exact invoice limits. Do not automatically raise caps or launch extra calibration requests. Any small host-only model probe belongs to disclosed setup overhead, not a hidden free run. Run `python bench.py doctor`.
5. Before freezing, record host setup evidence in `config.local.json` disclosures: Codex build, permission profile, hook identity/version, scope, activation/trust verification, model resolution, any supported adapter change, and unavailable account-debit telemetry. Model or provider changes require refreshed official rate evidence in a new dated pricing file. Never overwrite a historical price snapshot.
6. Run `python bench.py prepare --preset full` for the requested full matrix, or `--preset pilot` for the two-run pilot. Use `--models terra` and `--repeat 3` only when requested. Native initialization is done deterministically by the runner in disposable candidates; do not run a paid init conversation for every task.

## Execute one matched pair, then the remaining matrix

Run `python bench.py run --max-runs 2`. Use the host terminal's normal long-running command observation. If the tool wait expires while the process continues, attach to that process or inspect `status`/heartbeat. Never launch another controller on top of it.

Inspect first-pair evidence before continuing: native Plumbline activated, the approved local role profiles actually dispatched, reported root model/effort match configuration, the exact Ponytail hook affected only implementers, Git checkpoint operations worked, and all descendant usage reconciles to `complete-observed`. Check for native warnings about untrusted or skipped hooks, ignored settings, unsupported models/efforts, protected Git paths, or fallback roles.

Do not require the pilot task to pass before continuing: a valid measured coding failure is a result. Require the **harness and treatment to be valid**. Do not repair a candidate, rewrite a fixture to help it, or feed hidden failures back to the agent.

When the mechanics are valid and a full campaign was requested, run `python bench.py run` to continue the SAME campaign. Do not make a second pilot copy. The script skips finalized cells, enforces limits, writes intermediate reports, and stops on gaps. A telemetry/host repair changes the harness and needs a new frozen campaign; retain failed setup/runs as disclosed overhead. Do not erase earlier evidence.

If interrupted, inspect PID/state first. Use `recover` only after both controller and candidate are confirmed stopped. Recovery finalizes the interrupted attempt; it does not silently retry it. Ask for an explicit new campaign or repetition only when the user wants new attempts. Never poll a quiet worker to death.

## Report

Run `python bench.py report`. Import actual debits only through `import-charges` with authoritative per-run evidence; absence is `N/A`. Do not derive subscription dollars from tokens or a percentage bar. Keep controller/preflight/setup cost separate and disclose whether it could be measured.

Return the report paths and a compact account of paired verified passes, failure/timeout counts, observed all-attempt spend per verified completion, time, false claims, incomplete cost coverage, and the treatment disclosure. Distinguish statistical uncertainty, unmatched partial cohorts, and code-health diagnostics from measured quality improvements. Do not automatically buy judge-agent runs or add arms.

Use the raw report for numbers, not memory. Cite exact local evidence when explaining a failure. Do not claim Plumbline won merely because it delegated, generated more tests, used fewer tokens, or cost less on only its successful runs.
