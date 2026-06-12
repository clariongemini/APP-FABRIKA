# FCM Push Standardı

Katman: **11, 20** | Şablon: `AppFirebaseMessagingService.kt`

## Kurulum

1. Firebase Console → proje oluştur
2. `google-services.json` → `app/` (git'e commit etme — CI secret)
3. `google-services.json.example` referans al

## Davranış

| Senaryo | Aksiyon |
|---------|---------|
| Data message | SyncWorker tetikle |
| Notification | Kanal IMPORTANCE_HIGH |
| Token refresh | V2 backend'e gönder |
| OEM kill sonrası | FCM high-priority recovery |

## OEM Entegrasyonu

```kotlin
override fun onMessageReceived(message: RemoteMessage) {
    oemCompat.prepareForBackgroundWork()
    syncScheduler.enqueueOneTime()
}
```

## Denetçi

- `POST_NOTIFICATIONS` runtime izni (API 33+)
- Notification channel tanımlı
- PII payload'da yok
