# Android Platform Adapter

**Durum:** Operational (Android Factory v3.1 — frozen)

## Implementation (repo kökü — dokunulmaz)

| Kaynak | Path |
|--------|------|
| Gradle scaffold | `templates/android/project/` |
| Bootstrap | `scripts/init-new-app.sh` |
| CI smoke | `scripts/ci-template-build.sh` |
| Standards | `docs/03-STANDARDS/` |
| Governance (geçiş) | `governance/` |

## Stack

- Kotlin · Jetpack Compose · Clean Architecture
- Modular: app + 7 core + 3 feature
- Offline-first · Room/SQLCipher · Hilt
- i18n JSON · Liquid Glass design tokens
- Play Integrity · FCM · OEM compat

## Venture akışı

```bash
git clone https://github.com/clariongemini/APP-FABRIKA.git my-venture
cd my-venture
./scripts/init-new-app.sh "Venture Name" "com.company.app"
# SVOS: 08-ventures charter + 05-templates/android-app checklist
```

## Validation

- `./scripts/factory-quality-gate.sh`
- GitHub Actions: Factory Validation v3.1.0
- Platform gate: `assembleDebug` smoke

## SVOS ilişkisi

Android Factory = bu adaptörün **ilk tam implementasyonu**.  
SVOS bu dosyaları kopyalamaz; referans eder.
