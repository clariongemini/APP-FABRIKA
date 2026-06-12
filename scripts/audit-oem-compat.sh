#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MATRIX="$ROOT/docs/03-STANDARDS/OEM_MATRIX.yaml"
STANDARD="$ROOT/docs/03-STANDARDS/OEM_COMPATIBILITY.md"
AGENT="$ROOT/.cursor/rules/05-oem-compat-auditor.mdc"

ERRORS=0
WARNINGS=0

echo "==> OEM / ROM Uyumluluk Denetimi"

for f in "$MATRIX" "$STANDARD" "$AGENT"; do
  if [[ ! -f "$f" ]]; then
    echo "HATA: Eksik — $f"
    ERRORS=$((ERRORS + 1))
  fi
done

# P0 üreticiler tanımlı mı?
for oem in samsung xiaomi; do
  if ! grep -q "^  ${oem}:" "$MATRIX" 2>/dev/null; then
    echo "HATA: P0 üretici eksik — $oem"
    ERRORS=$((ERRORS + 1))
  fi
done

# Kritik MIUI / Samsung kontrolleri
for check in autostart battery_unrestricted battery_no_restrict; do
  if ! grep -q "id: ${check}" "$MATRIX" 2>/dev/null; then
    echo "HATA: Kritik OEM check eksik — $check"
    ERRORS=$((ERRORS + 1))
  fi
done

# Katman 22 OEM bileşenleri architecture belgesinde mi?
OEM_COMPONENTS=(
  "Samsung One UI Compatibility"
  "Xiaomi MIUI HyperOS Compatibility"
  "OEM Manufacturer Detection Engine"
  "OEM Battery Optimization Handler"
  "OEM Autostart Permission Flow"
)
ARCH="$ROOT/docs/33-LAYER-ARCHITECTURE.md"
for comp in "${OEM_COMPONENTS[@]}"; do
  if [[ -f "$ARCH" ]] && ! grep -Fq "$comp" "$ARCH"; then
    echo "HATA: KATMAN 22 bileşeni eksik — $comp"
    ERRORS=$((ERRORS + 1))
  fi
done

# Android projesi varsa core/oem modülünü kontrol et
if [[ -f "$ROOT/settings.gradle.kts" || -f "$ROOT/settings.gradle" ]]; then
  OEM_MODULE="$ROOT/core/oem"
  if [[ ! -d "$OEM_MODULE" ]]; then
    echo "UYARI: Android projesi var ama core/oem/ modülü yok"
    WARNINGS=$((WARNINGS + 1))
  else
    for kt in ManufacturerDetector.kt OemCompatFacade.kt; do
      if ! find "$OEM_MODULE" -name "$kt" 2>/dev/null | grep -q .; then
        echo "UYARI: core/oem/$kt bulunamadı"
        WARNINGS=$((WARNINGS + 1))
      fi
    done
  fi

  REPORT="$ROOT/docs/02-ARCHITECTURE/OEM_TEST_REPORT.md"
  if [[ ! -f "$REPORT" ]]; then
    echo "UYARI: OEM_TEST_REPORT.md eksik (release öncesi zorunlu)"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  echo "    (Fabrika reposu — Android OEM kod denetimi atlandı)"
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "==> OEM denetimi BAŞARISIZ ($ERRORS hata, $WARNINGS uyarı)"
  exit 1
fi

echo "==> OEM standartları doğrulandı ($WARNINGS uyarı — fabrika modu normal)."
