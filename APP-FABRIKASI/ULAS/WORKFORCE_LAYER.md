# ULAS Workforce Layer — Design (P4, blocked)

**Status:** BLOCKED until **Work Engine** (P2) is proven on real tasks.  
**Not:** new departments, councils, or governance inflation.

> **Jobs before workers.** Workforce recipes sit on top of Work Packages — not the other way around.

See: [`work/WORK_ENGINE.md`](work/WORK_ENGINE.md)

---

## Strategic shift

APP-FABRIKA today ≈ **Company Constitution** (strong).  
Target ≈ Constitution + **AI Workforce** + **Execution** + **Model Abstraction**.

```
ULAS (target axes)
├── GOVERNANCE   ← policies, gates, audit (exists)
├── KNOWLEDGE    ← compression, ADR, patterns (exists)
├── DECISION     ← decide, risk, trust (exists)
└── EXECUTION    ← MISSING — run workforce, verify, feed evidence
```

CL4R1T4S value is not more prompts — it is the loop:

```
Context → Reasoning → Execution → Verification → Memory
```

We are strong on Verification + Memory + Governance.  
Weak on **Execution** and **Reasoning orchestration**.

---

## Workforce model (capabilities × platform)

Not departments. **Workforce = capability recipes per platform.**

```
CEO (orchestrator — existing)
 │
 ├─ Android Workforce   → architect, qa, security, ux, performance
 ├─ Web Workforce       → architect, ux, accessibility, qa, performance
 ├─ iOS Workforce       → architect, ux, qa, performance
 └─ AI Workforce        → planner, researcher, critic, auditor, verifier
```

Maps to existing `03-agents/` capabilities — **no new `.mdc` files required for P2**.

Each workforce entry is a **recipe**:

| Field | Meaning |
|-------|---------|
| `platform` | android \| web \| ios \| ai |
| `capabilities` | ordered list |
| `context_tier` | from decision class |
| `verify_chain` | read → act → verify |
| `model_slot` | abstract — filled by P3 |

---

## Execution OS (P2 scope)

Execution is **not** another ULAS score. It is:

```
decide APPROVED
    → execution manifest (what to run, where, which workforce)
    → model adapter dispatches (P3)
    → artifact output (code, test log, diff)
    → verification hook (existing auditor + evidence)
    → outcome record (evidence-bound)
```

Lives under: `APP-FABRIKASI/10-runtime/execution/` (future, after P0).

---

## Model Abstraction Layer (P3)

Single interface; pluggable backends:

| Slot | Examples |
|------|----------|
| planner | Claude, Cursor, Gemini |
| coder | Cursor, Devin, Cline |
| verifier | same pool, different recipe |

**Not started.** No adapter code until Workforce + Execution prove on target codebase.

---

## Prerequisites (hard gates)

| Gate | Requirement |
|------|-------------|
| P0 | `bridge-venture.sh` — venture ↔ target venture ↔ evidence |
| P1 | outcome/calibrate validation, overrides-reset |
| P2 | Workforce recipes + execution manifest |
| P3 | model adapter interface |

---

## Maturity scores (Mimar baseline)

| Area | Score | Note |
|------|-------|------|
| Governance | 95 | strong |
| Knowledge | 92 | strong |
| Decision OS | 85 | strong |
| Workforce OS | 25 | design only |
| Execution OS | 30 | no dispatch loop |
| Real Validation | 20 → **P0 fixes** | bridge script |
| Model Abstraction | 10 | intentional defer |

**~74/100** — constitution without workforce.

---

## Anti-patterns

- Phase 7 scoring system — **forbidden**
- Risk Agent / Forecast Agent — **forbidden**
- New governance council for Workforce — **forbidden**
- Workforce before venture bridge — **forbidden**

---

*Next action: run `./APP-FABRIKASI/scripts/bridge-venture.sh` — not expand ULAS.*
