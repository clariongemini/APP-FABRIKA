# Claude-Native Akıl Yürütme (v2)

**Sürüm:** v2.0.0-reasoning-alpha  
**Kural:** `.cursor/rules/19-claude-reasoning.mdc` (`alwaysApply: true`)

## Amaç

- Halüsinasyon ve rewrite loop riskini düşürmek
- Token bütçesini korumak (muafiyet kuralları)
- CAO/CEO denetim zinciri ile uyumlu, kanıtlanabilir planlama

## Akış

```
YAPILACAKLAR oku → [zorunluysa] <thinking> + <architecture_check> → departman ajanı → kod → gradle-build-loop → L1
```

## Zorunlu tetikleyiciler

| Durum | Blok |
|-------|------|
| Faz `işleniyor` + kod görevi | Evet |
| Gradle / Manifest / Room / Network core | Evet |
| Modüller arası taşıma | Evet |
| quality-gate / build-loop debug | Evet |
| Doc typo, `/faz-durumu` | Hayır |

## İlgili dosyalar

| Dosya | Rol |
|-------|-----|
| `.cursorrules` | Overmind anayasası — protokol özeti |
| `00-overmind-zero-hallucination.mdc` | Faz + build kanıtı |
| `18-state-recovery.mdc` | Truncation recovery |
| `docs/CURSOR_CONTEXT_BUDGET.md` | layer-NN.yaml dilimleri |
| `test/run-factory-audit.sh` | V2.* statik regex denetimi |

## Executive OS

Reasoning blokları **tek ajan onayı yerine geçmez**. Hiyerarşik zincir: `governance/executive/HIERARCHICAL_AUDIT_CHAIN.md`.
