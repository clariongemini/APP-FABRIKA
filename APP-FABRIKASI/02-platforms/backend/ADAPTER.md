# Backend Platform Adapter

**Durum:** Blueprint only

## Target

- API-first design
- Observable services (metrics, traces, structured logs)
- Security by default (auth, rate limit, input validation)
- Reliability (health checks, graceful degradation)

## Stack options (venture-dependent)

| Tier | Stack |
|------|-------|
| Serverless | Cloud Functions / Edge |
| Service | Node or Go microservice |
| Data | Postgres + Redis |

## Proposed concerns

```
api/          # HTTP layer
domain/       # Business logic
infra/        # DB, queue, cache
observability/
security/
```

## Validation (future)

- Contract tests (OpenAPI)
- Load test baseline
- Security scan in CI

## Template

→ [`../../05-templates/saas/BLUEPRINT.md`](../../05-templates/saas/BLUEPRINT.md)
