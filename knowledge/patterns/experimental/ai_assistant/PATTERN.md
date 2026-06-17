> **Status:** experimental (not yet proven in production)

# Pattern: AI Assistant

## Intent

User-facing AI with clear latency, privacy, and cost boundaries.

## When to use

- In-app copilot, tutoring, generation features

## Architecture checklist

- [ ] Abstraction: `AiGateway` interface (on-device vs cloud)
- [ ] Prompt templates in assets/locales — not hard-coded
- [ ] Rate limit + timeout + fallback copy (i18n)
- [ ] PII scrubbing before cloud call
- [ ] On-device path: model size, NNAPI/GPU delegate decision documented

## Security

- API keys never in APK — remote config or backend proxy
- `docs/03-STANDARDS/SECURITY.md`

## Anti-patterns

- Sending full user database as context
- Blocking main thread on inference
- No cancellation on navigation away

## Future

- Wear / XR: shorter context windows — separate ADR when needed

## Evidence

*(cost per MAU, latency p95, slug)*
