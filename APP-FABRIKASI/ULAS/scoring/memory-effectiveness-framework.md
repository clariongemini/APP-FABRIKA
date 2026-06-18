# Memory Effectiveness Framework

## Purpose

Prove NEVER_AGAIN prevents repeated mistakes — not just blocks decisions.

## Metrics

| Metric | Key | How |
|--------|-----|-----|
| Registry size | `entries.length` | never-again.json |
| Hits at decide | `never_again_hits` | auto in metrics |
| Prevented failures | `prevented_failures` | `ulas outcome --result prevented_failure` |
| Repeat failures | `repeat_failures` | same category failure post-entry — **manual tag** |
| Prevention rate | `prevented / (prevented + repeat)` | when N>0 |

## Severity ladder

| Level | Blocks | Measurable prevention |
|-------|--------|----------------------|
| minor | No | No |
| major | Ack only | Partial |
| critical | Yes | Yes if override avoided |
| never_again | Yes | Yes if conflict blocked |

## Closed loop target

```
Failure → postmortem → NEVER_AGAIN entry (critical/never_again)
    → similar proposal → GATE_MEMORY block
    → ulas outcome prevented_failure
    → prevention rate ↑
```

## Current status

Registry empty. **Effectiveness unproven** — expected until first venture postmortem.
