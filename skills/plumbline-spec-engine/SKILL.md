---
name: plumbline-spec-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects specification work.
---

# Specification engine

## Outcome and completion

Create or adopt one controlling product specification for the current task. A
specification is complete when it states the product outcome, users/workflows,
scope, non-goals, required behavior, constraints, acceptance/proof direction,
and remaining assumptions or residual questions clearly enough for planning.

## Adopt the strongest source

Assess sufficiency, not Plumbline conformance. Accept a user-supplied internal
or external design, handoff, attachment, or prior plan when it settles outcome,
users/workflows, scope, non-goals, behavior, constraints, and acceptance/proof.
Adopt it at the latest safe phase without replaying settled shaping.

When an artifact is sufficient for execution but lacks a separate specification
file, preserve the artifact. Do not require a separate file when the supplied
artifact is sufficient. Recommend a companion only when it materially
improves product clarity or recovery. Keep one controlling source for the task;
name competing candidates and ask the user to select one rather than silently
merging them.

Read `references/specification-template.md`,
`references/artifact-lifecycle.md`, and `references/product-autonomy.md` when
creating, adopting, or expanding a specification. Use the repository's
existing canonical/transient locations. For a blank repository, use
`docs/specs/<feature-slug>.md`.

## Adopt a shaping handoff

When an approved shaping handoff exists, promote it in place as the active
specification. Expand its compact headings into the existing specification
template instead of creating a competing file. Preserve decisions, research
findings and source links, open product questions, fog items, rejected
alternatives, and non-goals. Carry non-blocking fog into assumptions or
residual questions; leave it visible without blocking planning.

Materialize chat-only or attachment-only requirements before long-running work
when a durable record is needed. Preserve source and provenance, avoid
rewriting large or binary inputs wholesale, hash large inputs when appropriate,
and use a safe Markdown extraction when committing the original is unsafe.

## Resolve product questions only

Ask only blocking product questions, one at a time, with a recommendation. Technical
choices belong to the agent and should come from repository evidence, research,
conventions, and safe defaults. Record product amendments explicitly and keep
the approved source's intent intact.

When the controlling artifact is sufficient for the next phase, report the
adoption or companion recommendation once and direct the user to
`plumbline-plan` or `plumbline-execute`. Specification creates or adopts the
contract; it does not implement code.
