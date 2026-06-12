# Fabrika Kusursuzluk Skor Kartı

Otomatik güncelleme: `./scripts/factory-health.sh`

## Hedef: Her Kategori 10/10

| # | Kategori | Hedef | İçerik |
|---|----------|-------|--------|
| 1 | AI Orkestrasyon & Vizyon | 10 | Overmind, 5 ajan, 33 katman |
| 2 | 33 Katman Bütünlüğü | 10 | 360 bileşen manifest |
| 3 | Kullanışlılık (DX) | 10 | init, sync, scaffold scriptleri |
| 4 | Kod Tasarımı / Mimari | 10 | Clean Arch + tam modül scaffold |
| 5 | UI / Liquid Glass / i18n | 10 | Compose tema + locales |
| 6 | Güvenlik & Gizlilik | 10 | SECURITY, PRIVACY, PENTEST |
| 7 | Arka Plan & FCM | 10 | WorkManager + FCM şablonu |
| 8 | OEM / ROM | 10 | Samsung, MIUI matris + OEM modül |
| 9 | Monetizasyon & Integrity | 10 | Billing + Play Integrity |
| 10 | Test & CI/CD | 10 | Maestro + GitHub Actions |

## Tek Komutla Tam Kurulum

```bash
./scripts/init-new-app.sh "UygulamaAdi" "com.sirket.app"
```

Bu komut: belgeler + tam Android iskeleti + OEM + Billing + FCM oluşturur.
