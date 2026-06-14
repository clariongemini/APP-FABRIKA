#!/usr/bin/env bash
# Çift onay kapısı — iş paketi completed mi?
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QUEUE="$ROOT/governance/executive/APPROVAL_QUEUE.md"

if [[ ! -f "$QUEUE" ]]; then
  echo "HATA: APPROVAL_QUEUE.md bulunamadı"
  exit 1
fi

check_wp() {
  local wp="$1"
  local line
  line=$(grep "| $wp |" "$QUEUE" || true)
  if [[ -z "$line" ]]; then
    echo "HATA: $wp kuyrukta yok"
    return 1
  fi
  if echo "$line" | grep -q '`completed`'; then
    echo "✅ $wp — çift onay + completed"
    return 0
  fi
  if echo "$line" | grep -q '`blocked`'; then
    echo "⏸  $wp — bilinçli olarak blocked (dış kapsam)"
    return 0
  fi
  echo "❌ $wp — onay eksik: $line"
  return 1
}

echo "==> Ajan onay kapısı"

if [[ $# -eq 0 ]]; then
  echo ""
  grep '^| WP-' "$QUEUE" | while read -r row; do
    wp=$(echo "$row" | awk -F'|' '{print $2}' | tr -d ' ')
    status=$(echo "$row" | awk -F'|' '{print $7}' | tr -d ' `')
    printf "  %-6s %s\n" "$wp" "$status"
  done
  echo ""
  echo "Kullanım: $0 WP-01"
  exit 0
fi

FAIL=0
for wp in "$@"; do
  check_wp "$wp" || FAIL=1
done
exit "$FAIL"
