> **Status:** experimental (not yet proven in production)

# Pattern: Local Database

## Intent

Structured local persistence with migrations and encryption.

## When to use

- Any app with non-trivial state (default for factory apps)

## Architecture checklist

- [ ] Room entities versioned; auto-migrations where safe
- [ ] SQLCipher for sensitive columns or full DB
- [ ] DAO only in data layer; domain sees repositories
- [ ] Type converters for enums / instant
- [ ] Test migrations on sample schemas

## Testing

- In-memory Room for unit tests
- Migration test harness in `core:data`

## Anti-patterns

- God DAO with 40 queries
- Breaking migration without fallback
- Raw SQLite in feature modules

## Factory links

- `governance/dependency-rules.json`
- `docs/02-ARCHITECTURE/DATA_FLOW.md`

## Evidence

*(migration incidents → knowledge/failures/)*
