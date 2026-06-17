# Outcome Intelligence

Portföy metrikleri + **fabrika verimliliği** sinyalleri.

## Metrikler

| Metrik | Flag |
|--------|------|
| Users | `--users` |
| Retention D7/D30 | `--retention-d7` / `--retention-d30` |
| MRR | `--mrr` |
| ROI | auto / `--roi` |
| Crash rate | `--crash-rate` |
| Store rating | `--rating` |
| Uninstall rate | `--uninstall-rate` |
| Refund rate | `--refund-rate` |
| Development days | `--development-days` |
| Development hours | `--development-hours` |
| Development cost | `--development-cost` |
| Maintenance cost (monthly) | `--maintenance-cost` |
| AI usage percent | `--ai-usage-pct` |
| Launch duration (days) | `--launch-duration-days` |
| Feature count | `--feature-count` |

## Intelligence dimensions

| Dimension | Flag | Engine query |
|-----------|------|--------------|
| Patterns | `--patterns offline_first,subscription_app` | retention-by-pattern |
| Onboarding | `--onboarding value-first` | uninstall-by-onboarding |
| Monetization | `--monetization subscription` | revenue-by-monetization |
| Architecture | `--architecture clean-10-module` | crash-by-architecture |

## Kayıt örneği

```bash
python3 scripts/factory/record-outcome.py \
  --slug my-app --released \
  --users 2400 --retention-d30 31 --mrr 890 \
  --crash-rate 0.015 --rating 4.5 --uninstall-rate 9.2 \
  --development-hours 280 --ai-usage-pct 72 \
  --launch-duration-days 45 --feature-count 12 \
  --patterns subscription_app,offline_first \
  --onboarding value-first --monetization subscription \
  --architecture clean-10-module
```

## Analiz

```bash
python3 scripts/factory/intelligence-engine.py --last 10 --export
python3 scripts/factory/analyze-outcomes.py --top 5
```

Snapshots: `knowledge/outcomes/snapshots/intelligence-*.json`
