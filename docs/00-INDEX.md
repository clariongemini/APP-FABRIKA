# Fabrika hafızası

Bu dosya fabrika reposunun merkezi hafızasıdır. Uygulama projelerinde `init-new-app.sh` proje bilgileriyle günceller.

**Yazar:** [Ulaş Kaşıkcı](AUTHOR.md)

## Repo türü

| Alan | Değer |
|------|-------|
| Tür | GitHub Template / standart kaynağı |
| Amaç | Android projelerine AI kuralları + 33 katman + Executive OS aktarmak |
| Sürüm | v1.0.0 |
| Repo | Ulas Autonomous Android APP Factory |
| Son güncelleme | 2026-06-14 |

## Hızlı Bağlantılar

| Belge | Açıklama |
|-------|----------|
| [AUTHOR.md](AUTHOR.md) | Ulaş Kaşıkcı — proje sahibi |
| [README](../README.md) | GitHub ana sayfa |
| [BOOTSTRAP](./BOOTSTRAP.md) | Yeni proje kurulum kılavuzu |
| [Executive OS](./EXECUTIVE_OS.md) | CEO V7, hiyerarşik denetim |
| [YAPILACAKLAR Sistemi](./YAPILACAKLAR_SISTEMI.md) | F0–F8 faz planı, `/baslat` `/devam-et` |
| [33 Katman Anayasa](./33-LAYER-ARCHITECTURE.md) | Sistem DNA'sı (360 bileşen) |
| [33 Katman Manifest](./33-LAYER-MANIFEST.yaml) | Kaynak doğruluk (tam dosya okuma yasak) |
| [33 Katman Dilimleri](./33-LAYER-MANIFEST/README.md) | On-demand `layer-NN.yaml` — Cursor context budget |
| [Cursor Context Budget](./CURSOR_CONTEXT_BUDGET.md) | Token / okuma sırası rehberi |
| [State Recovery](./STATE_RECOVERY.md) | Truncation / yarım Gradle kurtarma |
| [ANDROID_STRUCTURE](./02-ARCHITECTURE/ANDROID_STRUCTURE.md) | Standart klasör yapısı |
| [Standartlar](./03-STANDARDS/) | Liquid Glass, i18n, Test, Performans |
| [TODO](./TODO.md) | Fabrika geliştirme görevleri |
| [AGENTS](../AGENTS.md) | 16 ajan + Executive katman |

## Kullanım Modları

| Mod | Komut |
|-----|-------|
| GitHub Template | `Use this template` → `init-new-app.sh` |
| Mevcut projeye aktar | `sync-standards.sh /hedef/proje` |
| Submodule | `.factory/` altına ekle → `sync-standards.sh` |

## Departman Ajanları (16 + Overmind)

| Ajan | Dosya | Katmanlar |
|------|-------|-----------|
| Overmind | `.cursorrules` + `00-overmind-zero-hallucination.mdc` | Koordinasyon, halüsinasyon sıfır |
| Ürün CPO | `01-product-cpo.mdc` | 0, 1, 2, 25, 26, 30 |
| Baş Mimar | `02-architect.mdc` | 7–15, 20, 23–24, 27–29 |
| Android Elite | `03-android-elite.mdc` | 3–6, 22 |
| Denetçi | `04-auditor-security.mdc` | 16–19, 21, 31, 32 |
| OEM Denetçi | `05-oem-compat-auditor.mdc` | K22 OEM (Samsung, MIUI, OPPO…) |
| MCP Orkestratör | `06-mcp-orchestrator.mdc` | MCP kurulum (P0: Browser, GitHub) |
| LIUD | `07-linguistic-intelligence.mdc` | Talep istihbaratı |
| CIKA | `08-curriculum-intelligence.mdc` | Müfredat |
| PDC | `09-product-decision-council.mdc` | Roadmap |
| Mavi Okyanus | `10-mavi-okyanus.mdc` | Portföy keşfi |
| CEO V7 | `11-ceo-agent.mdc` | Delivery orchestration |
| CAO | `12-chief-audit-officer.mdc` | Denetim kalitesi |
| CEC | `13-chief-execution-council.mdc` | Execution alignment |
| EGC | `14-executive-governance-council.mdc` | Company health |
| CDID | `15-chief-delivery-intelligence.mdc` | Decision → WP |
| AID | `16-analytics-intelligence.mdc` | Measurement (Sprint P) |
| Growth | `17-marketing-growth.mdc` | GTM, ASO |

Tam eşleme: `governance/executive/HIERARCHICAL_AUDIT_CHAIN.md`

## İlk Kurulum

```bash
./scripts/first-setup.sh
./scripts/check-mcp.sh
./scripts/init-new-app.sh "App" "com.sirket.app"   # governance + YAPILACAKLAR otomatik
```

[MCP Kılavuzu](./MCP_SETUP.md) | [GitHub Açıklamaları](./GITHUB_REPO_DESCRIPTION.md) | [Executive OS](./EXECUTIVE_OS.md)

## Fabrika vs Uygulama Projesi

| | Fabrika Repo (bu) | Uygulama Projesi |
|---|-------------------|------------------|
| Android kodu | Şablon (`templates/android/`) | `app/`, `feature/` |
| PRODUCT_BRIEF | Şablon | Proje özel |
| YAPILACAKLAR | Fabrika geliştirme planı | Proje faz planı (`init-yapilacaklar.sh`) |
| governance runtime | Seed charter + script | `init-governance.sh` ile proje verisi |
| Amaç | Standartları yaymak | Uygulama geliştirmek |
