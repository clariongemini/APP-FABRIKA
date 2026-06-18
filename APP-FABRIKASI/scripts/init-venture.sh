#!/usr/bin/env bash
# Yeni venture charter oluşturur — her proje için tek komut.
# Kullanım: ./init-venture.sh "My App" my-app path/to/codebase/
set -euo pipefail

SVOS="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$SVOS/.." && pwd)"

DISPLAY="${1:-}"
SLUG="${2:-}"
CODEBASE="${3:-}"
PLATFORM="${4:-android}"

if [[ -z "$DISPLAY" || -z "$SLUG" ]]; then
  echo "Kullanım: $0 <Görünen Ad> <slug> [codebase_yolu] [platform]"
  echo "Örnek:   $0 \"My App\" my-app android/"
  exit 1
fi

if [[ -z "$CODEBASE" ]]; then
  CODEBASE="${SLUG}/"
fi

VENTURE_DIR="$SVOS/08-ventures/$SLUG"
EVIDENCE_DIR="$SVOS/07-evidence/$SLUG"
DATE="$(date +%Y-%m-%d)"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$VENTURE_DIR" "$EVIDENCE_DIR"

# codebase mutlak yol çözümü
if [[ "$CODEBASE" = /* ]]; then
  RESOLVED="$CODEBASE"
else
  RESOLVED="$REPO/$CODEBASE"
fi

cat > "$VENTURE_DIR/venture.json" <<EOF
{
  "name": "$SLUG",
  "slug": "$SLUG",
  "display_name": "$DISPLAY",
  "platform": ["$PLATFORM"],
  "template": "${PLATFORM}-app",
  "stage": "charter",
  "status": "planning",
  "evidence_status": "none",
  "charter": {
    "problem": "— Mimar/CPO dolduracak",
    "solution": "—",
    "market": "—",
    "competition": [],
    "monetization": "—",
    "success_metric": "—"
  },
  "results": {
    "launched_at": null,
    "users": null,
    "revenue_usd": null,
    "rating": null,
    "crash_free_rate": null
  },
  "evidence_ref": "07-evidence/$SLUG/",
  "learning_refs": [],
  "adapter": "02-platforms/$PLATFORM/ADAPTER.md",
  "created": "$DATE",
  "owner": "",
  "codebase_path": "$CODEBASE",
  "codebase_resolved": "$RESOLVED"
}
EOF

cat > "$EVIDENCE_DIR/EVIDENCE.md" <<EOF
# Evidence — $DISPLAY

> Venture ship sonrası doldurulur. Bridge: \`./APP-FABRIKASI/scripts/bridge-venture.sh $SLUG\`

| Kaynak | Durum |
|--------|-------|
| Build | ⬜ |
| Unit tests | ⬜ |
| Crash / analytics | ⬜ |
| Revenue | ⬜ |
EOF

mkdir -p "$SVOS/10-runtime/evidence/$SLUG"

python3 <<PY
import json
from pathlib import Path
svos = Path("$SVOS")
venture_path = Path("$VENTURE_DIR/venture.json")
v = json.loads(venture_path.read_text())
platform = (v.get("platform") or ["$PLATFORM"])[0]
defaults_path = svos / "02-platforms" / platform / "bridge.defaults.json"
if defaults_path.is_file():
    v["build"] = json.loads(defaults_path.read_text())
venture_path.write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n")
PY

echo "=== Venture oluşturuldu ==="
echo "  Charter: $VENTURE_DIR/venture.json"
echo "  Evidence: $EVIDENCE_DIR/"
echo ""
echo "Sonraki:"
echo "  1. Charter alanlarını doldur"
echo "  2. ./scripts/ulas.sh decide --venture $SLUG --class B --title \"...\" --reviewers architect,qa"
echo "  3. ./APP-FABRIKASI/scripts/svos-health.sh"
