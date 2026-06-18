# Provider Evaluation Framework

**Not** a trust score. **Not** synthetic ranking.

Answers: *"For capability X, did provider A or B produce better evidence-backed outcomes?"*

---

## When to compare

Same capability, same venture context, different `provider_id` in routing policy — run separately, compare scorecards.

Example question:

> Android Architecture — Cursor vs Claude for fixing module boundary tests?

---

## Methodology

### 1. Controlled comparison

| Control | Rule |
|---------|------|
| Same work package acceptance | Yes |
| Same verification manifest | Yes |
| Same codebase snapshot | Tag commit in evidence |
| Different variable | `provider_id` only |

### 2. Dimensions (evidence-derived)

| Dimension | Source |
|-----------|--------|
| `verification_pass_rate` | execution log attempts |
| `retry_count` | self-healing attempts |
| `time_to_evidence_sec` | dispatch log timestamps |
| `human_intervention_count` | manual_invoke count |
| `outcome` | `ulas outcome` record |

No dimension is filled until a real run exists.

### 3. Record shape

[`provider-scorecard.schema.json`](provider-scorecard.schema.json)

Populate after **two or more** provider runs — never pre-seed scores.

### 4. Decision use

Scorecard informs `routing-policy.json` default change — not automatic trust mutation.

---

## Anti-patterns

- Generating comparison scores without evidence
- Provider marketing claims as data
- Single-run "winner" declarations

---

## CLI (future)

```bash
ulas evaluate compare --capability android.architecture --providers cursor,claude
```

Reads execution + dispatch logs only. Returns empty comparisons until data exists.
