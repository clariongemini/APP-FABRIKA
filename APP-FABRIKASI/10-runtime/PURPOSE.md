# PURPOSE — 10-runtime

## Bu klasör neden var?

OS'un **ne öğrendiğini bilmesi** — context assembly, decision/pattern/evidence retrieval.

## Ne saklanır?

- Context manifest şeması (`context-manifest.schema.json`)
- Üretilmiş manifest'ler (`context/` — venture başına)
- Evidence index özeti (`evidence-index/`)

## Ne saklanmaz?

- Ham evidence (`07-evidence/{slug}/raw/`)
- Ephemeral cache (gitignore)
- Tüm repo'yu context'e yükleyen "oku her şeyi" politikası

## Başarı ölçütü

`ulas-player` build sırasında context manifest 8K token bütçesine uygun assemble edildi — gereksiz dosya okunmadı.
