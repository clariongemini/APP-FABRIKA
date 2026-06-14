#!/usr/bin/env bash
# MCP kurulumunu otomatik başlatır — .cursor/mcp.json şablonu.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXAMPLE="$ROOT/.cursor/mcp.json.example"
TARGET="$ROOT/.cursor/mcp.json"

echo "==> MCP Kurulum Asistanı"

mkdir -p "$ROOT/.cursor"

if [[ ! -f "$EXAMPLE" ]]; then
  echo "HATA: $EXAMPLE bulunamadı"
  exit 1
fi

if [[ ! -f "$TARGET" ]]; then
  cp "$EXAMPLE" "$TARGET"
  echo "✓ .cursor/mcp.json oluşturuldu (example'dan kopyalandı)"
else
  echo "✓ .cursor/mcp.json zaten mevcut (üzerine yazılmadı)"
fi

echo ""
echo "Manuel adımlar (P0 tamamlamak için):"
echo "  1. Cursor → Settings → MCP → cursor-ide-browser etkinleştir"
echo "  2. $TARGET içinde GITHUB_PERSONAL_ACCESS_TOKEN değerini gerçek PAT ile değiştir"
echo "     Gerekli scope: repo, read:org (minimal)"
echo "  3. Cursor'ı yeniden başlat"
echo ""
echo "Doğrulama: ./scripts/check-mcp.sh"
echo "Kılavuz: docs/MCP_SETUP.md"

bash "$ROOT/scripts/check-mcp.sh" --warn || true
