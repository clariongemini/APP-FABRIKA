# Cross-Platform Capability Matrix

Which capabilities are **shared** vs **platform-specific**.

Canonical IDs: [`marketplace/capability-marketplace.json`](marketplace/capability-marketplace.json)

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ● | Platform-native capability ID |
| ○ | Uses generic fallback |
| — | Not applicable |

---

## Matrix

| Capability domain | Android | iOS | Web | Backend | AI |
|-------------------|---------|-----|-----|---------|-----|
| **Planning** | android.planning | generic.planning | generic.planning | generic.planning | ai.research |
| **Architecture** | android.architecture | ios.architecture | web.architecture | backend.architecture | ai.reasoning |
| **Implementation UI** | android.ux | ios.design | web.frontend | — | — |
| **Design review** | android.ux | ios.design | web.design | — | — |
| **Testing** | android.testing | generic.qa | generic.qa | backend.api | ai.verification |
| **Performance** | android.performance | ios.performance | web.performance | — | — |
| **Security** | android.security | ○ | ○ | backend.security | — |
| **QA gate** | android.qa | generic.audit | generic.audit | generic.audit | ai.verification |

---

## Shared execution classes

All platforms share these **classes** (not IDs):

| execution_class | Meaning |
|-----------------|---------|
| planning | Scope, charter |
| implementation | Code / structure |
| verification | Automated tests |
| review | Human or AI review |
| gate | Evidence closure |

---

## Shared verification pattern

```
build_success → tests_pass → evidence_manifest → outcome
```

Platform adapters swap **how** (gradle / xcodebuild / vitest), not **what**.

---

## Router implication

Work package `role` + `platform` → marketplace map → capability_id.

Same role name (`architect`) → different capability_id per platform. Provider policy is per capability_id.

---

## Expansion rule

New platform = new `{platform}.*` entries in marketplace. Never fork ULAS or Execution Engine.
