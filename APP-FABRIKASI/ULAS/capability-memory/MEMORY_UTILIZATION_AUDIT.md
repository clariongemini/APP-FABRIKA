# Memory Utilization Audit

> **Taşınabilir şablon.** `MEMORY_UTILIZATION_REPORT.json` hedef projede `ulas memory utilization` ile üretilir.

> **Soru:** Knowledge üretimi > Knowledge kullanımı mı?  
> **Ölçüm:** Dispatch gerçekten doğru bilgiyi çekiyor ve geri besleme yapıyor mu?

## Döngü

```
Evidence → Memory → Dispatch (inject + rank)
                      ↓
              Memory Impact (success/failure)
                      ↓
              utilization counters + demote/promote
```

## Ne ölçülür

| Metrik | Anlam |
|--------|--------|
| `usage_count` | Entry kaç kez dispatch'e inject edildi |
| `success_count` | Verify/outcome başarısı sonrası +1 |
| `failure_count` | Verify fail veya tekrarlayan hata sonrası +1 |
| `last_used_at` | Son inject zamanı |
| `last_impact` | `success` \| `failure` |
| `injection_stats.utilization_rate` | Seçilen / aktif pool (tek dispatch) |
| `utilization_rate` (audit) | En az 1 kez kullanılan / aktif pool |

## Ölü bilgi tespiti

- `usage_count == 0` → **dead entry** (henüz hiç inject edilmedi)
- `failure_count > success_count` → güncelleme veya demote adayı
- Antipattern inject + verify fail → `injected_but_failed` regression signal

## Seçim (ranking)

`build_capability_context` artık ilk N değil **ranked selection** kullanır:

- proven status
- severity (antipattern)
- tag match (`task_hint` ile WP task metni)
- success/failure geçmişi
- kullanılmamış proven entry'lere küçük boost

## CLI

```bash
# Utilization raporu (tüm capability'ler)
ulas memory utilization

# Tek capability
ulas memory utilization --capability android.architecture --verbose

# Dispatch plan → utilization kaydı
ulas dispatch plan --decision-id DECISION_ID

# Execute sonrası memory impact (otomatik)
ulas execute run --decision-id DECISION_ID
```

## Runtime artefaktlar

| Dosya | İçerik |
|-------|--------|
| `10-runtime/capability-memory/utilization/{decision_id}.json` | Inject events |
| `10-runtime/capability-memory/utilization/impact-log.jsonl` | Success/failure impact |
| `10-runtime/capability-memory/MEMORY_UTILIZATION_REPORT.json` | Son audit özeti |

## Kabul kriteri

Sistem **evrimleşiyor** sayılır when:

1. `ulas memory utilization` dead oranı azalıyor (dispatch çalıştıkça)
2. Başarılı venture'larda `success_count` artıyor
3. Tekrarlayan hatalarda antipattern demote veya yeni entry oluşuyor
4. `injection_stats.utilization_rate` anlamlı (>0.1 küçük pool'larda)

## Bilinçli sınırlar (v1)

- Outcome/postmortem ingest henüz utilization'a bağlı değil
- Multi-venture karşılaştırması yok (P2)
- Token-budget aware selection yok — sabit tier limitleri (8/15/3)
