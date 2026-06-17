# 02 — Decision Reliability

## PURPOSE

False-positive onayları azaltmak. Her karar **confidence score** alır.

## Confidence model

```
confidence = weighted_sum(
  evidence_present,      # 0.30 — 07-evidence
  prior_outcomes,        # 0.20 — 06-learning outcomes
  known_failures_clear,  # 0.15 — 05 NEVER_AGAIN clear
  adr_alignment,         # 0.15 — 06-learning ADR
  pattern_support,       # 0.10 — proven patterns
  context_complete       # 0.10 — 01 CONTEXT_COMPLETE
)
```

Skor: `0.0` – `1.0`

| Band | Anlam | Aksiyon |
|------|-------|---------|
| 0.0–0.39 | Low | Block — gather context/evidence |
| 0.40–0.69 | Medium | Review chain mandatory |
| 0.70–0.84 | High | Standard review |
| 0.85–1.0 | Very high | Expedited (still ≥2 reviewers) |

## False-positive önleme

- **Linter loop cap:** max 3 fix attempts → escalate (Cursor principle)
- **Confidence before close:** emin değilsen READ_MORE (Cursor/Devin)
- **No speculation:** unopened file → confidence capped at 0.39

## Schema

→ [`confidence-score.schema.json`](confidence-score.schema.json)

## Entegrasyon

- Input: `07-evidence`, `06-learning`, `01-context-engineering`
- Output: `03-review-chains` threshold, `09-decision-audit`

## Başarı ölçütü

Ship kararlarının ≥80%'i confidence ≥0.70 ile loglandı.
