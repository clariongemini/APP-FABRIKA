#!/usr/bin/env bash
# Bootstrap full Executive OS for a Factory project (generic seeds, not live Konuşma data).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TPL="$ROOT/templates/governance"
GOV="$ROOT/governance"

APP_NAME="${1:-}"
PACKAGE_NAME="${2:-}"
SLUG="${3:-}"
DATE="$(date +%Y-%m-%d)"
FACTORY_VERSION="1.0.0"

if [[ -z "$APP_NAME" || -z "$PACKAGE_NAME" ]]; then
  if [[ -f "$ROOT/.factory/project.json" ]]; then
    APP_NAME="$(python3 -c "import json; print(json.load(open('$ROOT/.factory/project.json'))['app_name'])")"
    PACKAGE_NAME="$(python3 -c "import json; print(json.load(open('$ROOT/.factory/project.json'))['package_name'])")"
    SLUG="$(python3 -c "import json; print(json.load(open('$ROOT/.factory/project.json')).get('slug','app'))")"
  else
    echo "Usage: $0 <AppName> <com.pkg.app> [slug]"
    exit 1
  fi
fi
SLUG="${SLUG:-$(echo "$APP_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')}"

subst() { sed -e "s/{{APP_NAME}}/$APP_NAME/g" -e "s/{{PACKAGE_NAME}}/$PACKAGE_NAME/g" -e "s/{{SLUG}}/$SLUG/g" -e "s/{{DATE}}/$DATE/g" -e "s/{{FACTORY_VERSION}}/$FACTORY_VERSION/g" "$1"; }

echo "==> Executive OS full bootstrap: $APP_NAME ($PACKAGE_NAME)"

mkdir -p "$GOV"/{executive,reality,product_decision,execution,analytics,cao,cec,cdid,egc,csgb,audits,memory,market,linguistic,curriculum,blue_ocean,trends}
mkdir -p "$GOV/analytics/output" "$GOV/cao" "$GOV/execution"

# Project config + sprint lock (always refresh from templates)
subst "$TPL/project.config.template.json" > "$GOV/project.config.json"
subst "$TPL/SPRINT_LOCK.template.json" > "$GOV/executive/SPRINT_LOCK.json"
subst "$TPL/roadmap_priorities.template.json" > "$GOV/product_decision/roadmap_priorities.json"
subst "$TPL/SPRINT_P_ACTIVATION_GATE.template.json" > "$GOV/analytics/SPRINT_P_ACTIVATION_GATE.json"
subst "$TPL/APPROVAL_QUEUE.template.md" > "$GOV/executive/APPROVAL_QUEUE.md"

PACKAGE_PATH="$(echo "$PACKAGE_NAME" | tr '.' '/')"
export PACKAGE_PATH
subst "$TPL/SPRINT_P_EVENT_CATALOG.template.json" | sed "s|{{PACKAGE_PATH}}|$PACKAGE_PATH|g" > "$GOV/analytics/SPRINT_P_EVENT_CATALOG.json"
subst "$TPL/SPRINT_P_SCHEMA.template.json" > "$GOV/analytics/SPRINT_P_SCHEMA.json"

# Package placeholder in dependency rules (idempotent)
if grep -q '{{PACKAGE_NAME}}' "$GOV/dependency-rules.json" 2>/dev/null; then
  python3 - <<PY
from pathlib import Path
p = Path("$GOV/dependency-rules.json")
p.write_text(p.read_text(encoding="utf-8").replace("{{PACKAGE_NAME}}", "$PACKAGE_NAME"), encoding="utf-8")
PY
fi

# Full generic state (overwrites Konuşma live snapshots if present)
python3 "$ROOT/scripts/governance/seed-governance-state.py" "$APP_NAME" "$PACKAGE_NAME" "$SLUG"

chmod +x "$ROOT/scripts/"*.sh "$ROOT/scripts/ceo/"*.sh 2>/dev/null || true
python3 "$ROOT/scripts/execution/validate_roadmap_consumption.py" 2>/dev/null || true
python3 "$ROOT/scripts/governance/validate-audit-chain.py" 2>/dev/null || true
python3 "$ROOT/scripts/governance/validate-yapilacaklar.py" 2>/dev/null || true

echo ""
echo "   ✅ Full Executive OS seeded for $APP_NAME"
echo "   📋 Hierarchical audit: governance/executive/HIERARCHICAL_AUDIT_CHAIN.md"
echo "   🔄 CEO cycle: ./scripts/ceo/run_ceo_cycle.sh"
