# Venture Management Blueprint

> **Taşınabilir şablon.** Örnek venture yok — `init-venture.sh` ile hedef projede oluşturulur.

## Venture birimi

SVOS'ta takip edilen birim **kod değil, girişimdir**.

## Venture kaydı şeması

```json
{
  "slug": "{{SLUG}}",
  "display_name": "{{NAME}}",
  "status": "charter | build | shipped | learning | archived",
  "platform": ["android"],
  "template": "android-app",
  "project_type": "{template}",
  "charter": {
    "problem": "",
    "solution": "",
    "market": "",
    "competition": [],
    "monetization": ""
  },
  "build": {
    "build_task": ":app:assembleDebug",
    "unit_test_task": ":app:testDebugUnitTest",
    "junit_results_variant": "testDebugUnitTest"
  },
  "results": {
    "launched_at": null,
    "users": null,
    "revenue": null,
    "rating": null
  },
  "evidence_ref": "07-evidence/{slug}/",
  "learning_refs": []
}
```

`build` bloğu varsayılan olarak `02-platforms/{platform}/bridge.defaults.json` dosyasından gelir; proje özel Gradle task'ları için `venture.json` içinde override edilir.

## Lifecycle

| Status | Meaning |
|--------|---------|
| charter | V0 — problem/market defined |
| build | V1–V2 |
| shipped | V3 — store live |
| learning | V4 — postmortem active |
| archived | No active investment |

## Dizin

```
08-ventures/
├── PURPOSE.md
├── VENTURE_MANAGEMENT.md
├── _template/venture.json
└── {slug}/venture.json
```

## Platform adapter

Venture codebase'i hedef projede yaşar; charter `08-ventures/{slug}/` altında SVOS meta olarak tutulur. Android için: `02-platforms/android/ADAPTER.md`.
