# Pazar Analizi — Android + Cursor Fabrika Segmenti

**Tarih:** 2026-06-14 · **Ajan:** CPO / Growth · **Fabrika:** v2.1.0-stable

## Segment tanımı

Cursor IDE üzerinde Android (Kotlin/Compose) geliştiren geliştiriciler; AI agent kuralları, scaffold ve governance arayanlar.

## Karşılaştırmalı rakip tablosu

| Rakip / alternatif | Odak | Fabrikadan fark |
|--------------------|------|-----------------|
| [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | `.mdc` kural koleksiyonu | Kurallar var; Executive OS, faz kapısı, Gradle şablon yok |
| [nowinandroid-agent-kit](https://github.com/warrenth/nowinandroid-agent-kit) | NIA tabanlı scaffold + agent harness | Tek mimari (NIA); 33 katman / CEO OS yok |
| [Mobile-App-Developer-Tools](https://github.com/TMHSDigital/Mobile-App-Developer-Tools) | Expo/RN MCP + skills | Android-native + fabrika governance değil |
| [android-studio-lite](https://github.com/krishna-kudari/android-studio-lite) | Cursor'da build/run köprüsü | DX eklentisi; ürün/governance katmanı yok |
| Hibrit AS + Cursor ([rehber](https://dredyson.com/complete-beginners-guide-using-cursor-ide-for-android-development-kotlin-java-and-kmp-setup-workflows-and-common-misconceptions/)) | Studio build + Cursor edit | Standartlaştırılmış fabrika paketi değil |

## Fırsat alanları

1. **AI Studio import hattı** — ham export → governance + i18n + denetim (lab kanıtlı)
2. **Ölçülebilir kalite** — `factory-quality-gate.sh`, 40+ audit, CI smoke build
3. **Claude-Native reasoning zırhı** — v2.1 üç blok + XML denetimi (v2.2 transcript)

## Riskler

| Risk | Azaltma |
|------|---------|
| MCP/PAT kurulum sürtünmesi | `verify-environment.sh` + `setup-mcp.sh` |
| JDK eksikliği yerelde | CI `assembleDebug` kanıtı |
| Kural/enforcement aşırı ağırlık | Faz kapısı + muafiyetler (`CLAUDE_REASONING.md`) |

## Kaynaklar

- PatrickJS/awesome-cursorrules — Cursor Project Rules (`.mdc`)
- warrenth/nowinandroid-agent-kit — Android agent harness (2026)
- TMHSDigital/Mobile-App-Developer-Tools v0.4.0 — MCP mobile tooling
- Fabrika iç kanıt: `test/AUDIT_REPORT.md`, `test/bootstrap-aistudio-lab.sh`
