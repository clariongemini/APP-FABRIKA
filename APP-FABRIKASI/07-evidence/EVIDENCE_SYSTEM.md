# Evidence System Blueprint

**En kritik katman.** Gelecek kararların yakıtı.

## Evidence türleri

| Tür | Kaynak | SVOS path |
|-----|--------|-----------|
| Analytics export | Firebase, Play Console, App Store Connect | `07-evidence/{venture}/analytics/` |
| Crash reports | Crashlytics, Sentry | `07-evidence/{venture}/crashes/` |
| Ratings & reviews | Store APIs / manual export | `07-evidence/{venture}/ratings/` |
| Revenue | Stripe, Play billing | `07-evidence/{venture}/revenue/` |
| Retention | Analytics cohorts | `07-evidence/{venture}/retention/` |
| User feedback | Surveys, support tickets | `07-evidence/{venture}/feedback/` |

## Manifest

Her venture evidence bundle:

```json
{
  "venture_slug": "",
  "period": "2026-Q2",
  "sources": ["play_console", "firebase"],
  "raw_path": "raw/ (gitignored)",
  "summary_path": "EVIDENCE.md"
}
```

## Privacy

- `raw/` **gitignore** — PII repo'ya girmez
- Summary dosyaları aggregate only

## Gate

V3 exit: minimum evidence bundle exists + outcome recorded in `08-ventures/`

## Android Factory referans

`../knowledge/evidence/` + `../scripts/knowledge/init-evidence-bundle.sh`
