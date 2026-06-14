#!/usr/bin/env bash
# v2.2 — Transcript / handoff dosyalarında reasoning XML bütünlüğü (yalnızca ```xml``` blokları).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0
TAGS=(thinking architecture_check negative_constraints)

scan_file() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  local rel="${file#$ROOT/}"
  if ! python3 - "$file" "${TAGS[@]}" <<'PY'
import re, sys
path, *tags = sys.argv[1:]
text = open(path, encoding="utf-8").read()
blocks = re.findall(r"```xml\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
if not blocks:
    sys.exit(0)
failed = False
for i, block in enumerate(blocks, 1):
    for tag in tags:
        opens = len(re.findall(rf"<{tag}>", block))
        closes = len(re.findall(rf"</{tag}>", block))
        if opens != closes or (opens == 0 and closes > 0):
            print(f"HATA: {path} blok {i} <{tag}> dengesiz open={opens} close={closes}")
            failed = True
if failed:
    sys.exit(1)
PY
  then
    echo "HATA: transcript XML — $rel"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✅ $rel"
  fi
}

echo "==> Reasoning transcript XML doğrulama (v2.2)"

# Bilinçli geçerli fixture
scan_file "$ROOT/test/fixtures/reasoning-transcript-valid.md"

# Opsiyonel: CLI argümanları (agent transcript export)
for arg in "$@"; do
  [[ -f "$arg" ]] && scan_file "$arg"
done

# Snapshot handoff markdown (varsa)
if [[ -d "$ROOT/.cursor/snapshots" ]]; then
  while IFS= read -r -d '' f; do
    scan_file "$f"
  done < <(find "$ROOT/.cursor/snapshots" -name '*.md' -print0 2>/dev/null || true)
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Transcript XML doğrulama BAŞARISIZ ($ERRORS)"
  exit 1
fi

echo "==> Transcript XML doğrulama başarılı."
exit 0
