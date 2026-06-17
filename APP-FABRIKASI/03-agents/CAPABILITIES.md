# Capability Definitions

## planner

- Venture charter (problem, market, monetization hypothesis)
- Phase plan (V0–V5)
- Scope boundaries — what is explicitly out
- **Output:** charter.md, phase checklist

## architect

- Platform adapter selection
- Module / package structure
- Data flow (offline-first default)
- **Output:** architecture blueprint, adapter link

## security

- Threat model (STRIDE-lite)
- Secrets policy, PII handling
- Dependency audit requirement
- **Output:** security checklist signed

## qa

- Test pyramid for adapter
- Release checklist
- Regression scope
- **Output:** test plan, release gate sign-off

## performance

- Performance budget (startup, frame time, API p95)
- Profiling plan pre-release
- **Output:** perf budget doc

## ux

- User job-to-be-done alignment
- Design system token usage
- Accessibility review
- **Output:** ux review notes

## auditor

- Validation gates pass/fail
- Cross-capability consistency
- No self-approval
- **Output:** audit report (pass / fail + blockers)
