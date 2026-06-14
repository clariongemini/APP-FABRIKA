# Test — Fabrika Smoke Denetimi

Bu klasör, **fabrika kökünü değiştirmeden** repo özelliklerini doğrular.

## Hızlı başlangıç

```bash
chmod +x test/*.sh scripts/scaffold-android-project-to.sh
./test/run-all-tests.sh          # tam paket (önerilen)
./test/bootstrap-smoke-app.sh    # sadece smoke app
./test/bootstrap-aistudio-lab.sh # AI Studio import canlı infaz
```

## İçerik

| Yol | Açıklama |
|-----|----------|
| `bootstrap-smoke-app.sh` | `test/factory-smoke-app` Android iskeletini oluşturur + audit |
| `bootstrap-aistudio-lab.sh` | Stitch/AI Studio fixture → `bootstrap-external-project.sh` canlı infaz |
| `run-all-tests.sh` | Tam paket: reasoning XML + audit + AI Studio lab + kalite kapısı |
| `fixtures/aistudio-minimal/` | Minimal AI Studio export (hard-coded i18n — kasıtlı) |
| `aistudio-lab-run/` | Lab çıktısı (gitignore — bootstrap sonrası) |
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
- **BUILD:** `factory-smoke-app` → `assembleDebug` (JDK 17+; CI smoke-build job)
- **ENV:** `scripts/verify-environment.sh` — JDK + MCP + FACTORY_META

## Not

Tam `init-new-app.sh` akışı fabrika **kök** `docs/` dosyalarını değiştirir. Smoke test bunun yerine `scaffold-android-project-to.sh` ile izole `test/factory-smoke-app` kullanır.

**Runtime snapshot'lar** (`test/factory-smoke-app/.cursor/snapshots/recovery/` vb.) `.gitignore` ile commit dışıdır — bootstrap sırasında yerelde oluşur.
