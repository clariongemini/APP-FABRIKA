# APP-FABRIKASI — Software Venture Operating System (SVOS)

> **Mission:** Create repeatable software ventures that learn from evidence and improve capital allocation over time.  
> → [`NORTH_STAR.md`](NORTH_STAR.md)

| Meta | Değer |
|------|-------|
| **Sürüm** | v1.1.0-stabilization |
| **Mod** | **STABILIZATION** — scaffold genişlemesi durdu |
| **Canonical repo** | [github.com/clariongemini/APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) |
| **İlk validation venture** | [`ulas-player`](08-ventures/ulas-player/venture.json) |
| **Readiness** | **58/100** — iskelet tamam, kas yok (beklenen) |

---

## Factory değil, Operating System

| | Android-App (Factory) | APP-FABRIKASI (OS) |
|---|----------------------|---------------------|
| **Soru** | Nasıl üretirim? | Nasıl şirketleşirim, öğrenirim, portföy yönetirim? |
| **Birim** | Modül, APK | Venture |
| **Konum** | Repo kökü — **dokunulmaz** | `APP-FABRIKASI/` |
| **Başarı** | CI green | İlk venture uçtan uca |

Android Factory bir **platform adaptörünün** tam implementasyonudur. OS onu büyütmez; venture lifecycle'ında **referans eder**.

---

## Neden 01 … 10? (Tasarım hafızası)

Birkaç ay sonra "neden böyle?" diye sormaman için:

| # | Klasör | Neden ayrı? | PURPOSE |
|---|--------|-------------|---------|
| **01** | core | Governance platformdan bağımsız olmalı — iOS'a geçince kurallar yeniden yazılmaz | [`01-core/PURPOSE.md`](01-core/PURPOSE.md) |
| **02** | platforms | HOW ayrı WHAT'tan — Kotlin/Swift/TS sızmasın core'a | [`02-platforms/PURPOSE.md`](02-platforms/PURPOSE.md) |
| **03** | agents | 16 departman yerine 7 yetenek — enflasyon ölümü | [`03-agents/PURPOSE.md`](03-agents/PURPOSE.md) |
| **04** | design | AI-slop değil, kasıtlı UI — tüm venture'lar aynı kalite çubuğu | [`04-design/PURPOSE.md`](04-design/PURPOSE.md) |
| **05** | templates | Her venture sıfırdan checklist yazmasın | [`05-templates/PURPOSE.md`](05-templates/PURPOSE.md) |
| **06** | learning | Geçmiş unutulmasın — ADR, pattern, postmortem | [`06-learning/PURPOSE.md`](06-learning/PURPOSE.md) |
| **07** | evidence | **En kritik** — kanıt olmadan öğrenme yalan | [`07-evidence/PURPOSE.md`](07-evidence/PURPOSE.md) |
| **08** | ventures | Takip edilen birim kod değil girişim | [`08-ventures/PURPOSE.md`](08-ventures/PURPOSE.md) |
| **09** | portfolio | 100 saat nereye? — yalnızca veri sonrası | [`09-portfolio/PURPOSE.md`](09-portfolio/PURPOSE.md) |
| **10** | runtime | OS ne öğrendiğini bilsin — context assembly | [`10-runtime/PURPOSE.md`](10-runtime/PURPOSE.md) |

**Kural:** Bir şey nereye gideceğini bilmiyorsan → önce `08-ventures` charter'ına bak, sonra ilgili PURPOSE.md.

---

## Stabilization Mode (aktif)

→ [`STABILIZATION.md`](STABILIZATION.md)

| Yasak | İzin |
|-------|------|
| Yeni platform adapter | `ulas-player` ship |
| Yeni governance / agent | Evidence, postmortem, ADR |
| Yeni intelligence motor | Gerçek outcome verisi |
| Yeni üst klasör | PURPOSE / README netliği |

**Tek başarı metriği:** APP-FABRIKASI ilk gerçek venture'ını uçtan uca yönetti.

---

## İlk venture: ulas-player

```
08-ventures/ulas-player/venture.json   ← charter (şimdi)
        ↓
02-platforms/android + init-new-app    ← build
        ↓
Play Store release
        ↓
07-evidence/ulas-player/               ← analytics, crash, revenue
        ↓
outcome + 06-learning/postmortem
        ↓
01-core/intelligence                   ← gerçek veri
        ↓
09-portfolio (N≥2 sonrası)
```

Charter: [`08-ventures/ulas-player/venture.json`](08-ventures/ulas-player/venture.json)

---

## Olgunluk tablosu (dürüst skor)

| Alan | Skor | Durum |
|------|------|-------|
| Architecture | 92 | Güçlü |
| Governance | 88 | Güçlü |
| Android adapter | 95 | Operasyonel |
| Learning | 75 | Hazır, veri bekliyor |
| Intelligence | 35 | Şema hazır, veri yok |
| Evidence | 15 | Boş — doğru |
| Portfolio | 15 | Boş — doğru |
| **Venture validation** | **0** | **ulas-player bekliyor** |
| **Composite** | **58** | İskelet tamam, kas yok |

58 kötü değil. **58 + ilk venture loop = 75–80.**

---

## ULAS — Decision Intelligence Layer

> Kurum hafızası ve karar mühendisliği. **Prompt arşivi değil.**

→ [`ULAS/README.md`](ULAS/README.md) · **Phase 3:** [`ULAS/CONSOLIDATION.md`](ULAS/CONSOLIDATION.md) · `ulas report`

| ULAS | Rol |
|------|-----|
| `ulas decide` | Route · gate · audit |
| `ulas outcome` | Effectiveness feedback loop |
| `ulas report` | LOW_CONFIDENCE precision · tier usage |

CL4R1T4S'tan **prensip** çıkarıldı; prompt metni repoda **yok**.

---

```
Knowledge (06) → Insight (01) → Decision (ADR) → Execution (venture)
         ↑                                            │
         └──────────── Evidence (07) ─────────────────┘
```

---

## Repo haritası

```
APP-FABRIKA/
├── APP-FABRIKASI/          ← SVOS (bu dosya)
│   ├── ULAS/               ← Decision intelligence (not prompts)
│   ├── NORTH_STAR.md
│   ├── STABILIZATION.md
│   ├── 01-core … 10-runtime/   (+ PURPOSE.md her birinde)
│   └── 08-ventures/ulas-player/
├── templates/android/      ← Android adapter impl (frozen)
├── governance/               ← geçiş — Android Factory
└── scripts/                  ← init-new-app, CI
```

---

## Belge indeksi

| Belge | İçerik |
|-------|--------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Katman diyagramı, bağımlılık kuralları |
| [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) | Gap'ler ve readiness |
| [`MIGRATION.md`](MIGRATION.md) | Standalone repo yol haritası |
| [`01-core/governance/GOVERNANCE_DESIGN.md`](01-core/governance/GOVERNANCE_DESIGN.md) | Lightweight governance |

---

## Yasaklar (hatırlatma)

- Leaked prompt / CL4R1T4S kopyalama
- Scaffold hızı > venture hızı
- "Yeni klasör = ilerleme" illüzyonu

---

**Sonraki adım:** `ulas-player` build & ship — OS'u validate et, genişletme.
