# Evaluation and UAT

## Automated checks

Run:

```bash
python scripts/validate.py
```

It checks the manifest, root marketplace, 18 skill manifests, public/engine invocation policies, reference set, router word budget, agent TOML parsing, and helper-script syntax. The official plugin validator also passed when run with PyYAML available in an isolated temporary target directory.

## Platform smoke checks

- Root repo marketplace: passed with Codex CLI 0.144.0 and isolated `CODEX_HOME`.
- `codex plugin list`: discovered `plumbline@plumbline-development` at the repo root.
- Plugin browser install/enable/disable: requires an interactive Codex app or `/plugins` session and is listed in the UAT below.

## Behavioral scenarios

The compact prompts in `evals/prompts/` cover the consent boundary and latest-safe-phase choices. The expected outcomes in `evals/expected/` are deliberately behavior-level so they do not freeze model wording.

1. Uninitialized config change stays direct.
2. Explicit shape works without a router.
3. A rough idea selects Shape.
4. A sufficient external design selects Plan.
5. An active spec and plan select Execute.
6. A bug selects Diagnose.
7. A review request is report-only.
8. Accepted work selects Closeout.
9. Router deletion stops automatic routing.
10. Plugin disable prevents the router's engine path.

## User UAT

1. Add the GitHub marketplace and install Plumbline from `/plugins`.
2. Start a new task and make a normal config request in an uninitialized fixture; confirm no automatic takeover.
3. Run `$plumbline-shape` in that fixture; confirm it works without creating the router.
4. Run `$plumbline-init`, approve only the router, then start a fresh task and try a rough feature prompt.
5. Delete `.agents/skills/plumbline-router/` and confirm automatic routing stops.
6. Disable Plumbline in the plugin browser and confirm no Plumbline skill runs.
7. Run `$plumbline-offboard` and confirm it proposes only Plumbline-owned integration for removal.
