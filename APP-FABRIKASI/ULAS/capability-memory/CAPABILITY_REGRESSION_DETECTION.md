# Capability Regression Detection

Detect when **proven** capability knowledge is violated — without new governance.

---

## Signals

| Signal | Detection |
|--------|-----------|
| `proven_violated` | Verification fail on tag linked to proven anti_pattern |
| `failure_recurrence` | Same test class / check id fails on new venture |
| `verification_miss` | Evidence shows fail after proven success_recipe applied |

---

## Detection points (automatic)

1. **`ulas execute run`** — after verification fail, match failed check ids + test names against proven entry `tags`
2. **`ulas memory ingest --from execution`** — compare repair_plan to proven patterns
3. **`bridge-venture.sh`** — optional future hook: test class names in manifest

---

## On detection

Append to `regression_signals[]` on capability store:

```json
{
  "detected_at": "2026-06-18T...",
  "entry_id": "cap-k-003",
  "signal": "proven_violated",
  "venture_slug": "{slug}",
  "decision_id": "...",
  "detail": "module-boundary-test failed after cap-k-003 proven"
}
```

Entry status: `proven` → `experimental` (demote) until re-promoted.

---

## Example (hypothetical)

If `cap-k-001` is proven with tag `architecture`:

And the same architecture verification fails again → `regression_signal` + demote entry.

---

## CLI

```bash
ulas memory regressions --capability android.architecture
ulas memory regressions --all
```

---

## Not in scope

- Auto-block decisions (governance)
- Trust score penalty
- Council review

Regression **informs** promotion and query ranking only.
