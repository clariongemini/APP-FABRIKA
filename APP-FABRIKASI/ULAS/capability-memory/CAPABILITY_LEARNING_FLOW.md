# Capability Learning Flow

Venture learning → capability operational knowledge → future execution.

**Not** a new governance layer. Extends `06-learning/` + ULAS outcome chain.

---

## Flow

```
┌─────────────────────────────────────────────────────────────┐
│ SOURCES (venture-scoped)                                     │
│  outcome · postmortem · ADR · execution log · verification   │
└───────────────────────────┬─────────────────────────────────┘
                            │ ulas memory ingest
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ CAPABILITY MEMORY (capability-scoped)                        │
│  experimental entries per capability_id                      │
└───────────────────────────┬─────────────────────────────────┘
                            │ promote (evidence rules)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PROVEN KNOWLEDGE                                             │
│  patterns · anti_patterns · constraints                      │
└───────────────────────────┬─────────────────────────────────┘
                            │ compress + query
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ DISPATCH / EXECUTION                                         │
│  context_refs += capability-memory tier1/2                   │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
                    Next venture (fewer repeat mistakes)
```

---

## Ingest triggers

| Event | CLI | Target capabilities |
|-------|-----|---------------------|
| Outcome recorded | `ulas memory ingest --from outcome --decision-id ID` | From work package capability_ids |
| Postmortem written | `ulas memory ingest --from postmortem --venture SLUG --file PATH` | Tagged in frontmatter |
| Verification fail | `ulas memory ingest --from execution --decision-id ID` | repair_plan targets |
| Manual lesson | `ulas memory ingest --from manual --capability ID --title ...` | Explicit |

Ingest always creates **experimental** entries. Never auto-proven.

---

## Query triggers

| When | CLI | Tier |
|------|-----|------|
| Capability route | auto | tier1 titles only |
| Dispatch plan | auto | tier1 + tier2 compressed |
| Human / AI session | `ulas memory query --capability ID` | tier2 default |
| Deep debug | `--tier 3` | full body + source refs |

---

## Venture vs capability

| Venture memory | Capability memory |
|----------------|-------------------|
| `08-ventures/{slug}/` | `capability-memory/knowledge/{id}.json` |
| Dies with archive? | **Accumulates** across ventures |
| "What happened to venture X?" | "What must this capability never repeat?" |

Same postmortem feeds **both**: full text in `06-learning/`, compressed capability entries via ingest.

---

## CLI summary

```bash
ulas memory ingest --from outcome --decision-id ID
ulas memory query --capability android.architecture [--tier 1|2|3]
ulas memory promote --capability android.architecture --entry cap-k-001
ulas memory compress --capability android.architecture
ulas memory stats
```

---

## Anti-patterns

- Storing prompts in capability memory
- Auto-promote without evidence
- Trust score on entries
- Duplicate NEVER_AGAIN — link instead: capability entry may reference `never-again` id
