#!/usr/bin/env bash
# Maestro E2E köprüsü — Cursor emülatör çalıştıramaz; adb + maestro CLI gerekir.
#
# Kullanım:
#   ./scripts/run-maestro.sh
#   MAESTRO_FLOW=.maestro/flows/smoke.yaml ./scripts/run-maestro.sh
#   ./scripts/run-maestro.sh --strict
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

FLOW="${MAESTRO_FLOW:-.maestro/flows/smoke.yaml}"
SNAPSHOT_DIR="$ROOT/.cursor/snapshots/maestro"
mkdir -p "$SNAPSHOT_DIR"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$SNAPSHOT_DIR/maestro-${TIMESTAMP}.log"
LATEST="$SNAPSHOT_DIR/LATEST.maestro.log"

skip_or_fail() {
  local msg="$1"
  if [[ "$STRICT" == true ]]; then
    echo "HATA: $msg"
    exit 1
  fi
  echo "ATLA: $msg"
  exit 0
}

echo "==> Maestro E2E Bridge"

if [[ ! -f "$ROOT/$FLOW" ]]; then
  skip_or_fail "Flow bulunamadı: $FLOW (init-new-app veya scaffold gerekir)"
fi

if ! command -v maestro &>/dev/null; then
  skip_or_fail "maestro CLI yok — https://maestro.mobile.dev/docs/getting-started/installation"
fi

if command -v adb &>/dev/null; then
  if ! adb devices 2>/dev/null | grep -qE 'device$'; then
    skip_or_fail "adb cihaz/emülatör yok — Android Studio AVD veya fiziksel cihaz bağla"
  fi
else
  skip_or_fail "adb yok — Android SDK platform-tools gerekir"
fi

echo "    Flow: $FLOW"
set +e
maestro test "$ROOT/$FLOW" 2>&1 | tee "$LOG"
exit_code="${PIPESTATUS[0]}"
set -e
cp "$LOG" "$LATEST"

if [[ $exit_code -eq 0 ]]; then
  echo "==> ✅ MAESTRO PASS — log: $LOG"
  exit 0
fi

echo "==> ❌ MAESTRO FAIL — log: $LATEST"
exit 1
