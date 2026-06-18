# ULAS Phase 6 — Predictive Decision Framework

**Date:** 2026-06-18  
**Mode:** Prediction design — **gated activation**  
**Shift:** Adaptive (reactive) → **Predictive (proactive)**

---

## Mimar ayrımı (doğru)

Phase 5 ekseni:

```
Decision → Outcome → Adaptation
```

Phase 6 ekseni:

```
Observation → Prediction → Decision → Outcome → Adaptation
```

Phase 5 = hata oldu, davranış değişti.  
Phase 6 = **hata ihtimali yüksek**, önlem al.

---

## Olgunluk haritası

| Phase | Ad | Durum |
|-------|-----|-------|
| 1 | Factory | ✅ Android scaffold |
| 2 | Knowledge | ✅ ULAS principles |
| 3 | Learning | ⚠️ scripts, no venture data |
| 4 | Decision OS | ✅ decide/audit/metrics |
| 5 | Adaptive Decision OS | ✅ propagate/overrides |
| **6** | **Predictive Decision OS** | **📐 designed, gate closed** |

---

## Risk Engine (not Risk Agent)

Config: [`scoring/risk-engine.json`](scoring/risk-engine.json)

| Girdi | Nasıl |
|-------|-------|
| Decision class | class base score A=12 … D=72 |
| Trust | düşük avg trust → risk ↑ |
| Reviewer history | missed rate from metrics |
| Context tier | tier 3/critical → risk ↑ |
| Evidence | none → max evidence risk |
| Memory hits | NEVER_AGAIN hit → risk ↑ |
| Policy overrides | aktif adaptation → risk ↑ |
| Similar failures | geçmiş approved_failed → risk ↑ |
| Complexity | keyword + length heuristic |

| Çıktı | Davranış (gate açıkken) |
|-------|-------------------------|
| low (0–39) | mevcut akış |
| medium (40–59) | +auditor chain'e |
| high (60–79) | auditor zorunlu |
| critical (80–100) | auditor + security + founder gate |

---

## Neden hemen devreye alınmıyor?

Dürüst darboğaz: **Evidence katmanı zayıf.**

Öncelik sırası (Mimar):

1. Feedback loop closure  
2. Trust explainability  
3. Trend analysis  
4. Predictive risk ← **bu faz, gated**

Activation gate kapalı. Preview her zaman:

```bash
./APP-FABRIKASI/scripts/ulas.sh risk-gate
./APP-FABRIKASI/scripts/ulas.sh risk --venture SLUG --class B \
  --reviewers architect,qa --title "Risky change"
```

Gate açılınca `decide()` prediction'ı **enforce** eder.

---

## CLI

```bash
ulas risk-gate                              # activation criteria
ulas risk --venture SLUG --class B ...      # preview (always)
ulas decide ...                             # records prediction; escalates if gate open
```

---

## Model bağımsızlığı (değişmedi)

Risk engine = JSON weights + Python scoring + mevcut review chain.

Cursor, Claude, Gemini — hepsi aynı `ulas risk` çıktısını okur.

---

## Başarı kriteri

> "Bir yıl sonra aynı hatalı kararı verir mi?"

Phase 5: hayır (reaktif).  
Phase 6: **aynı risk profili gelmeden** auditor/founder gate devreye girer (proaktif).

Kanıt: gate açık + `prevented_failure` sayısı > `approved_failed` tekrarı.

→ Framework: [`scoring/PREDICTIVE_DECISION_FRAMEWORK.md`](scoring/PREDICTIVE_DECISION_FRAMEWORK.md)

---

## Yasaklar (aynı)

Yeni agent · departman · council · governance · platform adapter.
