# Explainable Trust Framework

## Principle

Trust must never be a black box. Every change must be **explainable**.

## Trust record structure

`scoring/trust-scores.json` per capability:

| Field | Purpose |
|-------|---------|
| `trust` | Current 0–100 |
| `reviews` | Count of calibrations |
| `calibration_delta` | Cumulative delta |
| `calibration_log[]` | **Why** each change happened |

## Log entry schema

```json
{
  "at": "2026-06-17T19:00:00Z",
  "previous_trust": 92,
  "new_trust": 92.5,
  "delta": 0.5,
  "outcome": "good",
  "decision_id": "my-app-b-...",
  "reason": "approved_success on charter review",
  "evidence": "venture charter shipped without rework"
}
```

## CLI

```bash
ulas calibrate --reviewer architect --outcome good \
  --decision-id ID --reason "approved_success"
```

## Audit questions

For any trust score, answer:

1. **Why changed?** → last `calibration_log` entry  
2. **What evidence?** → `decision_id` → decision JSON → `effectiveness`  
3. **Justified?** → human compares outcome to delta direction  

## Anti-patterns

- Trust change without log entry — **forbidden** (engine enforces log on calibrate)
- Trust change without decision link when outcome-driven — **warning**
- Auto-lowering trust below floor as punishment — **forbidden** (floor=50)
