# Pattern Library

**Kod değil — bilgi.** İki seviye: teori vs kanıt.

## Proven vs Experimental

| Tier | Path | Anlam |
|------|------|-------|
| **Proven** | `patterns/proven/` | Gerçek projede işe yaradı — `promote-pattern.py` |
| **Experimental** | `patterns/experimental/` | Fabrika standardı / henüz kanıtlanmadı |

AI önce **proven** okur; experimental yalnızca proven yoksa veya keşif fazındaysa.

## Experimental patterns

| Pattern | Ne zaman? |
|---------|-----------|
| [`offline_first/`](experimental/offline_first/PATTERN.md) | V1 offline |
| [`subscription_app/`](experimental/subscription_app/PATTERN.md) | Trial + Billing |
| [`media_app/`](experimental/media_app/PATTERN.md) | Playback, cache |
| [`chat_app/`](experimental/chat_app/PATTERN.md) | Messaging |
| [`ai_assistant/`](experimental/ai_assistant/PATTERN.md) | LLM features |
| [`local_database/`](experimental/local_database/PATTERN.md) | Room + SQLCipher |

## Promote to proven

```bash
python3 scripts/factory/promote-pattern.py \
  --name offline_first \
  --slug my-app \
  --evidence "D30 retention 34%, MRR $420"
```

## Intelligence

```bash
python3 scripts/factory/intelligence-engine.py --ask retention-by-pattern --last 10
```
