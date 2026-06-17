# 01 — Context Engineering

## PURPOSE

Düşük bağlamlı kararları önlemek. Kritik context eksikse karar **finalize edilemez**.

## Standards

### Context assembly sırası

1. Venture charter (`08-ventures/{slug}/`)
2. Platform adapter PURPOSE + standards
3. NEVER_AGAIN conflict check (`05-institutional-memory/`)
4. Relevant proven patterns (`06-learning/patterns/proven/`)
5. Evidence summary if exists (`07-evidence/`)
6. Token tier selection (`06-token-economy/`)

### Validation checklist

| Alan | Zorunlu | Kanıt |
|------|---------|-------|
| Venture slug | V0+ | `venture.json` exists |
| Platform adapter | V1+ | `02-platforms/{p}/ADAPTER.md` read |
| Target files identified | V2+ | grep/glob before edit |
| ADR conflicts | V1+ | `never-again-index` scan |
| Evidence baseline | V3+ | `EVIDENCE.md` or explicit `none` |

### READ_MORE_REQUIRED state

Karar **bloke** olur when:

```yaml
READ_MORE_REQUIRED:
  reason: "partial_file_view | missing_adapter | no_charter | never_again_unchecked"
  required_reads: []
  blocked_action: "finalize_decision | ship | merge"
```

Çıkış: tüm `required_reads` tamamlandı → state `CONTEXT_COMPLETE`.

## CL4R1T4S prensibi (extracted)

- Partial file view → proactive re-read (Cursor tools discipline)
- Never speculate about unopened code (Factory DROID)
- Explore before plan (Cline PLAN MODE)
- list_dir / search before deep read

## Schema

→ [`context-state.schema.json`](context-state.schema.json)

## Başarı ölçütü

Sıfır "tahminle finalize" kararı — her ship öncesi `CONTEXT_COMPLETE` log.
