# Gap Analysis & Production Readiness — SVOS Template

> **Taşınabilir şablon.** Repoda örnek venture yok. Skorlar hedef projede `ulas maturity audit` ile ölçülür.

**Tarih:** 2026-06-14  
**Kapsam:** APP-FABRIKASI scaffold vs production Venture OS (her projede ayrı validate)

---

## Özet skor

| Alan | Skor | Durum |
|------|------|-------|
| Architecture & structure | **92** | Scaffold complete |
| Governance design | **88** | Lightweight, no bloat |
| Android adapter | **95** | Operational (factory frozen) |
| iOS / Web / Backend / AI adapters | **25** | Blueprint only |
| Design system | **70** | Tokens + principles |
| Learning system | **75** | Schema + templates |
| Evidence system | **40** | Schema only, no ventures |
| Venture management | **50** | Schema only |
| Portfolio intelligence | **15** | Future — by design |
| Runtime / context assembly | **35** | Schema only |
| **Composite readiness** | **58** | **Scaffold — not production OS** |

> **58/100 = doğru.** Production OS ancak ilk venture + evidence sonrası 75+ olur.

---

## Güçlü yönler

1. **Clear WHAT/HOW separation** — Core vs adapters
2. **Android Factory preserved** — CI green, frozen policy intact
3. **No governance inflation** — 7 capabilities vs 16 departments
4. **Evidence-first philosophy** — Portfolio gated on data
5. **Migration path documented** — Monorepo → venture → extraction

---

## Gap'ler (öncelik sırası)

### P0 — Ship blocker (venture başlayınca)

| Gap | Çözüm |
|-----|-------|
| No venture charter | `init-venture.sh` → `08-ventures/{slug}/` |
| No evidence data | `07-evidence` bundle post-release |
| iOS/Web/Backend no CI | Adapter impl when venture selects platform |

### P1 — Post-first-ship

| Gap | Çözüm |
|-----|-------|
| No `assemble-svos-context.sh` | Script in `APP-FABRIKASI/scripts/` |
| Learning not migrated from `knowledge/` | Copy-on-venture |
| Portfolio allocation inactive | ≥2 outcomes required |

### P2 — Scale (3+ ventures)

| Gap | Çözüm |
|-----|-------|
| Monorepo size | Venture repo isolation |
| SVOS extraction | Faz 3 migration |
| Cross-platform design token sync | Platform mappers |

---

## Android Factory gap (unchanged)

| Alan | Skor |
|------|------|
| Governance | 95 |
| Architecture | 92 |
| Learning | 84 |
| Intelligence | 82 |
| Evidence | 20 |

Android Factory **complete for its role**. SVOS does not fix Android evidence — **ventures do**.

---

## Production readiness definition

SVOS is **production-ready** when:

- [ ] ≥1 venture `shipped` with evidence bundle
- [ ] ≥1 outcome recorded
- [ ] ≥1 postmortem
- [ ] Intelligence insight generated from real data
- [ ] Android adapter CI green (regression)
- [ ] No new executive departments added

---

## Recommendation

**STABILIZATION MODE active** — see [`STABILIZATION.md`](STABILIZATION.md).

**Do not expand scaffold.** Hedef projede: `init-venture.sh` → ship → evidence → learning loop.

```bash
./APP-FABRIKASI/scripts/init-venture.sh "Proje Adı" {slug} path/to/codebase/
./APP-FABRIKASI/scripts/bridge-venture.sh {slug}
```

Next score jump: **58 → 75** comes from first real venture lifecycle, not new folders.
