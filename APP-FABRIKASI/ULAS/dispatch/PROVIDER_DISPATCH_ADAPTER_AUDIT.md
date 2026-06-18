# Provider Dispatch Adapter Audit

> **Taşınabilir şablon.** `PROVIDER_DISPATCH_ADAPTER_AUDIT.json` ortam durumuna göre `ulas dispatch audit` ile güncellenir.

> **Darboğaz #1:** Execution OS'in önündeki son fiziksel engel — contract var, adapter yok.

## Mevcut durum

| Katman | Durum |
|--------|--------|
| Capability Router | ✅ `routing-policy.json` swap |
| Dispatch contract | ✅ `provider-contract.schema.json` |
| Envelope builder | ✅ `build_dispatch_envelope` + `capability_context` inject |
| `local_shell` | ✅ Gradle/script invoke |
| `human` | ✅ Manual queue |
| `ai_ide` / `ai_api` | ❌ **Not wired** — skipped at execute |

## Audit komutu

```bash
ulas dispatch audit
ulas dispatch audit --verbose
```

Çıktı: `ULAS/dispatch/PROVIDER_DISPATCH_ADAPTER_AUDIT.json`

## Adapter gereksinimleri (minimal)

Thin adapter her provider için:

1. `10-runtime/ulas/dispatch/{decision_id}.json` oku
2. `status: pending` envelope seç
3. `invoke.schema` tipine göre:
   - `ai_invoke` → IDE/API çağrısı
   - `shell_invoke` → mevcut `invoke_provider`
   - `manual_invoke` → human queue
4. Sonucu envelope `result` + `status` olarak yaz
5. Execute loop verify'e devam

## Swap testi (Capability → Provider)

```json
// routing-policy.json — tek satır değişiklik
"android.architect": "cursor_ide"
```

Kod değişmeden provider değişmeli. Adapter olmadan bu test **başarısız**.

## Blocker özeti

```
providers_wired: 2 (local_shell, human)
providers_unwired: N (cursor, claude, gemini, …)
ai_dispatch_ready: false
```

## Sonraki adım (P1)

1. `ulas dispatch execute --decision-id ID` — pending envelope'ları işle
2. `cursor_ide` adapter: envelope → Cursor task (manual bridge bile yeterli v0)
3. Execute run'da `skipped` yerine `dispatched` → verify

## İlişki: Memory Utilization

Adapter çalışmadan dispatch utilization **sadece plan aşamasında** kayıt alır.  
Gerçek ROI ölçümü: adapter + execute pass + `record_memory_impact` üçlüsü.
