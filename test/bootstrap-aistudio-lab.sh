#!/usr/bin/env bash
# AI Studio / Stitch ham export → bootstrap-external-project canlı infaz testi.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURE="$REPO_ROOT/test/fixtures/aistudio-minimal"
LAB_DIR="$REPO_ROOT/test/aistudio-lab-run"
APP_NAME="StitchLab"
PACKAGE="com.aistudio.stub.lab"
PROMPT="Stitch/AI Studio export — fabrika bootstrap canlı infaz; i18n, governance, F0–F8 yükseltme"
MAIN_KT="app/src/main/java/com/aistudio/stub/lab/MainActivity.kt"

echo "==> AI Studio bootstrap lab"

[[ -d "$FIXTURE" ]] || { echo "HATA: fixture yok — $FIXTURE"; exit 1; }

echo "==> [1/4] Fixture kopyala → test/aistudio-lab-run"
rm -rf "$LAB_DIR"
mkdir -p "$LAB_DIR"
cp -R "$FIXTURE/." "$LAB_DIR/"

echo "==> [2/4] bootstrap-external-project.sh"
FACTORY_REPO="$REPO_ROOT" "$REPO_ROOT/scripts/bootstrap-external-project.sh" \
  "$LAB_DIR" "$APP_NAME" "$PACKAGE" "$PROMPT"

echo "==> [3/4] Doğrulama"
fail=0
assert() {
  local label="$1"
  local path="$2"
  if [[ -e "$path" ]]; then
    echo "    ✅ $label"
  else
    echo "    ❌ $label — $path"
    fail=$((fail + 1))
  fi
}

assert "bootstrap_manifest" "$LAB_DIR/.factory/bootstrap_manifest.json"
assert "YAPILACAKLAR.md" "$LAB_DIR/YAPILACAKLAR.md"
assert "AI Studio MainActivity korundu" "$LAB_DIR/$MAIN_KT"
assert "governance executive" "$LAB_DIR/governance/executive/CEO_OPERATING_SYSTEM.md"
assert "19-claude-reasoning" "$LAB_DIR/.cursor/rules/19-claude-reasoning.mdc"
assert "20-aistudio-import" "$LAB_DIR/.cursor/rules/20-aistudio-import.mdc"

if ! (cd "$LAB_DIR" && python3 scripts/governance/validate-yapilacaklar.py &>/dev/null); then
  echo "    ❌ validate-yapilacaklar.py"
  fail=$((fail + 1))
else
  echo "    ✅ validate-yapilacaklar.py"
fi

if grep -q '"source": "aistudio-import"' "$LAB_DIR/.factory/project.json" 2>/dev/null; then
  echo "    ✅ project.json aistudio-import"
else
  echo "    ❌ project.json source"
  fail=$((fail + 1))
fi

if grep -q '2.1.0-stable' "$LAB_DIR/.factory/meta.json" 2>/dev/null || \
   grep -q '2.1.0-stable' "$REPO_ROOT/.factory/meta.json" >/dev/null; then
  echo "    ✅ fabrika sürüm 2.1.0-stable (kaynak repo)"
else
  echo "    ⚠️  meta.json lab altında opsiyonel"
fi

echo "==> [4/4] gradlew (opsiyonel)"
if [[ -x "$LAB_DIR/gradlew" ]] && command -v java &>/dev/null; then
  (cd "$LAB_DIR" && ./gradlew assembleDebug --quiet) && echo "    ✅ assembleDebug" || echo "    ⚠️  assembleDebug başarısız — JDK/AGP"
else
  echo "    ⏭️  gradlew veya JDK yok — bootstrap gradle adımı atlandı"
fi

echo ""
if [[ $fail -eq 0 ]]; then
  echo "==> AI Studio bootstrap lab: BAŞARILI"
  echo "    Sonraki: Cursor'da $LAB_DIR aç → /baslat"
  exit 0
fi

echo "==> AI Studio bootstrap lab: BAŞARISIZ ($fail)"
exit 1
