# AI Dispatch Gap Analysis

**Date:** 2026-06-18  
**Context:** Execution Validation Sprint proved shell + verify work; **AI Dispatch is STUB**.  
**Goal:** Close `Capability → Provider → Real work` without new governance layers.

---

## Problem statement

```
Today:
  routing-policy.json  →  envelope (ai_invoke)  →  invoke_provider()  →  skipped: not wired

Needed:
  envelope  →  adapter  →  code/files change  →  result write-back  →  execute verify
```

The missing piece is **not** memory, decision, or routing — it is a **provider adapter** behind `invoke_provider()` for `ai_ide` / `ai_api` types.

---

## Option matrix

Scoring: **Low / Medium / High** unless noted.  
**Automation:** % of dispatch→verify loop without human.  
**Reliability:** repeatability on same envelope in CI/dev.

| Option | Applicability | Automation | Reliability | Cost | Integration complexity | Notes |
|--------|---------------|------------|-------------|------|----------------------|-------|
| **A. Cursor IDE Agent Mode (manual)** | High | ~10% | Medium | $0 marginal | **Low** | Open repo; paste envelope prompt in chat. Proves chain semantics only. |
| **B. File-based dispatch queue** | High | ~20% | Medium–High | $0 | **Low** | `ulas dispatch execute` writes `10-runtime/ulas/dispatch/queue/{dispatch_id}.md`; human/agent completes; `ulas dispatch complete`. |
| **C. Cursor SDK — `Agent.prompt` (local)** | High | ~70% | Medium | API usage (Cursor subscription + model) | **Medium** | `cursor-sdk` / `@cursor/sdk`, `CURSOR_API_KEY`, `local: { cwd: path/to/codebase/ }`. Best first **programmatic** path. |
| **D. Cursor SDK — `Agent.create` + `send`** | High | ~75% | Medium | Same as C | **Medium** | Multi-turn repair (attempt 2–3). Watch: local context bugs reported in beta — include full context in each prompt until stable. |
| **E. Cursor SDK — cloud agent** | Medium | ~80% | Medium–High | Higher (VM + model) | **Medium–High** | Needs repo URL / clone; good for CI, less for local venture loop. |
| **F. Cursor desktop CLI (`cursor`)** | **Low** | ~0% | — | $0 | Low | **Not an agent API** — open files/diff/merge only. Cannot run Agent Mode from CLI today. |
| **G. MCP inside Cursor** | Medium | ~30% | Medium | $0 | **Medium** | MCP servers extend *in-IDE* agent tools. Does not replace external `ulas.py` dispatch; useful as adapter *tooling* (read envelope, run gradle). |
| **H. Claude / Gemini API (direct)** | Medium | ~85% | Medium | Per-token API | **Medium** | Fits `ai_api` in registry; no IDE integration; weaker on multi-file Android refactors without custom tooling. |
| **I. Human-in-the-loop gate** | High | ~40% | **High** | Human time | **Low** | Required for v0 anyway: approve diff before verify. Composes with B or C. |
| **J. GitHub Action + Cloud Agent** | Medium | ~90% | High (CI) | CI minutes + API | **High** | Post-v1; needs PAT, branch policy, secret management. |

---

## Per-option detail

### A — Cursor IDE Agent Mode (interactive)

**How:** Developer runs `ulas dispatch plan`, opens generated envelope, copies `instruction` + `capability_context` into Cursor chat.

| | |
|--|--|
| **Works for** | Proving dispatch payload quality, memory inject, acceptance criteria |
| **Fails for** | Unattended repair loop, outcome closure at scale |
| **Integration** | Zero code; documentation only |
| **Blocker** | No write-back to `dispatch log` → execute still sees `skipped` |

### B — File-based queue (recommended v0)

**How:**

```
ulas dispatch execute --decision-id ID
  → for each pending ai_invoke envelope:
       write 10-runtime/ulas/dispatch/queue/{dispatch_id}.md
       status: dispatched
  → human or Cursor chat completes task
ulas dispatch complete --dispatch-id DISPATCH_ID --result success|failed
  → update envelope.result, status
ulas execute run --decision-id ID
  → verify only (or full loop)
```

| | |
|--|--|
| **Automation** | Low unless paired with SDK |
| **Reliability** | High — auditable artefacts, no API key in v0 |
| **Cost** | Free |
| **Why first** | Closes **Dispatch → Execution → Verify** semantics before API risk |

### C/D — Cursor SDK (local agent)

**How:** Thin adapter `APP-FABRIKASI/ULAS/adapters/cursor_sdk_adapter.py`:

```python
# Pseudocode — not in core ulas.py
from cursor_sdk import Agent, AgentOptions, LocalAgentOptions

def handle_ai_invoke(envelope: dict, cwd: Path) -> dict:
    prompt = build_prompt(envelope)  # instruction + capability_context + acceptance
    result = Agent.prompt(prompt, AgentOptions(
        api_key=os.environ["CURSOR_API_KEY"],
        model="composer-2.5",
        local=LocalAgentOptions(cwd=str(cwd)),
    ))
    return {
        "success": result.status != "error",
        "stdout_ref": save_transcript(result),
        "exit_code": 0 if result.status != "error" else 1,
    }
```

| | |
|--|--|
| **Automation** | First path to real **code change without human paste** |
| **Reliability** | Beta SDK — distinguish `CursorAgentError` (never ran) vs `status==error` (ran, failed) |
| **Cost** | `CURSOR_API_KEY`; local mode still uses hosted models |
| **Prereqs** | Node or Python SDK install; API key; `cwd` = venture codebase (`path/to/codebase/`) |
| **APP-FABRIKA fit** | `provider-registry.json`: set `cursor.wired: true`, `adapter: adapters/cursor_sdk_adapter` |

**Not the same as:** `cursor` shell binary (editor only).

### E — Cloud agent

Use when local machine cannot run agent (no IDE, headless CI). Requires repo remote and cloud credentials. Defer until local SDK path proven on target codebase.

### F — Cursor CLI

Verified: `/usr/local/bin/cursor` = VS Code–style launcher (diff, merge, goto). **No `agent` subcommand.** Do not build adapter on CLI alone.

### G — MCP

MCP (e.g. `cursor-ide-browser`, custom tools) augments the agent **inside** Cursor. Possible pattern:

- External: `ulas dispatch execute` writes queue file
- In Cursor: rule/skill reads queue, calls MCP shell for gradle

Still needs human or SDK trigger. MCP is **complement**, not replacement for adapter.

### H — Claude / Gemini (`ai_api`)

| | |
|--|--|
| **Pros** | Swap via `routing-policy.json`; good for text-only tasks |
| **Cons** | No native workspace edit loop; need patch application layer |
| **When** | Second provider after Cursor adapter pattern exists |

### I — Human-in-the-loop

**Always on for v0:**

1. Adapter produces diff summary / transcript ref in `envelope.result`
2. Optional: `ulas dispatch complete` requires `--ack` or git diff non-empty
3. Founder gate for Class A decisions (already in ULAS)

Raises reliability; caps automation — acceptable for first proof.

---

## Architecture: first working chain (v0 → v1)

### Design principles (unchanged)

- **Capability → Provider** (never Provider → Capability)
- Core `ulas.py` calls `invoke_provider()` only
- Adapters live in `ULAS/adapters/` (new folder, not a new OS layer)
- Envelope schema unchanged (`provider-contract.schema.json`)

### v0 — Queue + complete (1–2 days)

```
dispatch plan
dispatch execute     ← NEW: materialize queue, mark dispatched
[Cursor chat / human]
dispatch complete    ← NEW: write result
execute run          ← verify sees real prior work
```

**Success criterion:** One envelope moves `pending → dispatched → completed`; verify run after manual fix shows fewer failures (or same until fix landed).

### v1 — Cursor SDK adapter (3–5 days)

```
dispatch execute
  → cursor_sdk_adapter.handle_ai_invoke(envelope, cwd)
  → git diff captured in result.stdout_ref
execute run (verify)
```

**Success criterion:** `ulas execute run` on target codebase WP-A reduces failure count without human paste.

### v1.5 — Repair loop integration

Wire `execute run` to call `dispatch execute` for `repair_plan` bindings before re-verify (max 3 attempts). Memory `record_memory_impact` on outcome.

---

## Provider registry changes (minimal)

```json
"cursor": {
  "type": "ai_ide",
  "dispatch": "delegated",
  "wired": true,
  "adapter": "ULAS/adapters/cursor_dispatch.py",
  "adapter_mode": "sdk_local",
  "requires_env": ["CURSOR_API_KEY"]
}
```

`invoke_provider()` extension:

```python
if ptype in ("ai_ide", "ai_api") and provider.get("wired"):
    return load_adapter(provider["adapter"]).handle(envelope, codebase)
return { "skipped": True, "reason": "..." }
```

---

## What NOT to do

| Anti-pattern | Why |
|--------------|-----|
| New governance phase for dispatch | Org expansion; zero execution proof |
| Embed Cursor SDK inside `ulas.py` | Violates adapter swap |
| Fix venture 10 tests before adapter | Product work; doesn't prove OS |
| Trust `cursor` CLI as agent | Wrong tool |
| Cloud-first before local SDK | Slower iteration on target codebase |

---

## Decision recommendation

| Priority | Deliverable |
|----------|-------------|
| **1** | `ulas dispatch execute` + `ulas dispatch complete` (file queue) |
| **2** | `ULAS/adapters/cursor_dispatch.py` using Cursor SDK `Agent.prompt` |
| **3** | `invoke_provider` adapter hook (10 lines in core) |
| **4** | work package WP-1 as **adapter proof**, not as OS milestone |
| **5** | Claude adapter copy-paste of cursor adapter interface |

---

## Honest positioning (aligned with Mimar)

| Label | Accurate today? |
|-------|-----------------|
| AI Company OS | No — no autonomous code change |
| AI Project Management OS | **Yes** |
| AI Company OS (after v1 adapter) | Partial — one provider, one venture |

Closing the adapter gap is the **first measurable step** from Project Management OS toward Company OS.

---

## References

- Contract: `ULAS/dispatch/provider-contract.schema.json`
- Runtime: `ULAS/dispatch/dispatch-runtime.md`
- Sprint proof: `ULAS/execution/EXECUTION_VALIDATION_SPRINT.md`
- Cursor SDK: https://cursor.com/docs/sdk/python · https://cursor.com/docs/sdk/typescript
- Audit CLI: `ulas dispatch audit`
