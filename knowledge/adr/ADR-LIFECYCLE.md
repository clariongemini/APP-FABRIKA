# ADR Lifecycle — Decision Memory Engine

Mimari ve ürün kararları **yaşar, eskir, supersede edilir**. 6 ay sonra AI hâlâ bilmeli.

## Durumlar

| Status | Anlam |
|--------|-------|
| `proposed` | Tartışılıyor |
| `accepted` | Uygulanıyor |
| `deprecated` | Artık önerilmez |
| `superseded` | Yeni ADR ile değiştirildi |

## Yaşam döngüsü

```
proposed → accepted → (deprecated | superseded)
                ↓
         review_due (90 gün default)
                ↓
    outcome / failure feedback → lesson
```

## Kayıt

```bash
python3 scripts/factory/record-adr.py \
  --title "Offline-first with Room + SQLCipher" \
  --status accepted \
  --context "V1 must work without network" \
  --alternative "Realm" --alternative-reason "Team Kotlin-first" \
  --alternative "Raw JSON files" --alternative-reason "No query layer" \
  --risk "Migration complexity" \
  --modules "core:data,domain" \
  --review-days 180
```

Çıktılar:

- `knowledge/adr/decisions/ADR-YYYY-NNN.md`
- `.factory/context/LAST_DECISION.md` (özet)
- `runtime/factory/memory/adr_index.json` (arama)

## Şablon

[`ADR.template.md`](ADR.template.md)

## İnceleme

`review_due` geçmiş ADR'ler `enforce-decision-reviews.py` ile listelenir (mevcut PDC accuracy motoru ile uyumlu).
