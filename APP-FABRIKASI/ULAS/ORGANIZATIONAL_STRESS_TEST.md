# ULAS Organizational Stress Test

**Date:** 2026-06-18  
**Mode:** Adversarial audit — **no expansion**  
**Auditor stance:** Attempt to break APP-FABRIKA before reality does.

> Success = discovering weaknesses, not proving strength.

---

## Executive verdict: Yanılıyor olabilir miyiz?

**Evet.** Özellikle şu varsayımlarda:

1. ULAS metrikleri gerçek organizasyon kalitesini ölçüyor.
2. `propagate` doğru outcome ile çalışıyor.
3. Sistem kendi kendini dürüstçe denetliyor.
4. Predictive katman evidence olmadan anlamlı.
5. OS geliştirmeye devam etmek, venture ship etmekten daha değerli.

**En ciddi bulgu (kanıtlı):** `status: BLOCKED` bir karara `approved_failed` yazıldı → trust düştü → class B'ye kalıcı auditor + tier_floor eklendi. Sistem **yanlış girdiye doğru öğrenmiş gibi davrandı**.

Bu, "öğretmen kendi sınavını okuyor" riskinin somut örneği.

---

## Sistem öz-değerlendirme tuzağı

```
APP-FABRIKA kuralları
        ↓
APP-FABRIKA metrikleri (ulas metrics / feedback-audit / risk-gate)
        ↓
APP-FABRIKA raporu ("readiness 53", "precision 1.0")
        ↓
"Maturity achieved"
```

Dış doğrulayıcı yok: Play Store crash, revenue, kullanıcı, bağımsız denetçi.

---

## Mevcut runtime kanıtları (2026-06-18)

| Sinyal | Değer | Sorun |
|--------|-------|-------|
| Toplam karar | 6 | Hepsi dev/test |
| Outcomes | 3 | Manuel tag |
| `approved_failed` | 2 | Biri **BLOCKED** kararda |
| `low_confidence_precision` | 1.0 | N=1 block değerlendirildi |
| NEVER_AGAIN entries | 0 | Bellek boş |
| Evidence bundles | 0 | Risk gate kapalı (doğru) |
| Policy overrides | auditor+tier_floor B | Sentetik propagate kaynaklı |

Kaynak: `10-runtime/ulas/metrics/aggregates.json`, `adaptations/policy-overrides.json`, decision JSON'ları.

---

## 1. Circular Logic

### W1.1 — Self-graded readiness

| | |
|--|--|
| **Scenario** | `feedback-audit` kendi `rebuild_metrics()` çıktısını okuyup "readiness 53" üretir. Aynı motor hem sınavı yapar hem not verir. |
| **Probability** | **Certain** (tasarım gereği) |
| **Impact** | High — yanlış güven, erken Phase geçişi |
| **Detection** | Readiness skorunu dış kaynakla (venture outcome) korelasyon; korelasyon yoksa invalid |
| **Mitigation** | Readiness **yalnızca** `07-evidence` + shipped venture verisiyle cap'lenir; self-score observe-only |

### W1.2 — Propagation on semantically invalid outcomes

| | |
|--|--|
| **Scenario** | `my-app-b-20260101000001`: `status: BLOCKED`, outcome: `approved_failed`. Propagate auditor zorunluluğu ve trust cezası uyguladı. "Onaylanmış hata" aslında "hiç onaylanmamış" karar. |
| **Probability** | **Observed** |
| **Impact** | Critical — tüm class B geleceği yapay olarak sıkılaştı |
| **Detection** | `outcome` komutunda `status == APPROVED` şartı; BLOCKED + approved_failed reject |
| **Mitigation** | Propagate öncesi outcome-class validation; mevcut overrides reset + changelog review |

### W1.3 — Precision metric on trivial N

| | |
|--|--|
| **Scenario** | `low_confidence_precision: 1.0` with 1 evaluated block. Rapor "mükemmel blok kalitesi" ima eder. |
| **Probability** | **Current state** |
| **Impact** | Medium — yanlış güven |
| **Detection** | N&lt;10 iken precision raporlama yasak; "insufficient data" |
| **Mitigation** | `metrics-schema.json` minimum sample gate |

---

## 2. Self-Confirming Metrics

### W2.1 — Outcome tagging is honor system

| | |
|--|--|
| **Scenario** | Operatör `approved_success` yazar, gerçekte ship başarısız. Trust artar, risk düşer. |
| **Probability** | High (no external binding) |
| **Impact** | Critical |
| **Detection** | Outcome ↔ `07-evidence` manifest hash linkage; mismatch alarm |
| **Mitigation** | Outcome yalnızca evidence script onayıyla (`record-outcome.py` gate) |

### W2.2 — Propagation-audit marks "partially closed" after synthetic runs

| | |
|--|--|
| **Scenario** | 1-2 propagate sonrası audit "influences future decide: yes" der. Gerçek venture yok. |
| **Probability** | **Observed** |
| **Impact** | Medium — meta ilerleme illüzyonu |
| **Detection** | `influences_future_decide` yalnızca `shipped_ventures > 0` iken true |
| **Mitigation** | Audit flags: `synthetic_data_warning` |

### W2.3 — Risk preview without enforcement looks like progress

| | |
|--|--|
| **Scenario** | `ulas risk` güzel JSON üretir, gate kapalı. Organizasyon "predictive OS var" sanır. |
| **Probability** | Medium |
| **Impact** | Medium — stratejik dikkat dağılması |
| **Detection** | Her raporda `risk_mode: observe` zorunlu banner |
| **Mitigation** | Phase 6 "designed" not "operational" in all outward comms |

---

## 3. Trust Score Manipulation

### W3.1 — Unauthenticated calibrate/propagate

| | |
|--|--|
| **Scenario** | Herhangi biri `ulas calibrate --reviewer architect --outcome good --decision-id test` çalıştırır. **Kanıt:** trust log'da `decision_id: "test"` kaydı var. |
| **Probability** | **Observed** |
| **Impact** | High — trust sinyali güvensiz |
| **Detection** | `decision_id` must exist + outcome_recorded; unknown ID reject |
| **Mitigation** | Validate decision_id in calibrate/propagate; signed changelog (future, no new agent) |

### W3.2 — Trust floor prevents real accountability

| | |
|--|--|
| **Scenario** | `floor: 50` — sürekli hata eden reviewer 50'de takılır, hâlâ zincirde sayılır. |
| **Probability** | Medium over time |
| **Impact** | Medium |
| **Detection** | Reviewer trust &lt; 60 + missed &gt; 3 → block from `provided_reviewers` |
| **Mitigation** | Floor ≠ inclusion; `excluded_below` threshold in review validation |

### W3.3 — Asymmetric deltas gameable

| | |
|--|--|
| **Scenario** | +0.5 good / -1.0 missed. Operatör 3 sahte `approved_success` yazar, 1 gerçek missed'i gizler. |
| **Probability** | Medium |
| **Impact** | High |
| **Detection** | Trust delta without linked evidence → quarantine flag |
| **Mitigation** | Outcome-evidence binding (W2.1) |

---

## 4. Reviewer Collusion

### W4.1 — Same agent, multiple hats

| | |
|--|--|
| **Scenario** | Tek Cursor oturumu `--reviewers architect,qa,auditor` geçer. "Üç bağımsız review" simülasyonu, gerçekte tek model. |
| **Probability** | **High** (current usage pattern) |
| **Impact** | Critical — review chain theatre |
| **Detection** | Reviewer identity ≠ CLI string; requires separate attestation per capability |
| **Mitigation** | Class C/D: min 2 distinct session IDs or human founder sign-off (process, not new agent) |

### W4.2 — Trust-weighted approval without veto power

| | |
|--|--|
| **Scenario** | `effective_trust_weight` hesaplanır ama düşük trust reviewer'ı zinciri durdurmaz; sadece isim listesi kontrol edilir. |
| **Probability** | Certain |
| **Impact** | Medium |
| **Detection** | Unit test: trust&lt;60 reviewer should fail weighted threshold |
| **Mitigation** | `satisfied` += min trust among provided ≥ threshold |

### W4.3 — Auditor never in loop until after failure

| | |
|--|--|
| **Scenario** | Auditor trust 90, reviews 0. Sistem auditor'ı eklemiş ama auditor hiç çalışmamış. |
| **Probability** | **Current state** |
| **Impact** | Medium — fake depth |
| **Detection** | `reviews == 0` capability cannot satisfy required_capabilities |
| **Mitigation** | Unreviewed capability = missing |

---

## 5. Feedback Loop Failures

### W5.1 — Learning layer disconnected

| | |
|--|--|
| **Scenario** | `06-learning/postmortems/` boş. Propagate policy override yazıyor ama postmortem/ADR yok. Lesson step atlanıyor. |
| **Probability** | **Current state** |
| **Impact** | High |
| **Detection** | propagate without postmortem ref within 48h → warning |
| **Mitigation** | `propagate --require-postmortem-ref` for production ventures |

### W5.2 — Factory intelligence parallel universe

| | |
|--|--|
| **Scenario** | `scripts/factory/intelligence-engine.py` ULAS metrics tüketmiyor. İki öğrenme hattı birbirini bilmiyor. |
| **Probability** | High |
| **Impact** | Medium — split brain |
| **Detection** | grep cross-import; none = fail |
| **Mitigation** | Single runtime bus (`10-runtime/`) — defer merge, document as known W5.2 |

### W5.3 — No prevented_failure ever recorded

| | |
|--|--|
| **Scenario** | `prevented_failures: 0`. Adaptasyonun işe yaradığını kanıtlayan metrik yok. |
| **Probability** | **Current state** |
| **Impact** | High — closure unproven |
| **Detection** | Monitor prevented_failures / repeat_failures ratio |
| **Mitigation** | first venture lifecycle test case (human-driven, not new engine) |

---

## 6. Prediction Failures

### W6.1 — Heuristic complexity

| | |
|--|--|
| **Scenario** | "Complex auth migration" keyword'leri risk 59 yapar; trivial ama riskli değişiklik düşük skor alır. |
| **Probability** | High when gate opens |
| **Impact** | High — false negative |
| **Detection** | Backtest risk score vs outcomes; AUC &lt; 0.6 = disable enforce |
| **Mitigation** | Gate stays closed until backtest passes (extend existing gate, no new engine) |

### W6.2 — Evidence factor ignored when evidence absent for all ventures

| | |
|--|--|
| **Scenario** | Tüm venture'larda `evidence_status: none`. Risk her zaman yüksek evidence bileşeni taşır — ama gate kapalı, etkisiz. Gate açılınca her şey "yüksek risk" → alarm yorgunluğu. |
| **Probability** | Medium on gate open |
| **Impact** | Medium |
| **Detection** | Distribution of risk scores; if &gt;80% medium+ → miscalibration |
| **Mitigation** | Normalize evidence factor per venture maturity |

### W6.3 — Prediction never validated

| | |
|--|--|
| **Scenario** | Phase 6 shipped in observe mode. Hiçbir zaman "yüksek riskli karar gerçekten kötü mü bitti?" sorusu cevaplanmadı. |
| **Probability** | **Current state** |
| **Impact** | Medium |
| **Detection** | Require 10 gated predictions with outcomes before "operational" label |
| **Mitigation** | Do not enable gate until venture evidence exists (already designed) |

---

## 7. Policy Override Abuse

### W7.1 — Permanent escalation stacking

| | |
|--|--|
| **Scenario** | Her `approved_failed` → +auditor, +tier_floor, +0.05 evidence weight. Üç sentetik hata sonrası class B pratik olarak class C+. |
| **Probability** | **Observed** (policy-overrides.json) |
| **Impact** | High — paralysis by override |
| **Detection** | `changelog.length` vs `outcomes_evaluated`; override age &gt; 90d without review |
| **Mitigation** | Override decay/TTL; max one escalation per class per quarter |

### W7.2 — Gitignored adaptations

| | |
|--|--|
| **Scenario** | `adaptations/*.json` gitignore'da. Ekip üyeleri farklı override state. "Organizasyon" fork'lanır. |
| **Probability** | Medium |
| **Impact** | High |
| **Detection** | `policy-overrides.json` hash mismatch across machines |
| **Mitigation** | Commit overrides for ventures in ship mode; or single remote runtime store |

### W7.3 — No rollback path

| | |
|--|--|
| **Scenario** | Yanlış propagate sonrası canonical policy değişmediği için "undo" sadece manual JSON edit. |
| **Probability** | **Observed need** |
| **Impact** | Medium |
| **Detection** | Missing `ulas overrides-rollback --decision-id` |
| **Mitigation** | Document manual rollback procedure; optional CLI undo (minimal, not new engine) |

---

## 8. Runtime Adaptation Drift

### W8.1 — Adaptation without outcome quality

| | |
|--|--|
| **Scenario** | Test verisi organizasyon davranışını kalıcı değiştirdi. Production'a geçildiğinde kurallar test senaryosuna göre ayarlı. |
| **Probability** | **Current state** |
| **Impact** | Critical |
| **Detection** | Tag decisions `environment: dev|prod`; prod propagate only in prod |
| **Mitigation** | Reset dev overrides; separate runtime namespaces |

### W8.2 — Confidence weight creep

| | |
|--|--|
| **Scenario** | `evidence_present` delta 0.05+0.05=0.10 stacked. Evidence hâlâ yok, ama ağırlık kaydı değişti. |
| **Probability** | **Observed** (0.10 in overrides) |
| **Impact** | Low-Medium until evidence exists |
| **Detection** | Sum of deltas &gt; cap → freeze |
| **Mitigation** | Max cumulative delta per factor |

---

## 9. Memory Corruption

### W9.1 — Substring NEVER_AGAIN matching

| | |
|--|--|
| **Scenario** | `scan_never_again`: summary substring in proposal. "ship" tag blocks "ownership" proposal false positive. Veya typo bypass. |
| **Probability** | Medium |
| **Impact** | Medium |
| **Detection** | Fuzz test scan_never_again |
| **Mitigation** | Token-boundary match; severity levels already exist — use block only for `never_again` level |

### W9.2 — Unvalidated memory append

| | |
|--|--|
| **Scenario** | `--apply-memory` writes arbitrary JSON to never-again.json. Garbage in → permanent blocks. |
| **Probability** | Low-Medium |
| **Impact** | High |
| **Detection** | Schema validate against `never-again-entry.template.json` |
| **Mitigation** | Required fields + founder ack for `never_again` level |

### W9.3 — Empty memory = no learning

| | |
|--|--|
| **Scenario** | `entries: []`. Memory layer theatre — scan always passes. |
| **Probability** | **Current state** |
| **Impact** | High (long-term) |
| **Detection** | `never_again_hits == 0` after first postmortem = failure |
| **Mitigation** | venture postmortem → first entry (human) |

---

## 10. Token Optimization Failure Modes

### W10.1 — Budget hints not enforced

| | |
|--|--|
| **Scenario** | `token_budget_hint: 8000` recorded; hiçbir şey gerçek context boyutunu ölçmez veya bloklamaz. |
| **Probability** | Certain |
| **Impact** | Medium — cost drift, context bloat |
| **Detection** | Compare manifest token estimate vs budget |
| **Mitigation** | `assemble` returns WARN if reads exceed hint (no new engine — extend assemble) |

### W10.2 — Tier escalation without compression

| | |
|--|--|
| **Scenario** | propagate `tier_floor: 3` → daha fazla dosya okunması önerilir; compression framework uygulanmıyor. |
| **Probability** | Medium |
| **Impact** | Medium |
| **Detection** | tier3 usage ↑ + average_context_budget ↑ |
| **Mitigation** | Tier floor requires compressed ADR/postmortem refs |

### W10.3 — Metrics optimize for looking efficient

| | |
|--|--|
| **Scenario** | `average_context_budget` hesaplanır ama karar kalitesine etkisi ölçülmez. Düşük budget + yüksek false_block = kötü tradeoff, görünmez. |
| **Probability** | Medium |
| **Impact** | Medium |
| **Detection** | Correlate token tier with false_block rate |
| **Mitigation** | Joint metric in existing `report` (no new scoring system) |

---

## Strategic failure (en büyük risk)

### W0 — OS geliştirme vs ürün geliştirme

| | |
|--|--|
| **Scenario** | 15 iterasyon: Factory → ULAS Phase 6. no venture shipped yet. Organizasyon simülasyonu mükemmelleşir, **sıfır venture kanıtı**. |
| **Probability** | **High** (observed pattern) |
| **Impact** | **Existential** — tüm metrikler sentetik |
| **Detection** | `shipped_ventures == 0` after N phases |
| **Mitigation** | **Feature freeze on OS** until first venture ship + 1 evidence bundle. Stress test bu maddeyi P0 sayar. |

---

## Attack playbook (red team)

Dışarıdan sistemi kırmak için minimum adımlar:

```bash
# 1. Sahte başarı
ulas outcome --decision-id ANY --result approved_success

# 2. Sahte güven
ulas calibrate --reviewer architect --outcome good --decision-id fake

# 3. Kalıcı kilitleme
ulas outcome --decision-id BLOCKED_ONE --result approved_failed --propagate

# 4. Self-congratulation
ulas feedback-audit   # readiness score ↑
```

**Sonuç:** Sistem teknik olarak çalışıyor; **güven modeli çalışmıyor** — çünkü dış doğrulama yok.

---

## Öncelikli düzeltmeler (yeni motor yok)

| P0 | Fix | Effort |
|----|-----|--------|
| 1 | `outcome` validate: `approved_*` only if `status==APPROVED` | Small |
| 2 | `calibrate`/`propagate` reject unknown decision_id | Small |
| 3 | Reset sentetik `policy-overrides.json` before prod | Trivial |
| 4 | **first venture ship** — dış doğrulayıcı | Large |
| 5 | Precision/risk raporları N&lt;10 → "insufficient data" | Small |

**Yapılmayacak:** Phase 7, yeni agent, yeni scoring sistemi, yeni governance.

---

## Sonuç

APP-FABRIKA çoğu AI coding framework'ünden **organizasyonel olarak ileride** — zincir var:

```
Decision → Review → Audit → Outcome → Learning → Adaptation → Prediction
```

Ama bu zincir şu an **kendi kendine applause** üretiyor. Gerçek stres testi:

> **first venture ship + evidence + bağımsız outcome**

olmadan geçilemez.

**Yanılıyor olabilir miyiz?** Evet — ve şu an en olası yanlışlık, sistemin güçlü olduğuna dair **kendi ürettiği kanıta inanmak**.

Bundan sonraki en değerli iş: güçlendirmek değil, **zorlamak**. Bu belge o zorlamanın ilk çıktısı.

---

*Adversarial audit. No new agents. No new engines. Weaknesses are the deliverable.*
