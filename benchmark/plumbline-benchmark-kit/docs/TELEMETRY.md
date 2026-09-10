# Token, cost, and account-debit telemetry

## Inputs and evidence

Every attempt has its own `codex-home/sessions` and `archived_sessions` plus normalized `events.jsonl` and raw `app-server.jsonl` from the stdio JSON-RPC stream. The parser recognizes current JSONL session metadata, turn context, cumulative `token_count` events, root completion events, and known child-dispatch identifiers. These shapes are host-version sensitive; validate a real root-plus-worker pair before a campaign continues.

Cumulative counters are differenced per thread. Archived copies are deduplicated by thread identity. Worker parent linkage and actual model IDs are required. A counter reset, missing child, unknown model price, missing token fields, unsupported service tier, or missing terminal receipt suppresses the complete price result. Root-only stdout is preserved as fallback evidence, never represented as the whole Plumbline bill.

`complete-observed` means the recognized rollouts in that dedicated home reconcile to the observed child dispatches. It does **not** mean the provider's invoice has been reconciled. A host that changes dispatch or telemetry formats can defeat completeness detection; the initial native calibration is essential. Keep representative sanitized parser fixtures after any adapter update.

## Standard rate-card equivalent

For each request delta and its observed model:

```text
(uncached input × input rate
 + cached input × cache-read rate
 + billed output × output rate) / 1,000,000
```

Total input includes cached input. Total output includes reasoning output. Those subset counters must not be billed again. The dated snapshot records rates and source URLs; no live price request happens during a candidate attempt.

For the captured model family, input contexts over 272,000 tokens have a different request tier. Classification is per request, not total session tokens. The parser uses `last_token_usage` where exposed; unknown large deltas are not optimistically priced at short-context rates. Do not reuse those tier assumptions for an unrelated future model without checking official pricing and updating the adapter.

The bundled estimate does **not** infer cache-write charges or hosted-tool fees. The fixture prompt and permissions exclude network/hosted tools, but the controller still checks effective capability. Cache-write rate fields are retained in the snapshot for provenance; the main scalar explicitly excludes them when they are not observable. `cold_estimate_usd` reprices all input without cache-read discounts and shares those exclusions. Neither number is an actual account debit.

The pilot maps the provider label `gpt-reserve` to the dated `gpt-5.6-luna` rate card through `model_aliases`. This is a theoretical Luna-equivalent estimate, not proof that the provider bills Reserve identically.

## Actual account debit import

Use authoritative per-run usage/credit/currency records if the installed product exposes them. Keep the original unit; credits are not dollars unless the provider establishes that conversion for the account. Do not infer charges from subscription time limits, a before/after percentage bar while other chats run, or a guessed fixed cost per token.

```json
[
  {
    "run_id": "EXACT ID FROM campaign.json",
    "amount": 1.25,
    "unit": "USD",
    "evidence": "local/path/to/authoritative-per-run-record.json"
  }
]
```

That is a schema example, not a measured charge. Import with:

```text
python bench.py import-charges --file <real-charges.json>
```

Amounts must be finite and nonnegative, and every entry needs a known run ID and evidence reference. Multiple distinct line items may exist for one run; do not import the same charge twice. Import replaces the campaign's prior charge file, so supply the complete current list. The report calculates actual amount/pass only when every attempted run in that group is covered for that unit; otherwise it displays partial coverage. Import does not itself audit the provider evidence, so the controller must verify it.

## Cost stops

The process is monitored against observed aggregate tokens, observed rate-card spend, and elapsed time. The aggregate-token stop may be set to `null` for a clean completion calibration; that removes only the token stop, not the wall or rate-card safety limits. The budget reserves the per-run cap before a new run starts. Reporting delay and in-flight inference can overshoot an estimate boundary; use actual product/account limits for a financial hard cap. If telemetry disappears, do not blindly continue until the wall cap; the controller treats that as a host failure.

## Privacy

Temporary homes contain copied login material while a candidate runs. The copy is removed on normal finalization; an abrupt controller kill can leave it until recovery. `recover` requires proof that no related process is alive. Do not publish raw auth state, hook secrets, session logs, or the entire external state folder. `scorecards.csv` and sanitized report files are the sharing surface.
