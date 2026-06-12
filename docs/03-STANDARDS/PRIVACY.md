# Gizlilik Standardı (KVKK / GDPR)

Katman: **17** | Sorumlu: Denetçi Ajanı

## Privacy By Design

1. Topla → yalnızca gerekli veri (Data Minimization)
2. Sakla → şifreli, süre sınırlı
3. Sil → kullanıcı talebi ile tam silme
4. Aktar → export (JSON) imkânı

## Zorunlu Ekranlar / Akışlar

| Akış | Zorunlu |
|------|---------|
| İlk açılış gizlilik onayı | ✅ |
| İzin isteme gerekçesi (runtime) | ✅ |
| Ayarlar → Verilerimi İndir | ✅ V1.1+ |
| Ayarlar → Hesabımı Sil | ✅ |
| Çerez/analitik opt-out | ✅ |

## KVKK (Türkiye)

- Açık rıza metni Türkçe (`tr.json`)
- Veri sorumlusu bilgisi
- Amaç ve hukuki sebep belirtilmeli
- 6698 sayılı kanun — silme/export hakları

## GDPR (AB kullanıcıları)

- Lawful basis documented
- DPO iletişim (varsa)
- Right to erasure 30 gün içinde

## Teknik Uygulama

```text
feature/privacy/
├── ConsentRepository.kt
├── DataExportUseCase.kt
└── AccountDeletionUseCase.kt   # soft delete + hard delete queue
```

## Analytics (Katman 18)

- Opt-out sonrası event gönderimi durur
- PII event parametrelerinde yasak
- User ID hash'lenmiş veya anonim

## Denetçi Red

- Analytics opt-out çalışmıyor
- Silme talebi queue'da takılı kalıyor
- PII loglarda görünüyor
