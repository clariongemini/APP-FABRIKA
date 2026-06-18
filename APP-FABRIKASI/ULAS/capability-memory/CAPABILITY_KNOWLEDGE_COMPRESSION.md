# Capability Knowledge Compression

Progressive disclosure for token economy — inspired by agent-memory / MCP recall patterns.

**Not** new documentation — operational recall for dispatch.

---

## Three tiers

| Tier | Content | Token budget | When loaded |
|------|---------|--------------|-------------|
| **1** | `title` + kind emoji | ~200 total per capability | Every route/dispatch |
| **2** | `body_compressed` (≤80 words/entry) | ~800 per capability | Dispatch ai_invoke |
| **3** | Full `body` + `source.ref` | On demand | `memory query --tier 3` |

---

## Compression rules

1. **Proven entries first** — experimental only if tier2 space remains
2. **Anti_patterns before patterns** — higher recall priority
3. **Dedupe by tag** — same test class name → merge entries on compress
4. **Venture-agnostic wording** — strip venture names from body_compressed

Example tier2 line:

```
[anti_pattern] Do not violate module boundary rules — relocate to correct layer per adapter. (architecture-test)
```

---

## Algorithm (`ulas memory compress`)

```
for each proven + experimental (ranked):
  body_compressed = first_sentence(body) + tag_suffix
merge duplicates by normalized title
truncate list to tier2_max_tokens (word estimate)
write compression_profile.last_compressed_at
```

No LLM required for v1 — rule-based. Optional v2: summarizer provider via dispatch contract.

---

## Query output shape

```json
{
  "capability_id": "android.architecture",
  "tier": 2,
  "entries": [
    {"id": "cap-k-001", "kind": "anti_pattern", "text": "..."}
  ],
  "token_estimate": 420
}
```

Injected into dispatch:

```json
"context_refs": [
  "10-runtime/ulas/work/....json#wp-2",
  "ULAS/capability-memory/knowledge/android.architecture.json?tier=2"
]
```

---

## Refresh policy

| Event | Action |
|-------|--------|
| promote | compress capability |
| ingest (if >5 experimental) | compress |
| nightly (future) | optional batch |

---

## Working memory boundary

| Store | Role |
|-------|------|
| `.cursorrules` / `AGENTS.md` | Session working memory — human curated |
| `capability-memory/` | Archive — machine ingested, evidence-backed |

Never dump full capability store into rules files.
