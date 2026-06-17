> **Status:** experimental (not yet proven in production)

# Pattern: Offline First

## Intent

Uygulama ağ olmadan tam değer sunar; sync ikincil.

## When to use

- Utility, productivity, education, field apps
- V1 launch before API exists

## Architecture checklist

- [ ] Room (or SQLCipher) single source of truth locally
- [ ] Repository: `Flow` from local; remote optional
- [ ] Outbox queue for writes; retry with backoff
- [ ] Conflict policy documented (LWW vs merge)
- [ ] UI never blocks on network for read path

## Data layer

- `core:data` — DAO, entities, migrations
- `domain` — use cases unaware of sync transport
- `data:sync` (V2) — WorkManager, delta sync

## Anti-patterns

- Remote-first with local cache pretending to be offline
- GlobalScope sync jobs
- Silent data loss on conflict

## Factory standards

- `docs/33-LAYER-ARCHITECTURE.md` Katman 9
- `docs/03-STANDARDS/BACKGROUND_PROCESSING.md`

## Evidence

*(Add after shipped apps: slug, metric, link to ADR/failure)*
