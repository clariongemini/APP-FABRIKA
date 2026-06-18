# Predictive Decision Framework

## Principle

**Prevention > reaction.**

Move from:

```
Decision → Outcome → Adaptation
```

to:

```
Observation → Prediction → Decision → Outcome → Adaptation
```

No Risk Agent. No Forecast Council. **Risk scoring inside existing ULAS.**

## Inputs (all existing surfaces)

| Input | Source |
|-------|--------|
| Decision class | `policies/decision-classes.json` |
| Reviewer trust | `scoring/trust-scores.json` |
| Reviewer history | `10-runtime/ulas/metrics/aggregates.json` |
| Context tier | context assembly |
| Evidence level | `08-ventures/*/venture.json` → `evidence_status` |
| Memory hits | `memory/never-again.json` scan |
| Policy overrides | `10-runtime/ulas/adaptations/policy-overrides.json` |
| Complexity | title/proposal heuristics + class tier |
| Similar failures | past `approved_failed` decisions |

## Outputs

| Band | Score | Behavior (when gate **active**) |
|------|-------|--------------------------------|
| **low** | 0–39 | Standard review chain |
| **medium** | 40–59 | +auditor suggested in chain |
| **high** | 60–79 | auditor required |
| **critical** | 80–100 | auditor + security + founder gate |

## Activation gate (mandatory)

Prediction is **designed** in Phase 6. **Enforcement** waits for evidence.

```bash
ulas risk-gate    # show criteria + current values
ulas risk ...     # always preview (observe mode)
```

Gate opens when **all** criteria met:

| Criterion | Threshold |
|-----------|-----------|
| Decisions recorded | ≥ 20 |
| Outcomes evaluated | ≥ 10 |
| Readiness snapshots | ≥ 4 |
| Evidence bundles | ≥ 1 |
| Shipped ventures | ≥ 1 |

Until then: `decide()` records `prediction` block but does **not** escalate.

## Priority order (Mimar)

1. Feedback loop closure  
2. Trust explainability  
3. Trend analysis  
4. **Predictive risk** ← Phase 6 (gated)

## Anti-patterns

- Risk Agent / Prediction Agent — **forbidden**
- Auto-enable without evidence — **forbidden**
- New governance layer — **forbidden**

## Proof sequence (post-gate)

```bash
ulas risk --venture SLUG --class B --reviewers architect,qa --title "Complex refactor"
# risk_score: 82, band: critical, factors: {...}

ulas decide ...   # with gate active → FOUNDER_GATE or missing auditor
```
