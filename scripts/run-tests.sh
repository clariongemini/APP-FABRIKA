#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Test çalıştırılıyor..."

if [[ -f "$ROOT/gradlew" ]]; then
  "$ROOT/gradlew" test --quiet
  echo "==> Gradle testleri tamamlandı."
else
  echo "==> Henüz Android projesi yok — test atlandı."
fi
