# Knowledge OS — Learning Factory (V2.1)

**Policy:** No new agents — Knowledge → Insight → Decision

| Evrim | Odak |
|-------|------|
| V1 Factory-centric | Governance, scaffold, gates |
| V2 Knowledge-centric | Context, ADR, patterns, failures, outcomes |
| **V2.1 Intelligence** | `intelligence-engine.py` — otomatik içgörü |

## Pipeline

```
Bilgi topla → intelligence-engine → içgörü → karar (ADR) → uygulama
```

## Sistemler

### 1. Context OS — `.factory/context/`

`assemble-context.sh` → `SESSION_CONTEXT.md`

### 2. Decision Memory — `knowledge/adr/`

`record-adr.py` + ADR-LIFECYCLE

### 3. Pattern Library — `proven/` vs `experimental/`

```bash
python3 scripts/factory/promote-pattern.py --name offline_first --slug my-app --evidence "..."
```

### 4. Failure Intelligence — `knowledge/failures/`

`promote-failure.py`

### 5. Postmortems — `knowledge/postmortems/`

`record-postmortem.py` — proje hikayesi (failure'dan farklı)

### 6. Venture Factory — `knowledge/ventures/`

`record-venture.py` — problem, solution, market skorları

### 7. Outcome Intelligence — genişletilmiş metrikler

`record-outcome.py`: users, MRR, retention, crash, rating, uninstall, **dev hours, AI %, launch duration, feature count, maintenance cost, refund rate**, onboarding, monetization, architecture

### 8. Factory Intelligence Engine

```bash
python3 scripts/factory/intelligence-engine.py --last 10 --export
python3 scripts/factory/intelligence-engine.py --ask revenue-by-monetization
```

Sorular: retention-by-pattern · uninstall-by-onboarding · revenue-by-monetization · crash-by-architecture · feature-count-vs-rating · ai-usage-vs-launch

## Skor (Mimar ölçeği)

| Alan | Skor |
|------|------|
| Governance | 95 |
| Architecture | 90 |
| Knowledge | 90 |
| Learning | 80 |
| Intelligence | 82 (motor hazır) |
| Productization | 88 |
| **Toplam** | **~89** |

**90+** yalnızca gerçek uygulama verisiyle.

## Related

- [`LEARNING_FACTORY.md`](LEARNING_FACTORY.md)
- [`FACTORY_EVOLUTION_DIRECTIVE_AUDIT.md`](FACTORY_EVOLUTION_DIRECTIVE_AUDIT.md)
