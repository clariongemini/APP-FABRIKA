# ULAS Production Readiness

> **Taşınabilir şablon.** Aşağıdaki skorlar iskelet durumunu tanımlar; venture kanıtı hedef projede oluşur.

## Özet

| Alan | Skor | Durum |
|------|------|-------|
| Architecture & schemas | **85** | Tanımlı |
| Review chain system | **80** | Matrix + schema |
| Accountability framework | **75** | Schema only |
| Institutional memory | **70** | Empty registry (correct) |
| Token economy | **80** | Tier rules defined |
| Knowledge compression | **75** | Templates ready |
| Pattern extraction | **70** | Workflow defined |
| Decision audit | **75** | Schema ready |
| **Operational validation** | **25** | Engine hazır; henüz karar yok |
| **Effectiveness proof** | **10** | Outcome yok — ilk venture sonrası ölçülür |
| **Composite** | **78** | Decision OS instrumented; venture proof pending |

> Karar katmanı iskeleti hazır; **venture kanıtı hedef projede** kapanır.

---

## Production-ready tanımı (hedef projede)

ULAS production-ready when **in the deployed project**:

- [ ] `{slug}` charter passed review chain (≥2)
- [ ] ≥1 decision audit record with real outcome
- [ ] ≥0 NEVER_AGAIN or proven pattern from real postmortem
- [ ] Context tier logged per major decision
- [ ] Zero prompt text in repo audit

```bash
./APP-FABRIKASI/scripts/init-venture.sh "Proje Adı" {slug} path/to/codebase/
./APP-FABRIKASI/scripts/ulas.sh decide --venture {slug} --class D --title "Charter" --reviewers architect,qa
```

---

## Next step

**Validate ULAS through first venture in target project** — not expand ULAS.

```
charter review → build → ship audit → evidence → postmortem → pattern/NEVER_AGAIN
```

Expected composite after first loop: **75–78**.
