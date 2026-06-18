# Memory Ingestion Matrix

How venture artifacts write to capability memory layers.

---

## Matrix

| Source | CLI / Trigger | Knowledge | AntiPatterns | Playbooks | Benchmarks |
|--------|---------------|-----------|--------------|-----------|------------|
| **Outcome** | `ingest --from outcome` | success_recipe if approved_success | — | — | — |
| **Postmortem** | `ingest --from postmortem` | patterns, constraints | failure lessons | repair steps | — |
| **ADR** | `ingest --from adr` | constraints | — | — | — |
| **Execution** | `ingest --from execution` | — | failure_mode → antipattern | repair_plan → playbook | — |
| **Evidence** | `ingest --from evidence` | — | test-class tags | — | metrics row |
| **Verification fail** | auto on `execute run` | — | tag match + regression | — | — |
| **Manual** | `ingest --from manual --layer X` | any | any | any | any |

---

## Routing rules

| Content signal | Target layer |
|----------------|--------------|
| `kind` failure_mode, anti_pattern, "don't", test fail | **antipatterns** |
| `kind` pattern, constraint, checklist, ADR accepted | **knowledge** |
| Ordered steps, repair_plan.plans | **playbooks** |
| Numeric metrics, manifest sources | **benchmarks** |

---

## Provenance (required)

Every entry needs `source.type` + `source.ref`. No anonymous memory.

---

## Dedup

Before ingest: match `title` + primary `tag`. Increment `evidence_count` on antipattern instead of duplicate row.

---

## Example: first venture P0 close

```
1. ingest --from evidence --venture SLUG
   → benchmark bm-001 (failed: 10)
2. [human] fix tests
3. execute run → pass
4. ingest --from evidence  → benchmark bm-002 (failed: 0)
5. promote antipattern entries after review
6. ingest --from outcome --decision-id ID
   → knowledge success_recipe
```
