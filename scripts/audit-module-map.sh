#!/usr/bin/env bash
# Modül haritası ↔ Gradle iskelet tutarlılığı (F2.4 ArchUnit yerine statik denetim).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETTINGS="$ROOT/templates/android/project/settings.gradle.kts"
MODULE_MAP="$ROOT/docs/02-ARCHITECTURE/MODULE_MAP.md"
FAIL=0

echo "==> Mimari modül denetimi (F2)"

[[ -f "$SETTINGS" ]] || { echo "HATA: settings.gradle.kts yok"; exit 1; }
[[ -f "$MODULE_MAP" ]] || { echo "HATA: MODULE_MAP.md yok"; exit 1; }

for mod in app core:common core:designsystem core:i18n core:database core:network core:security core:oem feature:home feature:settings feature:premium; do
  if grep -q ":$mod" "$SETTINGS" 2>/dev/null || grep -q "\":$mod\"" "$SETTINGS" 2>/dev/null; then
    echo "  ✅ Gradle :$mod"
  else
    echo "  ❌ Gradle :$mod eksik"
    FAIL=$((FAIL + 1))
  fi
done

if grep -q "com.ulas.factory" "$ROOT/governance/dependency-rules.json" 2>/dev/null; then
  echo "  ✅ dependency-rules.json package"
else
  echo "  ❌ dependency-rules.json package uyumsuz"
  FAIL=$((FAIL + 1))
fi

bash "$ROOT/scripts/audit-layers.sh" &>/dev/null && echo "  ✅ audit-layers.sh" || { echo "  ❌ audit-layers.sh"; FAIL=$((FAIL + 1)); }

if [[ $FAIL -gt 0 ]]; then
  echo "==> Mimari denetim BAŞARISIZ ($FAIL)"
  exit 1
fi

echo "==> Mimari denetim başarılı."
exit 0
