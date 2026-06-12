# Güvenlik Standardı

Katman: **16** | Sorumlu: Denetçi + Android Elite | Denetim: `scripts/audit-security.sh`

## Zorunlu Kontroller

| Alan | Uygulama | Katman |
|------|----------|--------|
| Yerel DB | Room + **SQLCipher** | 16 |
| Hassas prefs | **EncryptedSharedPreferences** | 16 |
| Ağ | TLS 1.2+ (hedef TLS 1.3), Certificate Pinning (V2) | 16 |
| Kod | **R8/ProGuard** release build | 16 |
| Cihaz | Root + Emulator + Hook detection | 16 |
| Token | JWT refresh, secure storage, rotation | 16 |

## ProGuard / R8

```kotlin
// release build.gradle.kts
buildTypes {
    release {
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}
```

## Root / Emulator Detection

```text
core/security/
├── RootDetector.kt
├── EmulatorDetector.kt
└── SecurityChecker.kt    # Facade — kritik işlemler öncesi çağrılır
```

Release'de root/emulator tespiti → hassas işlem engelle veya kullanıcıyı bilgilendir (ürün kararı `SECURITY.md` brifinde).

## Secrets Yönetimi

- API anahtarları: `local.properties` veya CI secrets — **asla** git'e commit etme
- `.gitignore` içinde: `.env`, `*.keystore`, `google-services.json` (örnek hariç)
- BuildConfig ile debug/release ayrımı

## Denetçi Red Kriterleri

- Plain-text şifre/token saklama
- `android:usesCleartextTraffic="true"` (istisna yoksa)
- SQLCipher olmadan hassas veri
- Release'de minify kapalı
- Certificate pinning bypass (debug hariç)

## Proje Belgesi

Uygulama özel tehdit modeli: `docs/02-ARCHITECTURE/SECURITY.md` (init-new-app ile oluşturulur)
