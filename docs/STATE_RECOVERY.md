# State Recovery — Durum Kurtarma (v0.6.5)

Composer token truncation veya yarım Gradle/TOML edit sonrası fabrikayı kararlı duruma döndürür.

## Akış

```
[Composer / Gradle edit]
        │
        ▼
  --checkpoint (git stash veya dosya kopyası)
        │
        ▼
  gradle-build-loop.sh
        │
   ┌────┴────┐
   ▼         ▼
 PASS      FAIL (aynı hata ×2)
              │
              ▼
        --recover
              │
              ▼
   Etkilenen *.toml / *.gradle.kts / AndroidManifest geri yükle
              │
              ▼
   LATEST.recovery.handoff.json → Agent küçük batch yeniden yazar
```

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `./scripts/state-recovery.sh --checkpoint` | Build öncesi yedek |
| `./scripts/state-recovery.sh --recover` | Log analizi + selective rollback |
| `./scripts/state-recovery.sh --status` | Son checkpoint / handoff |

## Checkpoint yöntemleri

| Ortam | Yöntem |
|-------|--------|
| Git repo | HEAD commit'teki build dosyalarının kopyası |
| Git yok | Mevcut build dosyalarının kopyası |

Meta: `.cursor/snapshots/recovery/LATEST.checkpoint.json`

**Not:** Checkpoint çalışma kopyasını stash'lemez; yarım edit sonrası recover ile HEAD/kopya baseline'a döner.

## Recover tetikleyicileri

`LATEST.gradle.log` içinde (case-insensitive):

- `parse error`, `unclosed`, `unexpected end of file`
- `unresolved dependency`, `Could not parse`

## YAPILACAKLAR

Recover **aktif fazı değiştirmez**. Faz disiplini korunur; yalnızca build dosyaları rollback edilir.

## Ortam değişkenleri

| Değişken | Etki |
|----------|------|
| `RECOVERY_SKIP_CHECKPOINT=1` | gradle-build-loop checkpoint atlar |
| `RECOVERY_AUTO=1` | recover sonrası build loop otomatik tekrar |

## İlgili

- [`docs/CURSOR_TERMINAL_BRIDGE.md`](CURSOR_TERMINAL_BRIDGE.md)
- [`.cursor/rules/18-state-recovery.mdc`](../.cursor/rules/18-state-recovery.mdc)
