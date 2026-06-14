#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Pre-commit denetimi"

bash "$ROOT/scripts/validate-code.sh"
bash "$ROOT/scripts/audit-layers.sh"
bash "$ROOT/scripts/audit-layer-components.sh"
bash "$ROOT/scripts/audit-oem-compat.sh"
bash "$ROOT/scripts/audit-security.sh"
bash "$ROOT/scripts/audit-android-scaffold.sh"
bash "$ROOT/scripts/governance/validate-factory-governance.sh"
python3 "$ROOT/scripts/governance/validate-audit-chain.py"
if [[ -f "$ROOT/YAPILACAKLAR.md" ]]; then
  python3 "$ROOT/scripts/governance/validate-yapilacaklar.py"
fi
bash "$ROOT/scripts/check-mcp.sh" --warn
bash "$ROOT/scripts/run-tests.sh"

echo "==> Pre-commit denetimi başarılı."
