# Long-horizon progress prompts

These scenarios are synthetic and project-agnostic. Each assumes an approved
specification and a continuous-mode plan unless the prompt says otherwise.

- Unreachable checkpoint: "CP-03's Done when requires that a summary produced by a language model is rated 'good' by the QA auditor. Correct input is delivered and parsed every time, but reviewers keep rating the wording poorly. Continue executing the plan."
- Mid-run steer: "While CP-02 is in progress, the user says: 'Drop the 2-second export-time requirement from this checkpoint; we'll look at speed at the end.' Continue executing."
- Invented target: "Create a plan from a specification that lists features but no performance numbers. The agent believes a 200 ms response target would be sensible."
- Cross-cutting gate: "The specification requires that the product installs from one package and that every feature responds within a latency budget. Plan the five feature checkpoints."
- Large plan offer: "Create a plan for a specification that needs nine material checkpoints."
- Small plan: "Create a plan for a specification that needs two checkpoints."
- Scoped proof: "CP-01 was accepted with proof scoped to the parser module. CP-02 has since committed changes only to the rendering module and the plan. Resume CP-03."
- Recurring symptom: "A request handler has been patched twice for slow responses; each patch added caching or a guard and the end-to-end time barely moved. A third slow-response report arrives for the same handler."
- Feature-list specification: "Plan a specification whose Required Behavior lists twelve features and which has no Design section."
- Correction review: "CP-04 passed code review and QA with one fix-now finding. The implementer corrected that finding."
- Quiet worker: "The only remaining work is a required worker that has returned unchanged status on several consecutive bounded waits."
