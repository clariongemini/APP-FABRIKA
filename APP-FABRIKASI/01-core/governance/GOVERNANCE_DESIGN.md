# Governance Design — SVOS

## Amaç

Platform-bağımsız karar, faz ve kalite kapıları. **Departman enflasyonu yok.**

## Android Factory'den fark

| Android Factory (frozen) | SVOS Governance |
|--------------------------|-----------------|
| 16 departman ajanı | 7 yetenek (03-agents) |
| CEO/CAO/EGC hiyerarşisi | Lightweight audit chain |
| 33 katman manifest | Venture + adapter katmanları |
| F0–F8 bina metaforu | Venture lifecycle phases |

Android Factory governance **operasyonel kalır**; SVOS onu override etmez.

## Governance bileşenleri

### 1. Operating Principles (`principles.md`)

1. **Evidence over opinion** — Karar kanıt gerektirir.
2. **One OS, many adapters** — Platform logic adaptörde.
3. **Capabilities not departments** — Ajan = sorumluluk, unvan değil.
4. **Phase separation** — Plan → build → measure → learn.
5. **No governance bloat** — Yeni kural = mevcut kuralın yerini alır.
6. **Ship to learn** — Scaffold sonsuz büyümez; venture kanıtlar.

### 2. Venture Lifecycle Phases

| Faz | Anlam | Çıkış kapısı |
|-----|-------|--------------|
| V0 | Venture charter (problem, market) | Charter onaylı |
| V1 | Architecture + adapter seçimi | Blueprint onaylı |
| V2 | MVP build | Platform CI green |
| V3 | Release + evidence | İlk outcome kaydı |
| V4 | Learn + iterate | Postmortem + pattern |
| V5 | Portfolio signal | ROI / allocation hint |

### 3. Validation Gates

| Kapı | Ne doğrular? |
|------|--------------|
| Charter gate | Problem, market, monetization tanımlı |
| Adapter gate | Doğru platform + standartlar seçili |
| Quality gate | Platform adapter validation script |
| Evidence gate | Minimum analytics + crash pipeline |
| Learning gate | Outcome + postmortem kayıtlı |

### 4. Audit Model (lightweight)

```
Builder capability → Auditor capability (L1)
                 → Security capability (L2, if applicable)
```

Tek ajan kendi işini nihai onaylamaz — Android Factory'den alınan prensip, departman hiyerarşisi olmadan.

### 5. Freeze / Maintenance

SVOS scaffold aşamasında:
- Yeni executive council **yasak**
- Blueprint ve sözleşme ekleme **serbest**
- Production code **venture başlayınca**

## Politika dosyaları

| Dosya | İçerik |
|-------|--------|
| [`principles.md`](principles.md) | Operating principles |
| [`venture-phases.json`](venture-phases.json) | Faz tanımları (machine-readable) |
| [`validation-gates.json`](validation-gates.json) | Kapı tanımları |

## Yasaklar

- Leaked prompt arşivi
- Vendor-specific system prompt kopyası
- Her platform için ayrı governance tree
- "Chief X Officer" enflasyonu
