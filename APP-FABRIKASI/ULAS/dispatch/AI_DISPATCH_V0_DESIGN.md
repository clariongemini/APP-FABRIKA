# AI Dispatch v0 — First Working Chain

**Status:** v0 implemented · v1 adapter wired (`--mode sdk`)  
**Scope:** Minimal adapter surface. No governance. Proves `Capability → Provider → Work → Verify`.

---

## New CLI (only)

```bash
ulas dispatch execute --decision-id ID [--dry-run]
ulas dispatch complete --decision-id ID --dispatch-id DISPATCH_ID --result success|failed [--transcript PATH]
```

---

## File layout

```
10-runtime/ulas/dispatch/
  {decision_id}.json          # existing log
  queue/
    {dispatch_id}.md          # human/agent task card
    {dispatch_id}.result.json # optional transcript metadata
```

---

## Queue card format (`{dispatch_id}.md`)

```markdown
# Dispatch: {dispatch_id}

- **Decision:** {decision_id}
- **Work package:** {work_package_id}
- **Capability:** {capability_id}
- **Provider:** cursor
- **Codebase:** path/to/codebase/

## Instruction
{invoke.instruction}

## Acceptance
{invoke.acceptance}

## Capability context (tier 2)
{json capability_context — antipatterns, playbooks}

## Context refs
- {context_refs}

## Complete
When done:
ulas dispatch complete --decision-id ... --dispatch-id ... --result success
```

---

## State transitions

```
pending
  → dispatch execute → dispatched (+ queue file)
  → dispatch complete --result success → completed
  → dispatch complete --result failed → failed
  → execute run verify → evidence / memory impact
```

---

## `invoke_provider` hook (core change)

```python
# ulas.py — after provider registry lookup
adapter_path = provider.get("adapter")
if adapter_path and provider.get("wired"):
    mod = import_adapter(adapter_path)
    return mod.handle_ai_invoke(envelope, codebase)
if ptype in ("ai_ide", "ai_api"):
    return queue_fallback(envelope)  # v0: write .md, status=dispatched
```

v0 can ship **queue only** without SDK; v1 adds `cursor_dispatch.py`.

---

## Proof test (adapter acceptance)

1. `ulas dispatch plan --decision-id my-app-b-20260101000000`
2. `ulas dispatch execute --decision-id ...` → 2 queue files for wp-1, wp-2
3. Complete wp-1 after architect investigation (even doc-only result)
4. `ulas execute run` → verify still fails (expected until code fix)
5. **Pass:** envelope not `skipped`; dispatch log shows `dispatched`/`completed`

SDK v1 adds step 3 = actual code edit without manual paste.

---

## Environment

| Var | v0 | v1 |
|-----|----|----|
| `JAVA_HOME` | verify | verify |
| `CURSOR_API_KEY` | — | SDK adapter |
| `PLAYERS_ROOT` | optional cwd override | same |
