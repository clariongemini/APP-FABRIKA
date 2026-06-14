# CHANGELOG

## [2.1.0-stable] — 2026-06-14 — Reasoning zırhı (v2.1)

### Added

- `<negative_constraints>` — katman bypass, mock, DI atlama yasakları
- Kelime bütçesi: reasoning blokları başına **150–200 kelime** cap
- `scripts/validate-reasoning-template-xml.sh` — şablon XML açılış/kapanış dengesi
- Audit **V2.7–V2.9** (XML script, negative_constraints, kelime cap)

### Added (gap closure — 2026-06-14)

- `docs/FACTORY_META/` — fabrika F1 vizyon, pazar, monetizasyon, roadmap
- `scripts/verify-environment.sh` — JDK + MCP + meta raporu
- `scripts/validate-reasoning-transcript.sh` — v2.2 transcript XML (V2.10 audit)
- CI `smoke-build` job — JDK 17 + `assembleDebug`
- `templates/governance/factory_roadmap_priorities.json` — init-governance factory seed

### Added (lab patch)

- `test/run-all-tests.sh` — tek orkestratör (reasoning XML + audit + AI Studio lab + quality gate)
- `test/bootstrap-aistudio-lab.sh` + `test/fixtures/aistudio-minimal/` — `bootstrap-external-project.sh` dikey doğrulama
- `test/README.md` — lab ve orkestratör dokümantasyonu

### Fixed (lab patch)

- `scripts/factory-quality-gate.sh` — `Toplam:` grep eşleşmesi; `set -e` sessiz exit 1

### Docs (v2.1 tutarlılık)

- README, `00-INDEX`, `governance/README` — v2.1.0-stable + Claude-Native reasoning referansları
- Informal ifadeler kaldırıldı (Teacher/Student, anayasası vb.)
- Test harness: 40+ audit + `run-all-tests.sh` + AI Studio lab

### Changed

- `19-claude-reasoning.mdc` → v2.1 stable; üç blok zorunlu sıra
- `.cursorrules` — negative_constraints + Format Hatası notu
- `docs/CLAUDE_REASONING.md` — v2.2 runtime parser erteleme notu
- Fabrika sürümü: **2.1.0-stable**

### Deferred (v2.2)

- Canlı Cursor transcript XML kapanış parser → `phase-verifier`

---

## [2.0.0-reasoning-alpha] — 2026-06-14 — Claude-Native akıl yürütme (v2)

### Added

- `.cursor/rules/19-claude-reasoning.mdc` — `alwaysApply: true`; `<thinking>` + `<architecture_check>` şablonu
- `docs/CLAUDE_REASONING.md` — tetikleyiciler, muafiyetler, Executive OS uyumu
- `test/run-factory-audit.sh` — V2.1–V2.6 statik reasoning denetimi

### Changed

- `.cursorrules` — Claude-Native protokol özeti (Overmind merkez kural seti)
- `00-overmind-zero-hallucination.mdc` — reasoning adımı eklendi
- `19-aistudio-import` → **`20-aistudio-import.mdc`** (19 numarası reasoning için ayrıldı)
- `governance/phase-agents.json` — F0 ajan listesine `19-claude-reasoning`
- Fabrika sürümü: **2.0.0-reasoning-alpha**

---

## [1.0.0] — 2026-06-14 — İlk kararlı sürüm

**Yazar:** Ulaş Kaşıkcı

### Added

- `docs/AUTHOR.md` — proje sahibi ve kullanım notları
- Editorial geçiş: sade dil, geliştirici hitabı, gereksiz sürüm/emoji/pazarlama dili temizlendi
- Fabrika sürümü **1.0.0** — script, meta, LICENSE, GitHub Actions workflow hizalandı
- `scripts/validate-factory-version.sh` — sürüm tutarlılık denetimi (CI ilk adım)

### Includes (önceki geliştirme döngüsü)

Aşağıdaki [0.6.0] bölümündeki tüm özellikler bu sürümde birleştirildi.

---

## [0.6.0] — 2026-06-14 — Executive OS (geliştirme döngüsü)

### Added

- **Executive OS:** CEO V7, CAO, CEC, EGC, CDID, CSGB — hiyerarşik denetim zinciri
- **10 yeni ajan kuralı:** `00-overmind-zero-hallucination` + `07`–`16` + `17-marketing-growth`
- **YAPILACAKLAR sistemi:** F0–F8 bina metaforu, `/baslat` `/devam-et` `/denetle` komutları
- **4 skill + 4 subagent:** zero-hallucination, yapilacaklar-planner/executor, hierarchical-audit
- **governance/ ağacı:** executive, product_decision, reality, execution, analytics, market, linguistic…
- **Scriptler:** `init-governance.sh`, `run_ceo_cycle.sh`, `validate-audit-chain.py`, `validate-yapilacaklar.py`
- **DX wrapper'lar:** `scripts/run-ceo-cycle.sh`, `scripts/init-governance.sh`
- `docs/EXECUTIVE_OS.md`, `docs/YAPILACAKLAR_SISTEMI.md`
- `governance/market/DEPARTMENT_CHARTER.md`

### Changed

- Growth ajanı: `05-marketing-growth` → `17-marketing-growth` (OEM 05 çakışması giderildi)
- Public template metinleri — proje-özel referanslar generic hale getirildi

### Quality gate

- Gradle wrapper tam bootstrap (`bootstrap-gradle-wrapper.sh` + gerçek `gradlew`)
- `BillingRepository` Hilt `@ApplicationContext` — derlenebilir şablon
- `governance/FACTORY_REPO_POLICY.md` — runtime vs git ayrımı
- `scripts/factory-quality-gate.sh` — bileşik 100/100 kapı
- `scripts/setup-mcp.sh`, `validate-android-template.sh`, `validate-factory-governance.sh`
- Genişletilmiş `.gitignore` — governance runtime JSON

### Documentation

- `README.md` — kapsamlı TR/EN rehber, Cursor entegrasyonu, Mermaid diyagramlar, kullanıcı yolculuğu

### Cursor terminal bridge

- `scripts/gradle-build-loop.sh` — Gradle assembleDebug + stacktrace + retry + log snapshot
- `scripts/run-maestro.sh` — Maestro E2E terminal köprüsü
- `.cursor/snapshots/` — MCP handoff + build/maestro kanıt dizini
- `docs/CURSOR_TERMINAL_BRIDGE.md` — Cursor IDE sınırları ve protokol
- `00-overmind`, `02-architect`, `03-android`, `04-auditor`, `06-mcp`, `01-cpo` — build loop + glob optimizasyonu
- `16-analytics` — proje-özel glob kaldırıldı

### Context budget & faz ajanları

- `docs/33-LAYER-MANIFEST/layer-NN.yaml` — 33 katman dilimi (on-demand yükleme)
- `scripts/split-layer-manifest.py` + `scripts/validate-layer-slices.sh`
- `docs/CURSOR_CONTEXT_BUDGET.md` — tam manifest okuma yasağı + okuma sırası
- `governance/phase-agents.json` — F0–F8 aktif Cursor ajan eşlemesi
- `YAPILACAKLAR.md` — `Aktif ajanlar` satırı; `validate-yapilacaklar.py` otomatik senkron
- Ajan kuralları (`01`–`05`, `00-overmind`) — dilim referansları

### State Recovery

- `scripts/state-recovery.sh` — `--checkpoint` / `--recover` / `--status`
- `gradle-build-loop.sh` — pre-build checkpoint + aynı hata ×2 auto-recover
- `.cursor/rules/18-state-recovery.mdc` — truncation protokolü
- `docs/STATE_RECOVERY.md` — agent handoff + selective rollback akışı

### Factory smoke test

- `test/` — FactorySmoke + `run-all-tests.sh` orkestratör + AI Studio lab (40+ audit)
- `scripts/scaffold-android-project-to.sh` — hedef dizine Android iskelet
- Scaffold binary copy fix (`gradle-wrapper.jar`)
- `state-recovery.sh` — `RECOVERY_ROOT` ile alt proje checkpoint

### Gitignore fix

- `**/.cursor/snapshots/recovery/` — alt projelerde runtime checkpoint commit dışı
- Yanlışlıkla commit edilen smoke recovery dosyaları kaldırıldı
- `validate-code.sh` — tracked recovery snapshot kontrolü

### AI Studio import

- `docs/AI_STUDIO_IMPORT.md` — Stitch → AI Studio → Fabrika iş akışı
- `scripts/bootstrap-external-project.sh` — harici proje bootstrap (sync + governance + YAPILACAKLAR)
- `.cursor/commands/import-aistudio.md` + `20-aistudio-import.mdc`
- **Eklenmedi:** `auto-bootstrap.sh` / `alwaysApply` lifecycle (Cursor on-load yok; over-orchestration riski)

### ADR-009: Executive Operating System

**Durum:** Kabul edildi  
**Karar:** Tek ajan onayı yasak; CEO → CAO → EGC zinciri zorunlu; YAPILACAKLAR kod kapısı.  
**Gerekçe:** Fabrika ölçeğinde tutarlılık, halüsinasyon sıfır ve teslimat öngörülebilirliği.

---

## [0.5.0] — 2026-06-12 — Publish Ready + MCP

### Added

- **6. Ajan:** `06-mcp-orchestrator.mdc` — MCP kurulum orkestrasyonu
- `.cursor/mcp.required.json` — P0/P1/P2 MCP manifest
- `.cursor/mcp.json.example` — GitHub + Fetch şablonu
- `docs/MCP_SETUP.md` — TR/EN MCP kılavuzu
- `docs/GITHUB_REPO_DESCRIPTION.md` — Repo adı ve açıklamalar (TR/EN)
- `scripts/check-mcp.sh`, `scripts/first-setup.sh`
- README yenilendi: **Ulas Autonomous Android APP Factory** (TR/EN)

### ADR-008: MCP Güçlendirme Katmanı

**Durum:** Kabul edildi — FINAL  
**Karar:** Ajanlar P0 MCP (Browser, GitHub) olmadan tam otonom değil; ilk kurulumda kontrol zorunlu.  
**Gerekçe:** Güncel AI ajanları tek başına sınırlı; MCP ile pazar araştırması, CI ve build gerçek dünyaya bağlanır.

---

## [0.4.0] — Final Android Mimari Taslak

## [0.3.x] — Önceki sürümler
