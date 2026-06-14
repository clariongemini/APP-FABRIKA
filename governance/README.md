# Executive Operating System (CEO V7)

Portable governance layer for **any** Android project bootstrapped from the Factory.

| Alan | Değer |
|------|-------|
| Fabrika sürümü | **v2.1.0-stable** |
| Claude-Native reasoning | v2.1 — `docs/CLAUDE_REASONING.md`, kural `19-claude-reasoning.mdc` |
| Önceki reasoning sürümü | v2.0.0-reasoning-alpha (CHANGELOG geçmişi) |
| Executive OS | 7.0 |

## Purpose

Enforce the chain:

**Decision → Delivery → Measurement → Learning**

Not reports. Not charters alone. **User-visible product.**

## Bootstrap

After `init-new-app.sh`:

```bash
./scripts/init-governance.sh
```

Or automatically — `init-new-app.sh` calls it.

When syncing into an existing project:

```bash
./scripts/sync-standards.sh /path/to/project
cd /path/to/project && ./scripts/init-governance.sh
```

## Repo vs runtime (what lives where)

| Artifact | In Factory Git repo | Per-project (init / runtime) |
|----------|----------------------|------------------------------|
| Charters, README, protocols | ✅ `governance/**/DEPARTMENT_CHARTER.md` | Synced, then edited per project |
| Executive MD (CEO OS, audit chain) | ✅ `governance/executive/*.md` | Synced |
| Governance templates | ✅ `templates/governance/` | Copied by `init-governance.sh` |
| `SPRINT_LOCK.json` | ❌ gitignored | Generated per project |
| `APPROVAL_QUEUE.md` | ❌ gitignored | Generated per project |
| `roadmap_priorities.json` | ❌ gitignored | Generated per project |
| `project.config.json` | ❌ gitignored | Generated per project |
| Analytics output | ❌ gitignored | Device/Firebase kanıtı sonrası |
| `YAPILACAKLAR.md` | Template only | `init-yapilacaklar.sh` |

## Canonical sources (priority order)

1. `governance/executive/CEO_OPERATING_SYSTEM.md`
2. `governance/product_decision/roadmap_priorities.json`
3. `governance/reality/PRODUCT_REALITY_SCORE.json`
4. `governance/executive/SPRINT_LOCK.json`
5. `governance/executive/APPROVAL_QUEUE.md`

## Structure

| Path | Owner | Role |
|------|-------|------|
| `executive/` | CEO | Sprint lock, approval queue, operating system |
| `product_decision/` | PDC | Roadmap, rejected features |
| `reality/` | CEO V7 | Product reality score, no-new-P0 rule |
| `execution/` | CEC | Alignment, PDC consumption |
| `analytics/` | AID | Sprint P activation, event catalog |
| `cao/` | CAO | Audit scoreboard |
| `cdid/` | CDID | Work package engine |
| `egc/` | EGC | Company health, verdict |
| `csgb/` | CSGB | CEO performance review |
| `market/` | Growth | Demand intelligence, VOC, finans |
| `linguistic/` | LIUD | Locale intelligence |
| `curriculum/` | CIKA | Curriculum intelligence |
| `blue_ocean/` | Mavi Okyanus | Portfolio discovery |
| `trends/` | Trends | Search term discovery |

## Scripts (canonical paths)

```bash
./scripts/init-governance.sh              # Executive OS bootstrap
./scripts/run-ceo-cycle.sh                # CEO cycle
./scripts/agent-approval-gate.sh          # WP double-approval gate
python3 scripts/cao/run_cao_audit.py      # CAO audit
python3 scripts/execution/run_cec_audit.py
python3 scripts/reality/run_product_reality_layer.py
python3 scripts/governance/validate-audit-chain.py
python3 scripts/governance/validate-yapilacaklar.py
```

## Project config

`governance/project.config.json` — filled by init with app name, package, factory version.

Sprint lock slots P0–P4 are **project-specific** — edit after PDC first decisions.
