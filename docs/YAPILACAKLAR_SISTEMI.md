# YAPILACAKLAR Sistemi — Bina Metaforu & Hiyerarşik İşleyiş

## Amaç

Geliştirici prompt verdiğinde ajan **doğrudan koda atlamaz**. Önce `YAPILACAKLAR.md` oluşturulur; temelden (F0) anahtar teslime (F8) kadar faz faz ilerlenir. Halüsinasyon protokolü her oturumda otomatik — `.cursor/rules/00-overmind-zero-hallucination.mdc`.

## Metafor

| Faz | Bina | İçerik |
|-----|------|--------|
| F0 | Zemin & temel | MCP, governance, hafıza |
| F1 | Kolon | CPO vizyon, pazar |
| F2 | Kat döşeme | Mimari |
| F3 | Duvar & tesisat | Android iskelet |
| F4 | Cephe | UI / Compose |
| F5 | Elektrik & güvenlik | Denetim, OEM |
| F6 | Sayaçlar | Analytics / AID |
| F7 | İç mekan | Feature WP'ler |
| F8 | Anahtar teslim | CAO + CEO + gate |

## Durum ibareleri

- **bekliyor** — henüz başlanmadı
- **işleniyor** — aktif (aynı anda tek faz)
- **tamamlandı** — L1 doğrulandı

## Cursor entegrasyonu

| Bileşen | Dosya |
|---------|-------|
| Kural (always) | `.cursor/rules/00-overmind-zero-hallucination.mdc` |
| Reasoning (v2.1) | `.cursor/rules/19-claude-reasoning.mdc` — rehber: `docs/CLAUDE_REASONING.md` |
| `/baslat` | `.cursor/commands/baslat.md` |
| `/devam-et` | `.cursor/commands/devam-et.md` |
| `/denetle` | `.cursor/commands/denetle.md` |
| `/faz-durumu` | `.cursor/commands/faz-durumu.md` |
| Subagent L1 | `.cursor/agents/phase-verifier.md` |
| Plan genişletme | `.cursor/agents/plan-expander.md` |
| CAO vekili | `.cursor/agents/phase-auditor.md` |

## Keşif protokolü

Uygulama sırasında eksik tespit → `[EK-YYYYMMDD]` ile plana ekle (`plan-expander` veya `yapilacaklar-executor` skill). Atlama yasak.

## Bootstrap

```bash
./scripts/init-new-app.sh "MyApp" "com.company.app"
# veya
bash scripts/governance/init-yapilacaklar.sh "ürün açıklaması"
python3 scripts/governance/validate-yapilacaklar.py
```

## İlk prompt

Cursor chat:

```
/baslat

[Uygulama adı ve kısa açıklama — örn. offline-first alışkanlık takipçisi, 7 gün trial]
```

Sonra `/devam-et` ile F0 maddeleri sırayla tamamlanır.
