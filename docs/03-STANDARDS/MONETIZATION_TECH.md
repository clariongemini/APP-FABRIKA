# Monetizasyon Teknik Standardı

Katman: **25, 26** | Ürün kuralı: CPO Ajanı | Uygulama: Android Elite

## Ürün Kuralı (CPO — Değiştirilemez)

- **7 gün ücretsiz deneme** — deneme **abonelik başlatılarak** verilir
- 7 gün sonunda otomatik faturalama (kullanıcı iptal etmediyse)
- Bölgesel fiyat: US premium USD, TR alım gücüne uygun

## Teknik Stack

- **Google Play Billing Library** (güncel sürüm)
- Abonelik + base plan + offer (free trial)
- Server-side validation (V2) — V1'de client + Play Integrity stub

## Modül Yapısı

```text
feature/premium/
├── domain/
│   ├── model/SubscriptionState.kt
│   └── usecase/CheckPremiumAccessUseCase.kt
├── data/
│   └── billing/BillingRepositoryImpl.kt
└── presentation/
    ├── PaywallScreen.kt
    └── PremiumViewModel.kt
```

## Abonelik Durumları

```kotlin
sealed class SubscriptionState {
    data object Free : SubscriptionState()
    data class Trial(val expiresAt: Instant) : SubscriptionState()
    data class Active(val planId: String) : SubscriptionState()
    data object Expired : SubscriptionState()
}
```

## Paywall Konumu

CPO `docs/01-VISION/MONETIZATION.md` içinde belirler. Teknik kural:
- Paywall **değer anında** gösterilir (aha moment sonrası)
- Offline'da premium durumu cache'lenir (Room)
- Trial bitişinden 24s önce soft reminder (Katman 32 — gereksiz bildirim yok)

## Feature Flag Entegrasyonu (Katman 26)

Premium özellikler `FeatureGate` üzerinden:

```kotlin
featureGate.isEnabled("premium_analytics") // subscription + remote config
```

## Denetçi Kontrolleri

- Trial → paid geçiş Play Console'da doğru offer ile tanımlı
- Premium UI metinleri i18n'de
- Abonelik iptal akışı erişilebilir (Play Store deep link)
- Hassas billing verisi loglanmıyor

## Proje Belgesi

`docs/01-VISION/MONETIZATION.md` — fiyatlar ve paywall stratejisi
