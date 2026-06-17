# Portfolio Intelligence Blueprint

**Gelecek katman** — veri geldikten sonra aktif olur.

## Soru

> Sonraki 100 saatlik geliştirme zamanımı nereye yatırmalıyım?

## Girdi (minimum)

| Venture | Hours | Revenue | ROI | Retention | Maintenance burden |
|---------|-------|---------|-----|-----------|---------------------|
| A | 200 | $500 | 2.5x | 0.35 D7 | low |
| B | 150 | $50 | 0.3x | 0.12 D7 | high |

## Çıktı

```json
{
  "allocation_hint": "utility_category",
  "confidence": "low | medium | high",
  "reasoning": "Evidence-based summary",
  "ventures_considered": []
}
```

## Kurallar

1. N < 2 ventures with outcomes → **no allocation hint** (confidence: insufficient)
2. ROI alone is not sufficient — retention and maintenance weight
3. Human founder veto always applies

## Şema

- `09-portfolio/schema.json` — field definitions
- `09-portfolio/ventures_aggregate.json` — generated (future script)

## Evidence → Portfolio zinciri

```
07-evidence → 08-ventures.results → 09-portfolio aggregate → allocation_hint
```

Scaffold: blueprint only. Script: post-first-ship.
