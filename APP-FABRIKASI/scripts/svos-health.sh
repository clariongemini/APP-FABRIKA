#!/usr/bin/env bash
# SVOS sağlık + olgunluk denetimi — her projede çalıştırılabilir.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
cd "$REPO"

echo "=== SVOS Health ==="
echo "  SVOS: $ROOT"
echo "  Repo: $REPO"
echo ""

python3 "$ROOT/ULAS/bin/ulas.py" maturity audit "$@"
