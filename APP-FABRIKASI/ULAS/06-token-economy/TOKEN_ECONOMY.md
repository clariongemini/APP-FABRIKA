# Token Economy

## PURPOSE

Token israfını azaltmak. Context **risk ile orantılı** olmalı.

## Context tiers

| Tier | Token budget (hint) | Kullanım |
|------|---------------------|----------|
| **T1 minimal** | ~2K | Status check, single-file fix |
| **T2 standard** | ~8K | Feature work, venture build |
| **T3 deep** | ~20K+ | Architecture, security audit, postmortem |

## Tier seçim kuralları

| Risk | Tier |
|------|------|
| Read-only question | T1 |
| Single module edit | T2 |
| Ship / security / cross-module | T3 |
| Portfolio allocation | T3 + evidence summaries only |

## Yükleme yasağı

- T1'de full `governance/` tree
- T2'de raw evidence exports
- Her task'ta full organizational memory

## CL4R1T4S prensibi

- Partial file read first (Cursor)
- No redundant tool calls (Windsurf)
- Search targeted before full read
- Compressed handoff (Cline new_task)

## Entegrasyon

- `10-runtime/context-manifest.schema.json` → `tier` field
- `07-knowledge-compression` → summaries for T2/T3

## Başarı ölçütü

Ortalama context assembly T2 altında kalır (ship events hariç).
