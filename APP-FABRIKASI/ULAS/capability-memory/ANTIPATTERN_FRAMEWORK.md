# AntiPattern Framework

What a capability must **never** repeat.

> **Şablon.** Örnek JSON yapısıdır; repoda önceden doldurulmuş antipattern yoktur.

---

## Entry shape

```json
{
  "id": "android.architecture.001",
  "title": "Boundary violation in app module",
  "status": "experimental",
  "severity": "high",
  "body": "Implementation leaked into wrong module layer — fix per platform adapter.",
  "evidence_count": 1,
  "tags": ["architecture", "module_boundary"],
  "regression_watch": true,
  "source": {
    "type": "evidence",
    "venture_slug": "{slug}",
    "ref": "07-evidence/{slug}/manifest.json"
  }
}
```

---

## Severity

| Level | When |
|-------|------|
| critical | Data loss, security, ship blocker |
| high | Architecture test fail, boundary violation |
| medium | Recurring test flake with known fix |
| low | Style / minor debt |

---

## Lifecycle

```
observed → experimental (evidence_count=1)
        → proven (evidence_count≥2 OR 1 venture + verification pass after fix)
        → deprecated (platform no longer applies)
```

**Regression:** proven → experimental when tag matches verification fail.

---

## vs Knowledge

| AntiPattern | Knowledge pattern |
|-------------|-----------------|
| "Don't do X" | "Do Y" |
| severity + evidence_count | confidence + evidence_refs |
| Always in dispatch tier1 if proven | Tier2 if space |

Never store the same lesson in both — link via `tags` if needed.

---

## First ingest

After `ulas memory ingest --from evidence --venture {slug}`, antipatterns are **experimental** until promotion rules pass. No pre-seeded entries in the template repo.
