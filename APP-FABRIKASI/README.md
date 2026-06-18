<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Software_Venture_OS-v1.1.0-7c3aed?style=for-the-badge&labelColor=0f172a">
  <img alt="APP-FABRIKASI Software Venture OS v1.1.0" src="https://img.shields.io/badge/Software_Venture_OS-v1.1.0-7c3aed?style=for-the-badge">
</picture>

<br><br>

# APP-FABRIKASI

<h3>
  <em>Software Venture Operating System · Evidence-driven · Portable</em>
</h3>

<p>
  <strong>🇹🇷</strong> Kanıttan öğrenen, tekrarlanabilir yazılım girişimlerini yöneten<br>
  <strong>taşınabilir venture katmanı</strong> — charter, evidence, ULAS karar zekâsı.<br>
  Repoda örnek venture veya validation verisi <strong>bulunmaz</strong>.
</p>

<p>
  <strong>🇬🇧</strong> A portable <strong>venture operating layer</strong> for repeatable software ventures<br>
  that learn from evidence — charter, bridge, learning loop, ULAS decision intelligence.<br>
  No sample venture or validation artifacts in git.
</p>

<br>

<p>
  <a href="#turkce"><strong>🇹🇷 Türkçe</strong></a>
  &nbsp;·&nbsp;
  <a href="#english"><strong>🇬🇧 English</strong></a>
</p>

<br>

[![Mode](https://img.shields.io/badge/mod-STABILIZATION-f59e0b?style=flat-square)](STABILIZATION.md)
[![North Star](https://img.shields.io/badge/mission-NORTH_STAR-0f766e?style=flat-square)](NORTH_STAR.md)
[![Parent](https://img.shields.io/badge/parent-APP--FABRIKA-2563eb?style=flat-square)](../README.md)
[![ULAS](https://img.shields.io/badge/ULAS-decision_intelligence-8b5cf6?style=flat-square)](ULAS/README.md)

<br><br>

<table>
<tr>
<td align="center" width="25%">
  <strong>📋 Charter önce</strong><br>
  <sub><code>init-venture.sh</code> · venture.json</sub>
</td>
<td align="center" width="25%">
  <strong>🔗 Kanıt köprüsü</strong><br>
  <sub><code>bridge-venture.sh</code> · build + test</sub>
</td>
<td align="center" width="25%">
  <strong>🧠 ULAS</strong><br>
  <sub>decide → work → dispatch → outcome</sub>
</td>
<td align="center" width="25%">
  <strong>📊 Olgunluk</strong><br>
  <sub><code>svos-health.sh</code> · maturity audit</sub>
</td>
</tr>
</table>

<br>

**[North Star](NORTH_STAR.md)** ·
**[Architecture](ARCHITECTURE.md)** ·
**[Gap Analysis](GAP_ANALYSIS.md)** ·
**[Stabilization](STABILIZATION.md)** ·
**[ULAS](ULAS/README.md)** ·
**[Parent README](../README.md)**

<br>

<sub>
  <strong>OS ≠ APK</strong> · Venture birimidir; uygulama kodu hedef projede yaşar.<br>
  <strong>OS ≠ Factory</strong> · Android Factory repo kökünde; SVOS onu lifecycle'da referans eder.
</sub>

</div>

---

<a id="turkce"></a>

## 🇹🇷 Türkçe

**APP-FABRIKASI**, [APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) reposunun içinde yaşayan **Software Venture Operating System (SVOS)** katmanıdır. Android Factory *nasıl üretir* sorusunu yanıtlar; SVOS *nasıl şirketleşir, öğrenir ve portföy yönetir* sorusunu yanıtlar.

| Meta | Değer |
|------|-------|
| **Sürüm** | v1.1.0-stabilization |
| **Mod** | **STABILIZATION** — scaffold genişlemesi durdu |
| **Canonical repo** | [github.com/clariongemini/APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) |
| **İlk venture** | `init-venture.sh` ile oluşturulur — repoda örnek **yok** |
| **P0 köprü** | `bridge-venture.sh SLUG` |
| **Sağlık** | `svos-health.sh` |

### Factory vs Operating System

| | APP-FABRIKA (Factory) | APP-FABRIKASI (SVOS) |
|---|----------------------|----------------------|
| **Soru** | Nasıl üretirim? | Nasıl şirketleşirim, öğrenirim, portföy yönetirim? |
| **Birim** | Modül, APK | Venture |
| **Konum** | Repo kökü | `APP-FABRIKASI/` |
| **Başarı** | CI green, standart scaffold | İlk venture uçtan uca (charter → ship → evidence) |

Android Factory bir **platform adaptörünün** tam implementasyonudur. SVOS onu büyütmez; venture lifecycle'ında **referans eder**.

### Hızlı başlangıç

**1 — Yeni venture charter**

```bash
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh my-app
./APP-FABRIKASI/scripts/svos-health.sh
```

**2 — Mevcut projeye SVOS aktarımı**

```bash
./scripts/sync-standards.sh /path/to/my-project          # Factory + SVOS
# veya yalnızca SVOS:
./APP-FABRIKASI/scripts/install-svos-into-project.sh /path/to/my-project
```

**3 — AI bağlamı (token bütçesi)**

```bash
./APP-FABRIKASI/scripts/assemble-svos-context.sh my-app
```

Proje kökünde `.svos.json` kurulum meta verisini tutar.

### Venture döngüsü

```
08-ventures/{slug}/venture.json   ← charter
        ↓
02-platforms/{platform} + bridge.defaults.json
        ↓
release / ship
        ↓
07-evidence/{slug}/               ← analytics, crash, revenue
        ↓
outcome + 06-learning/postmortem
        ↓
01-core/intelligence              ← gerçek veri
        ↓
09-portfolio (N≥2 venture sonrası)
```

Şablon: [`08-ventures/_template/venture.json`](08-ventures/_template/venture.json)

### 01 … 10 — klasör mimarisi

| # | Klasör | Rol | PURPOSE |
|---|--------|-----|---------|
| **01** | core | Platformdan bağımsız governance | [`01-core/PURPOSE.md`](01-core/PURPOSE.md) |
| **02** | platforms | Android / iOS / Web adaptörleri | [`02-platforms/PURPOSE.md`](02-platforms/PURPOSE.md) |
| **03** | agents | 7 yetenek — departman enflasyonu yok | [`03-agents/PURPOSE.md`](03-agents/PURPOSE.md) |
| **04** | design | Kasıtlı UI kalite çubuğu | [`04-design/PURPOSE.md`](04-design/PURPOSE.md) |
| **05** | templates | Venture checklist şablonları | [`05-templates/PURPOSE.md`](05-templates/PURPOSE.md) |
| **06** | learning | ADR, pattern, postmortem | [`06-learning/PURPOSE.md`](06-learning/PURPOSE.md) |
| **07** | evidence | Kanıt olmadan öğrenme yok | [`07-evidence/PURPOSE.md`](07-evidence/PURPOSE.md) |
| **08** | ventures | Takip birimi: girişim | [`08-ventures/PURPOSE.md`](08-ventures/PURPOSE.md) |
| **09** | portfolio | Sermaye tahsisi (veri sonrası) | [`09-portfolio/PURPOSE.md`](09-portfolio/PURPOSE.md) |
| **10** | runtime | Context assembly, maturity raporları | [`10-runtime/PURPOSE.md`](10-runtime/PURPOSE.md) |

**Kural:** Bir artefakt nereye gideceğini bilmiyorsan → önce `08-ventures` charter'ına bak, sonra ilgili `PURPOSE.md`.

### Stabilization Mode

→ [`STABILIZATION.md`](STABILIZATION.md)

| Yasak | İzin |
|-------|------|
| Yeni platform adapter | İlk venture ship |
| Yeni governance / agent | Evidence, postmortem, ADR |
| Yeni intelligence motor | Gerçek outcome verisi |
| Yeni üst klasör | PURPOSE / README netliği |

**Tek başarı metriği:** İlk gerçek venture uçtan uca yönetildi.

### Olgunluk denetimi

```bash
./APP-FABRIKASI/scripts/svos-health.sh
# JSON: ./APP-FABRIKASI/scripts/svos-health.sh --json
# veya: ./APP-FABRIKASI/scripts/ulas.sh maturity audit
```

> **Şablon durumu:** Validation venture repoda yok — skorlar ilk gerçek venture sonrası anlam kazanır. Rapor: `10-runtime/maturity-report.json` (gitignore).

| Alan | Şablon beklentisi |
|------|-------------------|
| Architecture / Governance / ULAS | Scaffold tam |
| Learning / Evidence / Portfolio | Venture yokken düşük — **normal** |
| Venture validation | İlk ship + outcome sonrası yükselir |

**İlk venture sonrası checklist**

1. `init-venture.sh` + `bridge-venture.sh`
2. `ulas decide` → `work` → `dispatch` → `execute` → `outcome`
3. ADR + postmortem → `06-learning/`
4. `ulas memory ingest` → capability knowledge
5. Play Store ship → `stage: shipped`

### ULAS — Decision Intelligence

> Kurum hafızası ve karar mühendisliği. **Prompt arşivi değil.**

| Komut | Rol |
|-------|-----|
| `ulas decide` | Route · gate · audit |
| `ulas work generate` | Decision → work packages |
| `ulas capability route` | Capability → provider matching |
| `ulas dispatch plan` | Provider dispatch contracts |
| `ulas memory query` | Operational knowledge |
| `ulas execute run` | Verify → self-heal → evidence |
| `ulas dispatch next` | IDE queue card (API key gerekmez) |
| `ulas evidence collect` | Bridge + failure report sync |
| `ulas outcome` | Effectiveness feedback loop |
| `ulas maturity audit` | Olgunluk skoru + gap listesi |

CL4R1T4S'tan **prensip** çıkarıldı; prompt metni repoda **yok**. Detay: [`ULAS/README.md`](ULAS/README.md)

**AI Dispatch (IDE — birincil yol)**

```bash
ulas dispatch plan --decision-id ID
ulas dispatch execute --decision-id ID
ulas dispatch next --decision-id ID
# IDE'de düzelt → ulas dispatch complete --decision-id ID --dispatch-id DID --result success
ulas execute run --decision-id ID
```

Kural: [`.cursor/rules/dispatch-ide.mdc`](.cursor/rules/dispatch-ide.mdc)

### Öğrenme döngüsü

```
Knowledge (06) → Insight (01) → Decision (ADR) → Execution (venture)
         ↑                                            │
         └──────────── Evidence (07) ─────────────────┘
```

### Git koruması

Venture-specific veriler commit edilmez:

- `08-ventures/*` — yalnızca `_template/` ve PURPOSE dosyaları
- `07-evidence/*` — yalnızca `_template/` ve sistem belgeleri
- `10-runtime/` — maturity raporları, context/evidence alt klasörleri

Her projede `init-venture.sh` ile sıfırdan charter oluşturulur.

---

<a id="english"></a>

## 🇬🇧 English

**APP-FABRIKASI** is the **Software Venture Operating System (SVOS)** layer inside the [APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) repository. The Android Factory answers *how to build*; SVOS answers *how to run ventures, learn from evidence, and allocate capital*.

### Quick start

```bash
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh my-app
./APP-FABRIKASI/scripts/svos-health.sh
```

**Portable install (SVOS only):**

```bash
./APP-FABRIKASI/scripts/install-svos-into-project.sh /path/to/project
```

### Factory vs OS

| | APP-FABRIKA (Factory) | APP-FABRIKASI (SVOS) |
|---|----------------------|----------------------|
| **Question** | How do I build? | How do I venture, learn, portfolio? |
| **Unit** | Module, APK | Venture |
| **Success** | CI green | End-to-end venture lifecycle proof |

### Stabilization Mode

Scaffold expansion is frozen. Success = first real venture shipped with evidence loop closed. See [`STABILIZATION.md`](STABILIZATION.md).

### Maturity

Run `svos-health.sh` after creating a venture. Template repo scores are expected to be low on Learning/Evidence until real outcomes exist.

### ULAS CLI

Decision intelligence layer — not a prompt dump. Primary IDE dispatch path requires no API key. Full reference: [`ULAS/README.md`](ULAS/README.md).

---

## Repo haritası

```
APP-FABRIKA/                    ← Android Factory (parent)
├── APP-FABRIKASI/              ← SVOS (this document)
│   ├── ULAS/                   ← Decision intelligence
│   ├── scripts/                ← init-venture, bridge, svos-health
│   ├── 02-platforms/android/   ← bridge.defaults.json
│   ├── 08-ventures/_template/  ← charter template (live ventures gitignored)
│   ├── 01-core … 10-runtime/   ← PURPOSE.md in each layer
│   ├── NORTH_STAR.md
│   └── STABILIZATION.md
├── templates/android/          ← Gradle scaffold (factory)
├── governance/                   ← Executive OS (factory)
└── scripts/                    ← init-new-app, sync-standards, CI
```

---

## Belge indeksi

| Belge | İçerik |
|-------|--------|
| [`NORTH_STAR.md`](NORTH_STAR.md) | Mission ve tek başarı metriği |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Katman diyagramı, bağımlılık kuralları |
| [`STABILIZATION.md`](STABILIZATION.md) | Aktif mod kuralları |
| [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) | Gap'ler ve readiness |
| [`MIGRATION.md`](MIGRATION.md) | Standalone repo yol haritası |
| [`08-ventures/VENTURE_MANAGEMENT.md`](08-ventures/VENTURE_MANAGEMENT.md) | Venture charter rehberi |
| [`ULAS/README.md`](ULAS/README.md) | Decision intelligence giriş |
| [`ULAS/capability-memory/README.md`](ULAS/capability-memory/README.md) | Capability memory sistemi |
| [`01-core/governance/GOVERNANCE_DESIGN.md`](01-core/governance/GOVERNANCE_DESIGN.md) | Lightweight governance |
| [`../README.md`](../README.md) | Parent factory README |

---

## İlkeler

| ✅ Yap | ❌ Yapma |
|--------|----------|
| Charter → bridge → evidence → learning | Scaffold hızını venture hızı sanma |
| `PURPOSE.md` oku, sonra dosya ekle | "Yeni klasör = ilerleme" illüzyonu |
| Gerçek outcome verisiyle olgunluk ölç | Leaked prompt / CL4R1T4S kopyalama |
| `init-venture.sh` ile proje bazlı venture | Repoya validation venture commit etme |

---

<p align="center">
  <strong>Sonraki adım:</strong> Hedef projede <code>init-venture.sh</code> ile ilk venture charter'ı oluştur → <code>bridge-venture.sh</code> → <code>svos-health.sh</code>
</p>
