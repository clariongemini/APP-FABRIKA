#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TPL="$ROOT/templates/YAPILACAKLAR.template.md"
OUT="$ROOT/YAPILACAKLAR.md"
FACTORY_VERSION="2.0.0-reasoning-alpha"
DATE="$(date +%Y-%m-%d)"

APP_NAME="Factory"
PACKAGE_NAME="com.ulas.factory"

if [[ -f "$ROOT/.factory/project.json" ]]; then
  APP_NAME="$(python3 -c "import json; print(json.load(open('$ROOT/.factory/project.json'))['app_name'])")"
  PACKAGE_NAME="$(python3 -c "import json; print(json.load(open('$ROOT/.factory/project.json'))['package_name'])")"
fi

if [[ ! -f "$TPL" ]]; then
  echo "HATA: template missing: $TPL"
  exit 1
fi

sed -e "s/{{APP_NAME}}/$APP_NAME/g" \
    -e "s/{{PACKAGE_NAME}}/$PACKAGE_NAME/g" \
    -e "s/{{DATE}}/$DATE/g" \
    -e "s/{{FACTORY_VERSION}}/$FACTORY_VERSION/g" \
    "$TPL" > "$OUT"

if [[ $# -gt 0 ]]; then
  python3 "$ROOT/scripts/governance/init-yapilacaklar.py" --prompt "$*"
fi

python3 "$ROOT/scripts/governance/validate-yapilacaklar.py"
echo "   📋 YAPILACAKLAR.md → $OUT"
