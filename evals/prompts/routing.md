# Routing prompts

- Direct: "Fix the spelling mistake in README.md."
- Contract-complete direct: "The work order below already defines the scope, acceptance checks, current checkpoint, and closeout. Implement CP-02 without re-planning."
- Shape: "I want a new customer approval workflow, but I have not decided how it should behave."
- Shape research: "I want to add offline sync, but I do not know what options or product patterns are available."
- Shape fog: "Maybe this should support every future enterprise workflow, but I cannot say what that means yet."
- Shape handoff: "This approval platform will span several workflows and sessions; help me keep a durable shaping handoff."
- Shape prototype: "I am unsure whether this approval flow should be a reducer or a sequence of guarded transitions. Research any relevant options, then tell me whether a tiny throwaway probe would answer the behavior question faster."
- Plan: "Here is an approved design document. Create the implementation checkpoints without redoing product shaping."
- Execute: "The active spec and plan are ready. Implement the plan through all remaining checkpoints in serial order."
- Diagnose: "The import command started failing after yesterday's change. Find the root cause."
- Review: "Audit this completed diff for missing behavior and security problems."
- Closeout: "UAT passed. Reconcile the docs and finish the accepted change."
