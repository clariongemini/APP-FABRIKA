#!/usr/bin/env bash
# CEO V5 — Product Reality Enforcement (22-step cycle)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
FAST=false
if [[ "${1:-}" == "--fast" ]]; then
  FAST=true
fi

if [[ -d .venv-scraper/bin ]]; then
  # shellcheck disable=SC1091
  source .venv-scraper/bin/activate
fi

step() { echo ""; echo "━━━ Step $1: $2 ━━━"; }

echo "==> CEO cycle — product reality enforcement"
echo "Mode: $( $FAST && echo FAST || echo FULL )"
echo "Principle: No Feature Left Behind — agent freeze active"

# 1 Market
step 1 "Market Intelligence"
if $FAST; then
  echo "   ⏭ FAST — existing market outputs"
else
  ./scripts/scrapers/run_demand_intelligence.sh || true
  python scripts/scrapers/search_intent_analyzer.py || true
  python scripts/scrapers/forum_batch_fetch.py || true
  python scripts/scrapers/analyze_user_intent.py || true
  python scripts/scrapers/generate_market_report.py || true
  python scripts/trends/validate_trends_outputs.py || true
fi

# 2-7 Intelligence
step 2 "LIUD"
./scripts/linguistic/run_linguistic_intelligence.sh

step 3 "CIKA"
./scripts/curriculum/run_curriculum_intelligence.sh

step 4 "CLID"
python scripts/clinical/build_clid_output.py

step 5 "AID"
python scripts/analytics/build_aid_output.py

step 6 "LID"
python scripts/localization/build_lid_output.py

step 7 "FID"
python scripts/finance/build_fid_output.py

# 8-11 Decision + Delivery
step 8 "PDC"
./scripts/product_decision/run_product_decision_council.sh

step 9 "CAO Audit"
python scripts/cao/run_cao_audit.py

step 10 "CDID — Work Package Engine"
python scripts/cdid/run_cdid_cycle.py

step 11 "CEC — Execution Alignment"
python scripts/execution/run_cec_audit.py

step 12 "CDID — Auto Escalation"
python scripts/cdid/run_cdid_cycle.py --post-cec

step 13 "Product Reality Layer (V5)"
python scripts/reality/run_product_reality_layer.py

# 14-18 Factory
step 14 "CPO (Factory)"
echo "   📋 Consume CDID WPs + PDC roadmap"

step 15 "Architect (Factory)"
if [[ -x scripts/check-architecture.sh ]]; then
  scripts/check-architecture.sh && echo "   ✅ Architecture" || echo "   ⚠ Architecture issues"
fi

step 16 "Android (Factory)"
echo "   📋 Execute pending CDID WPs — F002 priority"

step 17 "Security (Factory)"
if [[ -x scripts/validate-code.sh ]]; then
  scripts/validate-code.sh >/dev/null 2>&1 && echo "   ✅ validate-code" || echo "   ⚠ validate-code issues"
fi

step 18 "OEM (Factory)"
if [[ -x scripts/audit-oem-compat.sh ]]; then
  scripts/audit-oem-compat.sh >/dev/null 2>&1 && echo "   ✅ OEM audit" || echo "   ⚠ OEM issues"
fi

# 19-22 Governance
step 19 "CEO Master Report"
python scripts/ceo/build_ceo_master_report.py

step 20 "CSGB Strategic Governance Review"
python scripts/ceo/build_strategic_governance_review.py

step 21 "EGC — Executive Governance Council"
python scripts/egc/run_egc_governance_cycle.py

step 22 "CEO Autonomous + Reality Reports"
python scripts/ceo/build_ceo_autonomous_report.py

echo ""
echo "==> CEO cycle tamamlandı"
echo "  Reality: governance/executive/CEO_PRODUCT_REALITY_REPORT.md"
echo "  Binding: governance/egc/EGC_VERDICT.json"
