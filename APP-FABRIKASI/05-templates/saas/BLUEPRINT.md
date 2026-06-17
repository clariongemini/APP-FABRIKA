# Template: saas

## Architecture blueprint

- Web frontend (`05-templates/web-app`)
- Backend API (`02-platforms/backend`)
- Auth + billing (Stripe)

## Launch checklist

- [ ] V0 charter + B2B/B2C clarity
- [ ] API contract (OpenAPI)
- [ ] Stripe products/prices
- [ ] Terms + privacy

## Analytics plan

- Product: activation, retention, MRR events
- Ops: API latency, error rate

## Testing plan

- Contract tests
- Auth flow E2E
- Load test baseline

## Release plan

- Staging → canary API → full rollout
