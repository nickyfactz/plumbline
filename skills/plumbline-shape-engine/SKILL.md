---
name: plumbline-shape-engine
description: Internal Plumbline engine. Use only after the Plumbline router or a Plumbline phase wrapper selects product shaping.
---

# Shape engine

## Outcome and completion

Shape product intent without implementing it. Establish the smallest useful
understanding of the destination, users, behavior, scope, non-goals, evidence,
open product questions, and fog. Complete Shape when the next safe phase is
clear or the one material product question is presented with a recommendation,
alternatives, tradeoff, and default.

Writing an explicitly approved transient shaping handoff is documentation, not
implementation. Read canonical repository docs, current code, tests, and
configuration for facts before asking anything. Read
`references/product-autonomy.md` and `references/research-policy.md` when the
task involves product decisions or external evidence.

## Classify before asking

Start with a targeted, read-only repository pass. Classify unresolved items as:

- repository facts, resolved from the repository;
- external capability or design questions, answered with bounded research;
- user-owned product decisions, asked one at a time;
- vague future uncertainty, parked as fog.

## Use a decision frontier

For broad shaping, keep a lightweight decision map in the working context. Map
material product decisions, the facts or research they depend on, and fog that
is not yet question-shaped. Do not create a durable decision-tree artifact
unless the user approves the existing shaping handoff.

The **decision frontier** is the set of material user-owned decisions whose
prerequisites are settled. Select the highest-leverage frontier question for
the next turn. Keep one question at a time, even when several frontier
questions are independent; this preserves the user's attention and Plumbline's
bounded conversation. Hold downstream questions until their prerequisites are
known. Recompute the frontier after a material answer, repository fact, or
research finding.

Research facts rather than asking the user for them. Independent factual
research may run in parallel when its questions and join condition are clear;
the main thread integrates the findings before selecting the next product
question. When the frontier is empty, or only fog and non-blocking residuals
remain, move to the next safe phase instead of manufacturing more questions.

For a material capability or design question whose options are not settled,
research before asking the user to choose. Do not make the user know which
tools, products, libraries, or patterns exist.

Use the matching project-local `researcher` for a bounded report-only brief
when available. Otherwise research directly on the main thread. Never use a
personal or global agent as fallback. Research
returns evidence to the main thread; it does not edit files, specifications,
plans, Git state, or the handoff, and it does not spawn children. Use one
researcher by default. Parallelize only independent questions with a stable
question set and a clear main-thread join.

Return a sufficient option landscape rather than an exhaustive catalog. For
each useful finding, provide the source, implication, recommendation, realistic
alternatives, tradeoffs, and remaining uncertainty. Use official documentation,
standards, or source repositories for current technical claims; use reputable
product or design sources for patterns; record versions or retrieval dates when
freshness matters. Stop once the evidence supports the next safe product
question.

Ask only questions whose answers change product behavior, scope, user
experience, privacy/security, destructive handling, compatibility, material
cost, or another difficult-to-reverse outcome. Resolve technical boundaries,
names, module placement, test seams, and implementation details from evidence,
conventions, and safe defaults. Use this question shape:

Ask one question or one bounded batch at a time.

1. recommendation;
2. realistic alternatives;
3. product tradeoff;
4. default if the user has no preference.

When the frontier contains numerous independent questions, use a small batch
instead of serial turns. A normal batch contains two to four questions; reduce
it when the decisions are high-consequence or cognitively dense, and expand it
only when the user asks for a larger pass. Keep each question independently
answerable and label the response mapping clearly:

❓ **Q1** - **<question title>**: <question body and realistic choices>
➡️ **Recommendation:** <recommended answer and why>

Include the tradeoff and default for each question. Wait for the user's batch
answers, accept partial answers, then recompute the decision frontier. Keep
dependent questions for a later batch and use one question when answering one
choice would change the meaning of another.

## Delegated architect escalation

When an architect working inside an active goal discovers a material product
question, return a structured escalation to the main orchestrator. Include the
affected checkpoint and overall objective, the plain-language question, why it
changes behavior or acceptance, recommendation, alternatives, tradeoff,
default, whether the checkpoint is blocked, and safe independent work.

The child returns the escalation; it does not ask the user directly, end the
goal, replace the plan, or start another lifecycle. The main orchestrator uses
the existing Shape conversation only when needed, preserves the active goal and
plan, and records the answer or residual uncertainty. Block only the affected
checkpoint when the answer is genuinely required; continue independent work
where possible.

## Optional prototype probe

After local facts and necessary research, decide whether the remaining
uncertainty is experiential rather than factual. Offer a throwaway prototype
only when a small runnable probe is likely to answer a material question faster
than another planning round. Keep the smallest useful form:

1. conversation, worked example, or state sketch;
2. in-memory logic, state, or data probe;
3. isolated UI or interaction variant.

Ask for approval before writing a repository prototype. State the question,
proposed location, one existing run command, and that the probe is transient,
clearly marked, excluded from production, and has no persistence by default.
Reuse an existing handoff or scratch convention. A project-local implementer may receive a
narrow write set; otherwise the main thread runs the small probe directly. No
worker edits the shaping handoff or spawns children.

Keep the probe near the real seam but unfinished: no polish, production
abstractions, or broad test suite. Expose the relevant state or result and
leave a small smoke/run check. Report the question, observed result, decision,
and residual uncertainty. Record only the material finding in the existing
handoff's `Research Findings` or `Decisions Made`; promote a validated contract
into the one active specification, not the prototype code.

## Optional shaping handoff

Offer one repository-local shaping handoff only when clear signals show broad
or multi-session work: multiple workflows or product surfaces, several
independent material decisions, external research or prototyping, or an
explicit handoff need. Small or already-settled work stays in chat.

Explain why the work appears long-running, what the handoff contains, that it
will not capture every question or link, the chat-only alternative, and the
durability-versus-noise tradeoff. Create or edit it only after explicit
approval. If the user declines, continue in chat and do not repeat the offer
unless scope materially expands.

Use the repository's existing transient specification location; for a blank
repository, use `docs/specs/<feature-slug>.md`. Reuse an existing shaping
handoff or active specification. Use these compact headings:

`Source and Status`, `Destination`, `Scope and Non-Goals`, `Decisions Made`,
`Research Findings`, `Open Product Questions`, `Not Yet Specified (Fog)`,
`Out of Scope`, and `Next Phase`.

The main thread owns the handoff. Update it after a material user decision,
research that changes the option landscape, a scope/non-goal change, a fog item
becoming concrete, or a session/phase handoff. Keep minor technical choices,
raw transcripts, and exhaustive rejected options out of it.

Treat precise unresolved material questions as open product questions. Treat
vague or premature possibilities as fog. Fog does not block planning unless
the destination genuinely depends on it. Promote fog when it becomes precise
and material; otherwise resolve it, park it, or move it to `Out of Scope`.

When intent is sufficient, summarize settled outcome, scope, non-goals,
constraints, open questions, fog, research evidence, and acceptance direction.
Tell the user to use `plumbline-spec` when a durable contract is needed. Shape
may finish without creating files.
