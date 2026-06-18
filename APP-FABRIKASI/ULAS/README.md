# ULAS — Work Engine (P2)

> **Decision → Work Package → Execution → Verification → Evidence**

| Meta | Değer |
|------|-------|
| **Execution** | `ulas work` — P2 |
| **Workforce** | P4 — blocked until work proven |

```bash
./APP-FABRIKASI/scripts/ulas.sh decide ...
./APP-FABRIKASI/scripts/ulas.sh work generate --decision-id ID
./APP-FABRIKASI/scripts/ulas.sh work show --decision-id ID
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh my-app
```

→ [`work/WORK_ENGINE.md`](work/WORK_ENGINE.md) · [`FOUR_AXES.md`](FOUR_AXES.md)

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

→ [`PHASE2.md`](PHASE2.md) · [`CONSOLIDATION.md`](CONSOLIDATION.md) · [`scoring/EFFECTIVENESS.md`](scoring/EFFECTIVENESS.md)

---

## Başarı

ULAS başarılı when **repeated mistakes ↓ unnecessary context ↓ unnecessary reviews ↓ low-confidence approvals ↓**

Not: more documents.
