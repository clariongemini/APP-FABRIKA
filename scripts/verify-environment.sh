#!/usr/bin/env bash
# Yerel ortam kapısı — JDK, MCP, Gradle smoke (puan düşüren eksikleri raporlar).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WARN=0
FAIL=0

section() { echo ""; echo "── $1 ──"; }

check_jdk() {
  section "JDK (Gradle assembleDebug)"
  if command -v java &>/dev/null && java -version &>/dev/null 2>&1; then
    local ver
    ver="$(java -version 2>&1 | head -1)"
    echo "  ✅ Java — $ver"
    if [[ -x "$ROOT/test/factory-smoke-app/gradlew" ]]; then
      if (cd "$ROOT/test/factory-smoke-app" && ./gradlew assembleDebug --quiet) &>/dev/null; then
        echo "  ✅ factory-smoke-app assembleDebug"
      else
        echo "  ⚠️  assembleDebug başarısız — AGP/SDK kontrol edin"
        WARN=$((WARN + 1))
      fi
    else
      echo "  ⏭️  gradlew yok — ./test/bootstrap-smoke-app.sh çalıştırın"
      WARN=$((WARN + 1))
    fi
  else
    echo "  ❌ JDK 17+ yok — https://adoptium.net veya Android Studio JDK"
    echo "     CI smoke-build job assembleDebug kanıtını sağlar"
    echo "     Kurulum sonrası: ./test/run-all-tests.sh"
    WARN=$((WARN + 1))
  fi
}

check_mcp() {
  section "MCP (P0)"
  if bash "$ROOT/scripts/check-mcp.sh" &>/dev/null; then
    echo "  ✅ check-mcp.sh geçti"
  else
    echo "  ⚠️  MCP eksik — ./scripts/setup-mcp.sh"
    echo "     Kılavuz: docs/MCP_SETUP.md"
    WARN=$((WARN + 1))
  fi
}

check_factory_meta() {
  section "Fabrika meta (F1)"
  local ok=true
  for f in PRODUCT_BRIEF.md MARKET_ANALYSIS.md MONETIZATION.md roadmap_priorities.json; do
    if [[ -f "$ROOT/docs/FACTORY_META/$f" ]]; then
      echo "  ✅ docs/FACTORY_META/$f"
    else
      echo "  ❌ eksik — docs/FACTORY_META/$f"
      ok=false
    fi
  done
  [[ "$ok" == true ]] || FAIL=$((FAIL + 1))
}

echo "==> Ortam doğrulama (v2.1.0-stable)"
check_jdk
check_mcp
check_factory_meta

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $FAIL -gt 0 ]]; then
  echo "  Ortam: ❌ $FAIL zorunlu eksik · $WARN uyarı"
  exit 1
fi
if [[ $WARN -gt 0 ]]; then
  echo "  Ortam: 🟡 $WARN uyarı — fabrika kullanılabilir, tam puan için giderin"
  exit 0
fi
echo "  Ortam: ✅ Tam — JDK + MCP + fabrika meta hazır"
exit 0
