# Dispatch Runtime

Runtime artefacts for provider dispatch — no governance expansion.

---

## Paths

| Path | Content |
|------|---------|
| `10-runtime/ulas/dispatch/{decision_id}.json` | Dispatch log (envelopes + results) |
| `10-runtime/ulas/execution/{decision_id}.json` | Execution + verification attempts |
| `10-runtime/ulas/work/{decision_id}.json` | Work chain + routing_manifest |

---

## Lifecycle

```
capability route
    → routing_manifest on work chain
dispatch plan
    → one envelope per manual/delegated binding
dispatch execute (v0)
    → pending ai_invoke / manual_invoke → queue/{dispatch_id}.md
    → envelope status: dispatched
dispatch complete
    → envelope status: completed | failed + result artefact
execute run
    → shell_invoke envelopes executed via invoke_provider()
    → ai_invoke without SDK adapter → still skipped on execute run (use dispatch execute first)
    → results appended to dispatch log
```

---

## Envelope status machine

```
pending → dispatched → completed | failed
pending → skipped (wired=false or manual policy)
```

---

## Provider adapter (future)

External adapter implements:

```python
def handle_ai_invoke(envelope: dict) -> dict:
    # cursor_adapter.py or claude_adapter.py — outside core
    ...
```

Core only validates contract shape and logs result. **Adapter swap = zero core diff.**

---

## Integration point

`ulas.py` → `build_dispatch_envelope()` → `dispatch_provider()` → `invoke_provider()`

Single entry. Execution Engine never imports provider SDKs.
