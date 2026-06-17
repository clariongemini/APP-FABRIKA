# Web Platform Adapter

**Durum:** Blueprint only

## Target stack

- Next.js (App Router)
- React · TypeScript
- Tailwind (token-driven, not utility soup)

## Design priorities

- Clarity over decoration
- Accessibility first (semantic HTML, focus, contrast)
- Maintainability over trend-chasing

## Anti-patterns (explicit)

- AI-generated gradient hero sections
- Glassmorphism abuse
- Dashboard syndrome without user job
- Animation without purpose

## Proposed structure

```
app/
components/
lib/
styles/tokens/
tests/
```

## Validation (future)

- `tsc --noEmit`
- ESLint + a11y plugin
- Playwright critical paths
- Lighthouse CI thresholds

## Template

→ [`../../05-templates/web-app/BLUEPRINT.md`](../../05-templates/web-app/BLUEPRINT.md)
