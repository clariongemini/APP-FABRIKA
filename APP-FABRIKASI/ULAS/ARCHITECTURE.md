# ULAS Architecture

```mermaid
flowchart TB
    subgraph ULAS["ULAS Decision Layer"]
        CE[01 Context Engineering]
        DR[02 Decision Reliability]
        RC[03 Review Chains]
        AC[04 Accountability]
        IM[05 Institutional Memory]
        TE[06 Token Economy]
        KC[07 Knowledge Compression]
        PE[08 Pattern Extraction]
        DA[09 Decision Audit]
        OP[10 Operating Principles]
    end

    subgraph SVOS["APP-FABRIKASI Core"]
        GOV[01-core governance]
        LRN[06-learning]
        EVI[07-evidence]
        PRT[09-portfolio]
        VEN[08-ventures]
    end

    CE --> DR
    DR --> RC
    RC --> AC
    IM --> DR
    EVI --> DR
    LRN --> PE
    PE --> IM
    DA --> AC
    TE --> CE
    KC --> CE
    OP --> CE
    RC --> GOV
    AC --> LRN
    DA --> EVI
    DR --> PRT
    VEN --> CE
```

## Katman pozisyonu

ULAS, SVOS'un **01–10** katmanlarının **üzerinde** çalışan çapraz karar katmanıdır:

- `01-core/governance` → **ne** onaylanır (kurallar)
- `ULAS` → **nasıl** güvenilir onaylanır (disiplin)

## Veri akışı

1. Venture talebi → `01-context-engineering` manifest assemble
2. `READ_MORE_REQUIRED` yoksa → `02-decision-reliability` confidence
3. Confidence ≥ threshold → `03-review-chains` matrix
4. Onay → execution; ret → gap log
5. Sonuç → `09-decision-audit` + `04-accountability`
6. Failure → `05-institutional-memory` NEVER_AGAIN candidate
7. Outcome → `08-pattern-extraction` → `06-learning`

## Dosya türleri

| Tür | Örnek |
|-----|-------|
| Standard | `STANDARDS.md`, `*_FRAMEWORK.md` |
| Schema | `*.schema.json` |
| Registry | `never-again.json`, `review-matrix.json` |
| State | `10-runtime/ulas/` (venture-specific, gitignored raw) |
