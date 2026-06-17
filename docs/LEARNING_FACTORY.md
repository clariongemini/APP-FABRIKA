# Learning Factory — V2

**V1:** Factory-centric (governance, scaffold, gates)  
**V2:** Knowledge-centric (context, ADR, patterns, failures, outcomes)  
**V2.1:** Intelligence-centric (Knowledge → Insight → Decision)

Yeni ajan yok. Yeni council yok. **Motor: `intelligence-engine.py`**

## V2.1 Intelligence-centric (Knowledge → Insight)

Yeni ajan yok. Motor: `intelligence-engine.py`

## V3 Evidence (gerçeklik — sıradaki değer)

**Pattern = teori · Evidence = gerçeklik**

```bash
./scripts/factory/init-evidence-bundle.sh --slug my-app-v1 --portfolio-slug my-app
```

Detay: [`docs/V3_EVIDENCE.md`](V3_EVIDENCE.md) · `knowledge/evidence/`

> 90+ skorun kalan puanı doküman değil — shipped app export'ları ile gelir.

## Pipeline

```
Ship app → record outcome / venture / postmortem
                ↓
        intelligence-engine.py
                ↓
    Insight (retention-by-pattern, revenue-by-monetization, …)
                ↓
    Human / AI decision → record-adr.py → next app
```

## Factory Intelligence Engine

```bash
# Tam analiz (son 10 uygulama)
python3 scripts/factory/intelligence-engine.py --last 10 --export

# Tek soru
python3 scripts/factory/intelligence-engine.py --ask retention-by-pattern --last 10
python3 scripts/factory/intelligence-engine.py --ask uninstall-by-onboarding
python3 scripts/factory/intelligence-engine.py --ask revenue-by-monetization
python3 scripts/factory/intelligence-engine.py --ask crash-by-architecture
python3 scripts/factory/intelligence-engine.py --ask feature-count-vs-rating
```

## Kayıt araçları

| Araç | Ne? |
|------|-----|
| `record-outcome.py` | MRR, retention, crash, rating, dev hours, AI %, feature count, … |
| `record-venture.py` | Problem / solution / market scores |
| `record-postmortem.py` | Proje hikayesi |
| `promote-pattern.py` | experimental → proven |
| `promote-failure.py` | runtime → knowledge/failures |

## Pattern tiers

- `knowledge/patterns/proven/` — kanıtlı
- `knowledge/patterns/experimental/` — teori / fabrika standardı

## Mimar skoru (hedef)

| Alan | Skor |
|------|------|
| Governance | 95 |
| Architecture | 90 |
| Knowledge | 90 |
| Learning | 80 |
| Intelligence | **82** (motor hazır; veri bekliyor) |
| **Evidence** | **20** (scaffold; gerçek export yok) |
| Productization | 88 |
| **Toplam** | **~89** (90+ = gerçek app evidence) |

> 90 üstü dokümanla değil — **shipped app + outcome + postmortem** ile gelir.

## North star shift

| Eski framing | Yeni framing |
|--------------|--------------|
| Android Product Factory | Software Venture Factory |
| Build apps | Build + learn from ventures |

Detay: [`KNOWLEDGE_OS.md`](KNOWLEDGE_OS.md) · [`FACTORY_MISSION.md`](../FACTORY_MISSION.md)
