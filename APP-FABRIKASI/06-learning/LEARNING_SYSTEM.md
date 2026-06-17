# Learning System Blueprint

## Amaç

Geçmişten öğrenmek — platform ve venture-agnostik.

## Varlıklar

| Varlık | Dizin | Lifecycle |
|--------|-------|-----------|
| **ADR** | `adr/` | Proposed → Accepted → Superseded |
| **Pattern** | `patterns/experimental/` → `patterns/proven/` | Evidence-required promotion |
| **Failure** | `failures/` | Incident → root cause → prevention |
| **Postmortem** | `postmortems/` | Ship sonrası zorunlu (V4) |
| **Lessons** | `lessons/` | Kısa çıkarımlar (postmortem özeti) |

## Pattern promotion kuralı

```
experimental + outcome evidence + postmortem reference → proven
```

Proven olmadan portfolio allocation'a girdi olamaz.

## Android Factory geçişi

| Kaynak | SVOS hedef |
|--------|------------|
| `../knowledge/adr/` | `06-learning/adr/` (migrate on copy) |
| `../knowledge/patterns/` | `06-learning/patterns/` |
| `../scripts/knowledge/promote-pattern.py` | Future: `APP-FABRIKASI/scripts/` |

Geçiş: **copy-on-venture**, Android Factory dosyaları değiştirilmez.

## Intelligence bağlantısı

Learning → `01-core/intelligence/` → Portfolio hint (09)

## Şablonlar

- [`adr/ADR.template.md`](adr/ADR.template.md)
- [`failures/TEMPLATE.md`](failures/TEMPLATE.md)
- [`postmortems/TEMPLATE.md`](postmortems/TEMPLATE.md)
