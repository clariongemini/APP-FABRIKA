# Capability Memory Audit

> **Taşınabilir şablon.** Skorlar ve örnekler hedef projede `bridge-venture.sh` + `ulas memory ingest` sonrası dolar.

**Scope:** Gap between venture-level learning and capability-level operational memory  
**Constraint:** No new governance · agent · council · trust score

---

## Executive finding

APP-FABRIKA has **three OS layers** at different maturity:

| OS | Maturity | Problem |
|----|----------|---------|
| Governance | ~90% | Diminishing returns on new files |
| Execution | ~55% | Dispatch stops at contract — no wired AI adapter |
| **Knowledge** | **~40%** | Lessons stored; **capability knowledge not operational** |

**Project Memory** (CL4R1T4S principle, not prompt copy): agents restart at zero each task. Target: `android.architecture` behaves better on venture #50 than #1.

---

## 1. What exists today?

| Asset | Location | Capability-linked? |
|-------|----------|-------------------|
| NEVER_AGAIN | `ULAS/memory/never-again.json` | ❌ Decision gate only |
| ADR | `06-learning/adr/` | ❌ Venture/project scoped |
| Patterns | `06-learning/patterns/` | ⚠️ Generic, not per capability_id |
| Postmortems | `06-learning/postmortems/` | ❌ Empty until first venture |
| Outcomes | `10-runtime/ulas/decisions/` | ❌ Not promoted to capability |
| Compressed postmortem | `ULAS/07-knowledge-compression/` | ❌ Template only |
| Context manifest | `10-runtime/context-manifest.schema.json` | ❌ No capability-memory section |
| Dispatch context_refs | work chain wp refs only | ❌ No memory injection |

**Verdict:** Learning **pipeline exists on paper**; capability **feedback loop does not**.

---

## 2. External memory patterns (research synthesis)

Modern agentic systems converge on similar splits — **not** copy any vendor prompt:

| Pattern | Examples | APP-FABRIKA mapping |
|---------|----------|---------------------|
| **Working vs archive memory** | `AGENTS.md` vs agent-memory archive | `03-agents/` vs `capability-memory/` |
| **Claim + provenance** | agent-knowledge UMSF | `source` block on each entry |
| **Progressive disclosure** | agent-memory tiered recall | compression tiers 1/2/3 |
| **MCP as provider adapter** | team-memory-mcp, total-agent-memory | Future: memory MCP feeds dispatch |
| **Temporal / decay** | team-memory Bayesian decay | Optional — deprecate stale experimental |
| **Cross-tool portability** | Provider-agnostic memory store | capability_id stable across Cursor/Claude |

**Reject for Capability Memory:** synthetic confidence scores, auto-trust mutation, governance councils for promotion.

---

## 3. Per-capability: what must be stored?

### android.architecture

| Kind | Examples (generic) | Source |
|------|-------------------|--------|
| anti_pattern | Module boundary / layer violation | verification fail |
| constraint | Adapter module layout rules | ADR |
| failure_mode | API boundary bypass in workers/services | test failure |
| pattern | Proven layout for this venture type | postmortem |
| checklist | Pre-ship architecture audit | execution log |

### android.testing

| Kind | Examples (generic) |
|------|-------------------|
| failure_mode | Test runtime / JDK / Robolectric mismatch |
| constraint | Use venture `build.unit_test_task` consistently |
| success_recipe | Zero-fail gate before evidence bridge |

### android.security / performance / ux

Store platform-standard constraints + venture-specific proven fixes.

### web.frontend / ios.design

Link to `04-design/DESIGN_PRINCIPLES.md` as **constraint** entries — anti-AI-pattern knowledge.

### ai.reasoning

| Kind | Examples |
|------|----------|
| anti_pattern | Unverified claim in decision rationale |
| constraint | Hallucination guard — file must exist before cite |

---

## 4. What is missing (gap list)

1. **Capability-scoped store** — was missing → now `capability-memory/knowledge/`
2. **Ingest path** — outcome/postmortem → capability entries
3. **Dispatch injection** — memory in `ai_invoke` context_refs
4. **Promotion** — experimental → proven with evidence rules
5. **Regression** — proven anti_pattern violated again
6. **Compression** — token-budget recall for 50+ entries
7. **Wired AI dispatch** — still blocked (Execution OS)

---

## 5. Synthetic vs real data

| Data | Status |
|------|--------|
| Capability knowledge entries | **0** (template — no fabrication) |
| Venture-specific failures | Ingest after first `bridge-venture.sh` |
| NEVER_AGAIN entries | Empty |
| Postmortems | None |

**First ingest:** execution or evidence failures → tagged `capability_id` via `ulas memory ingest`.

---

## 6. Provider dependency

Capability Memory is **provider-independent**. Same `android.architecture.json` feeds Cursor, Claude, or human dispatch envelopes.

---

## 7. Recommended architecture

```
Outcome / Postmortem / ADR / Verification fail
        ↓ ingest (tag capability_id)
capability-memory/knowledge/{capability_id}.json
        ↓ promote (evidence rules)
proven entries
        ↓ compress (tier 1/2/3)
ulas memory query --capability X
        ↓ inject
dispatch envelope context_refs + memory tier
        ↓
future execution (any provider)
```

---

## Maturity after this design

| Dimension | Before | After design | After first ingest |
|-----------|--------|--------------|-------------------|
| Capability Memory | 0% | 70% (schema+flow) | 85% |
| Knowledge OS | 40% | 55% | 65% |
| Cross-venture learning | 0% | Path defined | 1 venture |

---

## Deliverables index

| Doc | Purpose |
|-----|---------|
| [`CAPABILITY_LEARNING_FLOW.md`](CAPABILITY_LEARNING_FLOW.md) | End-to-end loop |
| [`capability-knowledge.schema.json`](capability-knowledge.schema.json) | Store shape |
| [`CAPABILITY_PROMOTION_RULES.md`](CAPABILITY_PROMOTION_RULES.md) | experimental → proven |
| [`CAPABILITY_REGRESSION_DETECTION.md`](CAPABILITY_REGRESSION_DETECTION.md) | Re-failure detection |
| [`CAPABILITY_KNOWLEDGE_COMPRESSION.md`](CAPABILITY_KNOWLEDGE_COMPRESSION.md) | Token tiers |
