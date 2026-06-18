# Institutional Memory — NEVER_AGAIN Registry

## PURPOSE

Bilinen hataları tekrarlamamak.

## Registry türleri

| Kategori | Örnek |
|----------|-------|
| `architecture` | Failed modular split, circular deps |
| `migration` | Broken Room migration, data loss |
| `dependency` | Abandoned SDK, license trap |
| `monetization` | Paywall placement killed retention |
| `process` | Ship without evidence pipeline |

## Entry şeması

```json
{
  "id": "NA-001",
  "category": "architecture",
  "summary": "One-line lesson",
  "venture_slug": "{slug}",
  "adr_ref": "SVOS-ADR-003",
  "failure_ref": "06-learning/failures/...",
  "created": "2026-06-14",
  "severity": "high | medium | low"
}
```

## Otomatik flag

Gelecek proposal `NEVER_AGAIN` ile çakışırsa:

```yaml
NEVER_AGAIN_CONFLICT:
  entry_id: NA-001
  action: block_until_override
  override_requires: founder + auditor
```

## CL4R1T4S prensibi

- Proactive memory under context limits (Windsurf)
- Learn from pop quiz / eval failures (Devin discipline)

## Dosyalar

- [`never-again.json`](never-again.json) — canonical registry (starts empty)
- Template: [`never-again-entry.template.json`](never-again-entry.template.json)

## Başarı ölçütü

Her postmortem failure → NEVER_AGAIN candidate review within 48h.
