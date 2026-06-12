# OEM / ROM Uyumluluk Standardı

Katman: **22** | Uygulama: Android Elite | Denetim: OEM Uyumluluk Denetçisi (`05-oem-compat-auditor.mdc`)

## Neden Zorunlu?

Aynı Android API seviyesi, farklı üreticide **tamamen farklı davranır**. MIUI arka planı agresif öldürür, Samsung sleeping apps listesi uygulamayı durdurur, ColorOS autostart ister. Fabrika standartları bunu **tek seferde** ele alır.

## Hedef Üreticiler (P0 — Release Blocker)

| Öncelik | Üretici | ROM | Kritik Risk |
|---------|---------|-----|-------------|
| P0 | Samsung | One UI | Sleeping apps, battery optimization |
| P0 | Xiaomi | MIUI / HyperOS | Autostart, aggressive kill, overlay |
| P1 | OPPO | ColorOS | Background freeze, autostart |
| P1 | vivo | OriginOS | Background restriction |
| P1 | Google | Stock / Pixel | Referans davranış |
| P2 | Huawei | EMUI | HMS, background limits |
| P2 | Motorola | My UX | Hafif sapmalar |
| P2 | Realme | Realme UI | ColorOS türevi |

Detaylı checklist: [`OEM_MATRIX.yaml`](./OEM_MATRIX.yaml)

## Zorunlu Modül Yapısı

```text
core/oem/
├── Manufacturer.kt              # enum: SAMSUNG, XIAOMI, OPPO, VIVO, ...
├── ManufacturerDetector.kt      # Build.MANUFACTURER + ROM fingerprint
├── OemBatteryOptimizer.kt       # Battery whitelist intent yönlendirme
├── OemAutostartGuide.kt         # MIUI/ColorOS autostart UI
├── OemNotificationHelper.kt     # Kanal önceliği OEM ayarı
├── OemWorkManagerConfig.kt      # OEM'e göre constraint gevşetme
├── OemIntentResolver.kt         # Üreticiye özel Settings intent'leri
└── OemCompatFacade.kt           # Tek giriş noktası (Facade)
```

## Kritik Davranış Matrisi

### Arka Plan Sync

```kotlin
// ✅ DOĞRU — OEM zinciri
fun scheduleSync() {
    when (manufacturerDetector.current()) {
        Manufacturer.XIAOMI -> oemAutostartGuide.showIfNeeded()
        Manufacturer.SAMSUNG -> oemBatteryOptimizer.requestUnrestricted()
        else -> Unit
    }
    workManager.enqueue(syncRequest.withOemConstraints())
}
```

### MIUI Özel (En Sık Sorun)

1. **Autostart** kapalıysa `WorkManager` çalışmaz → kullanıcıyı `OemAutostartGuide` ile yönlendir
2. **Battery saver** "Restricted" ise alarm gecikir → `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` + MIUI security center intent
3. **Display pop-up** (bazı overlay özellikleri) → ayrı izin akışı

### Samsung One UI

1. **Sleeping apps** — kullanıcıya "Never sleeping" rehberi
2. **Deep sleeping** — FCM high-priority + kullanıcı bildirimi
3. Knox güvenlik API'leri ile çakışma yok — standart Android API kullan

## Kullanıcı Rehberi (i18n)

OEM ayar ekranlarına yönlendirme metinleri `assets/locales/tr.json` / `en.json`:

```json
{
  "oem_miui_autostart_title": "Arka Plan İzni Gerekli",
  "oem_miui_autostart_body": "Xiaomi cihazlarda uygulamanın düzgün çalışması için Autostart'ı açın.",
  "oem_samsung_battery_title": "Pil Kısıtlamasını Kaldırın"
}
```

## Test Zorunluluğu

Her release öncesi `docs/02-ARCHITECTURE/OEM_TEST_REPORT.md` doldurulur:

| Üretici | Cihaz / Emülatör | Sync | Push | Alarm | Durum |
|---------|------------------|------|------|-------|-------|
| Xiaomi | Redmi Note serisi | ⬜ | ⬜ | ⬜ | |
| Samsung | Galaxy A/S serisi | ⬜ | ⬜ | ⬜ | |

Denetim: `./scripts/audit-oem-compat.sh`

## Auditor Entegrasyonu

Ana Denetçi (`04-auditor-security.mdc`) release onayı vermeden önce OEM Denetçisinin raporunu ister. P0 OEM fail = release blok.
