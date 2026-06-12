# Liquid Glass Tasarım Standardı

Katman: **3, 5** | Sorumlu: Android Elite Ajanı

## Prensipler

1. **Derinlik:** Katmanlı yüzeyler — arka plan blur + yarı saydam kartlar
2. **Hareket:** 120fps hedefi, spring tabanlı animasyonlar
3. **Adaptif:** Phone (compact) + Tablet (expanded) layout zorunlu
4. **Dark Mode:** Sistem temasına otomatik uyum

## Design Tokens

```kotlin
// core/designsystem/theme/GlassTokens.kt
object GlassTokens {
    val SurfaceBlur = 24.dp
    val GlassAlpha = 0.72f
    val CornerRadius = 20.dp
    val ElevationGlass = 0.dp  // blur ile derinlik, shadow değil
}
```

## Compose Bileşen Kuralları

- `Modifier.graphicsLayer { renderEffect = BlurEffect(...) }` — API 31+
- Düşük API: yarı saydam gradient fallback
- `animate*AsState` veya `spring()` — lineer animasyon yasak (micro-interaction hariç)
- Minimum dokunma alanı: **48dp**

## Yasaklar

- Material2 `Card` elevation-only tasarım
- Sabit renk hex — `MaterialTheme.colorScheme` veya token kullan
- Phone-only layout (tablet kırılımı zorunlu)

## Referans Yapı

```text
core/designsystem/
├── theme/Color.kt, Type.kt, Theme.kt, GlassTokens.kt
├── component/GlassCard.kt, GlassButton.kt, GlassTopBar.kt
└── animation/SpringSpecs.kt
```
