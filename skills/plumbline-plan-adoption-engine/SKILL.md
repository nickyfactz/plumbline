---
name: plumbline-plan-adoption-engine
description: Internal Plumbline engine. Use only after Plan or Execute selects adoption of an explicit Checkpoint Relay artifact.
---

# Plan adoption engine

## Outcome

Given an otherwise sufficient external specification, plan, handoff, work
order, or equivalent controlling artifact, create one **smallest companion live plan** for deterministic Checkpoint Relay. Keep the **source as authority**;
this is structural adoption, not another product-planning phase.

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

Preserve checkpoint meaning and useful source structure. Carry only source-
supported product behavior and acceptance into one companion execution plan.

## Readiness and Git boundary

Run `node runtime/relay-readiness.js <plan>` from the plugin root. The validator
checks only normalized structure and repository durability; it never interprets
arbitrary source prose. `relay_ready: false` blocks automatic Relay.

The main lifecycle owner reviews the companion and establishes the coherent Git
recovery boundary. Stage and commit only the companion and its selected
repository-local sources. Re-run readiness after that boundary; start Relay
only when the plan and those sources are tracked and unchanged.

## Completion

Adoption is complete when exactly one checkable result exists:

- `relay_compatible`: readiness identifies the existing plan as Relay Ready;
- `adoptable`: one source-referencing companion reaches `relay_ready: true`
  after the main-owned Git boundary; or
- `insufficient`: no companion is created and the missing material contract or
  product decision is named.
