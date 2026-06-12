#!/usr/bin/env bash
set -euo pipefail

WARN_ONLY=false
[[ "${1:-}" == "--warn" ]] && WARN_ONLY=true

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REQUIRED="$ROOT/.cursor/mcp.required.json"
ERRORS=0
WARNINGS=0

echo "==> MCP Kurulum Denetimi / MCP Setup Audit"
echo ""

# Cursor MCP config konumları
MCP_PATHS=(
  "$ROOT/.cursor/mcp.json"
  "$HOME/.cursor/mcp.json"
)

found_config=false
config_content=""
for p in "${MCP_PATHS[@]}"; do
  if [[ -f "$p" ]]; then
    found_config=true
    config_content="$(cat "$p")"
    echo "  ✓ MCP config: $p"
    break
  fi
done

if [[ "$found_config" == false ]]; then
  echo "  ✗ MCP config bulunamadı — .cursor/mcp.json.example → .cursor/mcp.json kopyala"
  ERRORS=$((ERRORS + 1))
fi

check_server() {
  local id="$1"
  local priority="$2"
  local label="$3"

  if [[ "$id" == "cursor-ide-browser" ]]; then
  echo "  ✓ [P0] cursor-ide-browser — Cursor built-in (Settings → MCP'de etkinleştir)"
    return 0
  fi

  if [[ -n "$config_content" ]] && echo "$config_content" | grep -qi "$id"; then
    echo "  ✓ [$priority] $label — yapılandırılmış"
    return 0
  fi

  if [[ "$priority" == "P0" ]]; then
    echo "  ✗ [P0] $label — EKSİK (zorunlu)"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ⚠ [$priority] $label — önerilir, kurulu değil"
    WARNINGS=$((WARNINGS + 1))
  fi
}

echo ""
echo "P0 — Zorunlu MCP:"
check_server "cursor-ide-browser" "P0" "Cursor IDE Browser"
check_server "github" "P0" "GitHub MCP"

echo ""
echo "P1 — Önerilen MCP:"
check_server "docker" "P1" "Docker MCP"
check_server "gitkraken" "P1" "GitKraken MCP"

echo ""
echo "P2 — Opsiyonel:"
check_server "fetch" "P2" "Fetch MCP"

# GITHUB_TOKEN kontrolü
if [[ -n "$config_content" ]] && echo "$config_content" | grep -q "GITHUB_PERSONAL_ACCESS_TOKEN"; then
  if echo "$config_content" | grep -q "<GITHUB_TOKEN"; then
    echo ""
    echo "  ✗ GitHub token placeholder — gerçek PAT girin"
    ERRORS=$((ERRORS + 1))
  fi
fi

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "==> MCP denetimi BAŞARISIZ ($ERRORS zorunlu eksik, $WARNINGS uyarı)"
  echo "    Kılavuz: docs/MCP_SETUP.md"
  echo "    Örnek config: cp .cursor/mcp.json.example .cursor/mcp.json"
  [[ "$WARN_ONLY" == true ]] && exit 0
  exit 1
fi

echo "==> MCP denetimi BAŞARILI ($WARNINGS opsiyonel uyarı)"
exit 0
