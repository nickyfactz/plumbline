# Specification template

Describe behavioral proof obligations and acceptable evidence methods in the
testing strategy. Do not set test-count or coverage targets.

Use the repository's existing spec location and format when one exists. For a blank repository, use `docs/specs/<feature-slug>.md` and these headings:

```markdown
# <Feature> Specification
## Source and Status
## Product Outcome
## Users and Workflows
## Scope
## Non-Goals
## Domain Language and Invariants
## Required Behavior
## Design
## Non-Deterministic Outputs
## Failure and Recovery Behavior
## Compatibility, Data, Privacy, and Security Constraints
## Acceptance Criteria
## Testing and Acceptance Strategy
## Canonical Documentation Impact
## Decisions and Rejected Alternatives
## Assumptions and Residual Questions
```

**Design** is required before planning a non-trivial feature; a list of
features is not a design. State the components and their owners, the data and
control flow along the main paths, the boundary shapes between owners, and the
expected cost of the hot paths (what runs per request or per turn, and what
must stay off that path). It may link a separate design note instead. A later
design change updates this section first; the plan then re-plans the affected
checkpoints.

**Non-Deterministic Outputs** applies when behavior depends on a model or
another non-deterministic external system. Acceptance proves what was sent to
it and how its output is handled: parsed, validated, rejected, stored, or
shown. Output quality is a gate only when this section gives an explicit
threshold and sample size, and that gate belongs to the plan's final
checkpoint. Omit the section when no such dependency exists.

Numeric targets the user did not supply are marked `proposed` with their source
and confirmed by the user before planning treats them as acceptance.

State whether the source is imported, chat-derived, or repository-derived. Separate current behavior from target behavior. Write acceptance criteria as observable outcomes, not implementation tasks. Product amendments need an explicit decision and date; technical refinements do not need a new product question when they preserve behavior.
