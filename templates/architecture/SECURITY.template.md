# Güvenlik Tehdit Modeli — {{APP_NAME}}

> Mimar Ajanı doldurur. Standart: `docs/03-STANDARDS/SECURITY.md`

## Varlıklar

| Varlık | Hassasiyet | Şifreleme |
|--------|------------|-----------|
| Kullanıcı verisi | Yüksek | SQLCipher |
| Auth token | Kritik | EncryptedSharedPreferences |
| Analytics | Düşük | — |

## Tehditler

| Tehdit | Önlem | Katman |
|--------|-------|--------|
| Root cihaz | RootDetector | 16 |
| Emulator | EmulatorDetector | 16 |
| MITM | TLS + pinning (V2) | 16 |
| OEM background kill | OemCompatFacade | 22 |

## Release Kontrolleri

- [ ] R8 aktif
- [ ] Secrets git'te yok
- [ ] Penetrasyon testi (opsiyonel)
