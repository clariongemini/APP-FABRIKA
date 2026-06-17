# Postmortems

Failure log ≠ postmortem. Postmortem **proje hikayesidir**.

| Failure | Postmortem |
|---------|------------|
| Teknik olay | Beklenti vs gerçeklik |
| `FAIL-*` kaydı | Ne öğrendik, tekrar olsa ne yapardık |
| `promote-failure.py` | `record-postmortem.py` |

## Kayıt

```bash
python3 scripts/factory/record-postmortem.py \
  --project "Offline Music App v1" \
  --expected "Stable offline playback from day one" \
  --actual "Metadata pipeline blocked release 6 weeks" \
  --why "External parser dependency without adapter layer" \
  --retry "Own metadata model first; import as secondary" \
  --result failed \
  --patterns media_app,offline_first
```

Şablon: [`TEMPLATE.md`](TEMPLATE.md)

## Intelligence

Postmortem sayısı `intelligence-engine.py` portföy raporunda görünür.
