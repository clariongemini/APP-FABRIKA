# Self-Healing Execution

Extends Execution Engine — no new governance.

---

## Loop

```
Verification Fail
    → Repair Plan (capability-targeted)
    → Retry (attempt ≤ max_retry)
    → Verification
    → [pass] Evidence
    → [fail] Repair Plan ...
```

`max_retry = 3` (from `verification_manifest.retry_policy.max_retry`)

---

## Repair plan shape

Generated from failed verification checks — not human guesswork:

```json
{
  "attempt": 1,
  "triggered_by": ["tests_zero_fail"],
  "plans": [
    {
      "target_capability_id": "android.architecture",
      "target_provider_id": "cursor",
      "action": "fix unit test failures",
      "failed_checks": ["tests_zero_fail"],
      "failures": 10,
      "dispatch_ref": "10-runtime/ulas/dispatch/{id}.json#wp-2"
    }
  ]
}
```

---

## Capability routing on repair

Repair always targets **capability_id** from routing manifest — not "architect person".

Provider comes from current policy binding. Swap Claude → only policy changes.

---

## What is automated today

| Step | Status |
|------|--------|
| Detect failure | ✅ verification manifest |
| Generate repair plan | ✅ `build_repair_plan()` |
| Retry loop | ✅ execute run |
| Auto-fix code | ❌ requires wired ai_invoke dispatch |
| Evidence on pass | ✅ bridge |

Honest boundary: self-healing **loops and plans**; code repair still needs provider dispatch wiring.

---

## State transitions (work chain)

```
ready → executing → repair → executing → verified | failed
```

Work packages: `repair_needed` on architect capability when verification fails.

---

## CLI

```bash
ulas execute run --decision-id ID     # includes repair plans in log
ulas execute status --decision-id ID  # shows repair_plan per attempt
```
