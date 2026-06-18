# Provider Dispatch

Completes the chain:

```
Capability  →  Provider  →  Dispatch  →  Execution
```

No Cursor/Claude/Gemini API calls in this layer — **contract only**.

---

## Contract

Every dispatch produces a [`provider-contract.schema.json`](provider-contract.schema.json) envelope:

```json
{
  "contract_version": "1.0",
  "dispatch_id": "my-app-b-...-wp-2-...",
  "capability_id": "android.architecture",
  "provider_id": "cursor",
  "provider_type": "ai_ide",
  "invoke": {
    "schema": "ai_invoke",
    "context_refs": ["10-runtime/ulas/work/....json#wp-2"],
    "instruction": "implement fixes...",
    "acceptance": "targeted tests pass locally"
  },
  "status": "pending"
}
```

Consumers (Execution Engine, future adapters) read **envelope** — never provider SDK.

---

## Invoke schemas

| Schema | Provider types | Payload |
|--------|----------------|---------|
| `shell_invoke` | local_shell | `cmd`, `cwd`, `timeout_sec` |
| `ai_invoke` | ai_ide, ai_api | `instruction`, `context_refs`, `acceptance` |
| `manual_invoke` | human | `instruction`, `acceptance` |

---

## Swap test

Change `routing-policy.json`:

```json
"android.architecture": "claude"
```

Unchanged: work packages, execution manifest, verification manifest, dispatch code path.

Only envelope `provider_id` + `provider_type` change.

---

## CLI

```bash
ulas dispatch plan --decision-id ID       # build dispatch envelopes (no API)
ulas dispatch execute --decision-id ID [--mode queue|sdk] [--dispatch-id DID]
ulas dispatch complete --decision-id ID --dispatch-id DID --result success|failed
ulas dispatch log --decision-id ID        # runtime dispatch log
ulas dispatch audit                       # adapter readiness
```

→ Runtime detail: [`dispatch-runtime.md`](dispatch-runtime.md)
