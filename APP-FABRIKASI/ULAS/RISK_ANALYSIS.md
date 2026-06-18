# ULAS Risk Analysis

## Risk register

| Risk | Olasılık | Etki | Mitigation |
|------|----------|------|------------|
| **Scaffold > venture** | Yüksek | Yüksek | STABILIZATION + ULAS principles #5 |
| **ULAS becomes prompt archive** | Orta | Kritik | SOURCE_PRINCIPLES: prompt yasak |
| **Review chain bureaucracy** | Orta | Orta | min=2, capability not department |
| **Confidence gaming** | Orta | Yüksek | Evidence-weighted model |
| **NEVER_AGAIN false blocks** | Düşük | Orta | Founder + auditor override |
| **Token tier under-load** | Orta | Orta | Ship events force T3 |
| **Duplicate governance** | Orta | Yüksek | ULAS integrates, not replaces |
| **CL4R1T4S drift** | Düşük | Düşük | Principle map review quarterly |

## En büyük risk (Mimar tespiti)

> Scaffold üretme hızı, venture üretme hızını geçer.

**Kontrol:** Success = first venture 7-step lifecycle, not new ULAS folders.

## Security

- Decision audit raw snapshots → gitignore
- NEVER_AGAIN entries → no secrets
- No external prompt paste vectors

## Failure modes

| Mode | Signal | Response |
|------|--------|----------|
| Analysis paralysis | No ship in 30d | Force V2 with T2 context only |
| Empty NEVER_AGAIN | No learning | Require postmortem after ship |
| Low confidence ships | Audit gap | Block ship gate |
