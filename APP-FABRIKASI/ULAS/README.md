# ULAS — Decision Intelligence Layer

> **ULAS is not a vendor archive. ULAS is institutional memory and decision engineering.**

| Meta | Değer |
|------|-------|
| **Tam ad** | Unified Learning & Accountability System |
| **Rol** | APP-FABRIKASI karar zekâsı katmanı |
| **Kaynak** | Industry pattern extraction — **prompt text yasak** |
| **Entegrasyon** | 01-core, 06-learning, 07-evidence, 09-portfolio üzerine oturur |

---

## Mission

APP-FABRIKASI'yı:

- **Aldatmaya daha dirençli**
- **Hataları tekrarlamaya daha dirençsiz**
- **Token açısından daha verimli**
- **Kararlarda daha tutarlı ve güvenilir**

hale getirmek.

---

## CL4R1T4S'tan ne alındı, ne alınmadı

| Alındı (prensip) | Alınmadı |
|------------------|----------|
| Context completeness before action | Prompt metni |
| Plan / act phase separation | Vendor personality |
| Tool proportionality & cost awareness | Leaked system prompts |
| Read-before-edit discipline | CL4R1T4S klasör kopyası |
| Multi-step review before ship | Yeni CEO / council |
| Institutional memory under context limits | `research/external-patterns/` |

Prensip haritası: [`SOURCE_PRINCIPLES.md`](SOURCE_PRINCIPLES.md)

---

## Dizin haritası

| # | Modül | Soru |
|---|-------|------|
| 01 | [context-engineering](01-context-engineering/) | Bağlam tam mı? |
| 02 | [decision-reliability](02-decision-reliability/) | Güven skoru yeterli mi? |
| 03 | [review-chains](03-review-chains/) | Kim onayladı? |
| 04 | [accountability](04-accountability/) | Onay kalitesi öğreniliyor mu? |
| 05 | [institutional-memory](05-institutional-memory/) | Bu hata daha önce oldu mu? |
| 06 | [token-economy](06-token-economy/) | Risk bağlamla orantılı mı? |
| 07 | [knowledge-compression](07-knowledge-compression/) | Özet yeterli mi? |
| 08 | [pattern-extraction](08-pattern-extraction/) | Outcome pattern oldu mu? |
| 09 | [decision-audit](09-decision-audit/) | Geçmiş karar izlenebilir mi? |
| 10 | [operating-principles](10-operating-principles/) | Kalıcı ilkeler |

---

## Master çıktılar

| # | Belge |
|---|-------|
| 1 | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| 2 | [`INTEGRATION.md`](INTEGRATION.md) |
| 3 | [`03-review-chains/REVIEW_CHAIN_SYSTEM.md`](03-review-chains/REVIEW_CHAIN_SYSTEM.md) |
| 4 | [`04-accountability/ACCOUNTABILITY_FRAMEWORK.md`](04-accountability/ACCOUNTABILITY_FRAMEWORK.md) |
| 5 | [`05-institutional-memory/NEVER_AGAIN_REGISTRY.md`](05-institutional-memory/NEVER_AGAIN_REGISTRY.md) |
| 6 | [`06-token-economy/TOKEN_ECONOMY.md`](06-token-economy/TOKEN_ECONOMY.md) |
| 7 | [`07-knowledge-compression/COMPRESSION_FRAMEWORK.md`](07-knowledge-compression/COMPRESSION_FRAMEWORK.md) |
| 8 | [`09-decision-audit/DECISION_AUDIT.md`](09-decision-audit/DECISION_AUDIT.md) |
| 9 | [`RISK_ANALYSIS.md`](RISK_ANALYSIS.md) |
| 10 | [`READINESS.md`](READINESS.md) |

---

## Intelligence zinciri (ULAS ile)

```
Context (01) → Confidence (02) → Review (03) → Decision → Execution
                    ↑                    │
              Evidence (07)         Accountability (04)
                    │                    │
              Memory (05) ← Compression (07) ← Audit (09)
                    │
              Pattern (08) → Learning (06) → Portfolio (09)
```

ULAS **governance'i replace etmez** — karar kalitesi katmanıdır.
