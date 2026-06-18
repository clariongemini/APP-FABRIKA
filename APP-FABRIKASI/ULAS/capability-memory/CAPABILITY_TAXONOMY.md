# Capability Taxonomy

Stable IDs across ventures, providers, and platforms.

---

## ID format

```
{platform}.{domain}
```

Examples: `android.architecture` · `web.frontend` · `ai.reasoning`

Sub-entry IDs:

| Layer | Format | Example |
|-------|--------|---------|
| Knowledge | `cap-k-NNN` | cap-k-012 |
| AntiPattern | `{capability_id}.NNN` | android.architecture.001 |
| Playbook | `{capability_id}.pb-NNN` | android.performance.pb-003 |
| Benchmark | `{capability_id}.bm-NNN` | android.architecture.bm-001 |

---

## Platform tree

```
android
  ├── architecture    implementation · module boundaries
  ├── testing         verification · gradle tests
  ├── performance     budgets · profiling
  ├── security        threats · secrets
  └── ux              design · a11y

web
  ├── architecture
  ├── frontend
  ├── performance
  └── design

ios
  ├── architecture
  ├── performance
  └── design

backend
  ├── architecture
  ├── api
  └── security

ai
  ├── research
  ├── reasoning
  └── verification
```

---

## execution_class (cross-cutting)

| Class | Typical layers |
|-------|----------------|
| planning | knowledge, playbooks |
| implementation | knowledge, antipatterns, playbooks |
| verification | knowledge, antipatterns, benchmarks |
| review | knowledge, antipatterns |
| gate | antipatterns, benchmarks |

---

## project_type (benchmarks)

`project_type` = venture `template` alanı (`05-templates/` ile aynı):

| project_type | Template |
|--------------|----------|
| android-app | `05-templates/android-app/` |
| ios-app | `05-templates/ios-app/` |
| web-app | `05-templates/web-app/` |
| saas | `05-templates/saas/` |
| ai-product | `05-templates/ai-product/` |

Benchmarks compare within `project_type`, not across unrelated apps.

---

## Mapping from work package

```
work_package.role + platform → marketplace.role_platform_map → capability_id
```

Dispatch and memory always use **capability_id**, never role name alone.
