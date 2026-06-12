#!/usr/bin/env bash
set -euo pipefail

# Fabrika standartlarını mevcut bir Android projesine aktarır.
# Kullanım:
#   FACTORY_REPO=~/autonomous-app-factory ./scripts/sync-standards.sh /path/to/target
# veya fabrika kökünden:
#   ./scripts/sync-standards.sh /path/to/target

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACTORY_ROOT="${FACTORY_REPO:-$(cd "$SCRIPT_DIR/.." && pwd)}"
TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Kullanım: FACTORY_REPO=<fabrika-yolu> $0 <hedef-proje-yolu>"
  echo "Örnek:   $0 ../my-android-app"
  exit 1
fi

TARGET="$(cd "$TARGET" && pwd)"

if [[ ! -d "$FACTORY_ROOT/.cursor/rules" ]]; then
  echo "HATA: Fabrika reposu bulunamadı: $FACTORY_ROOT"
  exit 1
fi

echo "==> Standartlar aktarılıyor"
echo "    Kaynak : $FACTORY_ROOT"
echo "    Hedef  : $TARGET"

SYNC_ITEMS=(
  ".cursorrules"
  ".cursor"
  "docs/00-INDEX.md"
  "docs/TODO.md"
  "docs/CHANGELOG.md"
  "docs/33-LAYER-ARCHITECTURE.md"
  "docs/BOOTSTRAP.md"
  "docs/01-VISION"
  "docs/02-ARCHITECTURE"
  "docs/03-STANDARDS"
  "scripts"
  "templates"
)

for item in "${SYNC_ITEMS[@]}"; do
  src="$FACTORY_ROOT/$item"
  dst="$TARGET/$item"

  if [[ ! -e "$src" ]]; then
    echo "  ATLA (yok): $item"
    continue
  fi

  if [[ -d "$src" ]]; then
    mkdir -p "$dst"
    rsync -a --delete "$src/" "$dst/"
    echo "  SYNC (dir): $item"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
    echo "  SYNC (file): $item"
  fi
done

# Fabrika meta
mkdir -p "$TARGET/.factory"
cat > "$TARGET/.factory/sync.json" <<EOF
{
  "factory_root": "$FACTORY_ROOT",
  "synced_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "factory_version": "0.3.0"
}
EOF

chmod +x "$TARGET/scripts/"*.sh 2>/dev/null || true

echo ""
echo "==> Senkronizasyon tamamlandı."
echo "    Hedef projede çalıştır: ./scripts/init-new-app.sh \"AppAdi\" \"com.pkg.app\""
