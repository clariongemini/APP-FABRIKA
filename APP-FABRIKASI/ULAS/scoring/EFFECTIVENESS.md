# ULAS Effectiveness Framework

## Purpose

Prove — not assume — that ULAS improves decisions over time.

---

## Decision metrics

| Metric | Key | Description |
|--------|-----|-------------|
| Total decisions | `total_decisions` | All `decide` runs |
| Approved | `approved` | status APPROVED |
| Blocked | `blocked` | status BLOCKED |
| Overturned | `overturned` | Approved then reversed |
| Failed after approval | `failed_after_approval` | Ship/build failure post-approve |

### Block quality (6-month question)

| Outcome tag | Meaning |
|-------------|---------|
| `correct_block` | Block was right — would have failed |
| `false_block` | Block was wrong — would have succeeded |
| `unknown` | Not yet evaluated |

**LOW_CONFIDENCE precision** = `correct_block / (correct_block + false_block)`

---

## Reviewer metrics

Per capability (`architect`, `security`, `qa`, `auditor`):

| Metric | Key |
|--------|-----|
| Reviews participated | `{cap}_reviews` |
| Accurate reviews | `{cap}_accurate` |
| Missed risks | `{cap}_missed` |
| Accuracy rate | `{cap}_accuracy` |

Updated via `ulas outcome` + `ulas calibrate`.

---

## Memory metrics

| Metric | Key |
|--------|-----|
| NEVER_AGAIN hits | `never_again_hits` |
| Repeat failures (same class) | `repeat_failures` |
| Prevented failures (tagged) | `prevented_failures` |

---

## Token metrics

| Metric | Key |
|--------|-----|
| Tier 1 usage | `tier1_usage` |
| Tier 2 usage | `tier2_usage` |
| Tier 3 + critical | `tier3_usage` |
| Avg context budget hint | `average_context_budget` |

Hypothesis: correct escalation → lower average waste vs always-T3.

---

## Outcome recording

```bash
./APP-FABRIKASI/scripts/ulas.sh outcome \
  --decision-id ulas-player-b-20260617194455 \
  --result correct_block \
  --note "Would have shipped without evidence"
```

Results: `correct_block` | `false_block` | `approved_success` | `approved_failed` | `overturned` | `unknown`

---

## Storage

- Per-decision: `10-runtime/ulas/decisions/{id}.json` → `effectiveness` block
- Aggregates: `10-runtime/ulas/metrics/aggregates.json` (rebuilt on `metrics`/`report`)

---

## Schema

→ [`metrics-schema.json`](metrics-schema.json)

---

## Success (Consolidation Mode)

| Proof | Threshold (initial) |
|-------|---------------------|
| LOW_CONFIDENCE precision | Track at N≥10 evaluated blocks |
| Review chain reliability | failure rate ↓ vs no-review baseline |
| NEVER_AGAIN | ≥1 prevented_failure tagged |
| Token efficiency | tier1+2 > 50% of decisions for low-risk work |

**Not:** more documents. **Yes:** answered questions.
