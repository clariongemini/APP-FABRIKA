> **Not:** Bu dosya scaffold denetimidir. Repoda örnek venture veya validation verisi bulunmaz — skorlar `ulas maturity audit` ile canlı ölçülür.


## Part 1 — Layer Audit

### 1. Which layers actually work?

| Layer | Evidence | Verdict |
|-------|----------|---------|
| **ULAS Decision** | `ulas decide`, `outcome`, `propagate` — runtime JSON in `10-runtime/ulas/decisions/` | ✅ Operational |
| **Work Engine** | `ulas work generate` — work chain with manifests | ✅ Operational |
| **Capability Router** | `ulas capability route/show` — routing_manifest on work chain | ✅ Operational |
| **Execution Engine** | `ulas execute run` — gradle, verify, retry, bridge | ✅ Partial (shell only) |
| **Evidence Bridge** | `bridge-venture.sh` — real build + test → `07-evidence/` | ✅ Operational |
| **Provider Dispatch** | `ulas dispatch plan` — contract envelopes, no API | ✅ Contract (post-consolidation) |
| **Capability Marketplace** | `marketplace/capability-marketplace.json` | ✅ Catalog |
| **Provider Evaluation** | Schema + methodology only | 📋 Framework |
| **Self-Healing** | Repair plans in execution log | ✅ Partial |
| **Venture Runtime** | Standard paths documented | 📋 Spec + partial data |
| **Design Principles** | `04-design/DESIGN_PRINCIPLES.md` | 📋 Standard |
| **Learning loop** | `06-learning/` — şablon ADR/postmortem | 📋 Awaiting first venture |
| **Portfolio** | `09-portfolio/` — venture yok | 📋 Blocked N≥2 |

### 2. Which layers are documentation only?

| Layer | Notes |
|-------|-------|
| Provider Evaluation comparisons | No scorecards populated — by design |
| Workforce Layer | Explicitly blocked until execution proven |
| Predictive Risk enforcement | Gate closed — observe only |
| iOS / Web / Backend adapters | Blueprint only — no venture |
| AI capabilities (`ai.*`) | Marketplace entries — no runtime proof |
| Trust / adaptive propagation | Exists but fed mostly by manual/synthetic history |

### 3. Which layers use synthetic data?

| Layer | Synthetic risk |
|-------|----------------|
| ULAS trust / calibrate | Pre-P1 bogus outcomes possible; P1 patches applied |
| Risk gate thresholds | Designed thresholds — not met |
| Readiness scores in meta.json | Self-assessed |
| Portfolio intelligence | No data |
| Provider scorecards | **None generated** (correct) |

### 4. Which layers are validated with real evidence?

| Layer | Template repo | After first venture |
|-------|---------------|---------------------|
| Evidence bridge | 📋 Script exists | `07-evidence/{slug}/manifest.json` from `bridge-venture.sh` |
| Execution log | 📋 `.gitignore` — empty | Real gradle attempts in `10-runtime/ulas/execution/` |
| Venture validation | 📋 No charter | `venture.json` validation block from bridge |
| Decision → Work → Route | 📋 CLI operational | Full chain on disk per `{decision-id}` |
| Outcome closure | 📋 N/A | `approved_success` recorded via `ulas outcome` |

### 5. Which layers are provider-dependent?

| Layer | Dependency |
|-------|------------|
| `android.architecture` default | Policy binds `cursor` — **swappable via policy** |
| Execution (today) | `local_shell` for verify — not IDE-specific |
| Human dispatch | Mimar/Cursor session for code changes |
| bridge-venture.sh | Local gradle — not provider |

**Core chain is provider-agnostic.** Only routing policy names cursor; code does not.

### 6. Which layers are capability-independent?

| Layer | Independence |
|-------|--------------|
| ULAS gates / policies | Platform-agnostic |
| Work package shape | role + platform → capability_id |
| Execution manifest schema | Platform fills commands |
| Verification manifest | Platform fills checks |
| Marketplace IDs | Stable across providers |
| Dispatch contract | Provider-agnostic envelope |

---

## Part 2 — Consolidation Deliverables

| # | Component | Status |
|---|-----------|--------|
| 1 | Capability Router | ✅ Pre-existing |
| 2 | Execution Engine | ✅ Pre-existing |
| 3 | Evidence Bridge | ✅ Pre-existing |
| 4 | Provider Dispatch | ✅ `dispatch/` + `ulas dispatch` |
| 5 | Capability Marketplace | ✅ `marketplace/` |
| 6 | Multi-Provider Verification | ✅ `evaluation/` framework |
| 7 | Self-Healing Execution | ✅ `SELF_HEALING_EXECUTION.md` + repair plans |
| 8 | Enterprise Design System | ✅ `04-design/DESIGN_PRINCIPLES.md` |
| 9 | Cross-Platform Matrix | ✅ `capability-matrix.md` |
| 10 | Venture Runtime OS | ✅ `venture-runtime.md` |

---

## Part 3 — Final Report

### 1. Capability OS maturity: **scaffold** (ölç: `ulas maturity audit`)

| Subsystem | Template repo |
|-----------|---------------|
| Decision + governance | CLI + policies operational |
| Work + routing | `work generate` + `capability route` |
| Execution + healing | `execute run` + repair plans |
| Dispatch + marketplace | Queue cards + catalog |
| Evidence + venture loop | Awaiting `init-venture.sh` |
| Learning + evaluation | Awaiting first postmortem |

**Interpretation:** OS is portable; maturity scores apply per deployed project.

### 2. Provider independence: **policy-swappable**

- ✅ Capability → provider in policy JSON
- ✅ Dispatch contract stable across providers
- ✅ Marketplace default_provider overridable
- 📋 AI provider adapters optional (`--mode sdk`)
- 📋 Provider scorecards — populate after dual-run

**Swap test:** `android.architecture: claude` changes binding only.

### 3. Execution maturity: **automation ready**

- ✅ Automated verify + retry + bridge scripts
- ✅ Repair plan generation
- 📋 Auto code repair — human/IDE dispatch (by design)
- 📋 First venture — run `bridge-venture.sh {slug}` in target project

### 4. Venture runtime maturity: **paths defined, data per project**

- ✅ Artefact paths documented (`venture-runtime.md`)
- 📋 No pre-seeded venture in template repo
- 📋 Outcome / postmortem — filled after first ship

### 5. Top gaps (template repo — close in target project)

1. **First venture loop** — `init-venture.sh` → ship → `approved_success`
2. **Wire dispatch adapter** (IDE queue or SDK) behind contract
3. **First provider scorecard** (optional dual-run)
4. **Learning writeback** — outcome → `06-learning/postmortem`
5. **Second venture** — prove OS is project-agnostic
6. **CI hook** — `ulas execute verify` on PR

### 6. Next 90 days (per deployed project)

| Weeks | Focus | Exit criteria |
|-------|-------|---------------|
| **1–2** | First venture + bridge | `failed: 0`, outcome recorded |
| **3–4** | Dispatch adapter v1 | One work package via dispatch queue |
| **5–6** | Bridge automation | execute → evidence without manual steps |
| **7–8** | Second venture (optional platform) | Full runtime tree for 2 ventures |
| **9–12** | Learning + portfolio | Postmortem + N≥2 portfolio stub |

---

## Model-independence verdict

> Android Architecture: Cursor today, Claude tomorrow — what changes?

**One policy line.** Work chain, manifests, verification, dispatch contract unchanged.

APP-FABRIKASI is **approaching** model-independent OS. Remaining gap is **wired dispatch**, not architecture.

---

## Index

| Doc | Path |
|-----|------|
| Marketplace | `ULAS/marketplace/CAPABILITY_MARKETPLACE.md` |
| Dispatch | `ULAS/dispatch/provider-dispatch.md` |
| Evaluation | `ULAS/evaluation/PROVIDER_EVALUATION_FRAMEWORK.md` |
| Self-healing | `ULAS/execution/SELF_HEALING_EXECUTION.md` |
| Design | `04-design/DESIGN_PRINCIPLES.md` |
| Matrix | `ULAS/capability-matrix.md` |
| Venture runtime | `ULAS/venture-runtime.md` |
