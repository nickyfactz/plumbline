---
name: plumbline-agent-team
description: Initialize, audit, retune, or extend a repository-adapted Codex agent team without global installation.
---

# Agent Team

This skill is explicit only. Read the repository's `AGENTS.md`, `.codex/agents/`, `.codex/config.toml`, and any established agent conventions before proposing changes.

## Operations

- **Initialize:** propose only the missing roles from the five archetypes in `templates/agents/`.
- **Audit:** compare project agents with current repository docs and report stale facts, overlap, missing boundaries, and capability gaps.
- **Retune:** preserve working `model`, `model_reasoning_effort`, sandbox, permissions, MCP, and other user settings unless a concrete problem justifies a change.
- **Add:** add one specialist only for a demonstrated need; do not create a role for every technical layer.

Do not copy agents into global configuration, install a team automatically, or delete a competing role. Project-local `.codex/agents/*.toml` files are user-owned and require approval before creation or editing.

Inspect multi-agent settings such as `features.multi_agent`, `agents.max_depth`, and managed policy. If a setting blocks the approved operation, show one exact reversible patch and wait for approval.

Each generated agent must have a narrow `name`, `description`, and `developer_instructions`; it must cite repository paths rather than embedding mutable architecture. Implementers never own Git operations or active plan edits. QA auditors are report-only. Run only a bounded, read-only discovery smoke test after approval.
