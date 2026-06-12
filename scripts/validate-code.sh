#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ERRORS=0

echo "==> Otonom Holding — Kod Doğrulama"

REQUIRED_FILES=(
  ".cursorrules"
  "README.md"
  "LICENSE"
  ".gitignore"
  ".cursor/rules/01-product-cpo.mdc"
  ".cursor/rules/02-architect.mdc"
  ".cursor/rules/03-android-elite.mdc"
  ".cursor/rules/04-auditor-security.mdc"
  ".cursor/rules/05-oem-compat-auditor.mdc"
  ".cursor/rules/06-mcp-orchestrator.mdc"
  ".cursor/mcp.required.json"
  ".cursor/mcp.json.example"
  "docs/MCP_SETUP.md"
  "docs/GITHUB_REPO_DESCRIPTION.md"
  "scripts/first-setup.sh"
  "scripts/check-mcp.sh"
  "docs/03-STANDARDS/OEM_COMPATIBILITY.md"
  "docs/03-STANDARDS/OEM_MATRIX.yaml"
  "docs/03-STANDARDS/SECURITY.md"
  "docs/03-STANDARDS/PRIVACY.md"
  "docs/03-STANDARDS/BACKGROUND_PROCESSING.md"
  "docs/03-STANDARDS/MONETIZATION_TECH.md"
  "docs/RELEASE_CHECKLIST.md"
  "AGENTS.md"
  "scripts/factory-health.sh"
  "scripts/audit-security.sh"
  "scripts/install-git-hooks.sh"
  "scripts/scaffold-oem-module.sh"
  "scripts/scaffold-android-project.sh"
  "scripts/audit-android-scaffold.sh"
  "docs/03-STANDARDS/FCM_PUSH.md"
  "docs/03-STANDARDS/PLAY_INTEGRITY.md"
  "docs/03-STANDARDS/PENTEST.md"
  "docs/FACTORY_SCORECARD.md"
  "templates/architecture/PENTEST_CHECKLIST.template.md"
  "templates/android/project/settings.gradle.kts"
  "templates/architecture/SECURITY.template.md"
  "templates/android/core-oem/OemCompatFacade.kt"
  "docs/00-INDEX.md"
  "docs/TODO.md"
  "docs/CHANGELOG.md"
  "docs/33-LAYER-ARCHITECTURE.md"
  "docs/33-LAYER-MANIFEST.yaml"
  "docs/BOOTSTRAP.md"
  "docs/02-ARCHITECTURE/ANDROID_STRUCTURE.md"
  "docs/03-STANDARDS/LIQUID_GLASS.md"
  "docs/03-STANDARDS/I18N.md"
  "docs/03-STANDARDS/TESTING.md"
  "docs/03-STANDARDS/PERFORMANCE.md"
  "scripts/init-new-app.sh"
  "scripts/sync-standards.sh"
  "templates/vision/PRODUCT_BRIEF.template.md"
  "templates/architecture/MODULE_MAP.template.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$ROOT/$file" ]]; then
    echo "HATA: Eksik dosya — $file"
    ERRORS=$((ERRORS + 1))
  fi
done

LEGACY_FILES=(
  ".cursor/rules/01-architect.mdc"
  ".cursor/rules/02-product.mdc"
  ".cursor/rules/03-android.mdc"
  ".cursor/rules/04-auditor.mdc"
)

for file in "${LEGACY_FILES[@]}"; do
  if [[ -f "$ROOT/$file" ]]; then
    echo "HATA: Eski ajan dosyası — $file (silinmeli)"
    ERRORS=$((ERRORS + 1))
  fi
done

if [[ -f "$ROOT/docs/33-LAYER-ARCHITECTURE.md" ]]; then
  for i in $(seq 0 32); do
    if ! grep -q "KATMAN $i" "$ROOT/docs/33-LAYER-ARCHITECTURE.md"; then
      echo "HATA: 33-LAYER-ARCHITECTURE.md içinde KATMAN $i eksik"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi

if command -v rg &>/dev/null; then
  if rg -l 'Text\("[^"]*[çğıöşüÇĞİÖŞÜ][^"]*"\)' --glob '*.kt' "$ROOT" 2>/dev/null | grep -q .; then
    echo "HATA: Hard-coded Türkçe string — i18n kullanın (Katman 3/6 ihlali)."
    ERRORS=$((ERRORS + 1))
  fi
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Doğrulama BAŞARISIZ ($ERRORS hata)"
  exit 1
fi

echo "==> Doğrulama başarılı."
