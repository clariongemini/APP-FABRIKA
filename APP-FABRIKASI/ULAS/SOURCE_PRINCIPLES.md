# CL4R1T4S → ULAS Principle Extraction

> **Bu dosya prompt içermez.** Yalnızca gözlemlenen **düşünce sistemleri** ve ULAS modül eşlemesi.

Kaynak: [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) — şeffaflık arşivi. Analiz tarihi: 2026-06-14.

---

## Extraction metodu

Soru: *"CL4R1T4S hangi prompt'u kullanıyor?"* → **YASAK**

Soru: *"CL4R1T4S'taki sistemler neden etkili?"* → **İZİNLİ**

---

## Prensip haritası

| Gözlemlenen sistem (vendor-agnostik) | Kaynak kategorileri | ULAS modülü |
|--------------------------------------|---------------------|-------------|
| **Complete context gate** — karar öncesi dosya/kanıt okuma; partial view → READ_MORE | Cursor tools, Factory DROID | `01-context-engineering` |
| **Speculation ban** — açılmamış kod hakkında iddia yok | Factory DROID | `01-context-engineering` |
| **Plan / Act separation** — plan onaysız implementasyon yok | Cline, Devin | `01-context-engineering` + `03-review-chains` |
| **Confidence before close** — emin değilsen daha fazla bilgi topla | Cursor, Devin | `02-decision-reliability` |
| **Environment / setup gate** — kod öncesi ortam doğrulama | Factory DROID | `03-review-chains` |
| **Pre-commit review** — diff review before ship | Factory DROID | `03-review-chains` |
| **Tool proportionality** — gereksiz tool çağrısı pahalı | Windsurf, Cursor | `06-token-economy` |
| **Targeted vs full read** — büyük dosyada partial-first | Cursor tools | `06-token-economy` |
| **Memory under window limits** — kritik bağlamı persist et | Windsurf memory | `05-institutional-memory` |
| **Linter loop cap** — 3 deneme sonra dur | Cursor | `02-decision-reliability` |
| **Root cause over symptom** | Cursor debug | `08-pattern-extraction` |
| **Safety gate for destructive ops** | Cline, Windsurf | `03-review-chains` |
| **Step confirmation** — tool sonucu doğrulanmadan devam yok | Cline | `04-accountability` |
| **Task handoff with compressed context** | Cline new_task | `07-knowledge-compression` |

---

## Bilinçli olarak alınmayanlar

| Gözlem | Neden reddedildi |
|--------|------------------|
| Persona / tone enforcement | Venture OS değil, chat UX |
| Prompt disclosure games | Güvenlik ve odak kaybı |
| Vendor-specific tool schemas | APP-FABRIKA kendi toolchain'i |
| Political / refusal framing | Governance değil, model policy |
| Jailbreak / leak amplification | Anayasa ihlali |

---

## ULAS kalıcılık kuralı

CL4R1T4S güncellenirse → **prensip haritası** gözden geçirilir.  
Prompt dosyası repoya **asla** eklenmez.
