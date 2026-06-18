# ULAS Integration Plan

ULAS mevcut SVOS katmanlarını **replace etmez** — onları güçlendirir.

---

## Entegrasyon matrisi

| SVOS katmanı | ULAS modülü | Entegrasyon |
|--------------|-------------|-------------|
| `01-core/governance` | 03-review-chains | Validation gates → review matrix |
| `01-core/intelligence` | 02-decision-reliability | Confidence model feeds insight |
| `01-core/knowledge` | 07-knowledge-compression | ADR/postmortem özetleri |
| `03-agents` | 03-review-chains | 7 capability → review edges |
| `06-learning` | 05, 08 | NEVER_AGAIN + pattern extraction |
| `07-evidence` | 02, 09 | Confidence input + audit outcome |
| `08-ventures` | 01, 09 | Charter context + decision log |
| `09-portfolio` | 02, 04 | Allocation only after confidence history |
| `10-runtime` | 01, 06 | Context manifest + token tier |

---

## Mevcut APP-FABRIKA dosyaları (dokunulmaz)

| Dosya | ULAS ilişkisi |
|-------|---------------|
| `.cursor/rules/20-agent-intent-gate.mdc` | → 01 plan/act separation (already aligned) |
| `docs/CURSOR_CONTEXT_BUDGET.md` | → 06 token economy (reference) |
| `APP-FABRIKASI/STABILIZATION.md` | ULAS authorized; no adapter expansion |
| Android Factory `governance/` | Geçiş referans; duplicate yok |

---

## Runtime path (gelecek)

```
APP-FABRIKASI/10-runtime/ulas/
├── context-manifests/
├── decision-log/
├── reviewer-stats/
└── never-again-index.json
```

Scaffold: şema tanımlı; script `ulas-assemble-context.sh` — **first venture ship sonrası**.

---

## İlk venture (`{slug}`) ULAS checklist

- [ ] Context manifest assembled (Tier 2)
- [ ] Charter confidence scored
- [ ] Review chain: planner → architect → security → qa
- [ ] Ship decision audited
- [ ] Post-release: outcome → audit closure

---

## Yasak entegrasyonlar

- CL4R1T4S klasörü repoya kopyalamak
- `research/external-patterns/cl4r1tas` gibi kaynak adlı dizin
- Yeni executive `.mdc` dosyaları
- Prompt arşivi
