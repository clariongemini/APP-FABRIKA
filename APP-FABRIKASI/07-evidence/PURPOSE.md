# PURPOSE — 07-evidence

## Bu klasör neden var?

**En kritik katman.** Gelecek kararların yakıtı — analytics, crash, revenue, retention, feedback.

## Ne saklanır?

- Venture başına evidence bundle (`{slug}/`)
- Aggregate summary (`EVIDENCE.md`)
- Manifest (`manifest.json`) — kaynak listesi
- Şablon (`_template/`)

## Ne saklanmaz?

- Ham export / PII (`raw/` — **gitignore**)
- Spekülasyon veya tahmin verisi
- Evidence olmadan portfolio allocation girdisi

## Başarı ölçütü

`ulas-player` ship sonrası: Play Console + Firebase (veya eşdeğer) summary mevcut, `evidence_status: collected`.
