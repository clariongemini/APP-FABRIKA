# Modül Haritası — Factory (fabrika şablonu)

> **Package:** `com.ulas.factory` · **Sürüm:** v2.1.0-stable  
> Kaynak iskelet: `templates/android/project/settings.gradle.kts` · Smoke: `test/factory-smoke-app`

## Core modüller

| Modül | Sorumluluk | Katman |
|-------|------------|--------|
| `:core:common` | Result, extensions, dispatcher | 7 |
| `:core:designsystem` | Liquid Glass, theme, GlassCard | 3, 4 |
| `:core:i18n` | Locale JSON loader (`assets/locales`) | 6 |
| `:core:database` | Room + SQLCipher | 8, 16 |
| `:core:network` | Retrofit/Ktor stub (V2 genişler) | 11 |
| `:core:security` | Root detect, encryption, Play Integrity | 16 |
| `:core:oem` | Samsung/MIUI/OPPO ROM uyumu | 22 |

## Feature modüller

| Modül | Açıklama | Durum |
|-------|----------|-------|
| `:feature:home` | Ana ekran / MVP loop | ⬜ Şablon |
| `:feature:settings` | Ayarlar, locale | ⬜ Şablon |
| `:feature:premium` | Billing, abonelik | ⬜ Şablon |

## Application

| Modül | Sorumluluk |
|-------|------------|
| `:app` | Hilt root, Navigation, Application sınıfı |

## Bağımlılık grafi

```text
:app
 ├── :feature:home
 ├── :feature:settings
 ├── :feature:premium
 ├── :core:designsystem
 ├── :core:i18n
 ├── :core:security
 └── :core:oem
      └── :core:common
```

## Feature iç yapı (her `:feature:*`)

```text
data/ → domain/ ← presentation/
         ↑
    core/* (designsystem, i18n, database…)
```

## AI Studio import notu

Ham Stitch/AI Studio export genelde yalnızca `:app` içerir. Bootstrap sonrası F3'te kademeli modül ayrımı bu haritaya göre yapılır (`bootstrap-external-project.sh`).

## ADR referansları

- ADR-009: Executive OS — `docs/CHANGELOG.md`
- Katman manifest: `docs/33-LAYER-MANIFEST.yaml`
