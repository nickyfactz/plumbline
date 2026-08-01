---
name: plumbline-offboard
description: Explain Plumbline's repository-local footprint and optionally remove selected activation files.
disable-model-invocation: true
---

# Offboard Plumbline

Read-only by default. Report whether `.agents/skills/plumbline-router/` exists, whether Plumbline-owned `.codex/agents/` or `.claude/agents/` files or local exclude lines exist, and which documents are project-owned rather than removable plugin residue.

The router directory is the single automatic kill switch. With explicit approval, remove only the selected router, matching local exclude entries, or clearly Plumbline-owned agent files. Do not delete canonical documentation, accepted implementation history, user agents, tests, source specifications, or plans by default. Explain that uninstalling the plugin removes the installed bundle but cannot clean a repository that the plugin does not own.
