# Current model selection

Recommend families, resolve exact supported IDs, and preserve approved profiles.
These are starting recommendations, not model slugs or mandatory effort levels:

| Role | Codex family / reasoning | Claude family / effort |
| --- | --- | --- |
| `frontend-architect` | latest supported Sol / medium | latest supported Opus / low |
| `backend-architect` | latest supported Sol / medium | latest supported Opus / low |
| `researcher` | latest supported Luna / medium | latest supported Sonnet / low |
| `implementer` | latest supported Luna / high | latest supported Sonnet / high |
| `code-reviewer` | latest supported Luna / high | latest supported Sonnet / high |
| `qa-auditor` | latest supported Luna / max | latest supported Opus / medium |

If a family is renamed or unavailable, propose a supported equivalent at the
same capability/cost tier; a different family or effort needs approval. Never
invent a slug by combining a new version number with a family name.

## Discovery on explicit setup, audit, or update

Every invocation of Init with a team, or Agent Team initialize, audit, retune,
add, or update must perform this read-only check before proposing writes.
An agent-team update request uses the existing audit then approved retune flow;
updating the plugin package alone never migrates agents in other repositories.

1. Identify the active host, version, provider, account/endpoint, selected role
   files, and existing approved model/effort values. Preserve custom settings;
   do not inspect secrets, add credentials, or change global configuration.
2. Obtain the current host/provider model catalog using its exposed model
   picker/list capability or an already-authorized provider Models API. Resolve
   the newest supported, available model in each recommended family and the
   effort levels it supports. Follow pagination when needed; list ordering or
   official release metadata determines recency, not lexical slug sorting.
   Cross-check official model/deprecation documentation for lifecycle status.
   For Codex, distinguish the active host's supported worker catalog from the
   public OpenAI API catalog; they need not expose the same models. Its
   `model/list` result may be cached. For Claude, account for provider-specific
   IDs, host-version support, family-alias overrides, and organization limits.
   Public documentation alone establishes release/support facts, not account
   access. Use explicit IDs for generated pins; `inherit` on Claude is available
   only as an explicitly approved alternative, not an automatic fallback.
3. Compare each installed model with that evidence. Distinguish active,
   deprecated-but-usable, retired, unavailable to this installation, and unknown.
   An older model is not necessarily deprecated; a missing catalog entry alone
   does not prove retirement. Keep valid approved profiles unless a change is
   requested. Warn about deprecation and propose an available replacement for
   retired/unavailable IDs. Report an unverified result honestly if discovery
   fails; keep existing profiles and leave new unresolved pins unapplied.
4. Show the existing and proposed exact model/effort per affected role, family,
   lookup source/date, availability/lifecycle status, and reason to keep or change
   it in the existing proposal. Use current source pointers, not a new catalog
   database or durable discovery artifact. Obtain approval for replacements.
5. Group approved roles with the same exact model/effort and preview every group
   using the existing host adapter with `--roles`, `--model`, and
   `--reasoning-effort` (Codex) or `--effort` (Claude), plus `--dry-run --format json`.
   Apply approved new roles with initialize; update existing profiles only with
   `--mode retune --update-profile`. Preserve instructions, permission boundaries,
   custom fields, and all unselected roles. Verify the resulting fields; do not
   claim runtime model use without host evidence. Running workers keep their
   creation profile. Ordinary feature work never performs automatic upgrades.

The adapters accept the resolved, approved values; they do not perform network
discovery or verify account access themselves. They have no bundled version
fallback and refuse new model fields without explicit model/effort values.
Audit, ordinary retune, instruction-only retune, and guidance-only refresh remain
usable without a replacement model and preserve existing approved values.

Official references: [Codex account model catalogs](https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference),
[OpenAI API model list](https://developers.openai.com/api/reference/resources/models/methods/list),
[Claude model configuration](https://code.claude.com/docs/en/model-config), and
[Claude Models API lifecycle filters](https://platform.claude.com/docs/en/api/models/list).
