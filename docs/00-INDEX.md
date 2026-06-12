# OTONOM TEKNOLOJİ HOLDİNGİ — FABRİKA HAFIZASI

Bu dosya **fabrika reposunun** merkezi hafızasıdır. Uygulama projelerinde `init-new-app.sh` bu dosyayı proje bilgileriyle günceller.

## Repo Türü

| Alan | Değer |
|------|-------|
| Tür | **GitHub Template / Standart Kaynağı** |
| Amaç | Android projelerine tek seferde AI kuralları + 33 katman aktarmak |
| Sürüm | v0.5.0-publish-ready |
| Repo | **Ulas Autonomous Android APP Factory** |
| Son Güncelleme | 2026-06-12 |

## Hızlı Bağlantılar

| Belge | Açıklama |
|-------|----------|
| [README](../README.md) | GitHub ana sayfa |
| [BOOTSTRAP](./BOOTSTRAP.md) | Yeni proje kurulum kılavuzu |
| [33 Katman Anayasa](./33-LAYER-ARCHITECTURE.md) | Sistem DNA'sı (340 bileşen) |
| [33 Katman Manifest](./33-LAYER-MANIFEST.yaml) | Kaynak doğruluk dosyası |
| [ANDROID_STRUCTURE](./02-ARCHITECTURE/ANDROID_STRUCTURE.md) | Standart klasör yapısı |
| [Standartlar](./03-STANDARDS/) | Liquid Glass, i18n, Test, Performans |
| [TODO](./TODO.md) | Fabrika geliştirme görevleri |

## Kullanım Modları

| Mod | Komut |
|-----|-------|
| GitHub Template | `Use this template` → `init-new-app.sh` |
| Mevcut projeye aktar | `sync-standards.sh /hedef/proje` |
| Submodule | `.factory/` altına ekle → `sync-standards.sh` |

## Departman Ajanları

| Ajan | Dosya | Katmanlar |
|------|-------|-----------|
| Ürün CPO | `.cursor/rules/01-product-cpo.mdc` | 0, 1, 2, 25, 26, 30 |
| Baş Mimar | `.cursor/rules/02-architect.mdc` | 7–15, 20, 23–24, 27–29 |
| Android Elite | `.cursor/rules/03-android-elite.mdc` | 3–6, 22 |
| Denetçi | `.cursor/rules/04-auditor-security.mdc` | 16–19, 21, 31, 32 |
| OEM Denetçi | `.cursor/rules/05-oem-compat-auditor.mdc` | K22 OEM (Samsung, MIUI, OPPO…) |
| MCP Orkestratör | `.cursor/rules/06-mcp-orchestrator.mdc` | MCP kurulum (P0: Browser, GitHub) |

## İlk Kurulum

```bash
./scripts/first-setup.sh
./scripts/check-mcp.sh
```

[MCP Kılavuzu](./MCP_SETUP.md) | [GitHub Açıklamaları](./GITHUB_REPO_DESCRIPTION.md)

## Fabrika vs Uygulama Projesi

| | Fabrika Repo (bu) | Uygulama Projesi |
|---|-------------------|------------------|
| Android kodu | Yok | `app/`, `feature/` |
| PRODUCT_BRIEF | Şablon | Proje özel |
| Amaç | Standartları yaymak | Uygulama geliştirmek |
