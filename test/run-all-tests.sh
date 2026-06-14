#!/usr/bin/env bash
# Fabrika test paketi — smoke audit + AI Studio bootstrap lab + kalite kapısı.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

FAIL=0

run() {
  local name="$1"
  shift
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  $name"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if "$@"; then
    echo "  → ✅ $name"
  else
    echo "  → ❌ $name"
    FAIL=$((FAIL + 1))
  fi
}

echo "==> Fabrika test paketi (v2.1.0-stable)"

run "validate-reasoning-template-xml" bash scripts/validate-reasoning-template-xml.sh
run "validate-factory-version" bash scripts/validate-factory-version.sh
run "validate-code" bash scripts/validate-code.sh
run "factory-audit (40 kontrol)" bash test/run-factory-audit.sh
run "AI Studio bootstrap lab" bash test/bootstrap-aistudio-lab.sh

# Smoke app yenileme (gradle varsa build dener)
if [[ -x test/bootstrap-smoke-app.sh ]]; then
  run "smoke bootstrap (mevcut app)" bash test/bootstrap-smoke-app.sh
fi

run "factory-quality-gate" bash scripts/factory-quality-gate.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $FAIL -eq 0 ]]; then
  echo "  TEST PAKETİ: ✅ TAMAMLANDI"
  exit 0
fi
echo "  TEST PAKETİ: ❌ $FAIL adım başarısız"
exit 1
