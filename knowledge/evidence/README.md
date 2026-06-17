# Evidence — V3 Gerçeklik Katmanı

Pattern teoridir. **Evidence gerçek ürün çıktısıdır.**

## Ne buraya girer?

| Dosya | Kaynak | Git |
|-------|--------|-----|
| `EVIDENCE.md` | İnsan özeti | ✅ |
| `manifest.json` | Dosya envanteri | ✅ |
| `summaries/*.json` | Sanitize metrikler | ✅ |
| `raw/play-console/` | Play export | ❌ gitignore |
| `raw/firebase/` | Analytics/Crashlytics | ❌ gitignore |
| `raw/revenue/` | Billing raporu | ❌ gitignore |
| `raw/reviews/` | Store yorumları | ❌ gitignore |

## Yeni bundle

```bash
./scripts/factory/init-evidence-bundle.sh \
  --slug offline-player-v1 \
  --portfolio-slug offline-player
```

## Doldurma sırası (ilk shipped app)

1. `raw/` — export'ları yerleştir (lokal)
2. `record-outcome.py` — özet metrikler runtime'a
3. `record-postmortem.py` — proje hikayesi
4. `promote-pattern.py` — kanıtlanan pattern'ler
5. `EVIDENCE.md` — ne öğrendik (1 sayfa)
6. `intelligence-engine.py --last 10` — portföy içgörüsü

## Şablon

[`_template/`](_template/) — kopyalanır, doldurulur.

**North star:** Repoyu geliştirmek değil — fabrikayı **beslemek**.
