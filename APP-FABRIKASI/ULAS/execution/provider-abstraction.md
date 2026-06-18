# Provider Abstraction

Providers execute capabilities. Capabilities do not belong to providers.

---

## Architecture rule

```
Work Package.capability  →  Provider Registry  →  Backend
```

**Wrong:** "Cursor is the architect."  
**Right:** "architect capability → provider=cursor (or claude, or human)."

---

## Routing (canonical)

Bindings live in [`../routing/routing-policy.json`](../routing/routing-policy.json):

```json
{
  "android.architecture": "cursor",
  "android.testing": "local_shell",
  "android.qa": "local_shell"
}
```

Swap Cursor → Claude: change **one policy line**. Work chain, manifests, verification unchanged.

Runtime override: `10-runtime/ulas/routing/policy-overrides.json`

---

## Provider registry

See [`../routing/provider-registry.json`](../routing/provider-registry.json)

---

## Provider interface (conceptual)

```json
{
  "provider_id": "local_shell",
  "invoke": {
    "cwd": "path/to/codebase/",
    "cmd": "./gradlew :app:testDebugUnitTest",
    "timeout_sec": 600
  },
  "result": {
    "exit_code": 0,
    "stdout_ref": "10-runtime/ulas/execution/logs/...",
    "success": true
  }
}
```

AI providers (future) same shape — different `invoke` payload:

```json
{
  "provider_id": "cursor",
  "invoke": {
    "capability": "architect",
    "context_refs": ["work_package_wp-2", "07-evidence/..."],
    "instruction": "implement fixes per acceptance criteria"
  }
}
```

---

## Why provider-last matters

In 2 years:

- Cursor, Claude Code, Gemini CLI, Codex, Devin may all change
- **android architect** capability does not

APP-FABRIKA center = capability graph + execution loop.  
Providers = replaceable plugins.

---

## P3 — Capability Router (operational)

Router produces `routing_manifest` on work chain. Execution Engine consumes it.

Wiring `cursor` / `claude` **dispatch** (API calls) is future; routing and policy swap work today.
