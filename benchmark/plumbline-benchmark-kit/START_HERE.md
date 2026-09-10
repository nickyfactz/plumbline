# Start the benchmark from one Codex conversation

Open this extracted folder as a **separate Codex project**. Do not open a fixture as your controller project and do not initialize the benchmark-kit repository with Plumbline.

Start a new Codex conversation in the kit folder and send:

```text
$plumbline-benchmark Run the full v1 benchmark across Luna, Terra, Sol,
and Astra at medium root reasoning. Use the pinned Plumbline defaults and
my existing Ponytail implementer-only hook. Handle the local setup and
fresh-session runs. Validate the first matched pair before continuing.
Keep the configured spending limits; do not increase them automatically.
Produce the consolidated report and explain cost per verified completion.
```

The repository-local skill is in `.agents/skills/plumbline-benchmark/SKILL.md`. If the host does not discover it, tell the same conversation to read that file and follow it explicitly. No global skill installation is required.

The controller is instructed to do the directory creation, native Plumbline setup, fresh Codex launches, grading, and report consolidation. Authentication or trusting your exact hook can require a one-time native approval; the controller must not bypass those controls silently.

## What happens

1. Run the offline self-tests, inspect the installed Codex interface, and prepare local configuration.
2. Locate the real Ponytail configuration on your computer and make a minimal isolated seed. No generic replacement hook is substituted.
3. Freeze the Plumbline revision, configuration, fixture hashes, agent profiles, pricing snapshot, and run matrix.
4. Execute the first vanilla/Plumbline pair on the configuration task using Terra. Check activation, hook behavior, local Git, and child-inclusive telemetry.
5. Continue the same campaign when those mechanics are valid. A correctly measured task failure is still a valid result and is not repaired by the controller.
6. Produce `report.html`, `report.md`, `report.json`, and `scorecards.csv` in the campaign folder.

A full pass is 24 task attempts: three tasks × four root models × two workflows. Re-running the command for an existing campaign continues only unattempted cells. It does not redo completed attempts or resume a candidate's model conversation.

## Default limits

The editable `config.local.json` is created from `config.example.json`. Defaults cap each attempt at 25 minutes, 400,000 aggregate observed tokens, or $10 observed rate-card equivalent; the campaign has a $60 estimate budget. These are **upper stopping limits, not runtime or cost predictions**. A campaign may finish partially when its budget is reached. The controller never raises limits automatically.

Token reporting is delayed, so these guards are not a billing-system hard cap. Actual account spending limits remain authoritative. The script reserves one full per-run budget before starting the next attempt.

## Smaller or repeated runs

For the initial two-attempt pilot only:

```text
$plumbline-benchmark Run the pilot only. Do not continue to the full matrix.
```

For repeatability on a single tier:

```text
$plumbline-benchmark Create a new full-task campaign for Terra only,
with three fresh attempts per task and workflow. Keep the same fixtures
and the current configured spending limits.
```

That second request creates 18 attempts. A 72-attempt full four-model repetition requires an explicit limit increase; it is not the default.

## What has actually been tested

The shipped validation is offline: reference solutions, legacy behavior, deliberately defective solutions, cost-parser cases, and a simulated Codex process exercising staging and reporting. No authenticated model benchmark has been run for you here. The local host preflight is part of the controller's first invocation, not evidence already collected.
