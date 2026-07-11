---
name: plumbline-shape-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects product shaping.
---

# Shape engine

Shape product intent without implementing it. Read the repository's canonical docs, current code, tests, and configuration for facts before asking anything. Read `references/product-autonomy.md` and `references/research-policy.md` when available.

Ask one question at a time. Ask only when the answer changes product behavior, scope, user experience, privacy/security, destructive handling, compatibility, material cost, or another difficult-to-reverse outcome. Every question must include:

1. your recommendation;
2. the realistic alternatives;
3. the product tradeoff;
4. the default if the user does not care.

Resolve technical boundaries, names, module placement, test seams, and implementation details yourself from repository evidence. Keep the product outcome whole; do not split frontend, backend, persistence, or documentation into separate features.

When intent is sufficient, summarize the settled outcome, scope, non-goals, constraints, open product questions, and acceptance direction. Tell the user to run `$plumbline-spec` when a durable contract is needed. Shape may stop without creating files. If the user explicitly asks for a spec, continue only through the specification phase.
