# Factory Audit Report — FactorySmoke

> Oluşturulma: 2026-06-14T18:55:03+0300  
> Fabrika: `/Users/ulas/Desktop/Repo`  
> Smoke app: `test/factory-smoke-app`

## Özet

| Metrik | Değer |
|--------|-------|
| ✅ Geçti | 41 |
| ❌ Başarısız | 0 |
| ⚠️ Uyarı | 0 |
| ⏭️ Atlandı | 1 |
| **Başarı oranı** | **97%** (fail hariç) |

## Adım denetimi

| ID | Adım | Sonuç | Detay |
|----|------|-------|-------|
| F0.1 | first-setup.sh mevcut | ✅ pass |  |
| F0.2 | init-governance.sh mevcut | ✅ pass |  |
| F0.3 | docs/00-INDEX.md | ✅ pass |  |
| F0.4 | YAPILACAKLAR.md + validator | ✅ pass | validate-yapilacaklar.py exit 0 |
| F0.5 | validate-audit-chain.py | ✅ pass |  |
| F0.MCP | check-mcp.sh P0 | ✅ pass |  |
| F1.1 | test/docs/SMOKE_APP_BRIEF.md | ✅ pass |  |
| F1.2 | templates/vision mevcut | ✅ pass |  |
| F2.1 | ANDROID_STRUCTURE.md | ✅ pass |  |
| F2.2 | MODULE_MAP template | ✅ pass |  |
| F2.3 | 33 layer slices (33 dosya) | ✅ pass |  |
| F3.1 | test/factory-smoke-app/settings.gradle.kts | ✅ pass | bootstrap-smoke-app.sh çalıştırın |
| F3.2 | 10 modül (settings.gradle.kts) | ✅ pass | include count=11 |
| F3.3 | gradlew executable | ✅ pass |  |
| F3.4 | audit-android-scaffold (template) | ✅ pass | fabrika template |
| F4.1 | locales tr.json + en.json | ✅ pass |  |
| F4.2 | GlassCard.kt | ✅ pass |  |
| F4.3 | hard-coded TR string yok (.kt) | ✅ pass | rg yoksa skip |
| F5.1 | audit-security.sh | ✅ pass |  |
| F5.2 | audit-oem-compat.sh | ✅ pass |  |
| F5.3 | RootDetector.kt şablon | ✅ pass |  |
| F6.1 | SPRINT_P schema template | ✅ pass |  |
| CX.1 | gradle-build-loop.sh | ✅ pass |  |
| CX.2 | state-recovery.sh | ✅ pass |  |
| CX.3 | validate-layer-slices.sh | ✅ pass |  |
| CX.4 | phase-agents.json | ✅ pass |  |
| CX.5 | 18-state-recovery.mdc | ✅ pass |  |
| V2.1 | 19-claude-reasoning.mdc mevcut | ✅ pass |  |
| V2.2 | 19-claude-reasoning alwaysApply: true | ✅ pass |  |
| V2.3 | thinking + architecture_check şablon (.mdc) | ✅ pass |  |
| V2.4 | .cursorrules Claude-Native protokol | ✅ pass |  |
| V2.5 | docs/CLAUDE_REASONING.md | ✅ pass |  |
| V2.6 | 20-aistudio-import (19 reasoning ayrımı) | ✅ pass |  |
| V2.7 | validate-reasoning-template-xml.sh | ✅ pass | thinking/architecture_check/negative_constraints dengesi |
| V2.8 | negative_constraints şablon (.mdc) | ✅ pass |  |
| V2.9 | kelime cap 150-200 (.mdc) | ✅ pass |  |
| QG.1 | validate-code.sh | ✅ pass |  |
| QG.2 | audit-layers.sh | ✅ pass |  |
| QG.3 | audit-layer-components.sh | ✅ pass |  |
| QG.4 | factory-health.sh 100 | ✅ pass |  |
| QG.5 | factory-quality-gate.sh | ✅ pass | MCP yerel uyarı olabilir |
| BUILD | factory-smoke-app assembleDebug | ⏭️ skip | JDK yok veya gradlew eksik — docs/BOOTSTRAP.md JDK 17+ |

## Fabrika akışı (uygulanması gerekenler)

| Sıra | Komut | Smoke testte |
|------|-------|----------------|
| 1 | `./scripts/first-setup.sh` | Fabrika kökünde mevcut |
| 2 | `./scripts/init-new-app.sh` | **Kökü değiştirmez** — `test/bootstrap-smoke-app.sh` kullanıldı |
| 3 | `./scripts/governance/init-governance.sh` | Fabrika kök governance seed |
| 4 | `./scripts/scaffold-android-project-to.sh` | `test/factory-smoke-app` |
| 5 | `./scripts/gradle-build-loop.sh` | BUILD satırında test |
| 6 | `./scripts/state-recovery.sh --checkpoint` | bootstrap adım 5 |
| 7 | `python3 scripts/governance/validate-yapilacaklar.py` | F0.4 |
| 8 | `./scripts/factory-quality-gate.sh` | Manuel: fabrika kökünden |

## Sonraki adım

```bash
./test/bootstrap-smoke-app.sh    # smoke app oluştur / yenile
./test/run-factory-audit.sh      # yalnızca audit
```
