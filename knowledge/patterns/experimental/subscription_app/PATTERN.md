> **Status:** experimental (not yet proven in production)

# Pattern: Subscription App

## Intent

7-day trial → paid subscription; Play Billing as source of truth.

## When to use

- Consumer apps with recurring revenue
- Feature gating by entitlement

## Architecture checklist

- [ ] BillingClient wrapper in `core:monetization`
- [ ] Entitlement state in encrypted prefs + server verify (V2)
- [ ] Trial start = billing connection + offer token
- [ ] Grace period and account hold handling
- [ ] Restore purchases on reinstall

## Monetization layer

- `docs/03-STANDARDS/MONETIZATION_TECH.md`
- AID events: trial_start, conversion, churn_signal

## UX rules

- Paywall after value demonstration, not first screen
- Clear trial end date (i18n)
- No dark patterns (Auditor P0)

## Anti-patterns

- Custom payment outside Play (policy violation)
- Hard-coded SKU strings in Composables

## Evidence

*(Post-ship: conversion %, MRR, slug)*
