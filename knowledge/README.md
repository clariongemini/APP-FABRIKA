# Knowledge OS — Öğrenen Fabrika

Governance **karar verir**. Knowledge OS **öğrenir**. Intelligence Engine **içgörü üretir**.

| Sistem | Konum |
|--------|-------|
| Context OS | `.factory/context/` |
| Decision Memory | `knowledge/adr/` |
| Patterns proven / experimental | `knowledge/patterns/` |
| Failures | `knowledge/failures/` |
| Postmortems | `knowledge/postmortems/` |
| Ventures | `knowledge/ventures/` + `runtime/factory/ventures/` |
| Outcomes | `runtime/factory/outcomes/` + snapshots |
| **Intelligence** | `scripts/factory/intelligence-engine.py` |

## Hızlı komutlar

```bash
./scripts/factory/assemble-context.sh
python3 scripts/factory/intelligence-engine.py --last 10 --export
python3 scripts/factory/record-venture.py --slug ... --problem "..." --solution "..."
python3 scripts/factory/record-postmortem.py --project "..." --expected "..." ...
python3 scripts/factory/record-outcome.py --slug ... --development-hours 120 --ai-usage-pct 65 ...
python3 scripts/factory/promote-pattern.py --name offline_first --evidence "..."
```

Detay: [`docs/LEARNING_FACTORY.md`](../docs/LEARNING_FACTORY.md) · [`docs/KNOWLEDGE_OS.md`](../docs/KNOWLEDGE_OS.md)
