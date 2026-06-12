# Modül Haritası — {{APP_NAME}}

> Mimar Ajanı bu dosyayı uygulama geliştikçe günceller.

## Core Modüller

| Modül | Sorumluluk | Katman |
|-------|------------|--------|
| `:core:common` | Result, extensions, dispatcher | 7 |
| `:core:designsystem` | Liquid Glass, theme | 3 |
| `:core:i18n` | Locale JSON loader | 6 |
| `:core:database` | Room + SQLCipher | 8, 16 |
| `:core:network` | Retrofit/Ktor (V2 stub) | 11 |
| `:core:security` | Root detect, encryption | 16 |

## Feature Modüller

| Modül | Açıklama | Durum |
|-------|----------|-------|
| `:feature:home` | Ana ekran | ⬜ Planlandı |
| `:feature:settings` | Ayarlar | ⬜ Planlandı |
| `:feature:premium` | Monetizasyon | ⬜ Planlandı |

## Bağımlılık Grafi

```text
:app
 ├── :feature:home
 ├── :feature:settings
 ├── :feature:premium
 └── :core:designsystem
      └── :core:common
```

## Notlar

*(Mimar Ajanı ADR referansları buraya)*
