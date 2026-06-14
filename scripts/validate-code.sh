#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ERRORS=0

echo "==> Kod doğrulama"

REQUIRED_FILES=(
  ".cursorrules"
  "README.md"
  "LICENSE"
  ".gitignore"
  "AGENTS.md"
  "templates/YAPILACAKLAR.template.md"
  ".cursor/rules/00-overmind-zero-hallucination.mdc"
  ".cursor/rules/01-product-cpo.mdc"
  ".cursor/rules/02-architect.mdc"
  ".cursor/rules/03-android-elite.mdc"
  ".cursor/rules/04-auditor-security.mdc"
  ".cursor/rules/05-oem-compat-auditor.mdc"
  ".cursor/rules/06-mcp-orchestrator.mdc"
  ".cursor/rules/07-linguistic-intelligence.mdc"
  ".cursor/rules/08-curriculum-intelligence.mdc"
  ".cursor/rules/09-product-decision-council.mdc"
  ".cursor/rules/10-mavi-okyanus.mdc"
  ".cursor/rules/11-ceo-agent.mdc"
  ".cursor/rules/12-chief-audit-officer.mdc"
  ".cursor/rules/13-chief-execution-council.mdc"
  ".cursor/rules/14-executive-governance-council.mdc"
  ".cursor/rules/15-chief-delivery-intelligence.mdc"
  ".cursor/rules/16-analytics-intelligence.mdc"
  ".cursor/rules/17-marketing-growth.mdc"
  ".cursor/mcp.required.json"
  ".cursor/mcp.json.example"
  ".cursor/skills/zero-hallucination/SKILL.md"
  ".cursor/skills/yapilacaklar-planner/SKILL.md"
  ".cursor/skills/yapilacaklar-executor/SKILL.md"
  ".cursor/skills/hierarchical-audit/SKILL.md"
  ".cursor/commands/baslat.md"
  ".cursor/commands/devam-et.md"
  ".cursor/commands/denetle.md"
  "docs/MCP_SETUP.md"
  "docs/GITHUB_REPO_DESCRIPTION.md"
  "docs/EXECUTIVE_OS.md"
  "docs/YAPILACAKLAR_SISTEMI.md"
  "scripts/first-setup.sh"
  "scripts/check-mcp.sh"
  "scripts/run-ceo-cycle.sh"
  "scripts/init-governance.sh"
  "scripts/agent-approval-gate.sh"
  "scripts/governance/init-governance.sh"
  "scripts/governance/validate-audit-chain.py"
  "scripts/governance/validate-yapilacaklar.py"
  "scripts/ceo/run_ceo_cycle.sh"
  "governance/executive/CEO_OPERATING_SYSTEM.md"
  "governance/executive/HIERARCHICAL_AUDIT_CHAIN.md"
  "governance/executive/AGENT_APPROVAL_PROTOCOL.md"
  "governance/market/DEPARTMENT_CHARTER.md"
  "scripts/validate-factory-version.sh"
  "scripts/bootstrap-gradle-wrapper.sh"
  "scripts/validate-android-template.sh"
  "scripts/setup-mcp.sh"
  "scripts/factory-quality-gate.sh"
  "scripts/gradle-build-loop.sh"
  "scripts/run-maestro.sh"
  "scripts/state-recovery.sh"
  "docs/CURSOR_TERMINAL_BRIDGE.md"
  "docs/STATE_RECOVERY.md"
  ".cursor/rules/18-state-recovery.mdc"
  ".cursor/snapshots/RECOVERY.template.json"
  ".cursor/snapshots/README.md"
  ".cursor/snapshots/HANDOFF.template.json"
  "scripts/governance/validate-factory-governance.sh"
  "governance/FACTORY_REPO_POLICY.md"
  "governance/README.md"
  "templates/governance/SPRINT_LOCK.template.json"
  "templates/governance/APPROVAL_QUEUE.template.md"
  "docs/03-STANDARDS/OEM_COMPATIBILITY.md"
  "docs/03-STANDARDS/OEM_MATRIX.yaml"
  "docs/03-STANDARDS/SECURITY.md"
  "docs/03-STANDARDS/PRIVACY.md"
  "docs/03-STANDARDS/BACKGROUND_PROCESSING.md"
  "docs/03-STANDARDS/MONETIZATION_TECH.md"
  "docs/RELEASE_CHECKLIST.md"
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
  "docs/33-LAYER-MANIFEST/README.md"
  "docs/CURSOR_CONTEXT_BUDGET.md"
  "governance/phase-agents.json"
  "scripts/split-layer-manifest.py"
  "scripts/validate-layer-slices.sh"
  "scripts/bootstrap-external-project.sh"
  "docs/AI_STUDIO_IMPORT.md"
  ".cursor/rules/19-claude-reasoning.mdc"
  "scripts/validate-reasoning-template-xml.sh"
  "scripts/validate-reasoning-transcript.sh"
  "scripts/audit-module-map.sh"
  "docs/FACTORY_META/README.md"
  "docs/FACTORY_META/PRODUCT_BRIEF.md"
  "docs/CLAUDE_REASONING.md"
  ".cursor/rules/20-aistudio-import.mdc"
  ".cursor/commands/import-aistudio.md"
  "scripts/scaffold-android-project-to.sh"
  "test/bootstrap-smoke-app.sh"
  "test/run-factory-audit.sh"
  "test/README.md"
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

# Wrapper scripts must be executable
for script in run-ceo-cycle init-governance agent-approval-gate gradle-build-loop run-maestro state-recovery scaffold-android-project-to bootstrap-external-project validate-factory-version validate-reasoning-template-xml validate-reasoning-transcript verify-environment; do
  if [[ ! -x "$ROOT/scripts/${script}.sh" ]]; then
    echo "HATA: Çalıştırılabilir değil — scripts/${script}.sh"
    ERRORS=$((ERRORS + 1))
  fi
done

# No duplicate 05-marketing (renamed to 17)
if [[ -f "$ROOT/.cursor/rules/05-marketing-growth.mdc" ]]; then
  echo "HATA: Eski Growth kuralı — 05-marketing-growth.mdc (17 olmalı)"
  ERRORS=$((ERRORS + 1))
fi

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

if git -C "$ROOT" rev-parse --git-dir &>/dev/null; then
  if git -C "$ROOT" ls-files | grep -q 'snapshots/recovery/'; then
    echo "HATA: Runtime recovery snapshot commit edilmiş — gitignore + git rm --cached"
    ERRORS=$((ERRORS + 1))
  fi
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Doğrulama BAŞARISIZ ($ERRORS hata)"
  exit 1
fi

echo "==> Doğrulama başarılı."