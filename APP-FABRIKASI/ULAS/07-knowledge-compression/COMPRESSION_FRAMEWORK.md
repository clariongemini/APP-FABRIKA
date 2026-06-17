# Knowledge Compression Framework

## PURPOSE

Binlerce belgeyi tekrar tekrar okumamak. Kurumsal bilgi **zamanla küçülmeli**.

## Compression türleri

| Tür | Max boyut | Kaynak |
|-----|-----------|--------|
| ADR compressed | 15 satır | `06-learning/adr/` |
| Postmortem distilled | 25 satır | `06-learning/postmortems/` |
| Venture lesson | 10 satır | `08-ventures/` |
| Pattern card | 20 satır | `06-learning/patterns/` |

## Compression kuralları

1. **Fact only** — spekülasyon yok
2. **Link to source** — full doc path
3. **Date + venture slug** zorunlu
4. Full doc silinmez; summary üretilir

## Şablonlar

- [`compressed-adr.template.md`](compressed-adr.template.md)
- [`compressed-postmortem.template.md`](compressed-postmortem.template.md)

## CL4R1T4S prensibi

- Task handoff with thorough summary (Cline new_task)
- Context window deletion awareness (Windsurf memory)

## Başarı ölçütü

T2 context assembly %70+ compressed summary'den beslenir (full doc read exception logged).
