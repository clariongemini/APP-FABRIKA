# Play Integrity Standardı

Katman: **16** | Şablon: `PlayIntegrityChecker.kt`

## Amaç

Sahte cihaz, mod APK ve billing fraud önleme.

## V1 (Stub)

- `DefaultPlayIntegrityChecker` stub token döner
- Kritik işlemlerde interface hazır

## V2 (Production)

1. Backend nonce üretir
2. Client `IntegrityManagerFactory` ile token alır
3. Backend Google API ile doğrular
4. Başarısız → işlem engelle

## Tetikleme Noktaları

- Premium satın alma öncesi
- Hassas veri sync
- API auth token yenileme

## Denetçi

- Production'da stub kalmamalı (V2 gate)
- Nonce tek kullanımlık
