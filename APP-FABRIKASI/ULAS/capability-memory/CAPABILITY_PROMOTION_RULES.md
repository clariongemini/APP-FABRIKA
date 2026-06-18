# Capability Promotion Rules

Promotes knowledge **experimental → proven**. Not a trust score — evidence gate only.

---

## States

```
experimental → proven → deprecated → superseded
```

| State | Meaning |
|-------|---------|
| experimental | Single source or unverified |
| proven | Meets promotion criteria below |
| deprecated | Superseded by better entry or platform change |
| superseded | Replaced by `superseded_by` entry id |

---

## Promotion criteria (ALL required)

### For `pattern` / `success_recipe`

1. At least **2 ventures** OR **1 venture + execution verification pass** after apply
2. `evidence_refs` non-empty (manifest, test log, or ADR)
3. No open `regression_signal` for same title/tags
4. Human or auditor ack via `ulas memory promote` (explicit CLI — not auto)

### For `anti_pattern` / `failure_mode`

1. Observed failure at least **2 times** OR **1 time + NEVER_AGAIN candidate**
2. Linked verification check id or test class name in `tags`
3. `regression_watch: true` on promote

### For `constraint` / `checklist`

1. Source type `adr` with Accepted status OR platform standard reference
2. One venture application sufficient if from factory standard

---

## Confidence field (not score)

| Value | Meaning |
|-------|---------|
| single_venture | One data point |
| multi_venture | 2+ ventures |
| cross_platform | Same lesson on 2+ platforms |

Used for **query ranking**, not automated blocking.

---

## Demotion

| Trigger | Action |
|---------|--------|
| Regression detected | `proven` → `experimental` + regression_signal |
| Platform adapter major version | review → `deprecated` |
| Contradicting ADR accepted | old entry → `superseded` |

---

## CLI

```bash
ulas memory promote --capability android.architecture --entry cap-k-001 [--force]
```

`--force` skips venture count only with `--reason` (logged in entry metadata).

---

## Relationship to 06-learning

| 06-learning | Capability memory |
|-------------|-------------------|
| `patterns/proven/` | Mirror **summary** — canonical store is capability JSON |
| Pattern promotion script | Future: calls `ulas memory promote` |

One direction: venture pattern → capability entry. Not duplicate maintenance.
