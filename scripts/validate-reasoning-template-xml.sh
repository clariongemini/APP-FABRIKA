#!/usr/bin/env bash
# Şablon ```xml``` bloklarında reasoning etiket bütünlüğü (açılış = kapanış).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

check_file() {
  local file="$1"
  shift
  local tags=("$@")
  if [[ ! -f "$file" ]]; then
    echo "HATA: dosya yok — $file"
    ERRORS=$((ERRORS + 1))
    return
  fi
  local rel="${file#$ROOT/}"
  if ! python3 - "$file" "${tags[@]}" <<'PY'
import re, sys
path, *tags = sys.argv[1:]
text = open(path, encoding="utf-8").read()
blocks = re.findall(r"```xml\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
if not blocks:
    print(f"HATA: ```xml``` şablon bloğu yok ({path})")
    sys.exit(1)
failed = False
for i, block in enumerate(blocks, 1):
    for tag in tags:
        opens = len(re.findall(rf"<{tag}>", block))
        closes = len(re.findall(rf"</{tag}>", block))
        if opens != closes or opens == 0:
            print(f"HATA: blok {i} <{tag}> dengesiz — open={opens} close={closes} ({path})")
            failed = True
if failed:
    sys.exit(1)
PY
  then
    echo "HATA: XML şablon dengesi — $rel"
    ERRORS=$((ERRORS + 1))
  fi
}

echo "==> Reasoning şablon XML doğrulama"

REASONING="$ROOT/.cursor/rules/19-claude-reasoning.mdc"
check_file "$REASONING" thinking architecture_check negative_constraints
check_file "$ROOT/docs/CLAUDE_REASONING.md" thinking architecture_check negative_constraints

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Reasoning XML doğrulama BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Reasoning şablon XML doğrulama başarılı."
