#!/usr/bin/env bash
# Gradle build-feedback loop — Cursor Agent terminal köprüsü.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

MAX_RETRIES="${GRADLE_LOOP_MAX_RETRIES:-3}"
TASK="${GRADLE_TASK:-assembleDebug}"
SNAPSHOT_DIR="$ROOT/.cursor/snapshots/build"
mkdir -p "$SNAPSHOT_DIR"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$SNAPSHOT_DIR/gradle-${TASK//:/-}-${TIMESTAMP}.log"
LATEST="$SNAPSHOT_DIR/LATEST.gradle.log"
RECOVERY="$ROOT/scripts/state-recovery.sh"

skip_or_fail() {
  local msg="$1"
  if [[ "$STRICT" == true ]]; then
    echo "HATA: $msg"
    exit 1
  fi
  echo "ATLA: $msg"
  exit 0
}

echo "==> Gradle build loop"
echo "  Task    : $TASK"
echo "  Retries : $MAX_RETRIES"
echo ""

if [[ ! -f "$ROOT/gradlew" ]]; then
  skip_or_fail "gradlew yok — ./scripts/init-new-app.sh sonrası tekrar dene"
fi

if ! command -v java &>/dev/null; then
  skip_or_fail "JDK bulunamadı — JDK 17+ kur, JAVA_HOME ayarla"
fi

chmod +x "$ROOT/gradlew" 2>/dev/null || true

if [[ -x "$RECOVERY" && "${RECOVERY_SKIP_CHECKPOINT:-0}" != "1" ]]; then
  echo "==> State recovery checkpoint (pre-build)"
  "$RECOVERY" --checkpoint || echo "    UYARI: checkpoint atlandı/başarısız"
  echo ""
fi

attempt=1
while [[ $attempt -le $MAX_RETRIES ]]; do
  echo "==> Deneme $attempt/$MAX_RETRIES: ./gradlew $TASK --stacktrace"
  set +e
  "$ROOT/gradlew" "$TASK" --stacktrace 2>&1 | tee "$LOG"
  exit_code="${PIPESTATUS[0]}"
  set -e

  cp "$LOG" "$LATEST"

  if [[ $exit_code -eq 0 ]]; then
    echo ""
    echo "==> ✅ BUILD SUCCESS"
    echo "    Log: $LOG"
    echo "    Son: $LATEST"
    exit 0
  fi

  echo ""
  echo "==> ❌ BUILD FAILED (exit $exit_code) — log: $LOG"

  if [[ -x "$RECOVERY" ]]; then
    if "$RECOVERY" --maybe-auto-recover "$LATEST" 2>/dev/null; then
      echo "    Auto-recover tetiklendi."
    elif [[ $attempt -ge 2 ]]; then
      echo "    İpucu: ./scripts/state-recovery.sh --recover"
    fi
  fi

  if [[ $attempt -lt $MAX_RETRIES ]]; then
    echo "    Cursor Agent: logu oku, düzelt, tekrar dene."
  fi
  attempt=$((attempt + 1))
done

echo ""
echo "==> BUILD FAILED — $MAX_RETRIES deneme tükendi"
echo "    Cursor Agent ZORUNLU: $LATEST dosyasını okuyup hatayı düzelt."
echo "    Kurtarma: ./scripts/state-recovery.sh --recover"
exit 1
