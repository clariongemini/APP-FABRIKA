# ULAS Operating Principles

Kalıcı karar mühendisliği ilkeleri — prompt değil, **düşünce sistemi**.

1. **Context before action** — READ_MORE_REQUIRED bitmeden finalize yok.

2. **Evidence before confidence** — Kanıt olmadan yüksek confidence yok.

3. **Multiple reviews before approval** — `minimum_review_count >= 2`.

4. **Memory before repetition** — NEVER_AGAIN scan zorunlu.

5. **Learning before scaling** — İkinci venture, birincinin evidence'si olmadan büyümez.

6. **Compression before expansion** — Özet oku; full doc istisna.

7. **Proportionality before depth** — Token tier risk ile eşleşir.

8. **Audit before amnesia** — Major decision → decision audit record.

9. **Patterns before doctrine** — Proven yalnızca evidence ile.

10. **Founder before automation** — Portfolio allocation hint ≠ emir.

---

## Anti-principles (reddedilen)

- Prompt collection as knowledge
- Single-reviewer ship
- Full-repo context every task
- Confidence without evidence
- Governance expansion as progress

---

## Daily check (venture work)

```
[ ] Context tier selected?
[ ] NEVER_AGAIN scanned?
[ ] Confidence computed?
[ ] Review chain satisfied?
[ ] Audit record queued?
```
