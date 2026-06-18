# Capability Memory

Operational long-term memory per **capability_id** — not per venture, not per provider.

---

## Problem

```
Lesson (06-learning)     ✅ stored
Capability Knowledge     ❌ was not operational
Future Execution         ❌ starts at zero
```

After 50 projects, `android.architecture` should not repeat `module-boundary-test` drift.

---

## Layout

```
ULAS/capability-memory/
├── index.json
├── capability-knowledge.schema.json
├── knowledge/{capability_id}.json
├── CAPABILITY_MEMORY_AUDIT.md
├── CAPABILITY_LEARNING_FLOW.md
├── CAPABILITY_PROMOTION_RULES.md
├── CAPABILITY_REGRESSION_DETECTION.md
└── CAPABILITY_KNOWLEDGE_COMPRESSION.md
```

Runtime mirror (optional): `10-runtime/capability-memory/`

---

## Four layers

```
Capability
 ├── knowledge/      patterns · constraints · success_recipe
 ├── antipatterns/   never again (severity + evidence_count)
 ├── playbooks/      procedural steps
 └── benchmarks/     project_type metrics
```

Schema: [`capability-store.schema.json`](capability-store.schema.json)

## CLI

```bash
ulas memory migrate
ulas memory health --capability android.architecture
ulas memory quality-report
ulas memory query --capability android.architecture --tier 2
ulas memory ingest --from evidence --venture SLUG
ulas memory test-regression --capability android.architecture --tag module-boundary-test
```

---

## Integration

| Consumer | Uses memory |
|----------|-------------|
| Capability Router | tier1 on route |
| Dispatch plan | tier2 in context_refs |
| Future AI adapter | full query tier 2/3 |

No governance expansion. No trust scores.
