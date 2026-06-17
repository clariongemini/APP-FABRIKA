# Agent Model — Capabilities Not Departments

SVOS ajanları **yetenek tanımlarıdır**. Unvan, council veya departman hiyerarşisi yoktur.

## Yetenekler

| Capability | Sorumluluk | L1 (audit) |
|------------|------------|------------|
| **planner** | Charter, faz planı, scope | architect |
| **architect** | Modül haritası, data flow, adapter seçimi | auditor |
| **security** | Threat model, secrets, privacy | auditor |
| **qa** | Test plan, release checklist | auditor |
| **performance** | Budget, profiling plan | architect |
| **ux** | Flow, a11y, design system uyumu | planner |
| **auditor** | Gate validation, cross-cutting review | — (final) |

## Android Factory mapping (referans)

| SVOS Capability | Android Factory (frozen) |
|-----------------|--------------------------|
| planner | CPO + CDID planning |
| architect | Baş Mimar |
| security | Denetçi |
| qa | Denetçi + OEM |
| performance | Android Elite |
| ux | CPO + Design |
| auditor | CAO-lite audit chain |

Mapping **bilgi amaçlı** — SVOS yeni `.mdc` departmanı oluşturmaz.

## Invocation model

```
Venture phase → Required capabilities[] → Platform adapter context
```

Örnek V2 (MVP build): `architect` + `security` + `qa`  
Örnek V3 (release): `qa` + `auditor` + evidence gate

## Cursor entegrasyonu (gelecek)

`03-agents/capabilities/*.md` — her yetenek için kısa kural dosyası (Android Factory `.cursor/rules/` genişletmesi değil, SVOS-specific overlay).

Scaffold aşamasında: [`CAPABILITIES.md`](CAPABILITIES.md) yeterli.
