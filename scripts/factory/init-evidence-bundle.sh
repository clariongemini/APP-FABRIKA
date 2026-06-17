#!/usr/bin/env bash
# Initialize per-venture evidence bundle (V3) — structure only, real data from shipped apps.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TPL="$ROOT/knowledge/evidence/_template"

SLUG=""
PORTFOLIO=""
VENTURE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2 ;;
    --portfolio-slug) PORTFOLIO="$2"; shift 2 ;;
    --venture-slug) VENTURE="$2"; shift 2 ;;
    *) echo "Unknown: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Usage: $0 --slug offline-player-v1 [--portfolio-slug offline-player] [--venture-slug offline-player-v1]"
  exit 1
fi

PORTFOLIO="${PORTFOLIO:-$SLUG}"
VENTURE="${VENTURE:-$SLUG}"
DEST="$ROOT/knowledge/evidence/$SLUG"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [[ -d "$DEST" && -f "$DEST/EVIDENCE.md" ]]; then
  echo "Already exists: $DEST" >&2
  exit 1
fi

mkdir -p "$DEST"/{raw/play-console,raw/firebase,raw/revenue,raw/reviews,summaries}

sed -e "s/{{SLUG}}/$SLUG/g" \
    -e "s/{{PORTFOLIO_SLUG}}/$PORTFOLIO/g" \
    -e "s/{{VENTURE_SLUG}}/$VENTURE/g" \
    -e "s/{{DATE}}/$NOW/g" \
    -e "s/{{RELEASED_AT}}/—/g" \
    "$TPL/EVIDENCE.md" > "$DEST/EVIDENCE.md"

sed -e "s/{{SLUG}}/$SLUG/g" \
    -e "s/{{PORTFOLIO_SLUG}}/$PORTFOLIO/g" \
    -e "s/{{VENTURE_SLUG}}/$VENTURE/g" \
    -e "s/{{DATE}}/$NOW/g" \
    "$TPL/manifest.json" > "$DEST/manifest.json"

touch "$DEST/raw/.gitkeep" "$DEST/summaries/.gitkeep"

echo "   ✅ $DEST"
echo "   Next: place exports in raw/ · fill EVIDENCE.md · record-outcome.py"
