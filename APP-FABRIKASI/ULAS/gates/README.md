# Gates — Executable Validation

Gate logic runs in [`../bin/ulas.py`](../bin/ulas.py) `decide` command.

| Gate | ID | Blocks when |
|------|-----|-------------|
| Context complete | `GATE_CONTEXT` | `READ_MORE_REQUIRED` — missing venture/adapter/never-again |
| Confidence | `GATE_CONFIDENCE` | band `low` (< 0.40) |
| NEVER_AGAIN | `GATE_MEMORY` | proposal matches registry entry |
| Review chain | `GATE_REVIEW` | missing required capabilities or count |
| Founder (class D) | `GATE_FOUNDER` | `founder_approval: true` — human step (logged, not auto) |

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | APPROVED — all gates pass |
| 1 | BLOCKED — see `blocked_reasons` in decision record |
| 2 | READ_MORE_REQUIRED (assemble only) |

## Decision record

Each `decide` writes:

`APP-FABRIKASI/10-runtime/ulas/decisions/{decision_id}.json`
