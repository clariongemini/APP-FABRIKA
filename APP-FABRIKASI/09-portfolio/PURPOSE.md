# PURPOSE — 09-portfolio

## Bu klasör neden var?

**Capital allocation** — "Sonraki 100 saati nereye yatırmalıyım?" sorusuna evidence-tabanlı cevap.

## Ne saklanır?

- Portfolio şeması (`schema.json`)
- Aggregate venture metrikleri (gelecek: `ventures_aggregate.json`)
- Allocation hint çıktısı (gelecek)

## Ne saklanmaz?

- Tek venture'ın ham verisi (→ `07-evidence/`)
- N < 2 outcome varken allocation "tavsiyesi"
- ROI-only karar (retention + maintenance burden dahil)

## Başarı ölçütü

≥2 venture outcome sonrası ilk `allocation_hint` üretildi — confidence: medium+.

**Şimdi:** Boş olması doğru. Stabilization Mode'da genişletilmez.
