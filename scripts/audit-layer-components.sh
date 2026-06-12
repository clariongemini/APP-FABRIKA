#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/docs/33-LAYER-MANIFEST.yaml"
ARCH="$ROOT/docs/33-LAYER-ARCHITECTURE.md"

ERRORS=0
TOTAL=0

if [[ ! -f "$MANIFEST" || ! -f "$ARCH" ]]; then
  echo "HATA: Manifest veya Architecture belgesi eksik"
  exit 1
fi

echo "==> 33 Katman Bileşen Denetimi"

while IFS= read -r component; do
  [[ -z "$component" ]] && continue
  TOTAL=$((TOTAL + 1))
  if ! grep -Fq "$component" "$ARCH"; then
    echo "HATA: Eksik bileşen — $component"
    ERRORS=$((ERRORS + 1))
  fi
done < <(awk '/^    components:/{flag=1;next} /^  [0-9]+:/{flag=0} flag && /^      - /{print substr($0,9)}' "$MANIFEST")

for i in $(seq 0 32); do
  if ! grep -q "### KATMAN $i —" "$ARCH"; then
    echo "HATA: KATMAN $i başlığı ARCHITECTURE belgesinde yok"
    ERRORS=$((ERRORS + 1))
  fi
done

if [[ $ERRORS -gt 0 ]]; then
  echo ""
  echo "==> Bileşen denetimi BAŞARISIZ ($ERRORS hata, $TOTAL bileşen tarandı)"
  exit 1
fi

echo "==> Tüm $TOTAL bileşen ve 33 katman başlığı doğrulandı."
