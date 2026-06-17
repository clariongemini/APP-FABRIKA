# ULAS Consolidation Mode

**Effective:** 2026-06-17  
**Phase:** 3 — Measure, do not expand  
**Policy:** `instrument_not_expand`

---

## Objective

ULAS'ı iyileştirmek değil — **ULAS'ı ölçmek**.

> "Karar motoru çalışıyor sanıyoruz ama gerçekten çalışıp çalışmadığını ölçemiyoruz."

Bu riski kapat.

---

## Frozen

| Yasak |
|-------|
| Yeni motor |
| Yeni governance / agent / adapter |
| Yeni üst klasör |
| CL4R1T4S extraction (tamamlandı) |

---

## Allowed

| İzin |
|------|
| `ulas outcome` — karar sonucu kaydı |
| `ulas metrics` / `ulas report` — effectiveness |
| Venture ship + evidence (ulas-player) |

---

## Success criteria (6 ay soruları)

ULAS şunları cevaplayabilmeli:

1. LOW_CONFIDENCE kararlarının kaçı **doğru** çıktı? (precision)
2. Review chain sonrası failure rate düştü mü?
3. NEVER_AGAIN kaç tekrar hatayı **önledi**?
4. Tier escalation token israfını **azalttı** mı?

---

## CLI

```bash
./APP-FABRIKASI/scripts/ulas.sh report
./APP-FABRIKASI/scripts/ulas.sh metrics
./APP-FABRIKASI/scripts/ulas.sh outcome --decision-id ID --result correct_block
./APP-FABRIKASI/scripts/ulas.sh audit
```

→ [`scoring/EFFECTIVENESS.md`](scoring/EFFECTIVENESS.md) · [`AUDIT.md`](AUDIT.md)
