# Test — Fabrika Smoke Denetimi

Bu klasör, **fabrika kökünü değiştirmeden** repo özelliklerini doğrular.

## Hızlı başlangıç

```bash
chmod +x test/*.sh scripts/scaffold-android-project-to.sh
./test/bootstrap-smoke-app.sh
```

## İçerik

| Yol | Açıklama |
|-----|----------|
| `bootstrap-smoke-app.sh` | `test/factory-smoke-app` Android iskeletini oluşturur + audit |
| `run-factory-audit.sh` | F0–F8 + Cursor bridge adımlarını denetler |
| `AUDIT_REPORT.md` | Son denetim raporu (otomatik üretilir) |
| `factory-smoke-app/` | Minimal 10 modüllü smoke uygulaması |
| `docs/SMOKE_APP_BRIEF.md` | F1 vizyon simülasyonu |

## Denetlenen fabrika adımları

- **F0:** Governance, YAPILACAKLAR, audit chain, MCP
- **F2:** Mimari belgeler, 33 katman dilimleri
- **F3–F4:** Android scaffold, i18n, Liquid Glass
- **F5:** Güvenlik + OEM audit script'leri
- **CX:** gradle-build-loop, state-recovery, context budget
- **QG:** validate-code, factory-health, layer audits
- **BUILD:** `factory-smoke-app` → `assembleDebug` (JDK gerekir)

## Not

Tam `init-new-app.sh` akışı fabrika **kök** `docs/` dosyalarını değiştirir. Smoke test bunun yerine `scaffold-android-project-to.sh` ile izole `test/factory-smoke-app` kullanır.

**Runtime snapshot'lar** (`test/factory-smoke-app/.cursor/snapshots/recovery/` vb.) `.gitignore` ile commit dışıdır — bootstrap sırasında yerelde oluşur.
