#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "==> Güvenlik Standardı Denetimi"

for f in \
  "docs/03-STANDARDS/SECURITY.md" \
  "docs/03-STANDARDS/PRIVACY.md" \
  "docs/03-STANDARDS/BACKGROUND_PROCESSING.md" \
  "docs/03-STANDARDS/MONETIZATION_TECH.md"
do
  if [[ ! -f "$ROOT/$f" ]]; then
    echo "HATA: Eksik — $f"
    ERRORS=$((ERRORS + 1))
  fi
done

# .gitignore secrets kontrolü
for pattern in ".env" "*.keystore" "google-services.json"; do
  if ! grep -qF "$pattern" "$ROOT/.gitignore" 2>/dev/null; then
    echo "HATA: .gitignore'da eksik — $pattern"
    ERRORS=$((ERRORS + 1))
  fi
done

# Android projesi varsa
if [[ -f "$ROOT/settings.gradle.kts" || -f "$ROOT/settings.gradle" ]]; then
  if grep -r "usesCleartextTraffic" "$ROOT/app" 2>/dev/null | grep -q 'true'; then
    echo "HATA: usesCleartextTraffic=true tespit edildi"
    ERRORS=$((ERRORS + 1))
  fi
  RELEASE_MINIFY=$(grep -r "isMinifyEnabled" "$ROOT" --include="*.kts" 2>/dev/null | grep -c "true" || true)
  if [[ "$RELEASE_MINIFY" -eq 0 ]]; then
    echo "UYARI: Release minify yapılandırması bulunamadı"
  fi
else
  echo "    (Fabrika modu — Android kod denetimi atlandı)"
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Güvenlik denetimi BAŞARISIZ ($ERRORS hata)"
  exit 1
fi

echo "==> Güvenlik standartları doğrulandı."
