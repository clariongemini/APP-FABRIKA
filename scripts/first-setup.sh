#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  Ulas Autonomous Android APP Factory — İLK KURULUM          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Script izinleri
chmod +x "$ROOT/scripts/"*.sh
echo "✓ Script izinleri ayarlandı"

# 2. MCP config şablonu
if [[ ! -f "$ROOT/.cursor/mcp.json" ]]; then
  echo "→ MCP: cp .cursor/mcp.json.example .cursor/mcp.json && GitHub PAT ekle"
else
  echo "✓ .cursor/mcp.json mevcut"
fi

# 3. MCP denetimi (uyarı modu)
if bash "$ROOT/scripts/check-mcp.sh" --warn; then
  echo "✓ MCP hazır"
else
  echo ""
  echo "⚠ MCP eksik — docs/MCP_SETUP.md takip edin"
  echo "  Cursor → Settings → MCP → cursor-ide-browser etkinleştir"
  echo "  GitHub token: .cursor/mcp.json içine PAT ekleyin"
fi

# 4. Git hooks
if [[ -d "$ROOT/.git" ]]; then
  bash "$ROOT/scripts/install-git-hooks.sh" 2>/dev/null || true
  echo "✓ Git pre-commit hook"
fi

# 5. Fabrika sağlık
echo ""
bash "$ROOT/scripts/factory-health.sh"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Sonraki adımlar:"
echo "  1. MCP kurulumunu tamamla (docs/MCP_SETUP.md)"
echo "  2. ./scripts/init-new-app.sh \"AppAdi\" \"com.sirket.app\""
echo "  3. Cursor'da: \"AppAdi'ni 33 katman standartlarına göre geliştir\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
