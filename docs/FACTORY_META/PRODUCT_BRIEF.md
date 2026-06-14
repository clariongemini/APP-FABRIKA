# Ürün Brifi — Ulas Autonomous Android APP Factory

**Sürüm:** v2.1.0-stable · **Paket:** `com.ulas.factory` · **Yazar:** Ulaş Kaşıkcı

## Özet

Cursor-native **GitHub template fabrika reposu**: Android uygulamalarını 33 katman, 16 departman ajanı, Executive OS ve otomatik kalite kapıları ile tekrarlanabilir şekilde üretmek.

Bu depo bir APK değildir; standartlar, governance, Gradle şablonu ve ajan kuralları burada yaşar.

## Hedef Kitle

- **Birincil:** Android geliştiriciler / teknik kurucular Cursor Agent Mode kullanan
- **İkincil:** Küçük ekipler aynı mühendislik disiplinini çoğaltmak isteyen

## Temel Problem

| Acı | Fabrika cevabı |
|-----|----------------|
| AI kod üretimi tutarsız, halüsinasyonlu | YAPILACAKLAR F0–F8 + zero-hallucination kapısı |
| Cursor kuralları dağınık | 21 `.mdc` kural + 16 ajan + hiyerarşik denetim |
| AI Studio / Stitch ham export olgun değil | `bootstrap-external-project.sh` + lab doğrulaması |
| Gradle + governance her projede sıfırdan | `init-new-app.sh` / `sync-standards.sh` |

## Mavi Okyanus Fırsatı

Rakipler genelde **tek boyutlu** (sadece `.cursorrules`, sadece scaffold, veya sadece NowInAndroid klonu). Fabrika **Executive OS + 33 katman + smoke/audit CI + AI Studio import** birleşiminde konumlanır.

## MVP Özellikleri (V1 — mevcut)

1. F0–F8 faz disiplini (`YAPILACAKLAR.md`, `/baslat`)
2. 10 modüllü Android iskelet + FactorySmoke test
3. Claude-Native v2.1 reasoning (`19-claude-reasoning.mdc`)
4. Harici AI Studio bootstrap + `run-all-tests.sh` orkestratör

## Başarı Metrikleri

| Metrik | Hedef |
|--------|-------|
| `factory-health.sh` | 100/100 |
| `run-factory-audit.sh` | 40+ pass, BUILD CI'da |
| Smoke `assembleDebug` | CI yeşil (JDK 17) |
| İlk gerçek app bootstrap | Lab ile aynı akış, F3 build kanıtı |

## Paket Bilgisi

- **Uygulama:** Factory
- **Package:** `com.ulas.factory`
- **Fabrika Sürümü:** v2.1.0-stable
