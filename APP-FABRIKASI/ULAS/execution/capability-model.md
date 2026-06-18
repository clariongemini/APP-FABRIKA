# Capability Model

Capabilities are **roles**, not people, not providers, not departments.

---

## Canonical capabilities

From `03-agents/` — unchanged set:

| Capability | Responsibility |
|------------|----------------|
| planner | Charter, scope, evidence plan |
| architect | Structure, implementation |
| security | Threat model, secrets |
| qa | Test verification |
| performance | Budget, profiling |
| ux | Flow, a11y |
| auditor | Gate, evidence closure |

---

## Platform dimension

Work packages add platform metadata only:

```json
{
  "capability": "architect",
  "platform": "android",
  "task": "fix worker-api-boundary-test"
}
```

Future platforms use same capability names:

| Platform | architect | qa |
|----------|-----------|-----|
| android | module boundaries | gradle unit tests |
| web | component architecture | vitest |
| ios | swift modules | xctest |

---

## Workforce (P4) maps here

When Workforce Layer arrives, it is **only** a recipe:

```
android_mvp_build = [planner, architect, qa, auditor]
```

No new capability names. No new governance.

---

## Execution binding

Capabilities route to providers via **Capability Router** — not hardcoded in engine code.

```bash
ulas capability route --decision-id ID
ulas capability show --decision-id ID
```

→ [`../routing/CAPABILITY_ROUTER.md`](../routing/CAPABILITY_ROUTER.md)
