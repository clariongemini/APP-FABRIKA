# APP-FABRIKASI — Software Venture Operating System (SVOS)

> **Mission:** Create repeatable software ventures that learn from evidence and improve capital allocation over time.  
> → [`NORTH_STAR.md`](NORTH_STAR.md)

| Meta | Değer |
|------|-------|
| **Sürüm** | v1.1.0-stabilization |
| **Mod** | **STABILIZATION** — scaffold genişlemesi durdu |
| **Canonical repo** | [github.com/clariongemini/APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) |
| **İlk venture** | `init-venture.sh` ile oluşturulur — repoda örnek venture **yok** |
| **Köprü (P0)** | `./APP-FABRIKASI/scripts/bridge-venture.sh SLUG` |
| **Olgunluk** | `ulas maturity audit` — ilk venture sonrası ölçülür |

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
| Yeni platform adapter | İlk venture ship |
| Yeni governance / agent | Evidence, postmortem, ADR |
| Yeni intelligence motor | Gerçek outcome verisi |
| Yeni üst klasör | PURPOSE / README netliği |

**Tek başarı metriği:** İlk gerçek venture uçtan uca yönetildi (charter → ship → evidence → learning).

---

## İlk venture (şablon)

Repoda hazır venture **bulunmaz** — her projede sıfırdan charter:

```bash
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh my-app
```

Döngü:

```
08-ventures/{slug}/venture.json   ← charter
        ↓
02-platforms/{platform} + build
        ↓
release / ship
        ↓
07-evidence/{slug}/               ← analytics, crash, revenue
        ↓
outcome + 06-learning/postmortem
        ↓
01-core/intelligence              ← gerçek veri
        ↓
09-portfolio (N≥2 sonrası)
```

Şablon: [`08-ventures/_template/venture.json`](08-ventures/_template/venture.json)

---

## Olgunluk tablosu (`ulas maturity audit`)

```bash
./APP-FABRIKASI/scripts/svos-health.sh
# veya: ./scripts/ulas.sh maturity audit
# JSON: ./APP-FABRIKASI/scripts/svos-health.sh --json
```

> **Şablon durumu:** Repoda validation venture yok — skorlar ilk gerçek venture sonrası anlam kazanır. Rapor: `10-runtime/maturity-report.json`

| Alan | Şablon beklentisi |
|------|-------------------|
| Architecture / Governance / ULAS | Scaffold tam — 100'e yakın |
| Learning / Evidence / Portfolio | Venture yokken düşük — **normal** |
| Venture validation | İlk ship + outcome sonrası yükselir |
| **Composite** | `svos-health.sh` ile canlı ölçüm |

**İlk venture sonrası checklist:**

1. `init-venture.sh` + `bridge-venture.sh`
2. `ulas decide` → `work` → `dispatch` → `execute` → `outcome`
3. ADR + postmortem → `06-learning/`
4. `ulas memory ingest` → capability knowledge
5. Play Store ship → `stage: shipped`

---

## Her yeni projeye aktarım

Bu repo **Operating System** olarak tasarlandı — uygulama kodundan bağımsız:

```bash
# Fabrikadan hedef projeye (Android Factory + SVOS)
./scripts/sync-standards.sh /path/to/my-project

# Yalnızca SVOS katmanı
./APP-FABRIKASI/scripts/install-svos-into-project.sh /path/to/my-project

# Yeni girişim charter
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app src/

# AI bağlamı (8K token bütçesi)
./APP-FABRIKASI/scripts/assemble-svos-context.sh my-app
```

Proje kökünde `.svos.json` kurulum meta verisini tutar. AI akışı: **YAPILACAKLAR → dispatch queue → IDE düzeltme → verify → evidence**.

---

## ULAS — Decision Intelligence Layer

> Kurum hafızası ve karar mühendisliği. **Prompt arşivi değil.**

→ [`ULAS/capability-memory/CAPABILITY_MEMORY_AUDIT_v2.md`](ULAS/capability-memory/CAPABILITY_MEMORY_AUDIT_v2.md)

| ULAS | Rol |
|------|-----|
| `ulas decide` | Route · gate · audit |
| `ulas work generate` | Decision → work packages + manifests |
| `ulas capability route` | Capability → provider matching |
| `ulas dispatch plan` | Provider dispatch contracts |
| `ulas memory query` | Capability operational knowledge |
| `ulas execute run` | Verify → self-heal → evidence bridge |
| `ulas dispatch next` | IDE queue card (no API key) |
| `ulas evidence collect` | Bridge + failure report sync |
| `ulas outcome` | Effectiveness feedback loop |
| `ulas report` | LOW_CONFIDENCE precision · tier usage |
| `ulas maturity audit` | Olgunluk skoru + açık gap listesi |

CL4R1T4S'tan **prensip** çıkarıldı; prompt metni repoda **yok**.

### AI Dispatch (IDE — birincil yol)

API anahtarı gerekmez. Cursor/Claude içinde kuyruk kartı:

```bash
ulas dispatch plan --decision-id ID
ulas dispatch execute --decision-id ID      # queue kartları oluşturur
ulas dispatch next --decision-id ID           # sıradaki kartı göster
# IDE'de düzelt → ulas dispatch complete --decision-id ID --dispatch-id DID --result success
ulas execute run --decision-id ID             # yeniden doğrula
ulas dispatch reset --decision-id ID          # skipped → pending
```

Kural: [`.cursor/rules/dispatch-ide.mdc`](.cursor/rules/dispatch-ide.mdc) · Opsiyonel SDK: `--mode sdk` + `CURSOR_API_KEY`

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
│   └── 08-ventures/_template/
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

**Sonraki adım:** Hedef projede `install-svos-into-project.sh` veya `init-venture.sh` ile ilk venture charter'ı oluştur.
