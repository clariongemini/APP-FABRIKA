#!/usr/bin/env bash
# P0 — Venture ↔ codebase ↔ build ↔ test ↔ evidence bridge
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SVOS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENTURE_SLUG="${1:-}"

if [[ -z "$VENTURE_SLUG" || "$VENTURE_SLUG" == "-h" || "$VENTURE_SLUG" == "--help" ]]; then
  echo "Kullanım: $0 <venture-slug>"
  echo "Örnek:   $0 my-app"
  echo ""
  echo "Önce: ./init-venture.sh \"My App\" my-app path/to/codebase/"
  exit 1
fi

VENTURE_JSON="$SVOS/08-ventures/$VENTURE_SLUG/venture.json"
if [[ ! -f "$VENTURE_JSON" ]]; then
  echo "ERROR: Venture charter not found: $VENTURE_JSON" >&2
  echo "Run: ./APP-FABRIKASI/scripts/init-venture.sh \"Name\" $VENTURE_SLUG path/to/codebase/" >&2
  exit 1
fi

read -r CODEBASE_PATH CODEBASE_RESOLVED BUILD_TASK TEST_TASK JUNIT_VARIANT < <(python3 - <<PY
import json, sys
sys.path.insert(0, "$SVOS/ULAS/bin")
import gradle_test_parser as gtp
from pathlib import Path
v = json.loads(Path("$VENTURE_JSON").read_text())
cfg = gtp.load_bridge_config(Path("$SVOS"), v)
cp = v.get("codebase_path", "")
cr = v.get("codebase_resolved", "")
print(cp, cr, cfg["build_task"], cfg["unit_test_task"], cfg["junit_results_variant"])
PY
)

CODEBASE="${CODEBASE_RESOLVED:-$ROOT/$CODEBASE_PATH}"
JAVA_HOME="${JAVA_HOME:-}"
if [[ -z "$JAVA_HOME" ]]; then
  for j in /opt/homebrew/opt/openjdk@21 /opt/homebrew/opt/openjdk@17 /usr/local/opt/openjdk@21 /usr/local/opt/openjdk@17; do
  if [[ -d "$j/libexec/openjdk.jdk/Contents/Home" ]]; then
    JAVA_HOME="$j/libexec/openjdk.jdk/Contents/Home"
    break
  fi
  done
fi
export JAVA_HOME PATH="$JAVA_HOME/bin:$PATH"

EVIDENCE_DIR="$SVOS/07-evidence/$VENTURE_SLUG"
RUNTIME_EVIDENCE="$SVOS/10-runtime/evidence/$VENTURE_SLUG"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "=== APP-FABRIKA Venture Bridge (P0) ==="
echo "Venture: $VENTURE_SLUG"
echo "Codebase: $CODEBASE"
echo "Build:    $BUILD_TASK"
echo "Tests:    $TEST_TASK"

if [[ ! -d "$CODEBASE" ]]; then
  echo "ERROR: Codebase not found at $CODEBASE" >&2
  exit 1
fi

# --- Build ---
echo ""
echo "[1/5] Build..."
cd "$CODEBASE"
BUILD_OK=false
if ./gradlew "$BUILD_TASK" -q --no-daemon 2>/dev/null; then
  BUILD_OK=true
fi
BUILD_STATUS="success"
$BUILD_OK || BUILD_STATUS="failed"

# --- Unit tests ---
echo "[2/5] Unit tests..."
TEST_LOG="$(mktemp)"
set +e
./gradlew "$TEST_TASK" --no-daemon 2>&1 | tee "$TEST_LOG"
TEST_EXIT=$?
set -e

TOTAL=0
PASSED=0
FAILED=0
if grep -qE "tests completed" "$TEST_LOG"; then
  read -r TOTAL FAILED < <(grep -oE '[0-9]+ tests completed, [0-9]+ failed' "$TEST_LOG" | tail -1 | sed -E 's/ tests completed, / /;s/ failed//')
  PASSED=$((TOTAL - FAILED))
fi
TEST_STATUS="success"
[[ "$TEST_EXIT" -ne 0 ]] && TEST_STATUS="failed"

# --- Evidence bundle ---
echo "[3/5] Evidence manifest..."
mkdir -p "$EVIDENCE_DIR" "$RUNTIME_EVIDENCE"
MANIFEST="$EVIDENCE_DIR/manifest.json"
cat > "$MANIFEST" <<EOF
{
  "venture_slug": "$VENTURE_SLUG",
  "period": "$(date -u +%Y-%m)",
  "collected_at": "$TIMESTAMP",
  "codebase_path": "$CODEBASE_PATH",
  "codebase_resolved": "$CODEBASE",
  "bridge_version": "1.1",
  "build": {
    "build_task": "$BUILD_TASK",
    "unit_test_task": "$TEST_TASK",
    "junit_results_variant": "$JUNIT_VARIANT"
  },
  "sources": [
    {
      "type": "build",
      "task": "$BUILD_TASK",
      "status": "$BUILD_STATUS"
    },
    {
      "type": "unit_test",
      "task": "$TEST_TASK",
      "status": "$TEST_STATUS",
      "total": $TOTAL,
      "passed": $PASSED,
      "failed": $FAILED
    }
  ],
  "summary": "EVIDENCE.md",
  "raw_gitignored": true
}
EOF
cp "$MANIFEST" "$RUNTIME_EVIDENCE/manifest.json"

cat > "$EVIDENCE_DIR/EVIDENCE.md" <<EOF
# Evidence — $VENTURE_SLUG

**Collected:** $TIMESTAMP  
**Codebase:** \`$CODEBASE_PATH\`

## Build

- Task: \`$BUILD_TASK\`
- Status: **$BUILD_STATUS**

## Unit tests

- Task: \`$TEST_TASK\`
- Status: **$TEST_STATUS**
- Total: $TOTAL · Passed: $PASSED · Failed: $FAILED

## Bridge

Produced by \`APP-FABRIKASI/scripts/bridge-venture.sh\` — external validation for ULAS (not self-graded).
EOF

# --- Venture sync ---
echo "[4/5] Venture charter sync..."
python3 <<PY
import json
from pathlib import Path
p = Path("$VENTURE_JSON")
v = json.loads(p.read_text())
v["codebase_path"] = "$CODEBASE_PATH"
v["codebase_resolved"] = "$CODEBASE"
v.setdefault("build", {})
v["build"].update({
    "build_task": "$BUILD_TASK",
    "unit_test_task": "$TEST_TASK",
    "junit_results_variant": "$JUNIT_VARIANT",
})
v["stage"] = "validate"
v["status"] = "building"
v["evidence_status"] = "partial" if "$TEST_STATUS" == "success" and $FAILED == 0 else "collected"
v["validation"] = {
    "bridged_at": "$TIMESTAMP",
    "build": "$BUILD_STATUS",
    "tests": {"total": $TOTAL, "passed": $PASSED, "failed": $FAILED, "status": "$TEST_STATUS"},
}
p.write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n")
PY

# --- ULAS hygiene ---
echo "[5/5] ULAS P1 reset..."
"$SVOS/scripts/ulas.sh" overrides-reset --reason "bridge-venture pre-validation reset" >/dev/null || true

echo "[+] Failure report..."
python3 "$SVOS/scripts/collect-test-failures.py" "$VENTURE_SLUG" "$TEST_LOG" "$CODEBASE" || true

echo ""
echo "=== Bridge complete ==="
echo "  Evidence: APP-FABRIKASI/07-evidence/$VENTURE_SLUG/"
echo "  Venture:  evidence_status updated"
echo "  ULAS:     policy overrides reset"
"$SVOS/scripts/ulas.sh" risk-gate 2>/dev/null | grep -E "evidence_bundles|Gate active" || true
rm -f "$TEST_LOG"
