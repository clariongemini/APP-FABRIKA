# Decision Audit Framework

## PURPOSE

Geçmiş kararların analizi — context, reviewers, confidence, outcome, lessons.

## Audit record (her major decision)

→ [`decision-audit.schema.json`](decision-audit.schema.json)

| Alan | Kaynak |
|------|--------|
| context_snapshot | 01-context-engineering |
| reviewers | 03-review-chains |
| confidence | 02-decision-reliability |
| outcome | 07-evidence + 08-ventures |
| lessons | 06-learning + 05 NEVER_AGAIN |

## Major decision tanımı

- Ship to production
- Architecture sign-off
- Monetization model change
- Security exception
- Portfolio allocation hint

## Retention

- Summary in git (`09-decision-audit/log/`)
- Raw context snapshots gitignored

## Başarı ölçütü

100% major decisions have audit record within 24h of execution.
