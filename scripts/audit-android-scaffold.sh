#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT/templates/android/project"
ERRORS=0

echo "==> Android Scaffold Şablon Denetimi"

REQUIRED=(
  "settings.gradle.kts"
  "gradle/libs.versions.toml"
  "app/build.gradle.kts"
  "app/src/main/AndroidManifest.xml"
  "app/src/main/assets/locales/tr.json"
  "app/src/main/assets/locales/en.json"
  "core/designsystem/src/main/java/{{PACKAGE_PATH}}/core/designsystem/theme/Theme.kt"
  "core/designsystem/src/main/java/{{PACKAGE_PATH}}/core/designsystem/component/GlassCard.kt"
  "core/oem/src/main/java/{{PACKAGE_PATH}}/core/oem/OemCompatFacade.kt"
  "core/security/src/main/java/{{PACKAGE_PATH}}/core/security/RootDetector.kt"
  "feature/home/src/main/java/{{PACKAGE_PATH}}/feature/home/presentation/HomeScreen.kt"
  "feature/premium/src/main/java/{{PACKAGE_PATH}}/feature/premium/data/BillingRepository.kt"
  "app/src/main/java/{{PACKAGE_PATH}}/push/AppFirebaseMessagingService.kt"
  ".maestro/flows/smoke.yaml"
  ".github/workflows/android-build.yml"
)

for f in "${REQUIRED[@]}"; do
  if [[ ! -f "$TEMPLATE/$f" ]]; then
    echo "HATA: Scaffold eksik — $f"
    ERRORS=$((ERRORS + 1))
  fi
done

MODULES=(common designsystem i18n database network security oem)
for m in "${MODULES[@]}"; do
  [[ -f "$TEMPLATE/core/$m/build.gradle.kts" ]] || { echo "HATA: core/$m/build.gradle.kts"; ERRORS=$((ERRORS + 1)); }
done

for m in home settings premium; do
  [[ -f "$TEMPLATE/feature/$m/build.gradle.kts" ]] || { echo "HATA: feature/$m/build.gradle.kts"; ERRORS=$((ERRORS + 1)); }
done

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Scaffold denetimi BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Android scaffold şablonu eksiksiz ($((${#REQUIRED[@]})) kritik dosya)."
