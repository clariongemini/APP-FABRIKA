# Factory Freeze — Build Less, Ship More

**North star:** [`FACTORY_MISSION.md`](../FACTORY_MISSION.md)

| Alan | Değer |
|------|-------|
| **Status** | FROZEN |
| **Maturity** | PRODUCTION READY |
| **Mode** | MAINTENANCE |
| **Next objective** | Validate through products |

Fabrika geliştirmesi **3 production release + outcome validation** olana kadar meta-genişleme donduruldu.

## MAINTENANCE modunda izin verilen

- Bug fix
- Dokümantasyon
- `sync-standards.sh` iyileştirmeleri
- Hedef projede gerçek app verisi (`record-outcome`, portfolio)

## MAINTENANCE modunda yasak

- V5 / V6
- Yeni ajan · council · katman · intelligence motoru · governance sistemi

## Kural (`.factory/freeze.json`)

```json
{
  "until_apps_released": 3,
  "required_apps": [],
  "frozen": {
    "new_agents": true,
    "new_councils": true,
    "new_layers": true,
    "new_intelligence_motors": true
  }
}
```

App slug'ları fabrika şablonunda tanımlı değildir — yalnızca hedef projede `runtime/factory/portfolio/apps.json` içinde.

## Evrim

| Sürüm | Anlam |
|-------|--------|
| V1 | Android Template |
| V2 | Android Factory |
| V3 | Android Factory OS |
| V4 | Android Product Portfolio OS |

## 96 → 99 GitHub'da değil

| Gerekli | Nerede |
|---------|--------|
| Production release + kullanıcı + gelir | Play Store |
| Outcome validation | `runtime/factory/outcomes/` |

## V4 izin verilen yüzeyler (scaffold only)

1. **Portfolio** — register + release + KPI  
2. **Outcomes** — users, retention, MRR, ROI  
3. **Certification** — `certify-app.py`  
4. **Regression DB** — `scan-regression.py`  
5. **ROI Dashboard** — `build-factory-kpi.py`

Yeni ajan · yeni council · yeni katman → **YASAK** (`python3 scripts/factory/check-freeze.py`)

Detay: [`FACTORY_V4_PRODUCTIZATION.md`](FACTORY_V4_PRODUCTIZATION.md)
