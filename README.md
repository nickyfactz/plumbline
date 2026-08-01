# Plumbline

Plumbline is a lightweight engineering workflow plugin for Codex and Claude Code. It helps an agent move from product intent to useful implementation, verification, and current documentation without forcing every task through a heavyweight process.

If you are trying Plumbline for the first time:

1. Install the plugin for your coding tool.
2. Open the repository you want to work on and start a new session.
3. Invoke the front door: `$plumbline` in Codex or `/plumbline:plumbline` in Claude Code.
4. Give it the outcome you want and any specification, plan, handoff, or work order you already have.

The front door decides how much process the task needs. A small rename may stay direct. An ambiguous feature may go through Shape and research. A large change may use a specification, checkpoint plan, bounded workers, review, and closeout.

## Install

Plumbline is distributed from this GitHub repository. Plugin installation makes the skills available to your tool; it does not modify the project you are working in.

### Codex

From the Codex CLI, add the GitHub marketplace and install the plugin:

```bash
codex plugin marketplace add nickyfactz/plumbline@main
codex plugin add plumbline@plumbline
```

Start a new Codex session after installation. To use the plugin browser instead:

```text
codex
/plugins
```

Choose the `plumbline` marketplace and install `Plumbline`. The browser path is available in Codex CLI and the Codex desktop app.

For a local checkout of this repository:

```bash
codex plugin marketplace add .
codex plugin add plumbline@plumbline
```

### Claude Code

From Claude Code, add the GitHub marketplace and install the plugin:

```bash
claude plugin marketplace add nickyfactz/plumbline@main
claude plugin install plumbline@plumbline
```

For a local checkout:

```bash
claude plugin marketplace add .
claude plugin install plumbline@plumbline
```

Reload the current session with `/reload-plugins`, or start a new Claude Code session. Claude Code uses the same platform-neutral `SKILL.md` workflows; the Claude manifest and marketplace provide the installation surface.

## Your first project

There are two separate decisions:

- **Install the plugin** so the skills are available.
- **Initialize a repository** if you want project-local automatic routing, a local agent team, or both.

Installation alone is inert. Plumbline never silently creates project files, global files, agents, hooks, worktrees, or trackers.

### Use an uninitialized repository

You do not have to initialize a repository to use Plumbline. Invoke the front door and describe the work:

```text
$plumbline I want to add import/export support for the project configuration.
```

In an uninitialized repository, Plumbline works in convention mode:

- It reads the repository guidance and artifacts that matter to the request.
- It can use an existing specification, plan, handoff, or work order from any source.
- It may recommend a companion artifact when that would improve recovery, but it does not require Plumbline-generated files.
- It continues on the main thread when no project-local worker is available.
- It does not install a router or agent team unless you explicitly approve initialization.

This is the right mode for a small change, an established project with its own process, or a task where you want to try Plumbline before changing repository configuration.

### Initialize a repository

Initialization is useful when you want ordinary repository prompts to pass through Plumbline and/or want a project-local agent team. Use the explicit setup skill:

```text
$plumbline-init
```

You can also invoke `$plumbline` and say that you want to initialize the repository; the front door hands setup to the same consent boundary.

Initialization is read-only until you approve one complete proposal. The proposal explains each planned change, including:

- the repository-local Plumbline router;
- optional project-local agent roles and their model, reasoning, sandbox, and write boundaries;
- project multi-agent settings, including the recommended maximum depth of `1`;
- the Plumbline guidance added to `AGENTS.md`;
- local ignore and managed-worktree propagation behavior;
- any competing workflow controller that may need an explicit decision.

After approval, Plumbline applies only the selected items. You may choose the router without a team, the team without automatic routing, both, or neither. A setup validation failure is reported separately from unrelated repository checks that may be blocked because the project has not installed its own dependencies.

### Initialized versus uninitialized

| Repository state | How Plumbline starts | What changes in the project |
| --- | --- | --- |
| Uninitialized | You explicitly invoke `$plumbline` or a phase skill. | No project setup is required. Existing artifacts and repository conventions are used. |
| Router initialized | Ordinary repository prompts can be routed through the Plumbline front door. | A small repository-local router exists. It is the only automatic activation boundary. |
| Agent team initialized | Plumbline can dispatch approved project-local roles when the task benefits from delegation. | Local `.codex/` configuration and role files are created or audited according to the approved proposal. |
| Both initialized | Ordinary prompts route automatically and suitable work can use the local team. | The main thread still owns product decisions, artifacts, integration, and Git. |

The project-local router is available capability, not a reason to force every task through every phase. Explicit phase requests, sufficient imported artifacts, and small direct work remain valid.

If future managed worktrees need the untracked local setup, initialization can propose `.worktreeinclude` propagation. That manifest must be committed for new worktrees to receive it. Existing worktrees are not updated retroactively and need an explicit refresh.

## How to use Plumbline effectively

### Start with the outcome, not the phase name

Tell Plumbline what you want to accomplish, what must not change, and what evidence or files already exist. For example:

```text
$plumbline Add a retry policy for failed webhook delivery. Preserve the current API and keep this limited to the delivery worker. The design notes are in docs/webhooks.md.
```

Plumbline chooses the smallest suitable path:

- **Direct** for clear, low-risk work that needs no phase advancement.
- **Diagnose** for a defect, regression, failure, or performance problem.
- **Shape** when product intent, behavior, or the available solution space is unclear.
- **Specification** when the contract needs to be made precise or an imported design needs adoption.
- **Plan** when the design is sufficient but execution checkpoints are missing.
- **Execute** when a sufficient plan, work order, or specification already exists.
- **Review** when implementation needs an independent assessment.
- **Closeout** when accepted work needs reconciliation, integration, or transient-artifact cleanup.

It does not restart the lifecycle merely because an artifact came from ChatGPT, Claude, another repository, or a previous session. A sufficient external plan can go straight to execution; a sufficient specification can go to planning; unresolved material product choices return to Shape.

### Let Shape reduce uncertainty

For a material capability or design question, Shape first checks local repository facts and then performs bounded external research when the option space is open. It presents a concise recommendation, realistic alternatives, tradeoffs, source links, and remaining uncertainty before asking you to choose.

Shape may also offer:

- a small throwaway prototype when a behavioral unknown would be cheaper to test than to debate;
- one compact repository-local shaping handoff when the work is clearly broad or likely to span sessions;
- a fog-of-war item for uncertainty that is real but not yet precise enough to become a blocking question.

These are offers, not automatic ceremony. Small work stays in conversation. A handoff is created only with your approval, and it is updated only after material decisions, research findings, scope changes, meaningful fog promotion, or a phase/session transition.

### Use imported specifications and plans

If you already have a document, say which artifact controls the work:

```text
$plumbline Use docs/specs/payment-retry.md as the controlling specification. Check whether it is sufficient to plan and identify only the decisions that remain open.
```

Plumbline adopts settled decisions instead of grilling you again. It may recommend a companion plan or specification when one would make execution safer, but it does not block on missing Plumbline frontmatter, checkpoint IDs, or a particular directory name.

### Keep long work recoverable

For broad work, let the main thread maintain one active specification and one live checkpoint plan. Ask to resume from the current checkpoint rather than restating the whole history. Plumbline uses the plan, handoff, specification, and verification evidence as durable working memory and avoids broad rereads when nothing material has changed.

You remain the owner of product intent and irreversible choices. The agent owns ordinary implementation judgment within the agreed scope. If you do not know an answer yet, Plumbline can preserve it as fog and continue with independent decisions instead of forcing speculation.

### Use the agent team as a tool, not a requirement

When a project-local team is enabled, Plumbline recommends a role-aware starting profile aimed at the cheapest effective model and reasoning effort for each role. These are adjustable recommendations, not permanent policy; change or hot-swap them when evidence shows a better fit.

- Researchers, architects, and QA auditors are report-only and receive no write set.
- Implementers receive only the approved write set.
- The main thread owns specifications, plans, integration, and Git.
- Workers do not spawn children; `agents.max_depth = 1` is the recommended boundary.
- If no suitable local role exists, Plumbline reports `Direct: <reason>` and continues on the main thread rather than using a global fallback.

Each delegation wave reports the selected role names with configured model slugs and reasoning efforts in one compact line. This keeps delegation visible without turning every worker response into a ceremony.

### Keep orchestration explicit

An installed workflow is only an available capability. It does not own the session unless explicitly selected or installed as the repository-local Plumbline router. If another orchestration loop already owns checkpoint selection, plan advancement, review sequencing, or closeout, do not stack a second lifecycle controller on top of it.

## Public commands

Use these public entry skills. Internal `*-engine` skills are implementation details and should not be invoked directly.

| Purpose | Codex | Claude Code |
| --- | --- | --- |
| Front door | `$plumbline` | `/plumbline:plumbline` |
| Initialize or reassess setup | `$plumbline-init` | `/plumbline:plumbline-init` |
| Agent-team setup or audit | `$plumbline-agent-team` | `/plumbline:plumbline-agent-team` |
| Shape | `$plumbline-shape` | `/plumbline:plumbline-shape` |
| Specification | `$plumbline-spec` | `/plumbline:plumbline-spec` |
| Plan | `$plumbline-plan` | `/plumbline:plumbline-plan` |
| Execute | `$plumbline-execute` | `/plumbline:plumbline-execute` |
| Diagnose | `$plumbline-diagnose` | `/plumbline:plumbline-diagnose` |
| Review | `$plumbline-review` | `/plumbline:plumbline-review` |
| Closeout | `$plumbline-closeout` | `/plumbline:plumbline-closeout` |
| Stop project-local routing | `$plumbline-offboard` | `/plumbline:plumbline-offboard` |

Most users only need the front door. Use a side door when you already know the phase you want or when an external artifact makes the phase obvious.

## What Plumbline does not do

Plumbline is intentionally project-agnostic and skills-only. It does not:

- create GitHub issues, tickets, pull requests, labels, or an external tracker;
- install global agents, global instructions, hooks, MCP servers, or personal configuration;
- use global custom agents as a fallback for a missing project role;
- create a custom worktree system or silently create branches;
- require a specification, plan, handoff, prototype, or review for every request;
- treat a report-only role's `read-only` setting as proof of hard isolation when the parent is writable;
- make product decisions on the user's behalf;
- record every question, transcript line, minor technical choice, or rejected idea in a repository document.

## Developer reference

The sections below are for contributors, maintainers, and users who need to inspect or extend the plugin.

### Validation and local development

```bash
python scripts/validate.py
python scripts/install_router.py --root <target-repository> --dry-run --format json
python scripts/install_agent_team.py --root <target-repository> --mode initialize --model <approved-slug> --reasoning-effort <approved-effort> --update-agents
```

The installer commands are explicit proposal/apply helpers. Run `--dry-run --format json` while preparing a proposal and again after approval to preview every file, operation, and changed field without writing.

Use `--mode audit` for a read-only report. It detects stale router and `AGENTS.md` guidance without overwriting either. Use `--mode retune` with `--fill-missing` and/or the explicitly approved `--update-instructions`; retune preserves existing model, reasoning, sandbox, custom fields, and instructions unless a change is explicitly approved. `--propagate` includes the root `.gitignore` patch and `.worktreeinclude` behavior, so it must be shown in the proposal.

Run the repository checks for setup or packaging changes:

```bash
python scripts/validate.py
python scripts/test_install_agent_team.py
git diff --check
```

The validation script uses only the Python standard library. GitHub Actions runs it on pushes and pull requests.

### Repository map

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `.agents/plugins/marketplace.json` - Codex marketplace for GitHub and local installation.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` - Claude Code manifests.
- `skills/` - public entry skills and narrow internal workflow engines.
- `references/` - progressive-disclosure workflow policy.
- `templates/router/` - the repository-local activation shim.
- `templates/agents/` - project-owned role, config, and worktree templates.
- `scripts/` - validation and explicit router/agent-team installation helpers.
- `docs/` and `evals/` - design authority, migration guidance, and behavioral checks.

The approved specification and implementation plan are [docs/specs/plumbline-v1.md](docs/specs/plumbline-v1.md) and [docs/plans/plumbline-v1.md](docs/plans/plumbline-v1.md). They remain available until explicit release acceptance.

### Scope boundary

Plumbline does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
