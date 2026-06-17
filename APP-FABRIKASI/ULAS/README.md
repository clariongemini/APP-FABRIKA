# ULAS — Decision Execution OS

> **Phase 2:** Prensip deposu değil — **çalışan karar motoru**.

| Meta | Değer |
|------|-------|
| **Phase** | 2 — Operational |
| **Engine** | `bin/ulas.py` |
| **CLI** | `APP-FABRIKASI/scripts/ulas.sh` |

---

## Komutlar

```bash
./APP-FABRIKASI/scripts/ulas.sh route --class C
./APP-FABRIKASI/scripts/ulas.sh assemble --venture ulas-player --class B
./APP-FABRIKASI/scripts/ulas.sh decide --venture ulas-player --class B \
  --title "..." --reviewers architect,qa
./APP-FABRIKASI/scripts/ulas.sh calibrate --reviewer architect --outcome good
```

---

## Yapı (Phase 2 canonical)

```
ULAS/
├── policies/           context-escalation · decision-classes · review-matrix
├── workflows/          decision-lifecycle.json (state machine)
├── gates/              gate docs (logic in bin/ulas.py)
├── scoring/            confidence-weights · trust-scores.json
├── memory/             never-again.json + severity levels
├── bin/ulas.py         orchestrator
└── 01-10/              Phase 1 reference docs (frozen)
```

---

## Otomatik akış (`decide`)

```
Görev → Context Assembly → READ_MORE? → Sınıflandır (A/B/C/D)
     → Confidence → Review Chain → APPROVED | BLOCKED → Audit JSON
```

Kayıt: `10-runtime/ulas/decisions/{id}.json`

---

## Sistemler

| Sistem | Policy dosyası |
|--------|----------------|
| Context Escalation | `policies/context-escalation.json` |
| Decision Classes | `policies/decision-classes.json` |
| Review Matrix | `policies/review-matrix.json` |
| Trust Score | `scoring/trust-scores.json` |
| Memory Severity | `memory/never-again.json` |

→ [`PHASE2.md`](PHASE2.md) · [`SOURCE_PRINCIPLES.md`](SOURCE_PRINCIPLES.md)

---

## Başarı

ULAS başarılı when **repeated mistakes ↓ unnecessary context ↓ unnecessary reviews ↓ low-confidence approvals ↓**

Not: more documents.
