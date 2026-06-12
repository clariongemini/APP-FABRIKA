# Release Checklist — Play Store

Mimar onayı + tüm denetçiler geçmeden yayın yok.

## Otomatik Denetim

```bash
./scripts/factory-health.sh    # Fabrika sağlık + puan
./scripts/pre-commit.sh      # Tam denetim zinciri
```

## P0 — Release Blocker

- [ ] `./scripts/audit-oem-compat.sh` — Samsung + Xiaomi P0 test
- [ ] `docs/02-ARCHITECTURE/OEM_TEST_REPORT.md` — P0 passed
- [ ] `docs/03-STANDARDS/SECURITY.md` kontrolleri geçti
- [ ] SQLCipher + EncryptedSharedPreferences aktif
- [ ] ProGuard/R8 release build
- [ ] i18n tr + en tam
- [ ] 0 critical crash (Crashlytics)
- [ ] Offline-first sync veri kaybı testi

## P1 — Major

- [ ] OPPO + vivo OEM test
- [ ] Play Billing trial → paid akışı test
- [ ] Privacy consent + silme/export
- [ ] Performans: cold start < 1.5s mid-range
- [ ] Unit test — kritik use-case'ler

## P2 — Nice to Have

- [ ] Huawei EMUI test
- [ ] Tablet layout smoke test
- [ ] Maestro E2E ana akış

## Onay İmzaları

| Rol | Ajan | Onay |
|-----|------|------|
| Ürün | CPO | ⬜ |
| Mimari | Architect | ⬜ |
| Kod | Android Elite | ⬜ |
| Güvenlik | Auditor | ⬜ |
| OEM | OEM Denetçi | ⬜ |
| Mimar | Ulaş | ⬜ |
