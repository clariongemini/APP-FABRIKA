# Venture Runtime OS

Standard artefacts when a venture traverses:

```
Decision → Work → Route → Dispatch → Execute → Verify → Evidence → Outcome
```

---

## Runtime tree

```
10-runtime/
├── ulas/
│   ├── decisions/{decision_id}.json      # ULAS decide output
│   ├── work/{decision_id}.json           # work chain + routing_manifest
│   ├── dispatch/{decision_id}.json       # provider dispatch log
│   ├── execution/{decision_id}.json        # verify/repair attempts
│   ├── routing/policy-overrides.json     # optional provider overrides
│   └── metrics/aggregates.json           # effectiveness (existing)
├── evidence/{venture_slug}/manifest.json # runtime copy of evidence
└── ventures/{venture_slug}/state.json    # optional venture runtime (future)
```

Canonical evidence (durable): `07-evidence/{venture_slug}/manifest.json`

---

## Artefact contract

| Stage | Required fields | Producer |
|-------|-----------------|----------|
| Decision | `decision_id`, `status`, `venture_slug` | `ulas decide` |
| Work | `work_packages`, `execution_manifest`, `verification_manifest` | `ulas work generate` |
| Route | `routing_manifest.bindings` | `ulas capability route` |
| Dispatch | `envelopes[]` per delegated binding | `ulas dispatch plan` |
| Execute | `attempts[]`, `repair_plan` | `ulas execute run` |
| Evidence | `sources[]`, `failed` counts | `bridge-venture.sh` |
| Outcome | `effectiveness.outcome` | `ulas outcome` |

---

## Venture.json sync

`08-ventures/{slug}/venture.json` receives:

- `validation` from bridge
- `evidence_status`
- `codebase_path` / `codebase_resolved`
- `stage` transitions: charter → validate → ship

---

## Closure criteria (venture loop complete)

1. Decision `APPROVED`
2. Work chain `state: verified`
3. Evidence `unit_test.failed: 0` (or platform equivalent)
4. Outcome `approved_success`
5. Optional: postmortem in `06-learning/`

---

## Template venture state (no pre-seeded charter)

Repoda hazır venture yok. İlk kurulum:

```bash
./APP-FABRIKASI/scripts/init-venture.sh "My App" my-app path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh my-app
```

| Artefact | Template repo |
|----------|----------------|
| Decision / Work / Execution | Boş (`10-runtime/ulas/` — `.gitignore`) |
| Evidence | `_template/` only |
| Outcome / Learning | İlk venture sonrası doldurulur |

**Venture runtime maturity:** scaffold — loop ilk projede kapanır.

---

## CLI traverse

```bash
ulas decide --venture SLUG ...
ulas work generate --decision-id ID
ulas capability route --decision-id ID
ulas dispatch plan --decision-id ID
ulas execute run --decision-id ID
./scripts/bridge-venture.sh SLUG
ulas outcome --decision-id ID --result approved_success
```
