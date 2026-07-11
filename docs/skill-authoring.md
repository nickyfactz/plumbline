# Skill authoring

Keep each public skill small enough to scan. Put stable cross-phase doctrine in one `references/` file and point to it from the phase that needs it. Do not repeat the same policy in every skill.

Public wrappers are user-facing and explicit. Internal engines are only for the router or wrapper to select; their descriptions say that plainly. The local router stays under 180 words and performs classification only. It must not preload all phase instructions.

When changing a skill:

1. state the user-visible behavior change;
2. update the smallest owning skill or reference;
3. update a fixture/prompt if the routing contract changed;
4. run `python scripts/validate.py`;
5. check that the skill still has one clear job and no hidden bootstrap.

Avoid mandatory ceremonies, copied repository facts, speculative abstractions, global installers, and tests that freeze wording or private structure. The best skill is the shortest one that reliably changes the desired behavior.
