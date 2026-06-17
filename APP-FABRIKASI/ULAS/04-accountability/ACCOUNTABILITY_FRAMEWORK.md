# Accountability Framework

## PURPOSE

Karar kalitesini zaman içinde izlemek. **Cezalandırma değil — öğrenme.**

## Her onaylanan proposal kaydeder

| Alan | Açıklama |
|------|----------|
| `decision_id` | Unique |
| `reviewers[]` | Kim onayladı |
| `approval_chain` | Sıralı review kaydı |
| `confidence_at_approval` | 02 snapshot |
| `final_result` | shipped / reverted / failed |
| `outcome_quality` | post-hoc: success / partial / failure |

## Review stage failure analysis

Failure olduğunda:

1. Hangi review stage'de risk görülmedi?
2. Context eksikliği mi, confidence overrating mi?
3. `reviewer_reliability` güncelle (soft score)

## Reviewer reliability (öğrenme, ceza değil)

```
reliability += small_delta  # on good outcome correlation
reliability -= small_delta  # on missed risk (capped, never punitive block)
```

Amaç: hangi capability kombinasyonları daha güvenilir — **insan founder son söz**.

## Schema

→ [`accountability-record.schema.json`](accountability-record.schema.json)

## CL4R1T4S prensibi

- Step confirmation before proceed (Cline)
- Audit trail for commands (Factory pre-commit)

## Başarı ölçütü

Her ship sonrası accountability record + outcome_quality within 14 days.
