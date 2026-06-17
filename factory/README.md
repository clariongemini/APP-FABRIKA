# Factory — Öğrenen Katman (V3.1) + Portföy + Outcomes (V4)

**Governance karar verir. Factory öğrenir. Portfolio kaydeder. Outcomes kanıtlar.**

## Durum (2026-06-14)

| Aşama | Durum |
|-------|--------|
| Android Factory (scaffold, CI, standards) | ✅ Koru — asıl değer |
| Governance (16 ajan) | ✅ Yeterli — freeze |
| Intelligence (5 motor) | ✅ **FROZEN** — yeni engine yok |
| **Portfolio Registry** | ✅ Scaffold — gerçek app verisi bekliyor |
| **Outcomes** | ✅ Scaffold — Play Store verisi bekliyor |

## V4 yüzeyleri

```
.factory/context/      ← Context OS (oturum paketi)
knowledge/             ← pattern, ADR, failure, outcome (git)
factory/portfolio/     ← kayıt
factory/outcomes/      ← kullanıcı, retention, gelir, ROI
runtime/factory/       ← canlı veri (gitignore)
```

```bash
./scripts/factory/assemble-context.sh
python3 scripts/factory/intelligence-engine.py --last 10 --export
python3 scripts/factory/record-adr.py --title "..." --status accepted
python3 scripts/factory/promote-failure.py --id FAIL-2026-001
python3 scripts/factory/analyze-outcomes.py --top 5
python3 scripts/factory/register-app.py --name "My App" --package com.example.app --slug my-app
python3 scripts/factory/record-outcome.py --slug my-app --users 100 --mrr 200 --rating 4.5
python3 scripts/factory/build-portfolio-outcomes.py
python3 scripts/factory/build-factory-kpi.py
```

Detay: [`docs/KNOWLEDGE_OS.md`](../docs/KNOWLEDGE_OS.md)

## Dondurulmuş

Risk · Forecast · Strategy · Reflection Engine · V5 meta-layers · **yeni ajan/council**

**İzinli (Knowledge OS):** context, ADR lifecycle, patterns, failure/outcome intelligence — ajan eklemeden öğrenme katmanı.

Detay: [`docs/FACTORY_V4_PRODUCTIZATION.md`](../docs/FACTORY_V4_PRODUCTIZATION.md)
