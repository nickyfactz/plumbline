---
name: plumbline-plan-adoption-engine
description: Internal Plumbline engine. Use only after Plan or Execute selects adoption of an explicit Checkpoint Relay artifact.
---

# Plan adoption engine

## Outcome

Given an otherwise sufficient external specification, plan, handoff, work
order, or equivalent controlling artifact, create the smallest companion live
plan needed for deterministic Checkpoint Relay. Preserve the source as
authority; this is structural adoption, not another product-planning phase.

In short: create the **smallest companion live plan** and keep the **source as authority**.

Use this engine only when the user explicitly selected `checkpoint_relay` and
the controlling source is semantically sufficient for execution but does not
satisfy the normalized Relay Execution Contract in
`references/checkpoint-relay.md` and `references/plan-schema.md`. Ordinary
continuous Execute remains artifact-agnostic and does not require adoption.

## Classify before writing

Choose exactly one result:

- `relay_compatible`: validate the existing plan without rewriting it;
- `adoptable`: the source settles objective, scope, meaningful checkpoint
  outcomes/dependencies, and proof, but needs a companion execution record;
- `insufficient`: return to normal Plan or Shape because a material contract or
  product decision is absent.

Do not treat missing Plumbline headings alone as semantic insufficiency. Do not
normalize vague prose optimistically merely to make Relay start.

## Materialize the smallest companion

For an adoptable source, keep the source unchanged and reference it by relative
path plus hash. Carry only the execution/recovery structure Relay needs:

- one objective and selected source set;
- `execution_mode: checkpoint_relay`;
- an enumerable checkpoint sequence with explicit dependencies and observable
  acceptance;
- exactly one current checkpoint and matching status;
- one legal `next_safe_action` that names the current checkpoint;
- explicit approval gates, blockers, residual risks, and non-goals already in
  the source;
- the compact resume and recovery fingerprint fields from the plan schema.

Preserve checkpoint meaning and useful source structure. Do not invent product
requirements, reopen settled architecture, replace the source with a lossy
summary, manufacture unsupported acceptance, or create a second specification.

## Readiness and Git boundary

Run `node runtime/relay-readiness.js <plan>` from the plugin root. The validator
checks only normalized structure and repository durability; it never interprets
arbitrary source prose. `relay_ready: false` blocks automatic Relay.

The main lifecycle owner, never the adoption engine or relay runner, establishes
the coherent Git recovery boundary after reviewing the companion. Do not commit
unrelated work. The operational rule is: **do not commit unrelated work**.
Re-run readiness after that boundary; do not start Relay until
the plan and its selected repository-local sources are tracked and unchanged.
