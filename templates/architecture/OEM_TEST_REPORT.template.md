# OEM Test Raporu — {{APP_NAME}}

> OEM Denetçisi (`05-oem-compat-auditor.mdc`) release öncesi doldurur.
> Matris: `docs/03-STANDARDS/OEM_MATRIX.yaml`

## Özet

| Alan | Değer |
|------|-------|
| Sürüm | |
| Test Tarihi | |
| Denetçi Onayı | ⬜ Bekliyor |

## P0 Üreticiler (Release Blocker)

### Samsung One UI

| Test | Cihaz | Sonuç | Not |
|------|-------|-------|-----|
| Battery unrestricted | | ⬜ | |
| Background sync 30dk | | ⬜ | |
| FCM push | | ⬜ | |
| Exact alarm | | ⬜ | |

### Xiaomi MIUI / HyperOS

| Test | Cihaz | Sonuç | Not |
|------|-------|-------|-----|
| Autostart | | ⬜ | |
| Battery No restrictions | | ⬜ | |
| SyncWorker survives kill | | ⬜ | |
| Notification channels | | ⬜ | |

## P1 Üreticiler

| Üretici | ROM | Sync | Push | Durum |
|---------|-----|------|------|-------|
| OPPO ColorOS | | ⬜ | ⬜ | |
| vivo OriginOS | | ⬜ | ⬜ | |
| Google Pixel | | ⬜ | ⬜ | |

## Bilinen Sorunlar

| # | Üretici | Sorun | Çözüm | Durum |
|---|---------|-------|-------|-------|
| 1 | | | | |

## Denetçi Kararı

- [ ] P0 tüm testler geçti — release onaylı
- [ ] P0 fail — release blok
