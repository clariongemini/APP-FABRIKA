# Claude-Native Akıl Yürütme (v2.1 stable)

**Sürüm:** v2.1.0-stable  
**Kural:** `.cursor/rules/19-claude-reasoning.mdc` (`alwaysApply: true`)

## Amaç

- Halüsinasyon ve rewrite loop riskini düşürmek
- **Negative constraints** ile katman/DI/mock tembelliğini engellemek
- Kelime cap (150–200/blok) ile output token bütçesini korumak
- CAO/CEO denetim zinciri ile uyumlu planlama

## Akış (v2.1)

```
YAPILACAKLAR oku
  → <thinking>
  → <architecture_check>
  → <negative_constraints>
  → departman ajanı
  → kod
  → gradle-build-loop
  → L1
```

## Kelime bütçesi

| Blok | Limit |
|------|--------|
| `<thinking>` | max 150–200 kelime |
| `<architecture_check>` | max 150–200 kelime |
| `<negative_constraints>` | max 150–200 kelime |

Over-thinking (aynı cümleyi tekrarlama) yasak.

## Negative constraints (özet)

1. Katman bypass / veri sızdırma yok  
2. Geçici mock veya hard-coded fixture bırakma yok  
3. Hilt `@Inject` atlama yok  

## Statik XML denetimi (v2.1)

`scripts/validate-reasoning-template-xml.sh` — şablon dosyalarında açılış/kapanış dengesi:

- `.cursor/rules/19-claude-reasoning.mdc`
- `.cursorrules`
- `docs/CLAUDE_REASONING.md`

Audit: `test/run-factory-audit.sh` → **V2.7**

## v2.2 (transcript parser)

`scripts/validate-reasoning-transcript.sh` — agent transcript / snapshot `.md` dosyalarındaki fenced `xml` bloklarında kapanmamış etiketleri yakalar. Audit: **V2.10** · CI: `validate.yml` smoke-build job.

## Şablon (kapatılmış etiketler zorunlu)

```xml
<thinking>
- Faz / görev kapsamı (kısa)
</thinking>

<architecture_check>
- Katman sınırları ve mapping (kısa)
</architecture_check>

<negative_constraints>
- Katman bypass yok; mock bırakma yok; DI atlama yok
</negative_constraints>
```

## Executive OS

Reasoning blokları **tek ajan onayı yerine geçmez**.  
Zincir: `governance/executive/HIERARCHICAL_AUDIT_CHAIN.md`
