# Runtime System — Context Assembly & Retrieval

> **Taşınabilir şablon.** `context/`, `evidence/`, utilization ve maturity çıktıları hedef projede oluşur — çoğu `.gitignore` ile commit edilmez.

OS'un "ne öğrendiğini bilmesi" için runtime katmanı.

## Sorumluluklar

| Fonksiyon | Açıklama |
|-----------|----------|
| Context assembly | Venture + adapter + learning özetini birleştir |
| Decision retrieval | İlgili ADR'leri getir |
| Pattern retrieval | Proven + venture-relevant experimental |
| Evidence lookup | Summary metrics (raw değil) |
| Venture lookup | Active venture state |

## Assembly pipeline

```
1. Load venture.json (08-ventures)
2. Load platform adapter standards (02-platforms)
3. Load proven patterns (06-learning)
4. Load evidence summary if exists (07-evidence)
5. Load portfolio context if N≥2 (09-portfolio)
6. Write CONTEXT_MANIFEST.json → 10-runtime/context/
```

## Dizin

```
10-runtime/
├── README.md
├── context/              # {slug}/ manifests (gitignore — per venture)
├── evidence/             # {slug}/ bridge copies (gitignore)
├── capability-memory/      # utilization + quality reports (gitignore)
├── maturity-report.json  # svos-health output (gitignore)
├── ulas/                 # decisions, work, execution (gitignore JSON)
└── .gitignore
```

## Üretilen raporlar (hedef projede)

| Rapor | Komut |
|-------|--------|
| Maturity | `./APP-FABRIKASI/scripts/svos-health.sh` |
| Memory quality | `ulas memory quality-report` |
| Memory utilization | `ulas memory utilization` |
| Dispatch audit | `ulas dispatch audit` |
| Feedback closure | `ulas feedback-audit` |

## Android Factory referans

`../.factory/context/` + `assemble-context.sh` — pattern model, SVOS genişletmesi.

## Scaffold

Manifest şeması: [`context-manifest.schema.json`](context-manifest.schema.json)

Script: post-scaffold (`assemble-svos-context.sh` — future)
