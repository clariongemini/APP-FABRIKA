# Benchmark Framework

Measurable baselines per **`project_type`** (venture `template` alanı, örn. `android-app`, `saas`) — evidence from real builds.

---

## Entry shape

```json
{
  "id": "android.architecture.bm-001",
  "project_type": "android-app",
  "venture_slug": "{slug}",
  "metrics": {
    "unit_test_total": 0,
    "unit_test_failed": 0,
    "build_status": 1
  },
  "recorded_at": "2026-01-01T00:00:00Z",
  "source": {
    "type": "evidence",
    "ref": "07-evidence/{slug}/manifest.json"
  }
}
```

Future metrics (when measured):

```json
{
  "startup_ms": 900,
  "memory_mb": 180,
  "cold_start_p95_ms": 1200
}
```

---

## Rules

1. **Append-only** — new evidence creates new benchmark row or updates `recorded_at` on same venture
2. Compare ventures of same `project_type` only
3. No synthetic numbers — manifest or profiler evidence required
4. `android.performance` owns runtime metrics; architecture owns structural metrics (test counts, module count)

---

## Use in execution

Verification manifest `expect` can reference benchmark:

```json
{ "type": "benchmark", "metric": "unit_test_failed", "expect": 0 }
```

(Future — not wired in execution engine v1.)

---

## First benchmark (after bridge)

| Metric | Source |
|--------|--------|
| `unit_test_failed` | evidence manifest `sources[unit_test].failed` |
| `build_status` | evidence manifest `sources[build].status` |

Target after P0 closure: `unit_test_failed: 0`.
