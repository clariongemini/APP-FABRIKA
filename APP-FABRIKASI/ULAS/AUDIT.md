# ULAS Component Audit

**Phase 3** — theoretical vs executing vs measurable vs no feedback loop.

| Component | Status | Executes | Measurable | Feedback loop |
|-----------|--------|----------|------------|---------------|
| Context escalation (T1/T2/T3/critical) | Operational | `assemble`, `decide` | Tier usage metrics | ⚠️ outcome only |
| Decision classes A–D | Operational | `route`, `decide` | Per-class counts | ⚠️ outcome only |
| READ_MORE_REQUIRED gate | Operational | `decide` | Block reason counts | ✅ outcome tags |
| Confidence model | Operational | `decide` | Band precision | ✅ `outcome` cmd |
| Review matrix | Operational | `decide` | Reviewer accuracy | ✅ `outcome` + `calibrate` |
| Trust scores | Operational | `calibrate` | Per-capability trust | ✅ calibrate loop |
| NEVER_AGAIN scan | Operational | `decide` | Hit / prevented counts | ⚠️ manual prevented tag |
| Decision audit JSON | Operational | `decide` | total_decisions | ✅ `outcome` cmd |
| Memory update post-decision | **Theoretical** | — | — | ❌ needs venture postmortem |
| Pattern extraction auto | **Theoretical** | — | — | ❌ needs 06-learning hook |
| Portfolio allocation | **Theoretical** | N/A | N/A | ❌ N≥2 ventures |
| Founder approval gate (class D) | **Partial** | logged only | — | ❌ human step |

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Feedback loop exists (Phase 3) |
| ⚠️ | Partial — needs outcome data volume |
| ❌ | Not wired — do not build now; validate via venture |

---

## Priority

1. **Instrument** executing components (`metrics`, `outcome`, `report`)
2. **Collect** 10 → 50 → 100 decisions via real venture work
3. **Do not** add theoretical components until measured

---

## CL4R1T4S

Extraction **complete**. Remaining value is vendor prompt engineering — out of scope.

Captured: context discipline, review chains, confidence, escalation, memory, token economy, routing.
