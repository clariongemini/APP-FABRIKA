# Knowledge Layer — SVOS Canonical Schema

Platform-bağımsız bilgi modeli. Venture ve adapter kararları buraya referans verir.

## Varlıklar

| Varlık | Konum (SVOS) | Geçiş kaynağı |
|--------|--------------|---------------|
| ADR | `06-learning/adr/` | `../knowledge/adr/` |
| Pattern | `06-learning/patterns/` | `../knowledge/patterns/` |
| Failure | `06-learning/failures/` | `../knowledge/failures/` |
| Postmortem | `06-learning/postmortems/` | `../knowledge/postmortems/` |

## Kurallar

- Bir pattern `proven/` olmadan önce en az bir venture outcome ile ilişkilendirilmeli.
- ADR numaralandırması venture-agnostik (SVOS-ADR-NNN).
- Platform-specific pattern'ler adaptör altında `02-platforms/{platform}/patterns/` — core'a promote edilmeden önce kanıt gerekir.
