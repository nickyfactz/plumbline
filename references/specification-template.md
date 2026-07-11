# Specification template

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
## Failure and Recovery Behavior
## Compatibility, Data, Privacy, and Security Constraints
## Acceptance Criteria
## Testing and Acceptance Strategy
## Canonical Documentation Impact
## Decisions and Rejected Alternatives
## Assumptions and Residual Questions
```

State whether the source is imported, chat-derived, or repository-derived. Separate current behavior from target behavior. Write acceptance criteria as observable outcomes, not implementation tasks. Product amendments need an explicit decision and date; technical refinements do not need a new product question when they preserve behavior.
