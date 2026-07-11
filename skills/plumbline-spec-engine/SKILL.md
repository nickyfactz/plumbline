---
name: plumbline-spec-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects specification work.
---

# Specification engine

Create or adopt one active product specification. Read `references/specification-template.md`, `references/artifact-lifecycle.md`, and `references/product-autonomy.md` when available.

If the user supplied a design, handoff, attachment, or prior plan that already settles intent, adopt it at the latest safe phase. Do not re-grill settled decisions. Materialize chat-only or attachment-only requirements before long-running work. Preserve the original source and provenance; do not rewrite a large or binary input wholesale. Hash large inputs, avoid secrets, and use a safe Markdown extraction when committing the original would be unsafe.

Use the repository's existing canonical/transient locations. For a blank repository, default to `docs/specs/<feature-slug>.md`. Ensure there is only one active specification for the feature. Include outcome, users/workflows, scope, non-goals, domain language and invariants, required behavior, failure/recovery, compatibility/data/privacy/security constraints, acceptance criteria, testing/acceptance strategy, canonical-document impact, decisions/rejected alternatives, assumptions, and source/status.

Ask only blocking product questions, one at a time, with a recommendation. Technical choices belong to the agent. Record product amendments explicitly; do not silently change an approved source. Do not implement code. When the specification is sufficient, tell the user to run `$plumbline-plan`.
