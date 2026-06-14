#!/usr/bin/env bash
# Verify 33 layer slices match canonical manifest (count + layer headers).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/docs/33-LAYER-MANIFEST.yaml"
SLICE_DIR="$ROOT/docs/33-LAYER-MANIFEST"

if [[ ! -f "$MANIFEST" ]]; then
  echo "HATA: $MANIFEST yok"
  exit 1
fi

if [[ ! -d "$SLICE_DIR" ]]; then
  echo "HATA: $SLICE_DIR yok — python3 scripts/split-layer-manifest.py çalıştırın"
  exit 1
fi

missing=0
for i in $(seq 0 32); do
  f="$SLICE_DIR/layer-$(printf '%02d' "$i").yaml"
  if [[ ! -f "$f" ]]; then
    echo "HATA: eksik dilim — $f"
    missing=$((missing + 1))
    continue
  fi
  if ! grep -q "^# KATMAN $i " "$f"; then
    echo "HATA: layer-$i başlık uyuşmazlığı"
    missing=$((missing + 1))
  fi
  if ! grep -qE "^  ${i}:" "$MANIFEST"; then
    echo "HATA: manifest içinde layer $i yok"
    missing=$((missing + 1))
  fi
done

if [[ $missing -gt 0 ]]; then
  echo "==> Layer slice doğrulama BAŞARISIZ ($missing)"
  exit 1
fi

echo "==> 33 layer slice doğrulandı"
exit 0
