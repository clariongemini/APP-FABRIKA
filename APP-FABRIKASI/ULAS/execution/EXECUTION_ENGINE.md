# Execution Engine

**Status:** Operational (minimal) — built on ULAS + Work Engine only.

No new agents · phases · councils · scoring · trust · governance.

---

## Gap this closes

APP-FABRIKA was strong at:

```
Decide → Audit → Score → Measure → Predict → Adapt
```

Missing:

```
Decide → Do → Measure quality → Improve
```

CL4R1T4S execution loop:

```
Context → Reasoning → Execution → Verification → Repair → Verification → Complete
```

CEO, Auditor, Trust are **outcomes** of this loop — not the loop itself.

---

## Three axes (final)

| Axis | Role | Location |
|------|------|----------|
| **ULAS** | What should be done | `decide`, policies |
| **Work Engine** | Break into packages | `ulas work generate` |
| **Execution Engine** | Run verify-repair-complete | `ulas execute run` |

```
Decision (APPROVED)
    → Work Packages
    → Capability Router (matching)
    → Execution Manifest  (commands)
    → Verification Manifest (checks)
    → [fail] Repair → re-verify (max 3)
    → Evidence Manifest (bridge)
    → Outcome
```

---

## Capability-first (non-negotiable)

```
Capability  →  Provider
```

Never:

```
Provider  →  Capability
```

| Capability | Meaning | Default provider (today) |
|------------|---------|--------------------------|
| planner | scope, evidence | `human` |
| architect | design, implement | `human` |
| qa | verify tests | `local_shell` |
| auditor | evidence, gate | `local_shell` |
| security | threat review | `human` |

`Android Architect` is not a person — it is **architect** capability on **android** platform.

See: [`capability-model.md`](capability-model.md) · [`provider-abstraction.md`](provider-abstraction.md)

---

## CLI

```bash
ulas work generate --decision-id ID
ulas execute run --decision-id ID          # run manifest + verify + repair loop
ulas execute verify --decision-id ID       # verification only
ulas execute status --decision-id ID     # execution log
```

Runtime log: `10-runtime/ulas/execution/{decision_id}.json`

---

## What is automated today

| Step | Automated | Notes |
|------|-----------|-------|
| wp-1 investigate | ❌ | human / future AI provider |
| wp-2 implement | ❌ | human / future AI provider |
| wp-3 qa (gradle test) | ✅ | `local_shell` |
| wp-4 evidence | ✅ | `bridge-venture.sh` |
| Repair loop | ✅ | re-run verify up to 3× |
| Outcome record | ⚠️ | manual if tests fail |

Honest boundary: Execution Engine runs **shell verification + evidence bridge**. Code changes remain capability dispatch (P3 providers).

---

## Anti-patterns

- New Trust/Risk score for execution — **forbidden**
- Workforce before execution proves on target codebase — **forbidden**
- Cursor as architectural center — **forbidden** (provider slot only)

---

## First proof (P0)

```
decide "Fix venture unit test failures"
  → work generate
  → [human] fix 10 tests
  → execute run
  → evidence failed: 0
  → outcome approved_success
```

Success = **production conversion**, not new documentation.
