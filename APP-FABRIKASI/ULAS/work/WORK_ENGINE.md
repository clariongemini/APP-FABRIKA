# ULAS Work Engine

**Status:** P2 — operational (minimal)  
**Not:** Workforce, new agents, scoring systems, or model adapters.

---

## Problem

APP-FABRIKA is strong at **Decision** but weak at **İcra (Execution)**.

```
Today (too much):     Decision → Decision → Decision → Decision
Target:               Decision → Work → Execute → Verify → Evidence → Outcome
```

CL4R1T4S core loop (all tools share this):

```
Task → Subtask → Verification → Retry → Finish
```

Work Engine materializes that loop **after** ULAS `decide`.

---

## Chain

```
Decision (JSON)
    ↓
Work Package Generator
    ↓
Execution Manifest     ← what to run, where (codebase)
    ↓
Verification Manifest  ← how to prove done
    ↓
Evidence Manifest      ← where proof is stored
    ↓
Outcome                ← existing ulas outcome (evidence-bound)
```

---

## CLI

```bash
# After decide:
ulas work generate --decision-id ID
ulas work show --decision-id ID
ulas work list

# Execution (P2+):
ulas capability route --decision-id ID
ulas execute run --decision-id ID
ulas execute verify --decision-id ID
ulas execute status --decision-id ID
```

→ Capability Router: [`../routing/CAPABILITY_ROUTER.md`](../routing/CAPABILITY_ROUTER.md)  
→ Execution loop: [`../execution/EXECUTION_ENGINE.md`](../execution/EXECUTION_ENGINE.md)

---

## Work package shape

Capability slots only — **not** Workforce names. Platform is metadata.

```json
{
  "id": "wp-2",
  "sequence": 2,
  "capability": "architect",
  "platform": "android",
  "task": "implement fix for worker-api-boundary-test",
  "status": "pending",
  "acceptance": "test passes"
}
```

Workforce Layer (P4) maps onto these slots later. **Jobs before workers.**

---

## Model abstraction (P3 — not implemented)

Center is **capability**, not model:

```json
{
  "capability": "architecture_review",
  "preferred_backends": ["claude", "cursor", "gemini"]
}
```

Work Engine does not dispatch models — **Execution Engine** runs `local_shell` verification + bridge. AI dispatch is P3.

| Priority | Item |
|----------|------|
| P0 | venture unit test failures ↓ |
| P1 | `bridge-venture.sh` evidence chain |
| P2 | Work Engine + **Execution Engine** ← operational |
| P3 | Capability → provider dispatch |
| P4 | Workforce recipes |
| P5 | Multi-model orchestration |

---

## Anti-patterns

- Android Workforce recipe before Work Engine — **forbidden**
- New trust/risk score for work — **forbidden**
- Auto-execute without human/CI — **future** (dispatch is P3+)

→ Schema: [`work-package.schema.json`](work-package.schema.json)
