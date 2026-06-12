#!/usr/bin/env bash
# Kotlin OEM şablonlarını Android projesine kopyalar.
# Kullanım: ./scripts/scaffold-oem-module.sh "com.sirket.app"
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE="${1:-}"

if [[ -z "$PACKAGE" ]]; then
  echo "Kullanım: $0 <com.sirket.app>"
  exit 1
fi

PKG_PATH="${PACKAGE//.//}"
TARGET="$ROOT/core/oem/src/main/kotlin/$PKG_PATH/core/oem"
TEMPLATE="$ROOT/templates/android/core-oem"

mkdir -p "$TARGET"

for kt in "$TEMPLATE"/*.kt; do
  fname=$(basename "$kt")
  sed "s/{{PACKAGE}}/$PACKAGE/g" "$kt" > "$TARGET/$fname"
  echo "  Oluşturuldu: $TARGET/$fname"
done

echo "==> OEM modül şablonu hazır. settings.gradle.kts'e :core:oem eklemeyi unutma."
