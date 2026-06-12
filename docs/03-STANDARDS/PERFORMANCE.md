# Performans Standardı

Katman: **21, 32** | Sorumlu: Denetçi + Android Elite Ajanları

## Zorunlu Hedefler (Katman 32)

| Metrik | Hedef |
|--------|-------|
| Crash rate | 0% (release) |
| Cold start | < 1.5s (mid-range cihaz) |
| Frame time | 120fps hedef (ProMotion), min 60fps |
| ANR | 0 |
| Veri kaybı | 0 (offline queue + retry) |

## Compose Optimizasyonu

```kotlin
// ✅ Stable parametreler
@Composable
fun ItemRow(item: ItemUiModel) { ... }

// ✅ key ile LazyColumn
items(items, key = { it.id }) { ... }

// ✅ remember ile pahalı hesaplama
val filtered = remember(query, items) { items.filter { ... } }

// ❌ inline lambda her recomposition'da yeni instance
onClick = { viewModel.onClick() }  // method reference tercih et
```

## Bellek

- `viewModelScope` / `lifecycleScope` — GlobalScope yasak
- Flow: `SharingStarted.WhileSubscribed(5000)`
- Bitmap: boyut sınırı + Coil/Glide cache politikası
- Compose: `DisposableEffect` ile listener temizliği

## Başlangıç (Cold Start)

- Hilt lazy injection kritik path dışında
- `App Startup` ile paralel init
- Ana ekran için skeleton UI — blocking load yok

## Denetim

Auditor her PR'da kontrol eder:
- Gereksiz recomposition (Layout Inspector)
- LeakCanary (debug build)
- StrictMode (debug build)

## Düşük Uç Cihaz (Katman 22)

- `android:largeHeap` kullanma — mimari çözüm
- Animasyon degrade: sistem "animasyon kapalı" ise reduce motion
- Test: API 26, 2GB RAM emülatör
