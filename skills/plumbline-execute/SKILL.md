---
name: plumbline-execute
description: Execute an active Plumbline feature plan through all remaining checkpoints with evidence before advancement.
disable-model-invocation: true
---

# Execute

This is the explicit user-facing wrapper. Select the `plumbline-execute-engine` through the host's skill dispatcher when available. Otherwise read `../plumbline-execute-engine/SKILL.md` relative to this skill and follow it directly. Default to full-plan traversal in dependency order, using safe main-mediated parallel waves for ready independent work; pause only when the user explicitly requests checkpoint-by-checkpoint execution or an actual hard stop applies. Keep the main thread as the plan, delegation, and Git authority.
