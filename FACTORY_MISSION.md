# Factory Mission

> Factory'nin amacı daha fazla governance üretmek değil, daha kısa sürede daha başarılı Android ürünleri üretmektir.

**Amaç değil:** Kendi kendini yöneten yapay şirket kurmak.

---

## Durum

| Alan | Değer |
|------|-------|
| **Status** | FROZEN |
| **Maturity** | PRODUCTION READY — complete enough to ship |
| **Mode** | MAINTENANCE |
| **Next objective** | Validate through products |

CEO seviyesinde tek soru:

> **Factory kullanılarak ilk gelir ne zaman geliyor?**

---

## Doğru metrikler (dış)

| Metrik | Soru |
|--------|------|
| İlk APK | Kaç günde çıktı? |
| İlk beta | Kaç günde çıktı? |
| İlk kullanıcı | Kaç günde geldi? |
| İlk 100 kullanıcı | Kaç günde geldi? |
| **İlk ödeme** | Kaç günde geldi? |

Uzun vadede **Time to First Revenue**, Factory Health'ten daha değerli özet metrik.

## İç metrikler (destekleyici — amaç değil)

33 katman · 16 ajan · 100/100 quality gate · CEO V7 · Intelligence Layer

Bunlar fabrikanın **araçlarıdır**; başarı ölçütü değildir.

---

## Korunan çekirdek (dokunulmaz)

- **Factory:** `init-new-app.sh` · `sync-standards.sh`
- **Governance:** F0–F8 · CEO · CAO · PDC · CEC · CDID · AID · EGC
- **Architecture:** 33 layer · 10 modül · 13 standart · OEM
- **Measurement:** AID · Outcomes · Portfolio

---

## Outcome validation

```
Factory → sync-standards → Governance → AID → Release → User → Revenue → Outcome
```

Bu zincir **hedef projede** kanıtlanır — fabrika şablonunda örnek uygulama adı taşınmaz.

Detay: [`factory/outcomes/README.md`](factory/outcomes/README.md) · [`docs/FACTORY_FREEZE.md`](docs/FACTORY_FREEZE.md)
