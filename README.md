# Plumbline

Plumbline is a lightweight engineering workflow plugin for Codex and Claude Code. It helps an agent move from product intent to useful implementation, verification, and current documentation without forcing every task through a heavyweight process.

If you are trying Plumbline for the first time:

1. Install the plugin for your coding tool.
2. Open the repository you want to work on and start a new session.
3. Invoke the front door: `$plumbline` in Codex or `/plumbline:plumbline` in Claude Code.
4. Give it the outcome you want and any specification, plan, handoff, or work order you already have.

The front door decides how much process the task needs. A small rename may stay direct. An ambiguous feature may go through Shape and research. A large change may use a specification, checkpoint plan, bounded workers, review, and closeout.

## Install

Plumbline is distributed from this GitHub repository. Plugin installation makes the skills and optional continuity hook available to your tool; it does not modify the project you are working in.

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

If you want compaction/resume continuity, review and trust Plumbline's optional hook in `/hooks`. You can leave the plugin enabled while keeping this hook disabled.

#### Codex desktop app

In the ChatGPT desktop app, open the repository as your project and select
the **Codex** surface. Open **Plugins**, choose the `plumbline` marketplace,
and install **Plumbline**. The repository includes
`.agents/plugins/marketplace.json`, so a local checkout can provide the
marketplace entry. Start a new chat after installation.

If the marketplace is not visible, restart the app after opening the project.
You can also ask Codex to perform the setup:

```text
Install the Plumbline plugin from the GitHub repository nickyfactz/plumbline.
Register its plugin marketplace and install plumbline@plumbline. Do not modify
the repository files or initialize Plumbline; only configure the plugin, then
tell me what changed.
```

The equivalent CLI fallback is `codex plugin marketplace add
nickyfactz/plumbline@main`, followed by `codex plugin add plumbline@plumbline`.
See the [official Codex plugin documentation](https://learn.chatgpt.com/docs/plugins)
for the current desktop and marketplace UI.

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

The continuity hook is optional. Claude Code can disable the plugin from its plugin controls if you do not want resume reminders; run `/reload-plugins` after changing the setting. Even when enabled, the hook remains inert until the front door is explicitly invoked.

#### Claude Code desktop app

Open the repository in the Claude desktop app's **Code** tab. Select the `+`
button beside the prompt, choose **Plugins**, then **Add plugin**. If the
Plumbline marketplace is already configured, select **Plumbline** and install
it at the user, project, or local scope you prefer. Start a new session or run
`/reload-plugins` after installation.

If the marketplace is not listed, ask Claude Code from the Code session:

```text
Add the GitHub plugin marketplace nickyfactz/plumbline@main, install
plumbline@plumbline, and reload the plugins. Do not edit this repository or
initialize Plumbline; only configure the plugin and report what changed.
```

The direct in-session commands are:

```text
/plugin marketplace add nickyfactz/plumbline@main
/plugin install plumbline@plumbline
/reload-plugins
```

See the [Claude Code desktop plugin guide](https://code.claude.com/docs/en/desktop)
and [marketplace guide](https://code.claude.com/docs/en/discover-plugins) if
the labels differ in your installed version.

## Your first project

There are two separate decisions:

- **Install the plugin** so the skills are available.
- **Initialize a repository** if you want project-local automatic routing, a local agent team, or both.

Installation alone is inert. Plumbline never silently creates project files, global files, agents, project hook configuration, worktrees, or trackers. Its bundled continuity hook is also inert until the host enables it and you explicitly invoke the front door.

### Optional compaction continuity

The plugin includes one small, optional lifecycle hook for long-running sessions. It is designed to restore awareness after compaction without turning Plumbline into an automatic workflow controller:

- `$plumbline` in Codex or `/plumbline:plumbline` in Claude Code arms continuity for the current session and repository.
- On `resume` or `compact`, the hook adds one short reminder to read the active plan or resume record and continue the current phase.
- Ordinary prompts, Plumbline mentions, phase side doors, and unrelated repositories do not arm it.
- The hook never runs setup, selects a phase, creates files, dispatches agents, or replaces the active plan.
- State is host-local and session/repository keyed; no repository artifact or global configuration is created.
- During an explicitly selected Codex Checkpoint Relay, the `Stop` event may write one matching host-local wake marker. The relay controller—not the hook—rereads the plan and decides whether a legal successor exists. Non-relay tasks remain inert.

The hook has no npm dependencies but requires `node` on the host. If it is unavailable, disable the hook; the Plumbline skills remain usable through explicit invocation. Codex lets you review/trust or disable it from `/hooks`; Claude Code lets you enable or disable the plugin from `/plugin`.

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
- optional current Codex collaboration and concurrency settings;
- the Plumbline guidance added to `AGENTS.md`;
- local ignore and managed-worktree propagation behavior;
- any competing workflow controller that may need an explicit decision.

After approval, Plumbline applies only the selected items. You may choose the router without a team, the team without automatic routing, both, or neither. A setup validation failure is reported separately from unrelated repository checks that may be blocked because the project has not installed its own dependencies.

### What initialization changes

Initialization is project-local and explicit. The proposal shows a dry-run manifest of every file and field before anything is written. If you approve the agent team, the installer makes these changes:

| Approved item | What is created or updated |
| --- | --- |
| Project `.codex/config.toml` (Codex) | Current Codex releases enable subagents by default. When approved, Plumbline can record `agents.enabled = true` and a user-owned `agents.max_concurrent_threads_per_session` value; the starting template recommends 6 and preserves an approved alternative such as 12. Existing `features.multi_agent`, `agents.max_threads`, and `agents.max_depth` entries are reported as legacy and migrated only after approval. Explicit role files select their own models, including Luna as a leaf worker through current v2 delegation, without forcing the old v1 compatibility path. |
| Selected `.codex/agents/*.toml` | Creates only the roles you select. Each role has explicit `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`, and `sandbox_mode` fields. Researcher, architect, and QA templates are report-only with `read-only` intent; the implementer is the only write-capable role. |
| Selected `.claude/agents/*.md` (Claude Code) | Creates the same role contracts as Claude-native Markdown subagents. Each role records `model`, `effort`, `tools`, and `permissionMode`; report-only roles use restricted read tools and `plan` intent, while the implementer receives write-capable tools. The default model is `inherit`, so no Codex slug or provider is hard-coded. |
| `AGENTS.md` | When approved, adds a marked `## Local agent team` section listing only the selected roles. It explains that the main thread owns product decisions, plans, integration, Git, and all delegation; worker recommendations are advisory and return to the main thread; report-only roles get no write set; workers never spawn children; and global agents are never fallbacks. If the user explicitly invokes Plumbline initialization again, the installer can preview and refresh only this managed section without replacing roles or config. Older unmarked sections require a separate explicit replacement approval; content outside the managed section is preserved. |
| `.git/info/exclude` | Adds local-only ignore entries for `.codex/` and the project-local Plumbline router. This keeps generated setup out of the checkout without changing the repository’s tracked files. |
| `.agents/skills/plumbline-router/SKILL.md` | Creates the small repository-local router only if you approve automatic routing. It is the only automatic Plumbline activation boundary; it does not initialize teams, invoke internal engines, or create workers. |
| `.gitignore` and `.worktreeinclude` | Only when you approve propagation. The root ignore file receives the exact local setup entries, while `.worktreeinclude` lists the config, selected role files, and router for future managed worktrees. Commit the manifest for new worktrees to receive those ignored files; existing worktrees need an explicit refresh. |

The global Codex `config.toml` may be inspected to identify a host model candidate for the proposal, but Plumbline does not edit global config, install global agents, or use personal/global agent files as fallbacks. Claude Code has no equivalent Plumbline project `config.toml`: its project subagents are discovered from `.claude/agents/`, and Plumbline does not edit `~/.claude/settings.json` or enable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. Model and reasoning/effort choices are recommended starting points that you can adjust or hot-swap later; the host adapter writes them explicitly only to the local role files so the setup is reproducible.

The role instructions are shared across hosts; only the small configuration adapter changes format. Codex uses TOML model/reasoning fields, while Claude Code uses Markdown `model`/`effort`/tool/permission fields. Claude's native Agent Teams feature is separate and experimental; Plumbline's one-level team uses bounded project subagents instead.

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

Execute normally runs every remaining checkpoint in dependency order and may batch ready independent research, architecture, QA, or implementation work into a main-mediated parallel wave when contracts are stable, scopes are disjoint, results do not depend on one another, and the join condition is clear. Checkpoint boundaries are internal team handoffs; say “only execute CP-02” or “pause after CP-02” when you want slice-by-slice control. A worker's uncertainty does not automatically prompt the user or cancel the plan—the main thread resolves ordinary in-scope decisions and records them.

### Optional fresh-task checkpoint relay

Normal Execute is continuous and remains the recommended default. When a very
long plan benefits from stronger context isolation, you can explicitly choose
Checkpoint Relay in its controlling plan:

```yaml
execution_mode: checkpoint_relay
```

Then invoke Plumbline Execute normally. Plumbline first checks that the plan,
its source, the current checkpoint, acceptance conditions, next action, and Git
recovery baseline are unambiguous. It does not infer Relay from plan size and
does not rewrite an insufficient external work order. A sufficient external
plan may receive one small companion execution record after approval.

On Codex, the automatic adapter creates a named fresh root task for each
checkpoint, gives it only the durable repository contract, and waits for a
legal checkpoint transition before starting the successor. Desktop or Remote
follow-up turns stay in the same checkpoint task. A task that asks for user
input ends normally; the controller waits for the later turn's durable result
instead of holding a competing turn open. After all checkpoints complete, one
fresh Acceptance task presents the result. User acceptance remains explicit,
and accepted work runs Closeout in that same task.

On Claude Code and hosts without the automatic adapter, the same plan contract
uses a manual boundary: Plumbline completes one checkpoint, records the durable
next action, and tells you to start a fresh root conversation. Claude does not
load or require the Codex App Server adapter.

Relay is useful when clean context per checkpoint is worth additional task
startup and Git-boundary discipline. Keep `continuous` mode for ordinary work,
small plans, or work whose checkpoints benefit from conversational continuity.
Relay fails closed on ambiguous transitions, active or unknown duplicate tasks,
fingerprint drift, approval gates, or transport failures; it never retries
engineering work automatically.

Failed work remains active work. `CHANGES_REQUIRED` reopens the affected checkpoint; `INCONCLUSIVE`, environment, and test-harness failures block it and return to Diagnose. `Blocked` and `Reopened` never satisfy plan completion or Closeout, and severity alone never authorizes rollback, abandonment, or successor selection. If a safety rollback is needed, the active candidate is preserved in durable Git history first.

For blockers, regressions, repeated failures, and expensive validation failures, Diagnose traces the relevant failure path, broken owner, and contract before another correction cycle. A green rerun that only moves the error is not enough; trivial local fixes may stay lightweight when the local cause is confirmed.

It does not restart the lifecycle merely because an artifact came from ChatGPT, Claude, another repository, or a previous session. A sufficient external plan can go straight to execution; a sufficient specification can go to planning; unresolved material product choices return to Shape.

### Let Shape reduce uncertainty

For a material capability or design question, Shape first checks local repository facts and then performs bounded external research when the option space is open. It presents a concise recommendation, realistic alternatives, tradeoffs, source links, and remaining uncertainty before asking you to choose.

For broad shaping, it keeps a lightweight decision frontier: the currently answerable product decisions whose factual and research prerequisites are settled. It asks the highest-leverage frontier question one at a time by default, or presents a small `❓ Q1`/`➡️ Recommendation` batch when several independent questions are ready. It defers dependent questions, accepts partial answers, and moves on when only fog or non-blocking uncertainty remains. It does not create a permanent decision tree or interview you through every theoretical branch.

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

### Shape checkpoints around complete behavior

Plans prefer vertical slices: one observable behavior carried through the relevant storage, service, interface, and proof seams. The implementation may still work internally in layers; the checkpoint is simply not considered complete until the behavior works as a whole.

Foundational migrations, shared contracts, build foundations, and similar prerequisites remain valid horizontal checkpoints when they genuinely unlock later behavior. Plumbline labels those prerequisites, keeps them minimal, and connects them to the downstream slice. Broad refactors can use expand, migrate in bounded batches, then contract. This is planning guidance, not a requirement to reorganize every repository into a particular architecture.

### Keep deterministic operations single-owner

The main thread or a named project owner performs singleton builds, deployments, restarts, migrations, and package publication. Workers can recommend or inspect those commands, but they do not duplicate shared side effects. This prevents parallel agents from creating competing artifacts or runtime state.

### Ask for an explanation before changing the phase

If you are confused by a decision, ask Plumbline to re-explain it. It should restate the outcome, current choice, alternatives, and tradeoff in plain language using the project's terms, then continue the existing phase. Confusion alone does not create a new document, phase, or approval gate.

### Use the agent team as a tool, not a requirement

When a project-local team is enabled, Plumbline recommends a role-aware starting profile aimed at the cheapest effective model and reasoning effort for each role. These are adjustable recommendations, not permanent policy; change or hot-swap them when evidence shows a better fit.

- Researchers, architects, and QA auditors are report-only and receive no write set.
- Write-capable roles receive only their approved bounded write sets.
- The main thread owns specifications, plans, integration, and Git.
- For an Execute checkpoint, the main thread dispatches approved local roles for useful bounded research, architecture, implementation, review, testing, or other capability work before duplicating it. The active checkpoint records delegation roles/status so compaction can restore the delegation obligation. Product decisions, lifecycle/plan state, joins, integration, Git, singleton operations, and tiny coupled actions remain direct.
- Workers return to the main thread and never invoke, hand off to, or dispatch another worker; this is a Plumbline workflow boundary, not a required Codex depth setting.
- If no suitable local role exists, Plumbline reports `Direct: <reason>` and continues on the main thread rather than using a global fallback.

Each delegation wave reports the selected role names with the host-native model and reasoning/effort values in one compact line. Codex shows model slugs and reasoning efforts; Claude Code shows its model and effort values. Use the approved project-local role that matches the capability and preserve its configured values; Plumbline does not substitute arbitrary or global agents. This keeps the team visible without turning every worker response into a ceremony.

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

Plumbline is intentionally project-agnostic and skills-first. It does not:

- create GitHub issues, tickets, pull requests, labels, or an external tracker;
- install global agents, global instructions, or personal configuration, or modify project hook configuration;
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
python scripts/install_claude_agent_team.py --root <target-repository> --dry-run --format json
```

The installer commands are explicit proposal/apply helpers. Run `--dry-run --format json` while preparing a proposal and again after approval to preview every file, operation, and changed field without writing.

Use `--mode audit` for a read-only report. It detects stale router and `AGENTS.md` guidance without overwriting either. On an explicit repeat initialization, preview `--mode initialize --update-agents --refresh-agents --dry-run --format json`; apply the same guidance-only command after approval. If the preview reports an older unmarked section, review the exact diff and add `--replace-agents-guidance` only with explicit approval. Use `--mode retune` with `--fill-missing` and/or the explicitly approved `--update-instructions`; retune preserves existing model, reasoning, sandbox, custom fields, and instructions unless a change is explicitly approved. `--propagate` includes the root `.gitignore` patch and `.worktreeinclude` behavior, so it must be shown in the proposal.

Run the repository checks for setup or packaging changes:

```bash
python scripts/validate.py
python scripts/test_install_agent_team.py
python scripts/test_install_claude_agent_team.py
python scripts/test_plumbline_hook.py
git diff --check
```

The validation script uses only the Python standard library. GitHub Actions runs it on pushes and pull requests.

### Repository map

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `.agents/plugins/marketplace.json` - Codex marketplace for GitHub and local installation.
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` - Claude Code manifests.
- `hooks/` - the optional, front-door-gated Codex/Claude continuity hook.
- `skills/` - public entry skills and narrow internal workflow engines.
- `references/` - progressive-disclosure workflow policy.
- `templates/router/` - the repository-local activation shim.
- `templates/agents/` - project-owned role, config, and worktree templates.
- `scripts/` - validation and explicit router/agent-team installation helpers for Codex and Claude Code.
- `docs/` and `evals/` - current architecture, contributor guidance, and behavioral checks.

The current implementation boundaries are summarized in [docs/architecture.md](docs/architecture.md); validation and UAT guidance is in [docs/evaluation.md](docs/evaluation.md).

### Scope boundary

Plumbline does not create GitHub issues, tickets, pull requests, labels, remote worktrees, global agent files, or automatic repository setup. It leaves those choices with the user and the repository.
