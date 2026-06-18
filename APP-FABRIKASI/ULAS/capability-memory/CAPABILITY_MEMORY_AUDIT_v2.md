# Capability Memory Audit v2

> **Taşınabilir şablon.** Validation verisi repoda tutulmaz — ingest sonrası hedef projede dolar.

**Consolidation Sprint** — four-layer corporate memory  
**No:** phase · agent · council · governance · trust score

---

## v1 → v2 gap

| v1 | v2 |
|----|-----|
| Flat `entries[]` | **Knowledge** · **AntiPatterns** · **Playbooks** · **Benchmarks** |
| Failure mixed with pattern | AntiPatterns isolated with `severity` + `evidence_count` |
| No operational recipes | Playbooks with `steps[]` |
| No cross-venture baselines | Benchmarks per `project_type` |
| Stats only | **Health** — memory quality (counts, not score) |

---

## Layer audit (per capability)

| Layer | Purpose | Promotion |
|-------|---------|-----------|
| **Knowledge** | patterns · constraints · success_recipe | experimental → proven |
| **AntiPatterns** | what never to repeat | evidence_count ≥ 2 → proven |
| **Playbooks** | how to execute recurring work | proven after 1 successful venture run |
| **Benchmarks** | measurable baselines | append-only from evidence |

---

## Real-world validation (per deployed project)

| Signal | Capability | Layer | When |
|--------|------------|-------|------|
| Verification fail | `{capability_id}` | antipattern | `memory ingest --from execution` |
| Unit test regression | `android.testing` | antipattern | evidence manifest `failed > 0` |
| Build metrics | platform capability | benchmark | `memory ingest --from evidence` |

Template repo: all layers empty until first `bridge-venture.sh {slug}`.

---

## Compression at 1000+ entries

| Tier | Budget | Selection algorithm |
|------|--------|---------------------|
| 1 | 200 tokens | All proven antipattern titles (severity≥high) + top 5 proven patterns |
| 2 | 800 tokens | + body_compressed; max 15 antipatterns + 15 knowledge + 10 experimental |
| 3 | on demand | Full entries + playbook steps |

At 1000 entries: **never load all** — rank by `severity`, `status=proven`, `evidence_count`.

Dedup by normalized title on compress.

---

## Regression test scenario (synthetic)

1. Seed `android.architecture.001` proven with tag `module-boundary-test`
2. Run `ulas execute verify` → fail on boundary test
3. Expect: `regression_signals[]`, antipattern demoted to experimental, `health.trend=weakening`

CLI: `ulas memory test-regression --capability android.architecture --tag module-boundary-test`

---

## Governance inflation check

| Added | Type |
|-------|------|
| capability-store.schema.json | Memory schema |
| health block | **Computed** — not trust |
| Framework docs | Operational spec |
| `ulas memory health` | Read-only report |

**Not added:** council, phase, trust engine, readiness score.

---

## Maturity after v2

| Dimension | v1 | v2 |
|-----------|----|----|
| Knowledge OS | 55% | **68%** |
| Usable corporate memory | 30% | **55%** |
| Real validation | 35% | 40% (after first evidence ingest in target project) |

Next ROI: **first venture closure → promote entries → close learning loop**.
