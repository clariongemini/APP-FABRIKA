# Software Venture Factory

Repo sadece Android APK üretmez — **AI destekli mikro yazılım girişimleri** kaydeder.

## Venture kaydı

```bash
python3 scripts/factory/record-venture.py \
  --slug offline-music-v1 \
  --problem "People want offline music without streaming" \
  --solution "Offline Player" \
  --market 7 --competition 8 --revenue 6 \
  --result successful \
  --patterns media_app,offline_first \
  --portfolio-slug offline-player
```

| Alan | Anlam |
|------|-------|
| Problem | Kullanıcı acısı |
| Solution | Ürün adı / özet |
| Market / Competition / Revenue | 1–10 skor |
| Result | successful · failed · pivoted · ongoing |

## Runtime + git

| Konum | İçerik |
|-------|--------|
| `runtime/factory/ventures/ventures.json` | Arama, intelligence engine |
| `knowledge/ventures/{slug}.md` | Kalıcı özet |

## Gelecek fikir önerisi

```bash
python3 scripts/factory/intelligence-engine.py --ask portfolio-summary --last 10
```

Geçmiş venture skorları + outcome verileri birlikte değerlendirilir.
