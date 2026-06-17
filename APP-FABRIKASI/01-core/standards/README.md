# Platform-Agnostic Standards

SVOS çekirdek kalite standartları — tüm adaptörler bunları implement eder.

| Standart | Açıklama |
|----------|----------|
| **Security baseline** | Secrets yok, least privilege, dependency audit |
| **Privacy baseline** | PII minimization, consent, data retention |
| **Accessibility baseline** | WCAG-oriented (web), platform a11y API (mobile) |
| **Observability baseline** | Structured logging, crash reporting, key events |
| **i18n baseline** | No hard-coded user strings |
| **Offline-first default** | Mobile: local-first unless venture requires otherwise |
| **Test baseline** | Unit + critical path integration per adapter |
| **Release baseline** | Staged rollout, rollback plan, changelog |

Platform-specific detaylar → `02-platforms/{platform}/standards.md`
