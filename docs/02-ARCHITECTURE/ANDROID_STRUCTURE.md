# Android Proje Yapısı Standardı

Katman: **7, 8, 6** | Sorumlu: Baş Mimar Ajanı

Her Autonomous App Factory projesi bu klasör yapısını izler.

## Kök Yapı

```text
{proje}/
├── .cursorrules                    # Fabrikadan (sync veya template)
├── .cursor/rules/                  # Departman ajanları
├── docs/                           # Hafıza + vizyon + mimari
├── app/
│   └── src/main/
│       ├── assets/locales/         # tr.json, en.json
│       └── java/{package}/
├── core/                           # Paylaşılan modüller
│   ├── common/
│   ├── designsystem/
│   ├── i18n/
│   ├── network/
│   ├── database/
│   ├── security/
│   └── oem/                        # Samsung/MIUI/OPPO ROM uyumu (Katman 22)
├── feature/                        # Feature-based modüller
│   ├── home/
│   ├── settings/
│   └── premium/
├── build.gradle.kts
└── settings.gradle.kts
```

## Feature Modül İç Yapısı

```text
feature/home/
├── data/
│   ├── local/HomeDao.kt
│   ├── remote/HomeApi.kt
│   ├── mapper/HomeMapper.kt
│   └── repository/HomeRepositoryImpl.kt
├── domain/
│   ├── model/HomeItem.kt
│   ├── repository/HomeRepository.kt
│   └── usecase/GetHomeItemsUseCase.kt
└── presentation/
    ├── HomeScreen.kt
    ├── HomeViewModel.kt
    └── HomeUiState.kt
```

## Bağımlılık Kuralları

```
presentation → domain ← data
     ↓            ↓
   core/designsystem, core/i18n
```

- `domain` hiçbir Android framework sınıfına bağımlı olmaz
- `data` → `domain` interface implement eder
- `presentation` → `domain` use case çağırır, `data`'ya doğrudan erişmez

## Gradle Modül Stratejisi

| Modül | Tip | Açıklama |
|-------|-----|----------|
| `:app` | application | DI root, navigation |
| `:core:*` | library | Paylaşılan altyapı |
| `:feature:*` | library | İzole özellikler |

## V1 vs V2

| | V1 | V2 |
|---|----|----|
| Veri | Room + JSON assets | + REST API |
| Sync | Offline queue | Bi-directional sync |
| Auth | Local | JWT + refresh |

V1'de `core/network` interface hazır, implementasyon stub.

## Yeni Modül Ekleme Checklist

1. `docs/02-ARCHITECTURE/MODULE_MAP.md` güncelle
2. `feature/{name}/` klasör yapısını oluştur
3. `settings.gradle.kts`'e include et
4. Hilt modülü tanımla
5. i18n anahtarlarını `locales/*.json`'a ekle
