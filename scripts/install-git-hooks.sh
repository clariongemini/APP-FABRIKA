#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT/.git/hooks"

if [[ ! -d "$ROOT/.git" ]]; then
  echo "HATA: Git reposu değil. Önce: git init"
  exit 1
fi

mkdir -p "$HOOKS_DIR"

cat > "$HOOKS_DIR/pre-commit" << EOF
#!/usr/bin/env bash
exec "$ROOT/scripts/pre-commit.sh"
EOF

chmod +x "$HOOKS_DIR/pre-commit"
echo "==> Git pre-commit hook kuruldu → scripts/pre-commit.sh"
