# Template: web-app

## Architecture blueprint

- Next.js App Router · TypeScript
- Token-driven Tailwind
- Ref: `02-platforms/web/ADAPTER.md`

## Launch checklist

- [ ] V0 charter
- [ ] Domain + SSL
- [ ] SEO meta baseline
- [ ] Cookie/consent if EU

## Analytics plan

- Privacy-friendly analytics (Plausible / PostHog self-host)
- Web vitals monitoring

## Testing plan

- Unit: lib + components
- E2E: Playwright critical paths
- a11y: axe in CI

## Release plan

- Preview deploy → production (Vercel or equivalent)
