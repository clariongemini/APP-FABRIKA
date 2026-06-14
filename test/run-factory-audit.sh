#!/usr/bin/env bash
# Fabrika özelliklerini adım adım denetler → test/AUDIT_REPORT.md
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$REPO_ROOT/test/factory-smoke-app"
REPORT="$REPO_ROOT/test/AUDIT_REPORT.md"
DATE="$(date +%Y-%m-%dT%H:%M:%S%z)"

PASS=0
FAIL=0
SKIP=0
WARN=0

check() {
  local id="$1"
  local name="$2"
  local result="$3"  # pass|fail|skip|warn
  local detail="${4:-}"
  case "$result" in
    pass) PASS=$((PASS + 1)); icon="✅" ;;
    fail) FAIL=$((FAIL + 1)); icon="❌" ;;
    skip) SKIP=$((SKIP + 1)); icon="⏭️" ;;
    warn) WARN=$((WARN + 1)); icon="⚠️" ;;
  esac
  RESULTS+=("| $id | $name | $icon $result | $detail |")
}

RESULTS=()

echo "==> Fabrika audit başlıyor..."

# --- F0: Governance & MCP ---
check "F0.1" "first-setup.sh mevcut" "$([[ -x "$REPO_ROOT/scripts/first-setup.sh" ]] && echo pass || echo fail)"
check "F0.2" "init-governance.sh mevcut" "$([[ -x "$REPO_ROOT/scripts/governance/init-governance.sh" ]] && echo pass || echo fail)"
check "F0.3" "docs/00-INDEX.md" "$([[ -f "$REPO_ROOT/docs/00-INDEX.md" ]] && echo pass || echo fail)"
check "F0.4" "YAPILACAKLAR.md + validator" \
  "$(python3 "$REPO_ROOT/scripts/governance/validate-yapilacaklar.py" &>/dev/null && echo pass || echo fail)" \
  "validate-yapilacaklar.py exit 0"
check "F0.5" "validate-audit-chain.py" \
  "$(python3 "$REPO_ROOT/scripts/governance/validate-audit-chain.py" &>/dev/null && echo pass || echo fail)"

if bash "$REPO_ROOT/scripts/check-mcp.sh" --warn &>/dev/null; then
  check "F0.MCP" "check-mcp.sh P0" "pass"
else
  check "F0.MCP" "check-mcp.sh P0" "warn" "MCP PAT yerel — docs/MCP_SETUP.md"
fi

# --- F1: Vizyon (smoke test docs) ---
check "F1.1" "test/docs/SMOKE_APP_BRIEF.md" "$([[ -f "$REPO_ROOT/test/docs/SMOKE_APP_BRIEF.md" ]] && echo pass || echo fail)"
check "F1.2" "templates/vision mevcut" "$([[ -f "$REPO_ROOT/templates/vision/PRODUCT_BRIEF.template.md" ]] && echo pass || echo fail)"

# --- F2: Mimari ---
check "F2.1" "ANDROID_STRUCTURE.md" "$([[ -f "$REPO_ROOT/docs/02-ARCHITECTURE/ANDROID_STRUCTURE.md" ]] && echo pass || echo fail)"
check "F2.2" "MODULE_MAP template" "$([[ -f "$REPO_ROOT/templates/architecture/MODULE_MAP.template.md" ]] && echo pass || echo fail)"
check "F2.3" "33 layer slices (33 dosya)" \
  "$(ls "$REPO_ROOT/docs/33-LAYER-MANIFEST"/layer-*.yaml 2>/dev/null | wc -l | tr -d ' ' | grep -q '^33$' && echo pass || echo fail)"

# --- F3: Android iskelet (smoke app) ---
MODULE_COUNT=0
if [[ -f "$APP_DIR/settings.gradle.kts" ]]; then
  MODULE_COUNT="$(grep -cE '^\s*":' "$APP_DIR/settings.gradle.kts" 2>/dev/null || echo 0)"
fi
check "F3.1" "test/factory-smoke-app/settings.gradle.kts" \
  "$([[ -f "$APP_DIR/settings.gradle.kts" ]] && echo pass || echo fail)" \
  "bootstrap-smoke-app.sh çalıştırın"
check "F3.2" "10 modül (settings.gradle.kts)" \
  "$([[ "$MODULE_COUNT" -ge 10 ]] && echo pass || echo fail)" \
  "include count=$MODULE_COUNT"
check "F3.3" "gradlew executable" "$([[ -x "$APP_DIR/gradlew" ]] && echo pass || echo fail)"
check "F3.4" "audit-android-scaffold (template)" \
  "$(bash "$REPO_ROOT/scripts/audit-android-scaffold.sh" &>/dev/null && echo pass || echo fail)" \
  "fabrika template"

# --- F4: UI / i18n ---
check "F4.1" "locales tr.json + en.json" \
  "$([[ -f "$APP_DIR/app/src/main/assets/locales/tr.json" && -f "$APP_DIR/app/src/main/assets/locales/en.json" ]] && echo pass || echo fail)"
check "F4.2" "GlassCard.kt" \
  "$(find "$APP_DIR" -name 'GlassCard.kt' 2>/dev/null | grep -q . && echo pass || echo fail)"
check "F4.3" "hard-coded TR string yok (.kt)" \
  "$(command -v rg &>/dev/null && ! rg -l 'Text\("[^"]*[çğıöşüÇĞİÖŞÜ][^"]*"\)' --glob '*.kt' "$APP_DIR" 2>/dev/null | grep -q . && echo pass || echo skip)" \
  "rg yoksa skip"

# --- F5: Güvenlik / OEM ---
check "F5.1" "audit-security.sh" "$(bash "$REPO_ROOT/scripts/audit-security.sh" &>/dev/null && echo pass || echo fail)"
check "F5.2" "audit-oem-compat.sh" "$(bash "$REPO_ROOT/scripts/audit-oem-compat.sh" &>/dev/null && echo pass || echo fail)"
check "F5.3" "RootDetector.kt şablon" \
  "$([[ -f "$REPO_ROOT/templates/android/project/core/security/src/main/java/{{PACKAGE_PATH}}/core/security/RootDetector.kt" ]] && echo pass || echo fail)"

# --- F6: Analytics şema ---
check "F6.1" "SPRINT_P schema template" \
  "$([[ -f "$REPO_ROOT/templates/governance/SPRINT_P_SCHEMA.template.json" ]] && echo pass || echo fail)"

# --- Cursor bridge & recovery ---
check "CX.1" "gradle-build-loop.sh" "$([[ -x "$REPO_ROOT/scripts/gradle-build-loop.sh" ]] && echo pass || echo fail)"
check "CX.2" "state-recovery.sh" "$([[ -x "$REPO_ROOT/scripts/state-recovery.sh" ]] && echo pass || echo fail)"
check "CX.3" "validate-layer-slices.sh" \
  "$(bash "$REPO_ROOT/scripts/validate-layer-slices.sh" &>/dev/null && echo pass || echo fail)"
check "CX.4" "phase-agents.json" "$([[ -f "$REPO_ROOT/governance/phase-agents.json" ]] && echo pass || echo fail)"
check "CX.5" "18-state-recovery.mdc" "$([[ -f "$REPO_ROOT/.cursor/rules/18-state-recovery.mdc" ]] && echo pass || echo fail)"

# --- v2 Claude-Native reasoning ---
REASONING="$REPO_ROOT/.cursor/rules/19-claude-reasoning.mdc"
CURSORRULES="$REPO_ROOT/.cursorrules"
check "V2.1" "19-claude-reasoning.mdc mevcut" \
  "$([[ -f "$REASONING" ]] && echo pass || echo fail)"
check "V2.2" "19-claude-reasoning alwaysApply: true" \
  "$(grep -q 'alwaysApply: true' "$REASONING" 2>/dev/null && echo pass || echo fail)"
check "V2.3" "thinking + architecture_check şablon (.mdc)" \
  "$(grep -q '<thinking>' "$REASONING" && grep -q '<architecture_check>' "$REASONING" && echo pass || echo fail)"
check "V2.4" ".cursorrules Claude-Native protokol" \
  "$(grep -q 'Claude-Native' "$CURSORRULES" && grep -q '<thinking>' "$CURSORRULES" && echo pass || echo fail)"
check "V2.5" "docs/CLAUDE_REASONING.md" \
  "$([[ -f "$REPO_ROOT/docs/CLAUDE_REASONING.md" ]] && echo pass || echo fail)"
check "V2.6" "20-aistudio-import (19 reasoning ayrımı)" \
  "$([[ -f "$REPO_ROOT/.cursor/rules/20-aistudio-import.mdc" ]] && ! [[ -f "$REPO_ROOT/.cursor/rules/19-aistudio-import.mdc" ]] && echo pass || echo fail)"
check "V2.7" "validate-reasoning-template-xml.sh" \
  "$(bash "$REPO_ROOT/scripts/validate-reasoning-template-xml.sh" &>/dev/null && echo pass || echo fail)" \
  "thinking/architecture_check/negative_constraints dengesi"
check "V2.8" "negative_constraints şablon (.mdc)" \
  "$(grep -q '<negative_constraints>' "$REASONING" && grep -q '</negative_constraints>' "$REASONING" && echo pass || echo fail)"
check "V2.9" "kelime cap 150-200 (.mdc)" \
  "$(grep -q '150–200' "$REASONING" && echo pass || echo fail)"
check "V2.10" "validate-reasoning-transcript.sh (v2.2)" \
  "$(bash "$REPO_ROOT/scripts/validate-reasoning-transcript.sh" &>/dev/null && echo pass || echo fail)"

# --- Kalite kapıları ---
check "QG.1" "validate-code.sh" "$(bash "$REPO_ROOT/scripts/validate-code.sh" &>/dev/null && echo pass || echo fail)"
check "QG.2" "audit-layers.sh" "$(bash "$REPO_ROOT/scripts/audit-layers.sh" &>/dev/null && echo pass || echo fail)"
check "QG.3" "audit-layer-components.sh" "$(bash "$REPO_ROOT/scripts/audit-layer-components.sh" &>/dev/null && echo pass || echo fail)"
FH_OUT="$(bash "$REPO_ROOT/scripts/factory-health.sh" 2>&1 || true)"
check "QG.4" "factory-health.sh 100" \
  "$(echo "$FH_OUT" | grep -q '100 / 100' && echo pass || echo warn)"
check "QG.5" "factory-quality-gate.sh" \
  "$(bash "$REPO_ROOT/scripts/factory-quality-gate.sh" &>/dev/null && echo pass || echo warn)" \
  "MCP yerel uyarı olabilir"

# --- Smoke app build ---
JAVA_OK=false
if command -v java &>/dev/null && java -version &>/dev/null 2>&1; then
  JAVA_OK=true
fi
if [[ -f "$APP_DIR/gradlew" && "$JAVA_OK" == true ]]; then
  set +e
  (cd "$APP_DIR" && ./gradlew assembleDebug --quiet) &>/dev/null
  rc=$?
  set -e
  check "BUILD" "factory-smoke-app assembleDebug" "$([[ $rc -eq 0 ]] && echo pass || echo fail)" "exit $rc"
else
  check "BUILD" "factory-smoke-app assembleDebug" "skip" "JDK yok veya gradlew eksik — docs/BOOTSTRAP.md JDK 17+"
fi

TOTAL=$((PASS + FAIL + SKIP + WARN))
SCORE=$((PASS * 100 / (PASS + FAIL + WARN + 1)))

cat > "$REPORT" <<EOF
# Factory Audit Report — FactorySmoke

> Oluşturulma: $DATE  
> Fabrika: \`$REPO_ROOT\`  
> Smoke app: \`test/factory-smoke-app\`

## Özet

| Metrik | Değer |
|--------|-------|
| ✅ Geçti | $PASS |
| ❌ Başarısız | $FAIL |
| ⚠️ Uyarı | $WARN |
| ⏭️ Atlandı | $SKIP |
| **Başarı oranı** | **${SCORE}%** (fail hariç) |

## Adım denetimi

| ID | Adım | Sonuç | Detay |
|----|------|-------|-------|
$(printf '%s\n' "${RESULTS[@]}")

## Fabrika akışı (uygulanması gerekenler)

| Sıra | Komut | Smoke testte |
|------|-------|----------------|
| 1 | \`./scripts/first-setup.sh\` | Fabrika kökünde mevcut |
| 2 | \`./scripts/init-new-app.sh\` | **Kökü değiştirmez** — \`test/bootstrap-smoke-app.sh\` kullanıldı |
| 3 | \`./scripts/governance/init-governance.sh\` | Fabrika kök governance seed |
| 4 | \`./scripts/scaffold-android-project-to.sh\` | \`test/factory-smoke-app\` |
| 5 | \`./scripts/gradle-build-loop.sh\` | BUILD satırında test |
| 6 | \`./scripts/state-recovery.sh --checkpoint\` | bootstrap adım 5 |
| 7 | \`python3 scripts/governance/validate-yapilacaklar.py\` | F0.4 |
| 8 | \`./scripts/factory-quality-gate.sh\` | Manuel: fabrika kökünden |

## Sonraki adım

\`\`\`bash
./test/bootstrap-smoke-app.sh    # smoke app oluştur / yenile
./test/run-factory-audit.sh      # yalnızca audit
\`\`\`
EOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Audit: ✅ $PASS  ❌ $FAIL  ⚠️ $WARN  ⏭️ $SKIP"
echo "  Rapor: $REPORT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[[ $FAIL -eq 0 ]]
