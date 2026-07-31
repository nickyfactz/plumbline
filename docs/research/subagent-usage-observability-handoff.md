# Subagent Usage Observability — Research Handoff

## Source and Status

- Status: read-only research recommendation; no monitor implementation is authorized by this artifact.
- Date: 2026-07-31.
- Source: bounded Plumbline/model-routing analysis and current Codex usage-monitor boundaries.
- Confidence: medium for the opportunity, low for any field whose availability in rollout events has not yet been fixture-tested.

## Destination

Codex Usage Runway Monitor research and design review. Keep the monitor generic for any user who employs subagents; Plumbline is one optional enrichment source, not a dependency.

## Scope and Non-Goals

This handoff explores whether subagent lifecycle, model, reasoning, cost, and outcome data can become a first-class usage signal. It should help distinguish justified additional work from avoidable orchestration cost.

It does not request:

- a Plumbline runtime integration or shared product dependency;
- automatic changes to model or reasoning settings;
- reading private prompts, responses, source files, commands, or credentials in the passive monitor;
- causal claims from subagent counts alone;
- a repository artifact or transcript diary for every delegation.

## Observed Problem

The current optimization evidence can show that a lower-cost model eventually converged, but it cannot reliably separate:

- useful delegated work from duplicate work;
- implementer defects from missing contract requirements;
- main-thread repairs from worker remediation;
- early QA findings from final acceptance confirmation;
- model cost from environment or harness rerun cost.

That limits Pareto decisions. A subagent can increase raw usage while reducing total accepted-work cost, so the useful comparison is cost against accepted outcome and rework, not subagent count.

## Current Monitor Boundary

The existing usage monitor intentionally reads normalized snapshots and does not inspect rollout JSONL, prompts, responses, skill bodies, commands, source files, or credentials. That privacy boundary should remain intact for the passive scheduled run.

The first research question is therefore observability, not implementation:

1. Which native structured events expose subagent identity, role/type, model, reasoning effort, lifecycle, parent relationship, and per-agent usage?
2. Which fields are absent, ambiguous, cumulative, or only available in a raw rollout?
3. Can a fixture prove attribution without reading user content?
4. Can parent and child usage be counted without double-counting shared or cumulative token snapshots?

An unavailable field must remain `not exposed` or `unknown`, never be interpreted as measured zero.

## Recommended Generic Event Shape

Prefer native structured fields first. If a normalized record is needed, keep it provider-neutral and allow optional fields:

```json
{
  "schema_version": 1,
  "session_id": "opaque-session-id",
  "parent_thread_id": "opaque-parent-id",
  "agent_id": "opaque-agent-id",
  "parent_agent_id": null,
  "agent_type": "implementer",
  "role_name": "implementer",
  "model": "provider-model-slug",
  "reasoning_effort": "medium",
  "sandbox_intent": "workspace-write",
  "write_set_declared": true,
  "depth": 1,
  "lifecycle": "completed",
  "started_at": "timestamp",
  "finished_at": "timestamp",
  "usage": {
    "input_tokens": 0,
    "cached_input_tokens": 0,
    "output_tokens": 0,
    "reasoning_output_tokens": 0
  },
  "outcome": "accepted|remediated|reopened|failed|unknown",
  "evidence_bookmark": {
    "source_file_hash": "hash",
    "byte_offset_start": 0,
    "byte_offset_end": 0
  }
}
```

The schema should not require Plumbline fields. `role_name`, `sandbox_intent`, `write_set_declared`, `outcome`, and checkpoint identifiers are optional enrichment because other agent workflows will use different concepts.

## High-Value Derived Metrics

Start with metrics that can be explained and audited:

- delegated tasks by agent type, model, and reasoning effort;
- first-pass completion and first-pass acceptance rate;
- remediation turns per task;
- parent-thread intervention count, when observable;
- QA findings before versus after main-thread intervention;
- reopened checkpoints or equivalent retry/review transitions;
- elapsed time and gate reruns;
- input, cached-input, output, and reasoning tokens by agent and wave;
- cost per accepted bounded outcome;
- main-repair share: main-thread repairs divided by all observed repairs;
- QA-before-intervention rate;
- task-class cohorts such as research, mechanical, stateful, security, architecture, and QA.

Do not infer “bad delegation” from a high subagent count. Flag possible efficiency degradation only when comparable cohorts show higher normalized cost or rework without a proportional accepted-work increase, and retain the correlation-not-causation caveat.

## Visual Design Recommendations

Make subagents a first-class tracked item without replacing the existing quota/runway view:

1. **Delegation timeline:** parent turn, delegation waves, agent start/finish, review, remediation, and closeout transitions.
2. **Agent tree or wave graph:** parent-to-child relationships, depth, role/type, model, and reasoning effort. A flat list loses orchestration shape.
3. **Cost and work waterfall:** main thread, implementers, researchers, architects, QA, remediation, and environment reruns against one accepted outcome.
4. **Model/reasoning cohort table:** acceptance, remediation, elapsed time, normalized usage, and sample count. Suppress conclusions for small samples.
5. **Cost-versus-work scatter:** normalized cost on one axis, observable accepted work on the other, with task class and confidence visible.
6. **Workflow pressure panel:** compactions, repeated delegation, reopened checkpoints, direct main-thread repairs, and late QA as separate signals rather than one score.

Every chart should expose sample counts, retrieval window, missing-signal caveats, and evidence bookmarks. A visual “cost increase” should never imply that the plugin caused it without comparable cohort evidence.

## Integration Options

### Option A — Passive native parser (recommended first)

Extend rollout parsing only for stable structured subagent lifecycle and usage fields. Keep the current passive monitor contract and add fixtures before changing the dashboard. This has the smallest coupling and tests whether the data exists at all.

### Option B — Optional workflow enrichment

Allow workflow tools such as Plumbline to emit compact, opt-in, normalized receipts for role, task class, checkpoint, review timing, and outcome. The monitor may consume them when present but must work without them. Do not make Plumbline import the monitor or require its files.

### Option C — Shared orchestration contract

Define a provider-neutral event contract only after Option A shows that native events cannot answer the questions. This is the most capable option and the highest coupling risk; it should not be the starting point.

## Privacy, Attribution, and Accounting Constraints

- Preserve the passive monitor's prohibition on raw prompts, responses, source, commands, and credentials.
- Prefer opaque identifiers, hashes, offsets, and counts over content.
- Distinguish per-response usage from cumulative snapshots; never sum cumulative totals twice.
- Treat parent context and child context as separate only when the runtime proves separate billing/usage records.
- Keep model and reasoning values as telemetry, not policy. The monitor reports usage; the user decides whether to retune a team.
- Record environment and harness failures separately from model or workflow defects.
- Use `not exposed`, `unknown`, and `insufficient evidence` explicitly.

## Suggested Research Sequence

1. Build synthetic fixtures for every candidate subagent event and prove parser behavior, parent/child attribution, cumulative-token handling, and missing-field semantics.
2. Run a read-only sample against a small, explicitly selected set of rollout files if the user opts into that deeper analysis; do not broaden the passive scheduled task silently.
3. Compare whether the native fields support the high-value metrics above without workflow-specific assumptions.
4. Add a compact normalized data block and one timeline/tree view only after the evidence schema is stable.
5. Evaluate a Plumbline enrichment receipt separately from the generic parser; keep it optional.

## Open Questions (Fog)

- Does the current Codex rollout schema expose child model and reasoning effort separately from the parent turn context?
- Are child token counts directly attributable, or must they be reconstructed from separate rollout files?
- How are shared cached-input tokens and compaction costs charged across parent and child sessions?
- Can lifecycle events identify “first pass,” remediation, QA, and accepted outcome without reading natural-language reports?
- Which generic observable work proxy is defensible across coding, research, review, and non-Plumbline workflows?
- What minimum sample size should suppress a model/reasoning comparison?

## Next Phase

The receiving scheduler/monitor thread should first assess the art of the possible from current structured events and fixtures. It should return a small schema proposal, known limitations, and one visual prototype recommendation before any implementation or Plumbline integration is considered.
