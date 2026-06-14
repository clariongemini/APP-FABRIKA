# Cursor Terminal Bridge — Build & Test Feedback

Cursor IDE **Android derleyicisi veya emülatör barındırmaz**. Fabrika bu boşluğu terminal script'leri ile kapatır.

## Gradle build loop

```bash
./scripts/gradle-build-loop.sh
GRADLE_TASK=lintDebug ./scripts/gradle-build-loop.sh
GRADLE_LOOP_MAX_RETRIES=5 ./scripts/gradle-build-loop.sh
./scripts/gradle-build-loop.sh --strict   # fabrika dışı projede zorunlu mod
```

| Çıktı | Konum |
|-------|--------|
| Tam log | `.cursor/snapshots/build/gradle-*-.log` |
| Son build | `.cursor/snapshots/build/LATEST.gradle.log` |

**Cursor Agent protokolü:**

1. Kotlin/Gradle değişikliği yap
2. `./scripts/gradle-build-loop.sh` çalıştır
3. FAIL → `LATEST.gradle.log` oku → düzelt → tekrar (max 3)
4. PASS olmadan YAPILACAKLAR F3+ satırını `tamamlandı` yapma

## Maestro E2E

```bash
./scripts/run-maestro.sh
MAESTRO_FLOW=.maestro/flows/smoke.yaml ./scripts/run-maestro.sh
```

Gereksinim: `maestro` CLI, `adb`, cihaz/emülatör.

## MCP handoff

MCP çıktıları → `.cursor/snapshots/mcp/` — bkz. [`.cursor/snapshots/README.md`](../.cursor/snapshots/README.md)

## Gradle edit sırası (Composer)

1. `gradle/libs.versions.toml`
2. `**/build.gradle.kts`
3. `settings.gradle.kts` (gerekirse)
4. `AndroidManifest.xml`
5. `.kt` kaynak dosyaları

Bu sıra ihlal edilirse import/sync kırılması riski yüksektir.
