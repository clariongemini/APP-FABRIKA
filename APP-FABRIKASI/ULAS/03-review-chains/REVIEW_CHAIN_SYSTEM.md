# Review Chain System

## PURPOSE

Önemli değişikliklerde **tek capability onaylayamaz**.

## Minimum rule

```
minimum_review_count >= 2
```

"CEO" veya founder review yalnızca bu eşik sonrası — ULAS'ta ayrı executive yok; **founder veto** insan kapısıdır.

## Default review matrix

| Decision type | Chain (sıralı) |
|---------------|----------------|
| Charter (V0) | planner → architect |
| Architecture (V1) | architect → security |
| MVP build (V2) | architect → qa |
| Security-sensitive | security → qa → auditor |
| Ship (V3) | qa → auditor → founder |
| Postmortem (V4) | planner → auditor |

## Capability edges (from 03-agents)

```
planner → architect
architect → security
architect → qa
security → qa
qa → auditor
auditor → (final gate)
```

## Configurable matrix

→ [`review-matrix.json`](review-matrix.json)

## CL4R1T4S prensibi (extracted)

- Plan before act (Cline PLAN/ACT)
- Environment setup gate (Factory DROID)
- git diff before commit (Factory DROID)
- Destructive command approval (Cline/Windsurf safety)

## Schema

→ [`review-record.schema.json`](review-record.schema.json)

## Başarı ölçütü

Sıfır single-reviewer ship. Her audit'te `reviewers.length >= 2`.
