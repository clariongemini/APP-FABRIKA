#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> 33 Katman Ajan Atama Denetimi"

MANIFEST="$ROOT/docs/33-LAYER-MANIFEST.yaml"
ERRORS=0

if [[ ! -f "$MANIFEST" ]]; then
  echo "HATA: $MANIFEST bulunamadı"
  exit 1
fi

for file in 01-product-cpo.mdc 02-architect.mdc 03-android-elite.mdc 04-auditor-security.mdc; do
  if [[ ! -f "$ROOT/.cursor/rules/$file" ]]; then
    echo "HATA: Ajan dosyası eksik — $file"
    ERRORS=$((ERRORS + 1))
  fi
done

ASSIGNED_FILE="$(mktemp)"
python3 - "$MANIFEST" "$ASSIGNED_FILE" << 'PYEOF'
import re, sys
from pathlib import Path
text = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
layers = []
for m in re.finditer(r'  (\w+): \[(.*?)\]', text):
    for n in [int(x.strip()) for x in m.group(2).split(',')]:
        layers.append(n)
out.write_text("\n".join(map(str, sorted(layers))) + "\n")
PYEOF

ASSIGNED_COUNT=$(wc -l < "$ASSIGNED_FILE" | tr -d ' ')
UNIQUE_COUNT=$(sort -u "$ASSIGNED_FILE" | wc -l | tr -d ' ')

if [[ "$ASSIGNED_COUNT" != "$UNIQUE_COUNT" ]]; then
  echo "HATA: Bazı katmanlar birden fazla ajana atanmış"
  ERRORS=$((ERRORS + 1))
fi

for i in $(seq 0 32); do
  if ! grep -qx "$i" "$ASSIGNED_FILE"; then
    echo "HATA: KATMAN $i hiçbir ajana atanmamış"
    ERRORS=$((ERRORS + 1))
  fi
done

rm -f "$ASSIGNED_FILE"

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Ajan denetimi BAŞARISIZ ($ERRORS hata)"
  exit 1
fi

echo "==> 33 katman manifest ile ajanlara doğru atanmış."
