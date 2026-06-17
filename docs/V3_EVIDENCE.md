# V3 Evidence — Gerçeklik Katmanı

**Pattern = teori · Evidence = gerçeklik**

V1 Factory · V2 Knowledge · V2.1 Intelligence · **V3 Evidence**

Intelligence motorları script ile çalışır; **değer**, gerçek kullanıcı verisiyle gelir.

## "Repo silinse ne kaybederim?"

| Erken (kötü) | Olgun (hedef) |
|--------------|---------------|
| Bir sürü script | 3 uygulama × outcome |
| Boş pattern'ler | 8 kanıtlanmış pattern |
| Teorik ADR | 12 ADR + kanıt linki |
| — | 18 postmortem + evidence bundle |

## Klasör yapısı

```
knowledge/evidence/
└── {venture-slug}/          # örn. offline-player-v1
    ├── EVIDENCE.md          # insan özeti + linkler (git)
    ├── manifest.json        # hangi dosyalar var (git)
    ├── summaries/           # sanitize edilmiş JSON/CSV (git, opsiyonel)
    └── raw/                 # Play Console, Firebase export (gitignore — PII)
```

## Başlat

```bash
./scripts/factory/init-evidence-bundle.sh --slug offline-player-v1 \
  --venture-slug offline-player-v1 --portfolio-slug offline-player
```

Sonra `raw/` altına export'ları koy; `summaries/` veya `record-outcome.py` ile sanitize metrikleri gir.

## Bağlantılar

| Evidence | Motor |
|----------|-------|
| Play / Firebase export | `record-outcome.py` |
| Postmortem | `record-postmortem.py` |
| Pattern kanıtı | `promote-pattern.py` |
| Portföy içgörü | `intelligence-engine.py` |

## Politika

- **Belge yazmak evidence değildir** — export veya ölçülebilir metrik gerekir
- `raw/` asla commit edilmez (`.gitignore`)
- 90+ skorun ~8 puanı buradan gelir

Detay: [`knowledge/evidence/README.md`](../knowledge/evidence/README.md)
