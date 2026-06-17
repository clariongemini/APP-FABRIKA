# Venture Management Blueprint

## Venture birimi

SVOS'ta takip edilen birim **kod değil, girişimdir**.

## Venture kaydı şeması

```json
{
  "slug": "offline-media-player",
  "name": "Offline Media Player",
  "status": "charter | build | shipped | learning | archived",
  "platform": ["android"],
  "template": "android-app",
  "charter": {
    "problem": "",
    "solution": "",
    "market": "",
    "competition": [],
    "monetization": ""
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
├── README.md
├── VENTURE_MANAGEMENT.md
├── _template/venture.json
└── {slug}/venture.json
```

## Android Factory

Venture repo'su `init-new-app.sh` ile oluşturulur; charter `08-ventures/{slug}/` altında SVOS meta olarak yaşar.
