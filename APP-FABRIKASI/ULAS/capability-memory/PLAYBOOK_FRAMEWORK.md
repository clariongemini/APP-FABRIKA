# Playbook Framework

Repeatable **how-to** for a capability — not governance procedure.

---

## Entry shape

```json
{
  "id": "android.architecture.pb-001",
  "title": "Fix module boundary violation",
  "status": "experimental",
  "when_to_use": "module-boundary-test or app module drift detected",
  "steps": [
    "List files flagged by boundary / architecture test",
    "Move implementation to appropriate feature or core module",
    "Update Gradle dependencies per adapter guidelines",
    "Run project unit test task from venture.json build block",
    "Record antipattern with matching tags if root cause confirmed"
  ],
  "tags": ["module_boundary", "architecture"],
  "source": { "type": "manual", "ref": "ANTIPATTERN_FRAMEWORK.md" }
}
```

---

## When to create

| Trigger | Playbook |
|---------|----------|
| Same repair 2+ times | Extract steps from execution repair_plan |
| Proven antipattern | Pair 1:1 with fix playbook |
| Platform adapter doc | Link as `source.ref` — don't duplicate factory docs |

---

## Promotion

`experimental` → `proven` when playbook steps led to `verification_passed` on a venture.

---

## Dispatch injection

If work package task matches `when_to_use` or shared `tags` → attach `playbook_ref` in capability context.

---

## vs Knowledge

Playbooks are **procedural** (ordered steps). Knowledge patterns are **declarative** (rules/facts).
