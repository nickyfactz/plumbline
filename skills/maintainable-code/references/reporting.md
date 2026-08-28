# Audit reporting

Use before producing the final report.

## Report findings, not preferences

Every finding must include:

**[Severity] Title**

- **Location:** exact file/symbol/line or path
- **Evidence:** what the reviewer observed
- **Why it matters:** concrete maintenance, correctness, testability, operability, or performance consequence
- **Change pressure:** the kind of future change that will be expensive or risky
- **Refactor direction:** smallest credible design direction; avoid prescribing a rewrite unless necessary
- **Safety/validation:** tests, characterization, profiling, migration, or rollout needed
- **Confidence:** high / medium / low, especially when runtime behavior or intended ownership is uncertain

## Cite structure precisely

Prefer evidence such as:

- “retry policy is independently encoded in three call paths”
- “this orchestrator owns scheduling, persistence, worker lifecycle, and user status formatting”
- “changing one state value requires edits to the enum, parser, database mapper, UI mapping, and retry switch”
- “the helper has four caller-specific flags and seven branches; callers no longer share one abstraction”
- “the only coverage is an end-to-end test that does not assert this failure path”

For human-legibility findings, cite the cognitive consequence: hidden happy path, dense mixed operations, excessive navigation, generic naming, or abstraction-level jumps. Do not elevate brace/blank-line preferences into design findings.

Avoid weak claims such as:

- “too long”
- “not SOLID”
- “should use dependency injection”
- “bad naming”
- “too many comments”
- “duplicate code violates DRY”

Explain the consequence.

## Separate categories

Keep these distinct:

- **Defect:** behavior appears incorrect now
- **Design debt:** behavior may be correct, but future change is unnecessarily expensive/risky
- **Test debt:** behavior cannot be changed with sufficient confidence
- **Performance risk:** execution shape is plausibly costly and needs measurement or redesign
- **Human-legibility debt:** source shape materially increases the effort required to scan, understand, or safely modify correct behavior
- **Style/nit:** local preference with little architectural consequence

Do not elevate style into design debt.

## Prioritization

Rank by expected maintenance value:

`priority ≈ impact × likelihood of future pressure × breadth of affected code × change risk`

Use rough qualitative judgment, not fake numerical precision.

Prefer a small number of root-cause findings that explain many symptoms. If six local smells all arise from one missing boundary, report the boundary as the primary finding and list the smells as evidence.

## Executive summary

For a post-implementation audit, end with:

1. overall maintainability assessment
2. highest-leverage refactors
3. areas that should remain unchanged despite superficial smells
4. prerequisite tests/benchmarks before refactoring
5. recommended order of work
