#!/usr/bin/env bash
# Fabrika sürümü tek kaynak: .factory/meta.json → tüm referanslar hizalı mı?
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$ROOT/.factory/meta.json"
ERRORS=0

if [[ ! -f "$META" ]]; then
  echo "HATA: .factory/meta.json bulunamadı"
  exit 1
fi

EXPECTED="$(python3 -c "import json; print(json.load(open('$META'))['version'])")"

check_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if [[ ! -f "$file" ]]; then
    echo "HATA: $label — dosya yok: $file"
    ERRORS=$((ERRORS + 1))
    return
  fi
  if ! grep -q "$pattern" "$file"; then
    echo "HATA: $label — '$pattern' bekleniyordu ($file)"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "==> Fabrika sürüm doğrulama (beklenen: $EXPECTED)"

check_contains "$ROOT/scripts/init-new-app.sh" "FACTORY_VERSION=\"$EXPECTED\"" "init-new-app.sh"
check_contains "$ROOT/scripts/governance/init-governance.sh" "FACTORY_VERSION=\"$EXPECTED\"" "init-governance.sh"
check_contains "$ROOT/scripts/governance/init-yapilacaklar.sh" "FACTORY_VERSION=\"$EXPECTED\"" "init-yapilacaklar.sh"
check_contains "$ROOT/scripts/sync-standards.sh" "\"factory_version\": \"$EXPECTED\"" "sync-standards.sh"
check_contains "$ROOT/YAPILACAKLAR.md" "v$EXPECTED" "YAPILACAKLAR.md"
check_contains "$ROOT/docs/00-INDEX.md" "v$EXPECTED" "docs/00-INDEX.md"
check_contains "$ROOT/LICENSE" "$EXPECTED" "LICENSE"
check_contains "$ROOT/.github/workflows/validate.yml" "$EXPECTED" ".github/workflows/validate.yml"
check_contains "$ROOT/templates/android/project/.github/workflows/android-build.yml" "$EXPECTED" "template android-build.yml"

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Sürüm doğrulama BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Sürüm doğrulama başarılı ($EXPECTED)."
