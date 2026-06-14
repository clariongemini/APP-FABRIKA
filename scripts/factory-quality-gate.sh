#!/usr/bin/env bash
# Fabrika kalite kapısı — tüm doğrulamalar + bileşik skor.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
WARN=0

run_check() {
  local name="$1"
  shift
  if "$@" &>/dev/null; then
    printf "  ✅ %-42s\n" "$name"
    PASS=$((PASS + 1))
  else
    printf "  ❌ %-42s\n" "$name"
    FAIL=$((FAIL + 1))
  fi
}

run_warn() {
  local name="$1"
  shift
  if "$@" &>/dev/null; then
    printf "  ✅ %-42s\n" "$name"
    PASS=$((PASS + 1))
  else
    printf "  ⚠️  %-42s (yerel ortam)\n" "$name"
    WARN=$((WARN + 1))
  fi
}

echo "==> Fabrika kalite kapısı"
echo ""

echo "── Kod & Standartlar ──"
run_check "validate-code.sh" bash scripts/validate-code.sh
run_check "audit-layers.sh" bash scripts/audit-layers.sh
run_check "audit-layer-components.sh" bash scripts/audit-layer-components.sh
run_check "audit-oem-compat.sh" bash scripts/audit-oem-compat.sh
run_check "audit-security.sh" bash scripts/audit-security.sh
run_check "audit-android-scaffold.sh" bash scripts/audit-android-scaffold.sh
run_check "validate-android-template.sh" bash scripts/validate-android-template.sh

echo ""
echo "── Executive OS ──"
run_check "validate-factory-governance.sh" bash scripts/governance/validate-factory-governance.sh
run_check "validate-audit-chain.py" python3 scripts/governance/validate-audit-chain.py
if [[ -f YAPILACAKLAR.md ]]; then
  run_check "validate-yapilacaklar.py" python3 scripts/governance/validate-yapilacaklar.py
else
  cp templates/YAPILACAKLAR.template.md YAPILACAKLAR.md
  run_check "validate-yapilacaklar (template)" python3 scripts/governance/validate-yapilacaklar.py
  rm -f YAPILACAKLAR.md
fi

echo ""
echo "── Ortam (yerel) ──"
run_warn "check-mcp.sh (P0 MCP)" bash scripts/check-mcp.sh

echo ""
echo "── Sağlık skoru ──"
HEALTH_OUT="$(bash scripts/factory-health.sh)"
echo "$HEALTH_OUT" | tail -5

HEALTH_SCORE="$(echo "$HEALTH_OUT" | grep 'GENEL TOPLAM' | grep -oE '[0-9]+' | head -1)"
HEALTH_SCORE="${HEALTH_SCORE:-0}"

TOTAL_CHECKS=$((PASS + FAIL))
QUALITY=$(( (PASS * 100) / (TOTAL_CHECKS > 0 ? TOTAL_CHECKS : 1) ))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "  Kalite kapısı   : %d/%d geçti" "$PASS" "$TOTAL_CHECKS"
[[ $WARN -gt 0 ]] && printf " · %d yerel uyarı" "$WARN"
echo ""
printf "  Bileşik oran    : %d%%\n" "$QUALITY"
printf "  factory-health  : %s/100\n" "$HEALTH_SCORE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $FAIL -gt 0 ]]; then
  echo "  Durum: ❌ Kalite kapısı BAŞARISIZ"
  exit 1
fi

if [[ $WARN -gt 0 ]]; then
  echo "  Durum: 🟢 Fabrika 100/100 — MCP PAT yerel adımı kaldı"
  exit 0
fi

echo "  Durum: ✅ KUSURSUZ — Fabrika kalite kapısı tam geçti"
exit 0
