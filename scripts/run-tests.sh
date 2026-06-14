#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Test çalıştırılıyor..."

if [[ -f "$ROOT/gradlew" ]]; then
  if [[ "${GRADLE_LOOP_STRICT:-}" == "1" ]]; then
    bash "$ROOT/scripts/gradle-build-loop.sh" --strict
  else
    bash "$ROOT/scripts/gradle-build-loop.sh"
  fi
else
  echo "==> Henüz Android projesi yok — gradle build loop atlandı."
fi
