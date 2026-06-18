# Capability Marketplace

Canonical catalog of capabilities across platforms. **Not** a workforce roster.

Source of truth: [`capability-marketplace.json`](capability-marketplace.json)

Router reads marketplace for IDs, metadata, default providers. Policy overrides in `routing/routing-policy.json`.

---

## Structure per capability

| Field | Purpose |
|-------|---------|
| `label` | Human name ("Android Architecture") |
| `platform` | android · web · ios · backend · ai |
| `role` | Legacy work-package role mapping |
| `execution_class` | planning · implementation · verification · gate · review |
| `verification_requirements` | What must pass before done |
| `evidence_requirements` | What proof must exist |
| `default_provider` | Suggested binding (overridable in policy) |

---

## Catalog (v1)

### Android
`android.architecture` · `android.testing` · `android.performance` · `android.security` · `android.ux` · `android.qa` · `android.planning`

### Web
`web.architecture` · `web.frontend` · `web.performance` · `web.design`

### iOS
`ios.architecture` · `ios.performance` · `ios.design`

### Backend
`backend.architecture` · `backend.api` · `backend.security`

### AI
`ai.research` · `ai.reasoning` · `ai.verification`

### Generic fallbacks
`generic.planning` · `generic.architecture` · `generic.qa` · `generic.audit`

---

## Usage

```bash
ulas capability route --decision-id ID   # resolves via marketplace + policy
ulas capability policy                 # effective bindings
```

Adding a capability = one JSON entry. No new agent, phase, or council.

---

## Relationship to router

```
Work Package (role + platform)
    → marketplace.role_platform_map
    → capability_id
    → routing-policy.json (override default_provider)
    → dispatch contract
```

`capability-registry.json` remains a thin alias; marketplace is canonical.
