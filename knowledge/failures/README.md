# Failure Intelligence

Başarısız denemeler altın değerindedir. Runtime'da ara; git'te kalıcı tut.

## Akış

```
record-memory.py --type failure
        ↓
runtime/factory/memory/failures.json  (arama)
        ↓
promote-failure.py --id FAIL-2026-001
        ↓
knowledge/failures/FAIL-2026-001-slug.md  (kalıcı ders)
```

## Kayıt (runtime)

```bash
python3 scripts/factory/record-memory.py \
  --type failure \
  --title "Metadata parser unstable" \
  --tags media,metadata \
  --cause "External schema drift" \
  --resolution "Own metadata model + import adapter" \
  --modules "feature:library"
```

## Promote (git)

```bash
python3 scripts/factory/promote-failure.py --id FAIL-2026-001 --project my-app
```

## Şablon

[`TEMPLATE.md`](TEMPLATE.md)

## Sorgu

```bash
./scripts/factory/query-memory.sh metadata --graph
```

## İlişkili pattern

Hata vertical'a özgüyse ilgili `knowledge/patterns/*/PATTERN.md` dosyasına **Evidence** veya **Known failures** ekle.
