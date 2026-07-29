# Artifact lifecycle

Plumbline uses four artifact classes:

1. Imported source - a design, handoff, attachment, or kickoff prompt from outside the repository. Preserve provenance and hash; treat it as immutable evidence.
2. Active specification - the approved product contract for the current feature. It is tracked, authoritative during execution, and amended only for explicit product decisions.
3. Live implementation plan - the execution control plane. It records checkpoints, owners, dependencies, evidence, blockers, deviations, and recovery state. Keep it current as work advances.
4. Canonical documentation - long-lived project-owned docs describing the repository's actual current system. It is not a diary and is not automatically replaced by a transient plan.

A repository-local shaping handoff is a pre-specification state of the active specification, not a fifth artifact class. After explicit user approval, it uses the repository's existing transient specification location, records only durable shaping decisions and concise research evidence, and is promoted in place when the specification phase begins. It is never a second active specification.

A throwaway Shape prototype is transient scratch evidence, not a fifth artifact class. Keep it clearly marked and out of production; record only its material finding in the existing handoff or specification, and never promote its code automatically.

Imported source, specs, and plans are transient. They may be removed at accepted closeout only after the user explicitly accepts the result and canonical docs contain the resulting truth. Git history must retain the deleted artifacts. Never use closeout to hide a disagreement between code and docs; investigate it and record the resolution.

Every process artifact, announcement, or receipt must support recovery, validation, authorization, or ownership. Omit it when it serves none of those purposes.
