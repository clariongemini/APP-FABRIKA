# Policy Evolution Framework

## Principle

A mistake should be **capable** of producing a future policy improvement — not guaranteed automatically.

## Policy locations

| Policy | Path | Evolvable |
|--------|------|-----------|
| Context escalation | `ULAS/policies/context-escalation.json` | ✅ |
| Decision classes | `ULAS/policies/decision-classes.json` | ✅ |
| Review matrix | `ULAS/policies/review-matrix.json` | ✅ |
| Confidence weights | `ULAS/scoring/confidence-weights.json` | ✅ |

## Evolution triggers (manual gate)

| Trigger | Example action |
|---------|----------------|
| LOW_CONFIDENCE precision < 0.6 at N≥20 | Raise evidence weight |
| false_block rate > 20% | Lower confidence block threshold |
| repeat failure (NEVER_AGAIN miss) | Add class D requirement |
| tier3 overuse > 60% on class A/B | Tighten escalation rules |

## Change protocol

1. **Detect** — `feedback-audit` or postmortem  
2. **Propose** — SVOS-ADR in `06-learning/adr/`  
3. **Review** — planner + auditor (ULAS decide class C)  
4. **Apply** — edit policy JSON + git commit  
5. **Record** — ADR + optional `policy-changelog.md` entry  

## Automation status

| Step | Automated |
|------|-----------|
| Detect metrics | ✅ partial |
| Propose ADR | ❌ human |
| Apply policy | ❌ human |
| Audit trail | ✅ git + ADR |

## Why not auto-update policies

Auto policy mutation without venture evidence = **meta-factory drift**.  
Phase 4: prove manual loop first; automate only after N≥50 closed outcomes.
