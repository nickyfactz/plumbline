# Host setup contract

This page is for the controller agent. The runner is implemented, but the installed Codex build, login backend, effective permissions, and Nick's custom hook are local runtime facts. Verify them instead of guessing. Do not spend a whole matrix discovering an unsupported interface.

## 1. Scope and discovery

Work in this kit and a separate sibling state folder. Candidate paths must not be under the controller repository or a personal repository containing inherited `AGENTS.md` or `.agents` instructions. Inspect ancestor instructions and system/managed Codex policy. Disclose unavoidable managed behavior equally in both arms; do not bypass it.

Resolve `python --version`, `git --version`, `codex --version`, `codex app-server --help`, and native plugin subcommands. On Windows prefer an actual executable or the resolved Node CLI entry path if shell shims cannot be invoked reliably without a shell. Set `codex_command` to the corresponding argument array. Do not change the machine's default package installation.

The implementation uses one fresh `codex app-server --stdio` process and one fresh thread per cell, sends the prompt through `thread/start` and `turn/start`, and collects the dedicated local session logs. Raw JSON-RPC is retained beside normalized telemetry. If the installed host has a different event format or profile configuration, patch the host adapter before freezing and run self-tests. Do not adapt by removing child telemetry or treating missing models as cheap defaults.

## 2. Authentication

The runner uses saved file-backed Codex login, copies `auth.json` into each private temporary home, and deletes that copy when the attempt finalizes. It does not write the source login and does not forward ambient API keys into the candidate environment. Set `auth_source_home` when the login lives somewhere other than the usual Codex home.

A keychain-only login is not an `auth.json` file. Use the installed host's supported login flow in a **dedicated benchmark auth home** when required. A user may need to complete login once. Do not invent a login token, print one, export a managed credential, or convert the campaign to API billing without approval. Verify that repeated fresh homes authenticate and do not repeatedly invalidate the saved source session. A changed authentication adapter is a disclosed host change.

## 3. Plumbline snapshot and setup

The default snapshot is main at `a592eec`. The runner clones it into the external state folder and checks out a detached commit. It invokes native installation in a dedicated seed home:

```text
codex plugin marketplace add <pinned-local-plumbline-checkout>
codex plugin add plumbline@plumbline
```

For each Plumbline candidate it invokes the pinned source's own scripts:

```text
python <snapshot>/scripts/install_router.py --root <candidate>
python <snapshot>/scripts/install_agent_team.py --root <candidate> --update-agents
```

The generated local profiles and guidance are hashed. Do not replace these with remembered role definitions. Confirm six local roles, intended model/effort values, native availability, and actual worker selection in first-pair evidence. A model-ID migration may be necessary on a future host; apply only a documented approved profile refresh before the freeze, never an undisclosed fallback during a run.

Installing a plugin is not proof its hook or skill ran. Confirm router activation and the actual dispatched roles. Vanilla must not inherit Plumbline, Ponytail, or a benchmark controller skill.

## 4. Permissions and local commits

The default adapter uses a named `benchmark-local` permission profile, not full access. It grants filesystem reads, workspace writes including the **disposable candidate's `.git`**, keeps `.codex`/`.agents` read-only, disables command network access, and denies grader/reference paths. These are intended host permissions; this scaffold has not certified every host tool's enforcement.

Do not combine the new named permissions with legacy `sandbox_mode` in the same root config. The adapter rejects that collision in a seed. Existing role sandbox intent is preserved for workers. If the installed host cannot enforce the selected profile, stop before scoring or adapt its supported narrow permission surface. Never silently use `danger-full-access`, disable managed policy, or grant writes to the real home folder.

The alternative `permission_mode: workspace-write` is only for a host where you have verified that required local Git operations actually work. Some versions protect `.git` even when source files are writable. A benchmark that prevents Plumbline from committing would test a broken environment instead of the requested default workflow. Do not disable Git requirements just to make the benchmark continue; that is a different explicitly labeled treatment.

Validate the root's real ability to make a disposable checkpoint commit and a worker's actual effective permissions. Prefer the host's no-model sandbox/permission diagnostics where exposed. Record any necessary model-only probe as separate setup cost. Root write permission does not prove report-only workers have hard isolation.

## 5. Ponytail: resolve the real implementer-only hook

Default `ponytail_mode: required` intentionally blocks before paid execution when the exact local customization has not been identified. Do not satisfy that check by replacing it with upstream defaults or an implementer prompt approximation.

Read the user's existing hook/plugin configuration without mutating it. Identify the actual source/version, handler code, exact matcher/agent guard, injection text, and native hook trust state. Inspect all active hook sources: Codex may merge them, so adding another hook does not necessarily replace an existing all-agent hook.

Construct a minimal dedicated seed home in external benchmark state. Include only the exact Ponytail plugin/hook assets and necessary native registry/trust metadata. Do not copy the entire personal Codex home, unrelated plugins, agent roles, skills, sessions, or global instructions. Use stable audited hook paths where possible; relocating absolute command paths can change hook hashes and invalidate native trust.

Verify positive and negative controls on the actual handler and native host: implementer receives the intended instruction; root, researcher, architects, code-reviewer, and qa-auditor do not. Capture native execution evidence, not just a matcher string. A hook skipped for lack of trust counts as **not applied**, even if the files exist.

Place this evidence object in the seed as `ponytail-evidence.json`:

```json
{
  "source_version": "ACTUAL local commit or version",
  "target_agent_types": ["implementer"],
  "verified": true,
  "hook_path": "relative/path/to/actual/handler",
  "hook_sha256": "SHA256 OF THAT FILE",
  "verification_receipt": "verification/native-hook-check.json",
  "verification_receipt_sha256": "SHA256 OF THAT REAL RECEIPT",
  "negative_controls": ["root", "researcher", "backend-architect", "frontend-architect", "code-reviewer", "qa-auditor"]
}
```

The values above are documentation placeholders, not a usable receipt. The validator requires actual files and matching hashes. Set `ponytail_seed` to the resulting dedicated home. Native registries are version-specific; use the installed CLI to generate them rather than inventing TOML or JSON tables. A single handler hash is not the complete treatment hash: the entire frozen seed is also recorded and rechecked for drift.

`hook_trust_mode: persisted` is the default. Verify copied/rebased seeds retain valid native trust. If they do not, use the supported native trust flow. A separate `audited-bypass` mode passes the host's one-invocation hook-trust bypass, **only after explicit user approval of every enabled audited hook in that isolated home**; never enable it automatically or describe it as a sandbox bypass. Record that mode and the reviewed hook set in disclosures. It does not remove the evidence requirement.

When the user's hook cannot be found or reproduced, report the exact missing artifact. Do not silently switch to `ponytail_mode: off`. An off campaign is a legitimate separately labeled core-Plumbline comparison when the user explicitly chooses it.

## 6. Freeze and first-pair gate

Run all offline tests, then `doctor`, then `prepare`. The full matrix begins with the Terra configuration pair. Execute only those first two attempts initially. Verify both root model selections, actual Plumbline role dispatch, hook execution/scope, commits, normal completion semantics, and complete descendant usage before continuing the same campaign.

A coding FAIL with valid evidence does not block the study. Skipped hooks, ignored profiles, missing descendants, or unsupported runtime settings do. Preserve any paid invalid/preflight attempts as disclosed overhead; do not erase them. Fix host adapters outside the frozen campaign and start a new campaign. Never change hidden acceptance checks because a model failed them.
