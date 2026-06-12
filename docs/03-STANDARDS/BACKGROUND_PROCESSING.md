# Arka Plan İşleme Standardı

Katman: **9, 11, 20, 22** | OEM entegrasyon: `OEM_COMPATIBILITY.md`

Arka plan sync, alarm ve push — özellikle **MIUI/Samsung** ortamında — fabrika standardının kritik parçasıdır.

## Mimari Zincir

```text
UseCase → SyncScheduler
           ├── OemCompatFacade (autostart / battery önce)
           ├── WorkManager (birincil)
           ├── AlarmManager (exact alarm — OEM policy)
           └── FCM high-priority (push tetikleme)
```

## WorkManager (Birincil)

```kotlin
val request = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
    .setConstraints(
        Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()
    )
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
    .build()
```

- `CoroutineWorker` + `Result` pattern
- `UniqueWork` ile duplicate önleme: `KEEP` veya `REPLACE` bilinçli seçim
- OEM kill sonrası: uygulama açılışında `enqueueUniqueWork` ile recovery

## Offline-First Sync (Katman 9)

1. Yerel yaz → `SyncQueue` tablosu
2. Ağ varsa → batch upload
3. Conflict → `ConflictResolver` (son yazan / kullanıcı onayı)
4. Başarısız → exponential backoff + queue retention

## Exact Alarm (API 31+)

```kotlin
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    if (alarmManager.canScheduleExactAlarms()) { /* schedule */ }
    else { oemExactAlarmGuide.requestPermission() }
}
```

## Foreground Service Politikası

- Sadece kullanıcıya görünür uzun işlemler (medya, navigasyon)
- Sync için **WorkManager tercih** — gereksiz FGS yasak (Katman 32)
- FGS kullanılıyorsa `foregroundServiceType` doğru tanımlanmalı

## OEM Zorunlu Akış

Arka plan işi planlamadan **önce**:

```kotlin
oemCompat.prepareForBackgroundWork()  // autostart + battery check
syncScheduler.schedule()
```

## Denetçi Kontrol Listesi

| Kontrol | Zorunlu |
|---------|---------|
| WorkManager sync worker | ✅ |
| OEM facade entegrasyonu | ✅ |
| Offline queue veri kaybı yok | ✅ |
| GlobalScope kullanımı yok | ✅ |
| MIUI'de 30dk background test | ✅ P0 |

## Proje Belgesi

`docs/02-ARCHITECTURE/DATA_FLOW.md` — sync stratejisi burada detaylandırılır.
