# How to use Plumbline

The [README](../README.md) is the quick start. This page covers the exact installation paths and the optional choices that matter once you want Plumbline to work across a repository.

## Two separate decisions

Plumbline has two independent parts:

1. Install the plugin in Codex or Claude Code so the workflows are available.
2. Optionally initialize a repository if you want automatic routing, a project-local team, or both.

Installing the plugin does not change the repository. Initialization is a separate, explicit choice.

## Install in Codex

### Codex CLI

Add the GitHub marketplace, then install Plumbline:

```bash
codex plugin marketplace add nickyfactz/plumbline@main
codex plugin add plumbline@plumbline
```

Start a new Codex session after installation.

To use the plugin browser from the CLI, open Codex and run `/plugins`, then choose the `plumbline` marketplace and install **Plumbline**. The same browser is available in the Codex desktop app.

### Codex desktop

Open the repository as a project and select the **Codex** surface. Open **Plugins**, choose the `plumbline` marketplace, and install **Plumbline**. Start a new chat afterward.

If the marketplace is not visible, restart Codex after opening the project. You can also use the CLI commands above as a fallback.

### Local checkout

From a checkout of this repository:

```bash
codex plugin marketplace add .
codex plugin add plumbline@plumbline
```

See the [Codex plugin documentation](https://learn.chatgpt.com/docs/plugins) if the plugin or marketplace labels differ in your installed version.

## Install in Claude Code

### Claude Code CLI

Add the GitHub marketplace, then install Plumbline:

```bash
claude plugin marketplace add nickyfactz/plumbline@main
claude plugin install plumbline@plumbline
```

Reload the current session with `/reload-plugins`, or start a new session.

### Claude desktop

Open the repository in the **Code** tab. Select the **+** beside the prompt, choose **Plugins**, then **Add plugin**. If the Plumbline marketplace is already configured, select **Plumbline** and install it at the scope you prefer.

If the marketplace is not listed, run these commands from the Claude Code session:

```text
/plugin marketplace add nickyfactz/plumbline@main
/plugin install plumbline@plumbline
/reload-plugins
```

### Local checkout

From a checkout of this repository:

```bash
claude plugin marketplace add .
claude plugin install plumbline@plumbline
```

See the [Claude desktop plugin guide](https://code.claude.com/docs/en/desktop) and [Claude marketplace guide](https://code.claude.com/docs/en/discover-plugins) if the labels differ in your installed version.

## Make your first request

Open the repository you want to work on, then invoke Plumbline's front door:

- Codex: `$plumbline`
- Claude Code: `/plumbline:plumbline`

Start with the result you want, not a workflow name. Include any guardrails and point to notes that already exist.

A feature request might look like this:

```text
$plumbline Add import/export for the project configuration. Keep the existing format compatible. The design notes are in docs/configuration.md.
```

A bug report might look like this:

```text
/plumbline:plumbline Diagnose why webhook deliveries retry forever. Keep the public API unchanged and show me the evidence before changing code.
```

If you already have a plan, design, specification, handoff, or work order, name it directly:

```text
$plumbline Use docs/plans/payment-retry.md as the plan for this task. Check whether it is ready to execute and tell me what, if anything, is still missing.
```

You do not need to create a Plumbline document first. Plumbline can use a sufficient document from another tool or an earlier conversation.

## Let Plumbline choose the amount of process

The front door chooses the smallest suitable path:

| Path | Use it when |
| --- | --- |
| Direct | The task is small, clear, and low risk. |
| Diagnose | Something is broken, regressed, slow, or failing. |
| Shape | You need to decide what the product or behavior should be. |
| Specification | The intended behavior needs a precise, shared description. |
| Plan | The work is understood but needs safe steps and checkpoints. |
| Execute | A sufficient plan or work order is ready to carry out. |
| Review | You want an independent check of an implementation. |
| Closeout | Accepted work needs reconciliation or cleanup of temporary material. |

Most users only need the front door. These are the public side doors for cases where the path is already known:

| Purpose | Codex | Claude Code |
| --- | --- | --- |
| Initialize or reassess setup | `$plumbline-init` | `/plumbline:plumbline-init` |
| Settle product direction | `$plumbline-shape` | `/plumbline:plumbline-shape` |
| Write or adopt a specification | `$plumbline-spec` | `/plumbline:plumbline-spec` |
| Create a plan | `$plumbline-plan` | `/plumbline:plumbline-plan` |
| Carry out a plan | `$plumbline-execute` | `/plumbline:plumbline-execute` |
| Investigate a problem | `$plumbline-diagnose` | `/plumbline:plumbline-diagnose` |
| Review a change | `$plumbline-review` | `/plumbline:plumbline-review` |
| Reconcile accepted work | `$plumbline-closeout` | `/plumbline:plumbline-closeout` |
| Stop project-local routing | `$plumbline-offboard` | `/plumbline:plumbline-offboard` |

These public commands are the supported entry points. Internal `*-engine` skills are implementation details and should not be invoked directly.

## Use an uninitialized repository

An uninitialized repository is normal. In this mode, Plumbline:

- starts only when you explicitly invoke the front door or a side door;
- reads the repository guidance and the existing files relevant to your request;
- works with ordinary repository conventions and documents from any source;
- stays on the main conversation when no project-local role is available;
- may suggest a companion plan or note when it would make long work easier to resume;
- does not install a router or team unless you explicitly approve initialization.

If you already have a sufficient plan or specification, Plumbline can use it without initialization. If you decline setup, it continues with the task or phase you selected.

## Initialize a repository when you want local setup

Initialization is useful when you want ordinary repository prompts to reach Plumbline, or when you want a project-local team of bounded helpers.

Run `$plumbline-init` in Codex or `/plumbline:plumbline-init` in Claude Code. You can also invoke the front door and say that you want to initialize the repository.

Initialization is a reviewable setup conversation:

1. Plumbline inspects the current repository and prepares a read-only proposal.
2. The proposal lists each file, setting, role, model, permission, and write boundary it would change.
3. You choose the router, the team, both, or neither.
4. Plumbline applies only the choices you approve.

There is no silent bootstrap. A later explicit initialization can audit an existing setup and offer a narrow guidance or profile refresh; it does not replace user-owned configuration without approval. An older, unmarked guidance section requires approval of the exact replacement.

### What the proposal can include

| Choice | Project-local result |
| --- | --- |
| Router | `.agents/skills/plumbline-router/SKILL.md`, a small entry point that lets ordinary prompts reach the front door. It is the only automatic activation boundary. |
| Codex team | Selected `.codex/agents/*.toml` role files and, if approved, `.codex/config.toml` settings. |
| Claude Code team | Selected `.claude/agents/*.md` role files. Shared guidance stays in `AGENTS.md`, and `CLAUDE.md` imports it with `@AGENTS.md`. |
| Shared guidance | A marked, host-specific team section in `AGENTS.md`; Claude also receives the supported import in `CLAUDE.md`. |
| Local setup hygiene | `.git/info/exclude` entries for local setup, and optionally root `.gitignore` plus `.worktreeinclude` when propagation is approved. |

The proposal can select only part of this list. For example, a repository can use the router without a team, or a team without automatic routing.

Initialization does not edit global Codex or Claude settings, install global agents, enable Claude's experimental Agent Teams feature, create external tickets, or create a custom worktree system.

## Understand the project-local team

A team is a small set of helpers owned by the repository. It is not a second workflow controller.

| Who | Responsibility | Write access |
| --- | --- | --- |
| Main conversation | Product choices, plans, integration, Git, and one-owner operations such as builds or deployments. | Owns the task. |
| Researcher and architects | Gather evidence or recommend a design. | Report-only; no write set. |
| Code-reviewer | Check maintainability, design, and safe change. | Report-only; no write set. |
| QA auditor | Check acceptance, proof, and documentation alignment. | Report-only; no write set. |
| Implementer | Make an approved change within the assigned boundary. | Only the approved write set. |

Workers return recommendations to the main conversation. They do not spawn children, own the active plan, or perform shared Git and runtime operations. For material code, the code-reviewer normally runs before the QA auditor.

Codex `sandbox_mode = read-only` and Claude `permissionMode: plan` express permission intent. They are not proof of hard isolation when the parent task is writable or permissive. If hard read-only isolation is required and the host cannot provide it, Plumbline stays on the main conversation.

## How Codex and Claude handle teams

The two tools use the same role responsibilities but different project files.

### Codex

- Roles live in `.codex/agents/*.toml`.
- An approved team may also create or update project `.codex/config.toml`.
- Current Codex releases enable subagents by default. Plumbline records `agents.enabled = true` and a user-owned concurrency setting only when that setup choice is approved.
- The template recommends `agents.max_concurrent_threads_per_session = 12` as an adjustable starting point. Existing or explicitly approved alternatives are preserved.
- Older `features.multi_agent`, `agents.max_threads`, and `agents.max_depth` entries are reported as migration candidates and changed only with approval.
- Role files use full Codex model IDs in `model`, plus explicit `model_reasoning_effort` and `sandbox_mode` fields. `sol` and `luna` are not role-file model IDs.
- The global Codex configuration may be inspected for host capability, but it is not edited. Global agent files are never a fallback.

### Claude Code

- Roles live in project-local `.claude/agents/*.md` files.
- Claude has no required Plumbline project config switch. Role frontmatter carries `model`, `effort`, `tools`, and `permissionMode`.
- Use Claude's own family aliases—`opus`, `sonnet`, `haiku`, or `fable`—a full current model ID, or `inherit`; do not copy a Codex model ID into a Claude role.
- Claude reads `CLAUDE.md`, not `AGENTS.md`. Plumbline keeps shared, reviewable guidance in `AGENTS.md` and adds the supported `@AGENTS.md` import to `CLAUDE.md`, preserving other Claude instructions.
- Claude can match a role from its description. Use `@agent-<role>` for an explicit one-task invocation. `--agent <role>` makes that role the main session agent; it does not dispatch a worker.
- Claude hot-reloads edits to an existing `.claude/agents/` directory. Creating that directory for the first time may require a fresh session.
- Plumbline does not edit global Claude settings or enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. Project-local roles keep their intended permission and tool boundaries; Claude does not apply the same `permissionMode`, hook, or MCP frontmatter boundaries to plugin-provided agents.

### Suggested starting profiles

These are adjustable recommendations, not a required team. Before asking for approval, setup resolves the exact values supported by the active tool or provider. Existing tuned values remain user-owned during audit and retune.

| Role | Codex model / reasoning | Claude model / effort |
| --- | --- | --- |
| `frontend-architect` | `gpt-5.6-sol` / `medium` | `opus` / `low` |
| `backend-architect` | `gpt-5.6-sol` / `medium` | `opus` / `low` |
| `researcher` | `gpt-5.6-luna` / `medium` | `sonnet` / `low` |
| `implementer` | `gpt-5.6-luna` / `high` | `sonnet` / `high` |
| `code-reviewer` | `gpt-5.6-luna` / `high` | `sonnet` / `high` |
| `qa-auditor` | `gpt-5.6-luna` / `max` | `opus` / `medium` |

The model and reasoning/effort values are release-sensitive. The adapters do not call provider APIs or require credentials; the setup proposal supplies the values you approve.

## Optional continuity after a long session

Plumbline includes one small, optional continuity hook. It is meant to restore context when a tool resumes or compacts a long conversation, not to control the workflow.

When enabled and trusted by the host:

- An explicit `$plumbline` or `/plumbline:plumbline` invocation arms continuity for the current session and repository.
- A later `resume` or `compact` event adds a short reminder to read the active plan or resume record and continue the current step.
- Ordinary prompts, phase side doors, Plumbline mentions, and unrelated repositories do not arm it.
- The hook never runs setup, chooses a phase, creates files, dispatches agents, or replaces the active plan.
- State is host-local and keyed to the session and repository; it creates no repository artifact or global configuration.
- The hook has no npm dependencies but requires `node` on the host. If `node` is unavailable, disable the hook; the workflows remain usable through explicit invocation.

Codex lets you review, trust, or disable the hook from `/hooks`. Claude Code lets you enable or disable the plugin from `/plugin`. You can keep Plumbline installed while leaving this hook disabled.

During an explicitly selected Codex Checkpoint Relay, a `Stop` event may write one matching host-local wake marker. The relay controller—not the hook—rereads the plan and decides whether a legal successor exists. Non-relay work remains inert.

## Keep longer work easy to resume

If the work spans sessions, tell Plumbline which document is current. It keeps the active plan small: current decisions, checkpoint status, accepted proof, remaining risks, and the next action. It is not a transcript.

For material multi-step work in a Git repository, Execute asks once whether to create commits at coherent checkpoint or batch boundaries. Approval is assumed unless you opt out; opting out is reported as Git-unanchored. Unrelated dirty files, ignored setup, secrets, generated output, and diagnostic scratch are not staged just to satisfy this convention.

Builds, deployments, restarts, migrations, and package publication stay with the main conversation or a named project owner. Workers can inspect or recommend those actions, but they do not duplicate shared side effects.

### Optional Checkpoint Relay

Normal Execute is continuous. For a very long plan, you may explicitly set this in the controlling plan:

```yaml
execution_mode: checkpoint_relay
```

Relay creates a fresh root conversation for each checkpoint on Codex. On Claude Code and hosts without the automatic adapter, the same boundary is manual: finish one checkpoint, record the durable next action, and start a fresh root conversation.

Plumbline never infers Relay from plan size. It fails closed on ambiguous transitions, duplicate or unknown work, fingerprint drift, approval gates, or transport failures, and it never retries engineering work automatically. `CHANGES_REQUIRED` reopens the affected checkpoint. `Blocked` and `Reopened` do not count as completion, and user acceptance remains explicit.

## Worktree and uninstall boundaries

When propagation is approved, `.worktreeinclude` is the manifest that lets future managed worktrees receive the selected ignored setup. The manifest must be committed for future worktrees to see it; existing worktrees are not updated retroactively and need an explicit refresh or local copy.

Uninstalling the plugin removes the installed bundle, not files already created in a repository. Review project-local router, role, guidance, and ignore files before removing any setup. Preserve user-owned documentation, repository agents, and accepted history.

## Further reading

- [Architecture](architecture.md) explains the implementation boundaries.
- [Evaluation](evaluation.md) covers validation and behavioral checks.
- [Skill authoring](skill-authoring.md) is for contributors extending the plugin.

