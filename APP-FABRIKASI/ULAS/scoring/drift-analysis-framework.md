# Drift Analysis Framework

## Purpose

Answer: **"Are we getting better or worse?"** — requires trends, not point-in-time metrics.

## Drift types

| Type | Signal | Source | Threshold (initial) |
|------|--------|--------|---------------------|
| **Confidence drift** | avg confidence by month ↓ while failures ↑ | decision records | Review weights |
| **Reviewer drift** | accuracy ↓ over 90d | reviewer_metrics | calibrate review |
| **Trust drift** | trust ↑ without outcome support | calibration_log | audit log |
| **Memory drift** | NEVER_AGAIN stale (no hits in 180d) | never-again.json | archive review |
| **Policy drift** | policies/ changed without ADR | git + ADR index | block merge |

## Snapshot protocol

Each `ulas feedback-audit` appends to:

`10-runtime/ulas/metrics/readiness-history.json`

```json
{
  "snapshots": [
    {
      "at": "ISO8601",
      "self_improvement_score": 54,
      "total_decisions": 4,
      "low_confidence_precision": 1.0,
      "outcomes_evaluated": 1
    }
  ]
}
```

## Trend rules (when N≥4 snapshots)

| Trend | Interpretation |
|-------|----------------|
| precision ↑ + failures ↓ | Improving |
| precision flat + decisions ↑ | Learning (need more outcomes) |
| precision ↓ | Confidence model miscalibrated |
| trust ↑ + accuracy ↓ | Trust drift — investigate log |

## Automation status

| Component | Status |
|-----------|--------|
| Snapshot append | ✅ `feedback-audit` |
| Trend alerts | ❌ manual review |
| Auto policy rollback | ❌ out of scope |
