# ULAS Phase 4 — Self-Improvement & Feedback Closure Audit

> **Taşınabilir şablon.** Canlı skorlar hedef projede `./APP-FABRIKASI/scripts/ulas.sh feedback-audit` ile üretilir. Repoda örnek karar/outcome yoktur.

**Mode:** Validation — no expansion  
**Question:** Can APP-FABRIKA learn from its own decisions and modify future behavior?

---

## Executive answer

| Question | Answer |
|----------|--------|
| Can it make decisions? | **Yes** — ULAS Phase 2–3 |
| Can it learn from decisions? | **Partially** — loops exist, closure incomplete |
| Can it modify future behavior automatically? | **No** — policy/trust updates are manual or semi-manual |
| Self-Improvement Readiness | **Şablon** (live: `ulas feedback-audit` in target project) |

**Verdict:** APP-FABRIKA can **detect and explain** mistakes in principle. It cannot yet **prove** self-improvement at scale. First venture in each deployed project is the closure test.

Run live audit: `./APP-FABRIKASI/scripts/ulas.sh feedback-audit`

---

## 1. Feedback Loop Inventory

| Chain | Exists | Measurable | Automated | Actionable | Status |
|-------|--------|------------|-------------|------------|--------|
| Decision → Outcome → Lesson → Policy | Partial | ⚠️ | ❌ | ❌ | **Partially Closed** |
| Decision → Failure → Memory → Prevention | Partial | ⚠️ | ❌ | ⚠️ | **Partially Closed** |
| Review → Accuracy → Trust → Calibration | Yes | ✅ | ⚠️ | ⚠️ | **Partially Closed** |
| Context → Usage → Token Metrics → Optimization | Yes | ✅ | ✅ | ❌ | **Partially Closed** |
| Evidence → Insight → Pattern → Decision | Partial | ⚠️ | ⚠️ | ❌ | **Open** |
| Venture → Outcome → Portfolio → Capital Allocation | Schema only | ❌ | ❌ | ❌ | **Missing** |

### By subsystem

| Subsystem | Key loop | Status |
|-----------|----------|--------|
| **Governance** | Gate → venture phase | Partially Closed (manual) |
| **Knowledge** | ADR → compressed context | Open (no auto-feed) |
| **Learning** | postmortem → pattern | Partially Closed (`promote-pattern.py` manual) |
| **ULAS** | decide → outcome → metrics | Partially Closed |
| **Evidence** | bundle → confidence factor | Open (no venture data) |
| **Portfolio** | outcome → allocation | Missing (N<2) |
| **Runtime** | context manifest → tier | Partially Closed |

**Closed loops:** 0  
**Partially Closed:** 4  
**Open:** 2  
**Missing:** 0

> Scores and loop counts are **recomputed** on each `./scripts/ulas.sh feedback-audit`.

---

## 2. Drift Analysis Framework

→ [`scoring/drift-analysis-framework.md`](scoring/drift-analysis-framework.md)

| Drift type | Detectable today | Trend data | Alert |
|------------|------------------|------------|-------|
| Confidence drift | Point-in-time bands | ❌ | ❌ |
| Reviewer drift | trust-scores.json | ❌ | ❌ |
| Trust drift | calibration_delta | ⚠️ log Phase 4 | ❌ |
| Memory drift | never-again count | ❌ | ❌ |
| Policy drift | git diff on policies/ | Manual | ❌ |

**Requirement:** `readiness-history.json` snapshots on each `feedback-audit` — trend baseline starts now.

**Question answered:** "Are we getting better or worse?" → **Not yet** (need ≥4 weekly snapshots).

---

## 3. Explainable Trust Framework

→ [`scoring/explainable-trust-framework.md`](scoring/explainable-trust-framework.md)

| Criterion | Status |
|-----------|--------|
| Why trust changed | ✅ `calibration_log` per capability (Phase 4) |
| Evidence for change | ⚠️ optional `--decision-id` on calibrate |
| Justified change | Human review of log |
| Black box risk | **Mitigated** if log populated |

---

## 4. Policy Evolution Framework

→ [`scoring/policy-evolution-framework.md`](scoring/policy-evolution-framework.md)

| Criterion | Status |
|-----------|--------|
| Policies can evolve | ✅ JSON in `ULAS/policies/` |
| Triggers defined | ⚠️ framework only |
| Changes recorded | ❌ no `policy-changelog.json` auto |
| Changes audited | Manual git + ADR |

**Gap:** Mistake → policy improvement requires **human ADR** + manual JSON edit. Not auto — by design (no governance inflation).

---

## 5. Memory Effectiveness Framework

→ [`scoring/memory-effectiveness-framework.md`](scoring/memory-effectiveness-framework.md)

| Metric | Measurable | Value |
|--------|------------|-------|
| never_again_hits | ✅ | 0 |
| prevented_failures | ⚠️ manual `outcome prevented_failure` | 0 |
| repeat_failures | ❌ not wired | — |
| Prevention rate | ❌ needs N | — |

---

## 6. ULAS Effectiveness Review

| Metric | Measurable now | Needs evidence |
|--------|----------------|----------------|
| LOW_CONFIDENCE precision | ✅ (N≥1 evaluated) | N≥10 for confidence |
| Approval quality | ⚠️ approved_success/failed | venture ship |
| Block quality | ✅ correct_block/false_block | N≥10 |
| Reviewer accuracy | ⚠️ per-capability | outcome tags |
| Escalation efficiency | ✅ tier distribution | baseline vs always-T3 |

Current: `ulas report` — metrics populate after first venture decisions in target project.

---

## 7. Self-Improvement Readiness Score

→ [`scoring/self-improvement-readiness.json`](scoring/self-improvement-readiness.json)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Learning Capability | 62 | Scripts exist; no venture outcomes |
| Adaptation Capability | 38 | calibrate only; no policy auto-update |
| Explainability | 58 | trust log added; decision JSON rich |
| Auditability | 82 | Full decision audit trail |
| Drift Resistance | 32 | No trend analysis yet |
| Policy Evolution | 42 | Manual path only |
| Memory Effectiveness | 28 | Empty NEVER_AGAIN |
| **Composite** | **—** (run `feedback-audit`) | Run `feedback-audit` in target project |

---

## 8. Critical Gaps (P0)

1. **No venture outcomes** — entire Evidence→Portfolio chain inert  
2. **Zero closed feedback loops** — learning does not automatically change behavior  
3. **No trend history** — cannot answer "better or worse?"  
4. **Policy evolution manual** — mistakes do not auto-produce policy diffs  

---

## 9. Non-Critical Gaps (P1)

1. PDC `compute-decision-accuracy.py` parallel to ULAS — not unified  
2. `intelligence-engine.py` not fed ULAS metrics  
3. `06-learning` not auto-linked from `ulas outcome`  
4. Founder gate (class D) not instrumented  

---

## 10. Recommendations

**Do not expand.** Close loops in target project:

1. Every major decision → `ulas decide`  
2. Post-ship → `ulas outcome` + `record-outcome.py` + `record-postmortem.py`  
3. Weekly → `ulas feedback-audit` (trend snapshot)  
4. Postmortem → manual NEVER_AGAIN entry + ADR if policy change  
5. After 10 decisions → review LOW_CONFIDENCE precision  
6. After 50 → evaluate trust calibration vs outcomes  

**Success:** APP-FABRIKA demonstrates one **fully closed loop**:

```
first venture ship failure → postmortem → NEVER_AGAIN → blocks similar decision → prevented_failure counted
```

---

## Phase 4 restrictions (unchanged)

No new agents · departments · councils · adapters · intelligence engines · governance layers.
