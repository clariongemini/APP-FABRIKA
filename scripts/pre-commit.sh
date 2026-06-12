#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Otonom Holding — Pre-commit Denetimi"

bash "$ROOT/scripts/validate-code.sh"
bash "$ROOT/scripts/audit-layers.sh"
bash "$ROOT/scripts/audit-layer-components.sh"
bash "$ROOT/scripts/audit-oem-compat.sh"
bash "$ROOT/scripts/audit-security.sh"
bash "$ROOT/scripts/audit-android-scaffold.sh"
bash "$ROOT/scripts/check-mcp.sh" --warn
bash "$ROOT/scripts/run-tests.sh"

echo "==> Pre-commit denetimi başarılı."
