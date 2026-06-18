# North Star — APP-FABRIKASI

## Mission

**Create repeatable software ventures that learn from evidence and improve capital allocation over time.**

Türkçe:

> Kanıttan öğrenen ve zaman içinde sermaye tahsisini iyileştiren, tekrarlanabilir yazılım girişimleri oluştur.

---

## Android Factory vs APP-FABRIKASI

| | Android-App (Factory) | APP-FABRIKASI (OS) |
|---|----------------------|---------------------|
| **Soru** | Nasıl üretirim? | Nasıl şirketleşirim, öğrenirim, portföy yönetirim? |
| **Birim** | APK / modül | Venture |
| **Başarı** | CI green, scaffold ship | Uçtan uca venture lifecycle kanıtı |

Factory bir **adaptördür**. OS venture'ı yönetir.

---

## Tek başarı metriği (Stabilization Mode)

> **"APP-FABRIKASI ilk gerçek venture'ını uçtan uca yönetti."**

Değil: "Yeni klasör oluşturuldu."

---

## İlk venture (her projede)

Repoda hazır venture **yok**. Hedef projede `init-venture.sh` ile oluşturulur:

```bash
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
```

| Alan | Şablon |
|------|--------|
| **Slug** | `{slug}` — örn. `my-app` |
| **Ad** | Charter'da tanımlanır |
| **Platform** | `android`, `ios`, `web`, … |
| **Durum** | Charter → build → ship → evidence |

### Lifecycle checklist

- [ ] 1. Venture charter created (`08-ventures/{slug}/`)
- [ ] 2. Product shipped (store / production)
- [ ] 3. Evidence bundle generated (`07-evidence/{slug}/`)
- [ ] 4. Outcome recorded
- [ ] 5. Postmortem completed (`06-learning/postmortems/`)
- [ ] 6. Learning artifacts updated (ADR / pattern)
- [ ] 7. Intelligence consumes real data (`01-core/intelligence/`)

---

## Skor hedefi

| Durum | Skor | Anlam |
|-------|------|-------|
| Şimdi | **58** | İskelet tamam, kas yok — beklenen |
| İlk venture loop sonrası | **75–80** | OS validate edildi |
| 3+ venture + portfolio | **85+** | Capital allocation aktif |

---

## Stabilization Mode

→ [`STABILIZATION.md`](STABILIZATION.md)

Scaffold genişlemesi durdu. İlk venture hedef projede validate edilir.
