# Adaptive Decision Framework

## Principle

**Behavior change > documentation growth.**

Adaptation uses existing ULAS surfaces only — no new agents.

## Propagation surfaces

| Surface | File | Auto on propagate |
|---------|------|-------------------|
| Trust | `scoring/trust-scores.json` | ✅ |
| Review chain | `10-runtime/.../policy-overrides.json` | ✅ |
| Context tier | same overrides | ✅ |
| Confidence weights | same overrides | ✅ |
| NEVER_AGAIN | `memory/never-again.json` | ⚠️ `--apply-memory` |
| Canonical policy | `policies/*.json` | ❌ ADR + human |
| Patterns | `06-learning/patterns/` | ❌ manual script |

## Outcome → adaptation map

| Outcome | Trust | Review | Context | Confidence | Memory |
|---------|-------|--------|---------|------------|--------|
| approved_failed | missed | +auditor | tier↑ | evidence +0.05 | candidate |
| overturned | missed | +auditor | tier↑ | evidence +0.05 | candidate |
| approved_success | good | — | — | — | — |
| correct_block | good | — | — | — | — |
| false_block | good | — | — | evidence −0.03 | — |
| prevented_failure | good | — | — | — | confirm |

## Termination audit

Run `ulas propagation-audit` — maps each chain to:

- where feedback **terminates**
- manual vs automated steps
- whether `decide()` behavior changes

## Anti-patterns

- New Trust Manager Agent — **forbidden**
- Auto-edit `policies/*.json` — **forbidden** (use runtime overrides)
- Propagate without outcome — **blocked**

## Proof command sequence

```bash
ulas decide --venture SLUG --class B --title "Risky change" --reviewers architect,qa
ulas outcome --decision-id ID --result approved_failed --propagate
ulas decide --venture SLUG --class B --title "Similar change" --reviewers architect,qa
# Second decide should show: missing auditor, adaptations_applied: true
```
