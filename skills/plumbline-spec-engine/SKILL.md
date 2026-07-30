---
name: plumbline-spec-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects specification work.
---

# Specification engine

Create or adopt the controlling product specification for the current task. It may be a user-supplied internal or external design, handoff, attachment, or prior plan; do not require a generated file, path, frontmatter, or lifecycle vocabulary. Read references/specification-template.md, references/artifact-lifecycle.md, and references/product-autonomy.md when available.

First assess sufficiency, not Plumbline conformance. If the supplied artifact already settles outcome, users/workflows, scope, non-goals, behavior, constraints, and acceptance/proof, adopt it at the latest safe phase without re-grilling. If it is sufficient for execution but lacks a separate specification file, do not create a duplicate merely to satisfy Plumbline. Recommend a companion specification only when it materially improves product clarity or recovery. If product intent is materially unresolved, return to Shape for one blocking product question.

Materialize chat-only or attachment-only requirements before long-running work when a durable record is needed. Preserve original source and provenance; do not rewrite a large or binary input wholesale. Hash large inputs, avoid secrets, and use a safe Markdown extraction when committing the original would be unsafe.

Use the repository's existing canonical/transient locations when a repository artifact is warranted. For a blank repository, default to docs/specs/<feature-slug>.md. Select one controlling specification for this task; unrelated specifications are not blockers. If several competing candidates could control the same task, report the ambiguity and ask the user to select one rather than silently merging them.

When an approved shaping handoff already exists, adopt it in place and promote its status to the active specification. Expand its compact headings into the existing specification template instead of creating a second file. Preserve decisions, research findings and source links, open product questions, fog items, rejected alternatives, and non-goals. Carry non-blocking fog into assumptions or residual questions; do not block planning merely to eliminate uncertainty that does not affect the product outcome.

Ask only blocking product questions, one at a time, with a recommendation. Technical choices belong to the agent. Record product amendments explicitly; do not silently change an approved source. Do not implement code. When the controlling artifact is sufficient for the next phase, report the adoption or companion recommendation once and tell the user to use the explicit `plumbline-plan` or `plumbline-execute` skill as appropriate.
