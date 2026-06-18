# ULAS Phase 5 — Adaptive Decision System

**Date:** 2026-06-17  
**Mode:** Adaptation — no expansion  
**Shift:** Decision OS → **Adaptive Decision OS**

---

## The distinction

| | Decision OS (Phase 2–4) | Adaptive Decision OS (Phase 5) |
|---|------------------------|--------------------------------|
| Core action | Decides | Decides **and changes future behavior** |
| Outcome | Measured | **Propagated** |
| Trust | Manual calibrate | Auto via `propagate` |
| Policy | Manual ADR | Runtime overrides + ADR for canonical |
| Success metric | Documentation | **Behavior change** |

> "Bir yıl sonra APP-FABRIKA bugün verdiği hatalı kararları hâlâ veriyor olacak mı?"

Phase 5 exists to make the answer **no** — without new agents or governance.

---

## What was missing: Feedback Propagation

Not roles. Not departments. **Propagation.**

```
Failure → Postmortem → Lesson          ✅ (manual)
Lesson → Policy → Review → Trust → Future Decision   ❌ (was broken)
```

Phase 5 closes the second chain via **`ulas propagate`**.

---

## Adaptive loop

```
Decision → Outcome → propagate → Adaptation → Improved Future Decision
```

### On `approved_failed` (architect approved, output failed)

`propagate` answers all 9 questions:

| # | Question | Answer source |
|---|----------|---------------|
| 1 | Failure detected? | outcome tag |
| 2 | Which reviewer approved? | `review.provided_reviewers` |
| 3 | Why approved? | decision JSON + review chain |
| 4 | Similar decisions? | `find_similar_decisions()` |
| 5 | Policy gap? | policy_adaptations plan |
| 6 | Review matrix gap? | +auditor for class B/C |
| 7 | Trust affected? | auto `missed` calibration |
| 8 | NEVER_AGAIN? | candidate (`--apply-memory` to commit) |
| 9 | Context assembly? | tier_floor in runtime overrides |

---

## CLI

```bash
# Record failure and propagate in one step
./APP-FABRIKASI/scripts/ulas.sh outcome \
  --decision-id ID --result approved_failed --propagate

# Plan without applying
./APP-FABRIKASI/scripts/ulas.sh propagate --decision-id ID --dry-run

# Apply trust + policy overrides + NEVER_AGAIN
./APP-FABRIKASI/scripts/ulas.sh propagate --decision-id ID --apply-memory

# Where does feedback still stop?
./APP-FABRIKASI/scripts/ulas.sh propagation-audit
```

---

## Runtime adaptations (not canonical policy)

Canonical policies stay in `ULAS/policies/` — **unchanged**.

Learned behavior lives in:

`10-runtime/ulas/adaptations/policy-overrides.json`

| Override | Affects `decide()` via |
|----------|----------------------|
| `review_matrix.B.additional_required` | `validate_review_chain()` |
| `decision_classes.B.tier_floor` | `resolve_class()` → context tier |
| `decision_classes.B.min_reviews_delta` | min review count |
| `confidence_weight_deltas` | `score_confidence()` |

**Future decisions are stricter** after a failure — measurably, without editing governance.

---

## What remains manual (by design)

| Step | Why |
|------|-----|
| Postmortem write | Human narrative |
| Canonical policy ADR | Prevent meta-factory drift |
| `promote-pattern.py` | Venture evidence required |
| Portfolio allocation | N≥2 ventures |

---

## Model independence

ULAS is **not** Cursor, Claude, or Gemini.

It is:

- Policies (JSON)
- Runtime overrides (JSON)
- Trust calibration (JSON)
- NEVER_AGAIN (JSON)
- CLI engine (`ulas.py`)

Any model that can read/write JSON and run CLI can operate APP-FABRIKA.

---

## Success criteria

1. `approved_failed` → `propagate` → next class-B decision requires **auditor**
2. Trust drops for reviewers who approved the failure
3. `propagation-audit` shows `influences future decide(): yes`
4. One year test: same failure pattern blocked by NEVER_AGAIN or stricter chain

→ Framework: [`scoring/ADAPTIVE_DECISION_FRAMEWORK.md`](scoring/ADAPTIVE_DECISION_FRAMEWORK.md)
