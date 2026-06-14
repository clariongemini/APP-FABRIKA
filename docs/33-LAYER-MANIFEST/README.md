# 33 Katman — On-Demand Dilimler

Cursor context budget için **tam manifest okunmaz**. Yalnızca ilgili katman dilimini oku:

| Ajan | Dilimler |
|------|----------|
| CPO | `layer-00` … `02`, `25`, `26`, `30` |
| Android | `layer-03` … `06`, `22` |
| Architect | `layer-07` … `15`, `20`, `23`, `24`, `27` … `29` |
| Auditor | `layer-16` … `19`, `21`, `31`, `32` |

Üretim: `python3 scripts/split-layer-manifest.py`  
Kaynak doğruluk: `docs/33-LAYER-MANIFEST.yaml`  
Rehber: `docs/CURSOR_CONTEXT_BUDGET.md`
