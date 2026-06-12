#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

check_file() { [[ -f "$ROOT/$1" ]]; }

TOTAL=0

report() {
  local name="$1"
  local got="$2"
  local max="$3"
  local pct=$((got * 10 / max))
  [[ $pct -gt 10 ]] && pct=10
  printf "  %-28s %2d/10\n" "$name" "$pct"
  TOTAL=$((TOTAL + pct))
}

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Ulas Autonomous Android APP Factory — KUSURSUZLUK v0.5  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 1. AI Orkestrasyon & Vizyon
c=0
for f in .cursorrules AGENTS.md docs/33-LAYER-MANIFEST.yaml docs/33-LAYER-ARCHITECTURE.md docs/BOOTSTRAP.md; do
  check_file "$f" && c=$((c + 1))
done
for a in 01-product-cpo 02-architect 03-android-elite 04-auditor-security 05-oem-compat-auditor 06-mcp-orchestrator; do
  check_file ".cursor/rules/${a}.mdc" && c=$((c + 1))
done
report "AI Orkestrasyon & Vizyon" $c 10

# 2. 33 Katman
c=0
bash "$ROOT/scripts/audit-layers.sh" &>/dev/null && c=$((c + 5))
bash "$ROOT/scripts/audit-layer-components.sh" &>/dev/null && c=$((c + 5))
report "33 Katman (360 bileşen)" $c 10

# 3. Kullanışlılık
c=0
for s in init-new-app sync-standards scaffold-android-project install-git-hooks factory-health first-setup check-mcp; do
  [[ -x "$ROOT/scripts/${s}.sh" ]] && c=$((c + 1))
done
check_file ".cursor/mcp.required.json" && c=$((c + 1))
check_file "docs/MCP_SETUP.md" && c=$((c + 1))
check_file ".cursor/rules/06-mcp-orchestrator.mdc" && c=$((c + 1))
report "Kullanışlılık (DX)" $c 10

# 4. Kod Tasarımı
c=0
check_file "docs/02-ARCHITECTURE/ANDROID_STRUCTURE.md" && c=$((c + 2))
check_file "templates/architecture/MODULE_MAP.template.md" && c=$((c + 2))
bash "$ROOT/scripts/audit-android-scaffold.sh" &>/dev/null && c=$((c + 6))
report "Kod Tasarımı / Mimari" $c 10

# 5. UI / Compose
c=0
check_file "docs/03-STANDARDS/LIQUID_GLASS.md" && c=$((c + 3))
check_file "templates/android/project/core/designsystem/src/main/java/{{PACKAGE_PATH}}/core/designsystem/theme/Theme.kt" && c=$((c + 3))
check_file "templates/android/project/core/designsystem/src/main/java/{{PACKAGE_PATH}}/core/designsystem/component/GlassCard.kt" && c=$((c + 2))
check_file "templates/android/project/app/src/main/assets/locales/tr.json" && c=$((c + 1))
check_file "templates/android/project/app/src/main/assets/locales/en.json" && c=$((c + 1))
report "UI / Liquid Glass / i18n" $c 10

# 6. Güvenlik
c=0
check_file "docs/03-STANDARDS/SECURITY.md" && c=$((c + 2))
check_file "docs/03-STANDARDS/PRIVACY.md" && c=$((c + 2))
check_file "docs/03-STANDARDS/PENTEST.md" && c=$((c + 2))
bash "$ROOT/scripts/audit-security.sh" &>/dev/null && c=$((c + 2))
check_file "templates/android/project/core/security/src/main/java/{{PACKAGE_PATH}}/core/security/RootDetector.kt" && c=$((c + 1))
check_file "templates/architecture/PENTEST_CHECKLIST.template.md" && c=$((c + 1))
report "Güvenlik & Gizlilik" $c 10

# 7. Arka Plan & FCM
c=0
check_file "docs/03-STANDARDS/BACKGROUND_PROCESSING.md" && c=$((c + 3))
check_file "docs/03-STANDARDS/FCM_PUSH.md" && c=$((c + 2))
check_file "templates/android/project/app/src/main/java/{{PACKAGE_PATH}}/push/AppFirebaseMessagingService.kt" && c=$((c + 3))
check_file "templates/android/core-oem/SyncWorker.kt" && c=$((c + 2))
report "Arka Plan & FCM" $c 10

# 8. OEM
c=0
bash "$ROOT/scripts/audit-oem-compat.sh" &>/dev/null && c=$((c + 5))
check_file "docs/03-STANDARDS/OEM_MATRIX.yaml" && c=$((c + 3))
check_file "templates/architecture/OEM_TEST_REPORT.template.md" && c=$((c + 2))
report "OEM / ROM (Samsung MIUI)" $c 10

# 9. Monetizasyon
c=0
check_file "docs/03-STANDARDS/MONETIZATION_TECH.md" && c=$((c + 3))
check_file "docs/03-STANDARDS/PLAY_INTEGRITY.md" && c=$((c + 2))
check_file "templates/android/project/feature/premium/src/main/java/{{PACKAGE_PATH}}/feature/premium/data/BillingRepository.kt" && c=$((c + 3))
check_file "templates/android/project/core/security/src/main/java/{{PACKAGE_PATH}}/core/security/PlayIntegrityChecker.kt" && c=$((c + 2))
report "Monetizasyon & Integrity" $c 10

# 10. Test & CI
c=0
check_file "docs/03-STANDARDS/TESTING.md" && c=$((c + 2))
check_file "templates/android/project/.maestro/flows/smoke.yaml" && c=$((c + 3))
check_file "templates/android/project/.github/workflows/android-build.yml" && c=$((c + 2))
check_file ".github/workflows/validate.yml" && c=$((c + 2))
bash "$ROOT/scripts/audit-android-scaffold.sh" &>/dev/null && c=$((c + 1))
report "Test & CI/CD" $c 10

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "  GENEL TOPLAM: %d / 100\n" "$TOTAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $TOTAL -eq 100 ]]; then
  echo "  Durum: ✅ KUSURSUZ — Tüm kategoriler tam puan."
else
  echo "  Durum: Eksik kategori var — yukarıdaki tabloya bakın."
fi

exit 0
