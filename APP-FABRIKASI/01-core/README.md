# 01-core — Platform-Bağımsız Çekirdek

SVOS'un kalbi. Governance, knowledge, intelligence ve runtime **sözleşmeleri** burada yaşar.

## Alt dizinler

| Dizin | Rol |
|-------|-----|
| [`governance/`](governance/) | Kurallar, politikalar, operating principles |
| [`knowledge/`](knowledge/) | Canonical knowledge şeması (ADR, pattern referansları) |
| [`intelligence/`](intelligence/) | Knowledge → Insight → Decision motoru sözleşmesi |
| [`runtime/`](runtime/) | Çekirdek runtime path sözleşmeleri |
| [`standards/`](standards/) | Platform-agnostik kalite standartları |

## Android Factory ile ilişki

Repo kökündeki `governance/` ve `knowledge/` **geçiş dönemi kaynaklarıdır**.  
SVOS olgunlaştıkça canonical veri `APP-FABRIKASI/01-core/` altına taşınır; Android Factory dosyaları **değiştirilmez**.

## Prensip

> Bir venture iOS'a geçtiğinde governance yeniden yazılmaz. Yalnızca `02-platforms/ios` adaptörü devreye girer.
