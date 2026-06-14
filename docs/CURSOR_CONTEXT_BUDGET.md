# Cursor Context Budget — Ne Zaman Ne Okunur?

Cursor Agent'ın context penceresi sınırlıdır. Fabrika **minimum kanıt, maksimum odak** ilkesiyle çalışır.

## Altın kurallar

1. **Tam `33-LAYER-MANIFEST.yaml` okuma yasak** — yalnızca `docs/33-LAYER-MANIFEST/layer-NN.yaml` dilimleri.
2. **YAPILACAKLAR.md her oturum başında** — aktif faz + `Aktif ajanlar` satırı.
3. **MCP çıktısı sohbete değil dosyaya** — `.cursor/snapshots/mcp/LATEST.handoff.json`.
4. **Build kanıtı log dosyasından** — `.cursor/snapshots/build/LATEST.gradle.log`.
5. **v2 reasoning (zorunlu tetikleyicide)** — `<thinking>` + `<architecture_check>` aç; muafiyetlerde açma. Rehber: `docs/CLAUDE_REASONING.md`.

## Oturum başlangıcı (her zaman)

| Dosya | Neden |
|-------|--------|
| `YAPILACAKLAR.md` | Aktif faz, görevler, aktif ajanlar |
| `docs/00-INDEX.md` | Proje hafızası özeti |

## Faz bazlı okuma

| Faz | Okunacak | Okunmayacak |
|-----|----------|-------------|
| F0 | `docs/EXECUTIVE_OS.md`, `docs/MCP_SETUP.md` | Android kaynak, manifest dilimleri |
| F1 | `docs/01-VISION/*`, `governance/market/*`, manifest `layer-00`–`02` | `templates/android/**` |
| F2 | `docs/02-ARCHITECTURE/*`, manifest `layer-07`–`15` | Compose UI kodu |
| F3–F4 | manifest `layer-03`–`06`, `22`, ilgili `.kt` | Tüm governance JSON |
| F5 | `docs/03-STANDARDS/SECURITY.md`, OEM, manifest `layer-16`–`19` | Vizyon belgeleri |
| F6 | `governance/analytics/*`, manifest `layer-18`–`19` | MODULE_MAP yeniden yazımı |
| F7 | `APPROVAL_QUEUE.md`, roadmap JSON, aktif WP | Yeni mimari kararları |
| F8 | CAO/CEO script çıktıları, `CHANGELOG.md` | Yeni feature kodu |

Aktif ajan listesi: `governance/phase-agents.json` → `YAPILACAKLAR.md` `Aktif ajanlar` satırı (otomatik senkron).

## Manifest dilimleri

```
docs/33-LAYER-MANIFEST/layer-03.yaml   # yalnızca KATMAN 3
```

Üretim: `python3 scripts/split-layer-manifest.py`

## @ mention önerisi (Cursor chat)

```
@YAPILACAKLAR.md @docs/00-INDEX.md
```

Kod fazında ek:

```
@docs/33-LAYER-MANIFEST/layer-03.yaml @docs/03-STANDARDS/LIQUID_GLASS.md
```

Build hatasında:

```
@.cursor/snapshots/build/LATEST.gradle.log
```

## Token tasarrufu

| Yerine | Kullan |
|--------|--------|
| Tüm `governance/` ağacı | İlgili departman charter + runtime JSON |
| Tüm README | İlgili `docs/` alt belgesi |
| 33 katman ARCHITECTURE tamamı | İlgili KATMAN N bölümü + layer dilimi |
| Uzun chat geçmişi | `/devam-et` + YAPILACAKLAR tazeleme |

## İlgili

- `docs/CURSOR_TERMINAL_BRIDGE.md` — Gradle/Maestro köprüsü
- `.cursor/snapshots/README.md` — MCP handoff
- `governance/phase-agents.json` — faz → ajan eşlemesi
