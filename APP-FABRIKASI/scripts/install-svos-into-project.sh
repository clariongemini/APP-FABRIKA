#!/usr/bin/env bash
# APP-FABRIKASI'yı herhangi bir projeye taşınabilir OS olarak kurar.
# Kullanım:
#   ./APP-FABRIKASI/scripts/install-svos-into-project.sh /path/to/project
#   ./APP-FABRIKASI/scripts/install-svos-into-project.sh .   # mevcut repo kökü
set -euo pipefail

SVOS_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Kullanım: $0 <hedef-proje-kökü>"
  exit 1
fi

TARGET="$(cd "$TARGET" && pwd)"
DEST="$TARGET/APP-FABRIKASI"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "=== SVOS Install ==="
echo "  Kaynak: $SVOS_SRC"
echo "  Hedef : $DEST"

mkdir -p "$TARGET"
rsync -a \
  --exclude '.git' \
  --exclude '10-runtime/ulas/execution/logs' \
  --exclude '10-runtime/evidence/*/raw' \
  "$SVOS_SRC/" "$DEST/"

# Proje köküne ulas kısayolu
mkdir -p "$TARGET/scripts"
if [[ ! -f "$TARGET/scripts/ulas.sh" ]]; then
  cat > "$TARGET/scripts/ulas.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/APP-FABRIKASI/ULAS/bin/ulas.py" "$@"
EOF
  chmod +x "$TARGET/scripts/ulas.sh"
fi

# Cursor dispatch kuralı (merge — üzerine yazmaz)
mkdir -p "$TARGET/.cursor/rules"
if [[ -f "$DEST/.cursor/rules/dispatch-ide.mdc" && ! -f "$TARGET/.cursor/rules/dispatch-ide.mdc" ]]; then
  cp "$DEST/.cursor/rules/dispatch-ide.mdc" "$TARGET/.cursor/rules/dispatch-ide.mdc"
  echo "  COPY: .cursor/rules/dispatch-ide.mdc"
fi

# Proje meta
cat > "$TARGET/.svos.json" <<EOF
{
  "installed_at": "$TIMESTAMP",
  "svos_path": "APP-FABRIKASI",
  "version": "1.1.0-stabilization",
  "commands": {
    "health": "./APP-FABRIKASI/scripts/svos-health.sh",
    "venture": "./APP-FABRIKASI/scripts/init-venture.sh",
    "context": "./APP-FABRIKASI/scripts/assemble-svos-context.sh",
    "bridge": "./APP-FABRIKASI/scripts/bridge-venture.sh"
  }
}
EOF

chmod +x "$DEST/scripts/"*.sh 2>/dev/null || true
chmod +x "$TARGET/scripts/ulas.sh" 2>/dev/null || true

echo ""
echo "=== Kurulum tamam ==="
echo "  1. ./APP-FABRIKASI/scripts/init-venture.sh \"Uygulama\" slug [codebase/]"
echo "  2. ./APP-FABRIKASI/scripts/svos-health.sh"
echo "  3. ./scripts/ulas.sh maturity audit"
