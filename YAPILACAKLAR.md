# YAPILACAKLAR — Factory

> **Bina metaforu:** Zemin → taşıyıcı → katlar → tesisat → cephe → iç mekan → anahtar teslim  
> **Halüsinasyon sıfır:** Her madde dosya/kanıt referansı içerir; uydurma yasak.  
> **Protokol:** `.cursor/rules/00-overmind-zero-hallucination.mdc`

| Alan | Değer |
|------|-------|
| Proje | Factory |
| Package | `com.ulas.factory` |
| Yazar | [Ulaş Kaşıkcı](docs/AUTHOR.md) |
| Fabrika sürümü | v2.1.0-stable |
| Oluşturulma | 2026-06-14 |
| Aktif faz | **F1 — Kolon & Taşıyıcı** |
| Aktif ajanlar | `01-product-cpo`, `09-product-decision-council`, `17-marketing-growth`, `10-mavi-okyanus` · manifest: `layer-00.yaml`, `layer-01.yaml`, `layer-02.yaml`, `layer-25.yaml`, `layer-26.yaml`, `layer-30.yaml` |
| Kaynak prompt | Fabrika kalite kapısı — Executive OS + 33 katman + Gradle wrapper + governance policy |

---

## F0 — Zemin & Temel (Governance + MCP + Hafıza) · `tamamlandı`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F0.1 | `./scripts/first-setup.sh` + `./scripts/setup-mcp.sh` | MCP | Baş Mimar | P0 MCP yeşil | tamamlandı |
| F0.2 | `./scripts/governance/init-governance.sh` | CEO | CAO | sprint lock + approval queue | tamamlandı |
| F0.3 | `docs/00-INDEX.md` proje adıyla uyumlu | Overmind | CEO | INDEX güncel | tamamlandı |
| F0.4 | `YAPILACAKLAR.md` kaynak prompt dolduruldu | Overmind | CEO | prompt satırı dolu | tamamlandı |
| F0.5 | Hiyerarşik zincir doğrulama: `python3 scripts/governance/validate-audit-chain.py` | CAO | CEO | exit 0 | tamamlandı |

**F0 çıkış kapısı:** Tüm satırlar `tamamlandı` → F1 `işleniyor`

---

## F1 — Kolon & Taşıyıcı (Vizyon + Pazar + Monetizasyon) · `işleniyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F1.1 | `docs/01-VISION/PRODUCT_BRIEF.md` doldur | CPO | PDC | brief onaylı | bekliyor |
| F1.2 | `docs/01-VISION/MARKET_ANALYSIS.md` — rakip kanıtı (web/MCP) | CPO | PDC | kaynaklı analiz | bekliyor |
| F1.3 | `docs/01-VISION/MONETIZATION.md` | CPO | PDC | model tanımlı | bekliyor |
| F1.4 | PDC roadmap taslak: `governance/product_decision/roadmap_priorities.json` | PDC | CAO | P0 net | bekliyor |

**F1 çıkış kapısı:** CPO + PDC L1 onayı

---

## F2 — Kat Döşeme (Mimari & Modül Haritası) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F2.1 | `docs/02-ARCHITECTURE/MODULE_MAP.md` | Baş Mimar | CEC | modül listesi | bekliyor |
| F2.2 | `docs/02-ARCHITECTURE/DATA_FLOW.md` | Baş Mimar | CEC | akış diyagramı | bekliyor |
| F2.3 | `governance/dependency-rules.json` package uyumu | Baş Mimar | Denetçi | com.ulas.factory | bekliyor |
| F2.4 | ArchUnit / mimari script (varsa) | Denetçi | CAO | ihlal yok | bekliyor |

---

## F3 — Duvar & Tesisat (Android İskelet) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F3.1 | Gradle 10 modül iskeleti doğrula | Android Elite | Baş Mimar | build ok | bekliyor |
| F3.2 | Hilt + Room + Navigation iskelet | Android Elite | Baş Mimar | derleme | bekliyor |
| F3.3 | i18n `assets/locales/tr.json`, `en.json` boş şablon | Android Elite | CPO | hard-coded yok | bekliyor |

---

## F4 — Cephe & UI (Compose + Liquid Glass) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F4.1 | Design system / tema (standartlara uygun) | Android Elite | CPO | 33 katman UI | bekliyor |
| F4.2 | Ana ekran iskeleti (MVP loop) | Android Elite | Baş Mimar | Compose preview | bekliyor |
| F4.3 | Tablet/adaptive layout kontrol | Android Elite | CPO | responsive | bekliyor |

---

## F5 — Elektrik & Güvenlik (Denetim + OEM) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F5.1 | `./scripts/factory-health.sh` | Denetçi | CAO | skor raporu | bekliyor |
| F5.2 | Güvenlik checklist (`docs/03-STANDARDS/SECURITY.md`) | Denetçi | Baş Mimar | bulgu kapalı | bekliyor |
| F5.3 | OEM matris taraması (hedef cihaz varsa) | OEM Denetçi | Denetçi | matris | bekliyor |

---

## F6 — Ölçüm & Analitik (AID Sprint P) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F6.1 | `SPRINT_P_EVENT_CATALOG.json` proje olayları | AID | CAO | minimum_events | bekliyor |
| F6.2 | Analytics pipeline + session tracker | AID | CAO | kod mevcut | bekliyor |
| F6.3 | Cihaz kanıtı / gate ACTIVE | AID | CEO | gate json ACTIVE | bekliyor |

---

## F7 — İç Mekan & İnce İşçilik (Feature WP'ler) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F7.1 | `governance/executive/APPROVAL_QUEUE.md` WP'ler sırayla | CDID | CEC | L1+L2 onay | bekliyor |
| F7.2 | Roadmap P0 feature implementasyonu | Android Elite | CEC | reality score ↑ | bekliyor |

*Geliştirici promptundan türeyen ek WP'ler buraya `[EK-YYYYMMDD]` ile eklenir.*

## [EK-20260614] v2 Claude-Native Akıl Yürütme · `tamamlandı`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| EK.1 | `.cursor/rules/19-claude-reasoning.mdc` (`alwaysApply`) | Overmind | CAO | thinking + architecture_check şablonu | tamamlandı |
| EK.2 | `.cursorrules` + `docs/CLAUDE_REASONING.md` | Overmind | CEO | v2 protokol özeti | tamamlandı |
| EK.3 | `19-aistudio` → `20-aistudio-import.mdc` (numara ayrımı) | Overmind | CAO | referans güncel | tamamlandı |
| EK.4 | `test/run-factory-audit.sh` V2.1–V2.6 statik denetim | Denetçi | CAO | regex/ dosya varlığı | tamamlandı |
| EK.5 | Fabrika sürümü `2.0.0-reasoning-alpha` | Overmind | CEO | meta + CI hizalı | tamamlandı |

## [EK-20260614-v21] v2.1-stable — Reasoning zırhı · `tamamlandı`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| EK.6 | `<negative_constraints>` — 19-claude-reasoning.mdc | Overmind | CAO | 3 yasak maddesi | tamamlandı |
| EK.7 | Kelime cap 150–200 / blok | Overmind | CEO | over-thinking önleme | tamamlandı |
| EK.8 | `validate-reasoning-template-xml.sh` + audit V2.7 | Denetçi | CAO | XML dengesi | tamamlandı |
| EK.9 | Fabrika sürümü `2.1.0-stable` | Overmind | CEO | badge + CI sync | tamamlandı |
| EK.10 | v2.2 canlı transcript parser | — | — | AI Studio koşusu sonrası | bekliyor |

---

## F8 — Anahtar Teslim (Hiyerarşik kapanış) · `bekliyor`

| # | Görev | Ajan | L1 | Kabul | Durum |
|---|-------|------|----|-------|-------|
| F8.1 | `python3 scripts/cao/run_cao_audit.py` | CAO | CEO | rapor | bekliyor |
| F8.2 | `./scripts/ceo/run_ceo_cycle.sh` | CEO | CSGB | cycle ok | bekliyor |
| F8.3 | `./scripts/agent-approval-gate.sh` | Overmind | Geliştirici | gate pass | bekliyor |
| F8.4 | `docs/CHANGELOG.md` + release notları | CEO | EGC | ADR güncel | bekliyor |

---

## Keşifler & Dinamik Eklemeler

Uygulama sırasında tespit edilen eksikler (otomatik veya ajan önerisi):

| Ek ID | Faz | Görev | Neden | Durum |
|-------|-----|-------|-------|-------|
| EK-20260614-01 | F0 | Gradle wrapper bootstrap | gradlew placeholder | tamamlandı |
| EK-20260614-02 | F0 | `governance/FACTORY_REPO_POLICY.md` | runtime vs git ayrımı | tamamlandı |
| EK-20260614-03 | F0 | `scripts/factory-quality-gate.sh` | 100/100 kalite kapısı | tamamlandı |
| EK-20260614-04 | F3 | BillingRepository Hilt context | derlenebilir şablon | tamamlandı |
| EK-20260614-05 | F0 | `gradle-build-loop.sh` + snapshots | Cursor terminal köprüsü | tamamlandı |
| EK-20260614-06 | F0 | MCP handoff + auditor glob | context optimizasyonu | tamamlandı |
| EK-20260614-07 | F0 | `state-recovery.sh` + `18-state-recovery.mdc` | truncation / yarım Gradle kurtarma | tamamlandı |
| EK-20260614-08 | F0 | `test/` smoke harness | fabrika adım denetimi + FactorySmoke app | tamamlandı |
| EK-20260614-09 | F0 | AI Studio bootstrap lab | `bootstrap-external-project.sh` canlı infaz | tamamlandı |
| EK-20260614-10 | F0 | Dokümantasyon v2.1 denetimi | sürüm hizası + profesyonel dil | tamamlandı |

---

## Durum Özeti

| Faz | Ad | Durum |
|-----|-----|-------|
| F0 | Zemin & Temel | tamamlandı |
| F1 | Kolon & Taşıyıcı | işleniyor |
| F2 | Kat Döşeme | bekliyor |
| F3 | Duvar & Tesisat | bekliyor |
| F4 | Cephe & UI | bekliyor |
| F5 | Elektrik & Güvenlik | bekliyor |
| F6 | Ölçüm & Analitik | bekliyor |
| F7 | İç Mekan | bekliyor |
| F8 | Anahtar Teslim | bekliyor |

| **Son güncelleme:** 2026-06-14 · **Güncelleyen ajan:** Overmind
