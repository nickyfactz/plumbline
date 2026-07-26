---
name: plumbline-shape-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects product shaping.
---

# Shape engine

Shape product intent without implementing it. Writing an explicitly approved transient shaping handoff is documentation, not implementation. Read the repository's canonical docs, current code, tests, and configuration for facts before asking anything. Read `references/product-autonomy.md` and `references/research-policy.md` when available.

## Classify and research before asking

Start with a read-only repository pass. Classify unresolved items as repository facts, external capability/design questions, user-owned product decisions, or fog. Resolve repository facts from the repository. For a material capability or design question whose options are not already settled, perform a bounded external research pass before asking the user to choose. Do not make the user know which tools, products, libraries, or patterns exist.

Use the matching project-local `researcher` for a bounded report-only brief when available; otherwise research directly on the main thread. Never use a personal or global agent as fallback. A researcher does not edit files, the active specification, or plan, run Git operations, or spawn children. Use one researcher by default and parallelize only genuinely independent questions.

Research should return a small sufficient option landscape, not an exhaustive catalog. Synthesize each useful finding with its source, implication, recommendation, realistic alternatives, tradeoffs, and remaining uncertainty. Use official documentation, standards, or source repositories for current technical claims; use reputable product or design sources for patterns; record versions or retrieval dates when freshness matters. Stop once the evidence is sufficient to formulate the next safe product question.

Ask one question at a time. Ask only when the answer changes product behavior, scope, user experience, privacy/security, destructive handling, compatibility, material cost, or another difficult-to-reverse outcome. Every question must include:

1. your recommendation;
2. the realistic alternatives;
3. the product tradeoff;
4. the default if the user does not care.

Resolve technical boundaries, names, module placement, test seams, and implementation details yourself from repository evidence. Keep the product outcome whole; do not split frontend, backend, persistence, or documentation into separate features.

Use existing handoffs, specifications, plans, and cited research as the source of settled knowledge. Do not replay a question or reread a whole artifact when its relevant section and evidence are unchanged. A new question or a fresh read needs a material trigger: changed scope or contract, relevant repository drift, a failed or newly relevant check, a new capability question, or stale evidence.

## Optional prototype probe

After local facts and any necessary external capability research, decide whether the remaining uncertainty is experiential rather than factual. Offer a throwaway prototype only when a small runnable probe is likely to answer a material question faster than another planning round. Do not prototype settled implementation details, and do not make the probe a mandatory Shape step.

Use the smallest useful form, in this order:

1. a conversation, worked example, or state sketch when that is enough;
2. an in-memory logic/state/data probe for transitions and behavior;
3. an isolated UI or interaction variant when the question is visual or experiential.

Ask for approval before writing a repository prototype. State the question, proposed location, one existing run command, and the fact that it is clearly marked, transient, excluded from production, and has no persistence by default. Reuse an existing scratch convention; do not create a new skill, persona, dependency, worktree system, branch, tracker entry, or artifact type. A project-local implementer may receive a narrow write set; otherwise the main thread can run a tiny probe directly. No worker edits the shaping handoff or spawns children.

Keep the probe near the real seam but deliberately unfinished: no polish, production abstractions, or broad test suite. It must expose the relevant state or result and leave a small smoke/run check. Afterward report the question, observed result, decision, and residual uncertainty. Record only the material finding in the existing handoff's `Research Findings` or `Decisions Made`; promote a validated contract into the one active specification and do not automatically promote prototype code.

## Optional shaping handoff

Conservatively detect long-running work from clear signals such as multiple workflows or product surfaces, several independent material decisions, external research or prototyping, or an explicit multi-session/handoff need. Do not use a complexity score and do not offer a handoff for small or already-settled work.

When the signals are clear, offer one repository-local shaping handoff before creating it. Explain why the work appears long-running, what the handoff will contain, that it will not capture every question or research link, the option to keep the work in chat, and the durability-versus-noise tradeoff. Create or edit the handoff only after explicit approval. If declined, continue in chat without repeatedly offering it unless the scope materially expands.

Use the repository's existing transient specification location; for a blank repository, default to `docs/specs/<feature-slug>.md`. Reuse an existing shaping handoff or active specification instead of creating a parallel file. The shaping handoff uses these compact headings: `Source and Status`, `Destination`, `Scope and Non-Goals`, `Decisions Made`, `Research Findings`, `Open Product Questions`, `Not Yet Specified (Fog)`, `Out of Scope`, and `Next Phase`.

The main thread owns the handoff. Update it only after a material user decision, research that changes the option landscape, a scope or non-goal change, a fog item becoming concrete, or a session/phase handoff. Do not record minor technical choices, raw transcripts, or exhaustive rejected options.

Treat concrete unresolved material questions as open product questions. Treat vague, premature, or not-yet-question-shaped possibilities as `Not Yet Specified (Fog)`. Fog does not block planning unless the destination genuinely depends on it. Promote fog only when it becomes precise and material; otherwise resolve it, keep it parked, or move it to `Out of Scope`.

When intent is sufficient, summarize the settled outcome, scope, non-goals, constraints, open product questions, fog, research evidence, and acceptance direction. Tell the user to run `$plumbline-spec` when a durable contract is needed. Shape may stop without creating files. If the user explicitly asks for a spec, continue only through the specification phase.
