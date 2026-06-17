# ULAS Phase 2 — Decision Execution OS

## Shift

| Phase 1 | Phase 2 |
|---------|---------|
| Prensip deposu | **Karar motoru** |
| `01-context-engineering/` docs | `policies/` + `workflows/` JSON |
| "Nasıl düşünülmeli?" | **"Sistem nasıl karar verecek?"** |

## Executable surface

```bash
# Routing: class → tier → review chain
./APP-FABRIKASI/scripts/ulas.sh route --class D

# Context assembly only
./APP-FABRIKASI/scripts/ulas.sh assemble --venture ulas-player --class B

# Full lifecycle gate
./APP-FABRIKASI/scripts/ulas.sh decide \
  --venture ulas-player \
  --class B \
  --title "Charter approval" \
  --reviewers architect,qa

# Trust calibration after outcome
./APP-FABRIKASI/scripts/ulas.sh calibrate --reviewer architect --outcome good
```

## Lifecycle (automated in `decide`)

```
Task → Context Assembly → READ_MORE? → Classify → Confidence
  → Review Chain → Approval/BLOCK → Audit record → (Memory on outcome)
```

Decision records: `APP-FABRIKASI/10-runtime/ulas/decisions/*.json`

## Structure

```
ULAS/
├── policies/      ← executable rules (JSON)
├── workflows/   ← state machine
├── gates/       ← gate documentation (logic in bin/ulas.py)
├── scoring/     ← confidence + trust (JSON + calibrate cmd)
├── memory/      ← NEVER_AGAIN + severity
└── bin/ulas.py  ← orchestrator
```

Phase 1 folders (`01-10/`) remain as **reference docs** — canonical policy is `policies/`.

## Success metrics (reduce)

- Repeated mistakes → NEVER_AGAIN gate
- Unnecessary context → tier escalation
- Unnecessary reviews → decision class A/B/C/D
- Low-confidence approvals → confidence block

## Restrictions (unchanged)

No new adapters · no new agents · no new governance · no prompt archives
