#!/usr/bin/env bash
# AI için minimal bağlam derler — tüm repoyu okumaz; token bütçesine uygun özet.
# Kullanım: ./assemble-svos-context.sh [venture-slug]
set -euo pipefail

SVOS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$SVOS/.." && pwd)"
SLUG="${1:-}"

if [[ -z "$SLUG" ]]; then
  SLUG="$(ls "$SVOS/08-ventures" 2>/dev/null | head -1 || true)"
fi

if [[ -z "$SLUG" ]]; then
  echo "Kullanım: $0 <venture-slug>" >&2
  exit 1
fi

OUT_DIR="$SVOS/10-runtime/context/$SLUG"
OUT_FILE="$OUT_DIR/assembled-context.md"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
mkdir -p "$OUT_DIR"

VENTURE="$SVOS/08-ventures/$SLUG/venture.json"
YAPILACAKLAR="$REPO/YAPILACAKLAR.md"
MATURITY="$SVOS/10-runtime/maturity-report.json"

{
  echo "# SVOS Context — $SLUG"
  echo ""
  echo "assembled_at: $TIMESTAMP"
  echo "token_budget_hint: 8000"
  echo ""
  echo "## Venture charter"
  echo '```json'
  if [[ -f "$VENTURE" ]]; then cat "$VENTURE"; else echo '{}'; fi
  echo '```'
  echo ""
  echo "## Active plan (YAPILACAKLAR)"
  if [[ -f "$YAPILACAKLAR" ]]; then
    head -80 "$YAPILACAKLAR"
  else
    echo "_YAPILACAKLAR.md yok — /baslat veya init-new-app_"
  fi
  echo ""
  echo "## Maturity gaps (top)"
  if [[ -f "$MATURITY" ]]; then
    python3 - "$MATURITY" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
d = json.loads(p.read_text())
for i, g in enumerate(d.get("open_gaps", [])[:8], 1):
    print(f"{i}. [{g['dimension']}] {g['gap']}")
print(f"\nComposite: {d.get('composite_score')}/100")
PY
  else
    echo "_ulas maturity audit henüz çalışmadı_"
  fi
  echo ""
  echo "## Evidence summary"
  MANIFEST="$SVOS/07-evidence/$SLUG/manifest.json"
  if [[ -f "$MANIFEST" ]]; then
    echo '```json'
    cat "$MANIFEST"
    echo '```'
  else
    echo "_manifest yok — bridge-venture.sh $SLUG_"
  fi
  echo ""
  echo "## Dispatch queue (pending)"
  python3 - <<PY
import json
from pathlib import Path
svos = Path("$SVOS")
for f in sorted((svos / "10-runtime/ulas/dispatch").glob("*.json")):
    d = json.loads(f.read_text())
    pending = [e for e in d.get("envelopes", []) if e.get("status") in ("pending", "dispatched")]
    if pending:
        print(f"Decision: {d.get('decision_id')}")
        for e in pending[:3]:
            print(f"  - {e.get('dispatch_id')} [{e.get('status')}] {e.get('work_package_id')}")
PY
} > "$OUT_FILE"

# context manifest
cat > "$OUT_DIR/context-manifest.json" <<EOF
{
  "\$schema": "svos-context-manifest-v1",
  "venture_slug": "$SLUG",
  "assembled_at": "$TIMESTAMP",
  "assembled_ref": "10-runtime/context/$SLUG/assembled-context.md",
  "token_budget_hint": 8000
}
EOF

echo "Context: $OUT_FILE"
wc -c "$OUT_FILE" | awk '{print "Bytes:", $1, "(~", int($1/4), "token tahmini)"}'
