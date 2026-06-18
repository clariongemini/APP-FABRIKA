# Capability Router

**Status:** P3 — operational (registry + policy + CLI)  
**Not:** Workforce · Agency · Council · new governance

---

## Position in chain

```
ULAS (Decision)
    ↓
Work Engine (Planning)
    ↓
Capability Router (Matching)     ← this layer
    ↓
Execution Engine (Doing)
    ↓
Verification (Checking)
    ↓
Evidence (Proving)
```

The system asks **which capability is needed**, not **who is working**.

---

## Model-independence test

> Android Architecture runs on Cursor today. Claude tomorrow. What changes?

**Answer: one line in `routing-policy.json`.**

```json
"android.architecture": "claude"
```

Unchanged:

- Decision record
- Work packages + tasks + acceptance
- Execution manifest commands
- Verification manifest checks
- Evidence manifest paths

---

## Components

| File | Role |
|------|------|
| [`capability-registry.json`](capability-registry.json) | Stable IDs (`android.architecture`) |
| [`provider-registry.json`](provider-registry.json) | Backends (cursor, claude, local_shell) |
| [`routing-policy.json`](routing-policy.json) | **Capability → provider** (swap here) |
| [`routing-manifest.schema.json`](routing-manifest.schema.json) | Router output shape |

Runtime override (optional): `10-runtime/ulas/routing/policy-overrides.json`

---

## CLI

```bash
ulas work generate --decision-id ID
ulas capability route --decision-id ID    # produce routing_manifest on work chain
ulas capability show --decision-id ID     # human-readable bindings
ulas execute run --decision-id ID         # auto-routes if manifest missing
```

Example output for "Fix failing Android test":

```
Capabilities Needed
  ✓ Android Architecture   → cursor (delegated, not wired)
  ✓ Android Testing        → local_shell (automated)
  ✓ Android QA             → local_shell (automated)
```

---

## Binding rules

1. Work package `role` + `platform` → `capability_id` via registry
2. `capability_id` → `provider_id` via policy (then runtime override)
3. Execution Engine reads **routing_manifest**, never hardcoded role→provider
4. Unwired AI providers skip dispatch with explicit log — no silent fake execution

---

## Anti-patterns

| Wrong | Right |
|-------|-------|
| `architect = human` in Python | `android.architecture → cursor` in policy |
| Cursor as system center | Capability as center, Cursor as plugin |
| New agent per platform | Same capability IDs, platform dimension |

---

## Proof

```bash
# Swap provider — zero code change
jq '.defaults["android.architecture"] = "claude"' ULAS/routing/routing-policy.json
ulas capability route --decision-id ID
ulas capability show --decision-id ID
# bindings show claude; work chain tasks unchanged
```
