# Intelligence Layer — SVOS

## Zincir

```
Knowledge (06-learning + 07-evidence)
    → Insight (korelasyon, trend)
    → Decision (ADR, charter update, allocation hint)
    → Execution (venture V2+, adapter invoke)
```

## Motor sözleşmesi (scaffold)

| Girdi | İşlem | Çıktı |
|-------|-------|-------|
| outcomes.json | Korelasyon | insight_report.md |
| ventures/*.json | Karşılaştırma | venture_ranking.json |
| patterns/proven | Eşleştirme | recommended_patterns.json |
| portfolio aggregates | ROI hesap | allocation_hint.json |

## Android Factory referansı

`../scripts/factory/intelligence-engine.py` — geçiş döneminde Android outcomes için kullanılabilir.  
SVOS motoru aynı **sözleşmeyi** platform-agnostik veriyle genişletir; Android scripti değiştirilmez.

## Minimum veri (insight için)

- ≥1 shipped venture
- ≥1 recorded outcome
- ≥1 evidence bundle

Scaffold aşamasında motor **boş çalışır** — bu beklenen davranış.
