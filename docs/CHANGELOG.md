# CHANGELOG

## [0.6.0] — 2026-06-14 — Executive OS

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

### Quality gate (v0.6.1)

- Gradle wrapper tam bootstrap (`bootstrap-gradle-wrapper.sh` + gerçek `gradlew`)
- `BillingRepository` Hilt `@ApplicationContext` — derlenebilir şablon
- `governance/FACTORY_REPO_POLICY.md` — runtime vs git ayrımı
- `scripts/factory-quality-gate.sh` — bileşik 100/100 kapı
- `scripts/setup-mcp.sh`, `validate-android-template.sh`, `validate-factory-governance.sh`
- Genişletilmiş `.gitignore` — governance runtime JSON

### Documentation (v0.6.2)

- `README.md` — kapsamlı TR/EN rehber, Cursor entegrasyonu, Mermaid diyagramlar, kullanıcı yolculuğu

### Cursor 10/10 bridge (v0.6.3)

- `scripts/gradle-build-loop.sh` — Gradle assembleDebug + stacktrace + retry + log snapshot
- `scripts/run-maestro.sh` — Maestro E2E terminal köprüsü
- `.cursor/snapshots/` — MCP handoff + build/maestro kanıt dizini
- `docs/CURSOR_TERMINAL_BRIDGE.md` — Cursor IDE sınırları ve protokol
- `00-overmind`, `02-architect`, `03-android`, `04-auditor`, `06-mcp`, `01-cpo` — build loop + glob optimizasyonu
- `16-analytics` — proje-özel glob kaldırıldı

### Context budget & faz ajanları (v0.6.4)

- `docs/33-LAYER-MANIFEST/layer-NN.yaml` — 33 katman dilimi (on-demand yükleme)
- `scripts/split-layer-manifest.py` + `scripts/validate-layer-slices.sh`
- `docs/CURSOR_CONTEXT_BUDGET.md` — tam manifest okuma yasağı + okuma sırası
- `governance/phase-agents.json` — F0–F8 aktif Cursor ajan eşlemesi
- `YAPILACAKLAR.md` — `Aktif ajanlar` satırı; `validate-yapilacaklar.py` otomatik senkron
- Ajan kuralları (`01`–`05`, `00-overmind`) — dilim referansları

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
