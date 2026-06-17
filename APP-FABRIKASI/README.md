# APP-FABRIKASI — Software Venture Operating System (SVOS)

> **One Venture OS. Multiple platform adapters.**  
> Governance, knowledge, intelligence and quality are platform-independent.  
> Android, iOS, Web, Backend and AI products plug in — they do not rebuild the core.

| Meta | Değer |
|------|-------|
| **Sürüm** | v1.0.0-svos-scaffold |
| **Durum** | Scaffold — blueprints only, no production code |
| **Canonical repo** | [github.com/clariongemini/APP-FABRIKA](https://github.com/clariongemini/APP-FABRIKA) |
| **Android Factory** | Repo kökünde — **dokunulmaz**, operasyonel |

---

## İlişki: Android Factory ↔ SVOS

```
Repo (APP-FABRIKA)
├── [Android Factory]     ← v3.1 frozen, CI green, template + governance
│   templates/android/
│   governance/
│   knowledge/            ← geçiş döneminde referans; SVOS kendi katmanını büyütür
│   scripts/
│   ...
└── APP-FABRIKASI/        ← YENİ: platform-bağımsız Venture OS çekirdeği
    01-core … 10-runtime
```

Android Factory bir **platform adaptörünün** ilk implementasyonudur. SVOS onu büyütmez; ona **bağlanır**.

---

## Çekirdek felsefe

| Yapma | Yap |
|-------|-----|
| Ayrı Android / iOS / Web fabrikası | Tek Venture OS |
| Departman enflasyonu | Yetenek tanımları (planner, architect, …) |
| Prompt arşivi / sızdırılmış içerik | Tasarım prensibi çıkarımı |
| Klasör sayısı = başarı | Kanıtlanabilir venture çıktısı |

**Ayrım:** *WHAT we build* (venture, product, market) · *HOW we build it* (platform adapter)

---

## Dizin haritası

| # | Dizin | Sorumluluk |
|---|-------|------------|
| 01 | [`01-core/`](01-core/) | Governance, standards, intelligence — platform-bağımsız |
| 02 | [`02-platforms/`](02-platforms/) | android · ios · web · backend · ai adaptörleri |
| 03 | [`03-agents/`](03-agents/) | Yetenek tanımları (departman değil) |
| 04 | [`04-design/`](04-design/) | Ürün tasarım sistemi blueprint |
| 05 | [`05-templates/`](05-templates/) | Venture şablonları (blueprint only) |
| 06 | [`06-learning/`](06-learning/) | ADR · pattern · failure · postmortem |
| 07 | [`07-evidence/`](07-evidence/) | Analytics · crash · revenue · retention |
| 08 | [`08-ventures/`](08-ventures/) | Girişim kaydı (kod değil, venture birimi) |
| 09 | [`09-portfolio/`](09-portfolio/) | Capital allocation (gelecek — veri sonrası) |
| 10 | [`10-runtime/`](10-runtime/) | Context assembly · retrieval · lookup |

---

## Master directive çıktıları

| # | Belge | Konum |
|---|-------|-------|
| 1 | Repository Structure | Bu dosya + [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| 2 | Governance Design | [`01-core/governance/GOVERNANCE_DESIGN.md`](01-core/governance/GOVERNANCE_DESIGN.md) |
| 3 | Platform Adapter Design | [`02-platforms/ADAPTER_DESIGN.md`](02-platforms/ADAPTER_DESIGN.md) |
| 4 | Design System Blueprint | [`04-design/DESIGN_SYSTEM.md`](04-design/DESIGN_SYSTEM.md) |
| 5 | Learning System Blueprint | [`06-learning/LEARNING_SYSTEM.md`](06-learning/LEARNING_SYSTEM.md) |
| 6 | Evidence System Blueprint | [`07-evidence/EVIDENCE_SYSTEM.md`](07-evidence/EVIDENCE_SYSTEM.md) |
| 7 | Venture Management Blueprint | [`08-ventures/VENTURE_MANAGEMENT.md`](08-ventures/VENTURE_MANAGEMENT.md) |
| 8 | Portfolio Intelligence Blueprint | [`09-portfolio/PORTFOLIO_INTELLIGENCE.md`](09-portfolio/PORTFOLIO_INTELLIGENCE.md) |
| 9 | Migration Path | [`MIGRATION.md`](MIGRATION.md) |
| 10 | Gap Analysis & Readiness | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |

---

## Intelligence zinciri

```
Knowledge → Insight → Decision → Execution
     ↑                              │
     └──────── Evidence ────────────┘
```

---

## Tasarım ilhamı (prensip only)

Cursor · Claude · Devin · Factory.ai · Linear · Figma · Stripe · Notion · Vercel — **context engineering, validation gates, phase separation, decision memory**.  
Harici referans: [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) (tasarım gözlemi; prompt kopyalama yasak).

---

**Sonraki adım:** İlk venture seç → platform adaptörü → ship → evidence → learning loop.
