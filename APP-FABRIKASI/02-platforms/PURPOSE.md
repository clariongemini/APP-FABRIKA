# PURPOSE — 02-platforms

## Bu klasör neden var?

**HOW we build it** — platform adaptörleri. Her adaptör standart, mimari, tooling, validation ve release sürecini taşır; governance taşımaz.

## Ne saklanır?

- Adapter blueprint'leri (`android/`, `ios/`, `web/`, `backend/`, `ai/`)
- Platform-specific standart referansları
- `ADAPTER_DESIGN.md` — adapter sözleşmesi

## Ne saklanmaz?

- Duplicate governance tree
- Production uygulama kodu (venture repo'sunda veya `templates/android/` kökünde)
- Stabilization Mode'da: **yeni adapter implementasyonu**

## Başarı ölçütü

Android adaptörü operasyonel (CI green). Diğer adaptörler blueprint kalır — venture seçene kadar genişletilmez.
