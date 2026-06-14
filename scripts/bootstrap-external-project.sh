#!/usr/bin/env bash
# AI Studio / harici Android projesine fabrika standartlarını bootstrap eder.
# Mevcut app/ kaynağını SİLMEZ — sync-standards + governance + YAPILACAKLAR.
#
# Kullanım:
#   FACTORY_REPO=~/Android-App-Factory ./scripts/bootstrap-external-project.sh \
#     /path/to/aistudio-export "AppAdi" "com.sirket.app" "Vizyon promptu"
#
# Zaten sync edilmiş proje kökünden:
#   ./scripts/bootstrap-external-project.sh . "AppAdi" "com.sirket.app"
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACTORY_ROOT="${FACTORY_REPO:-$SCRIPT_DIR/..}"
TARGET="${1:-}"
APP_NAME="${2:-}"
PACKAGE="${3:-}"
PROMPT="${4:-}"

usage() {
  echo "Kullanım: FACTORY_REPO=<fabrika-yolu> $0 <hedef-proje> <AppAdi> <com.pkg.app> [prompt]"
  exit 1
}

[[ -z "$TARGET" || -z "$APP_NAME" || -z "$PACKAGE" ]] && usage

TARGET="$(cd "$TARGET" && pwd)"
FACTORY_ROOT="$(cd "$FACTORY_ROOT" && pwd)"

if [[ ! -d "$FACTORY_ROOT/.cursor/rules" ]]; then
  echo "HATA: Fabrika reposu bulunamadı: $FACTORY_ROOT"
  echo "      FACTORY_REPO=~/Android-App-Factory ayarlayın"
  exit 1
fi

echo "==> Bootstrap external project (AI Studio / mevcut app)"
echo "  Fabrika : $FACTORY_ROOT"
echo "  Hedef   : $TARGET"
echo "  App     : $APP_NAME ($PACKAGE)"
echo ""

# 1. Standartları aktar (hedef ≠ fabrika kökü ise)
if [[ "$TARGET" != "$FACTORY_ROOT" ]]; then
  echo "==> [1/5] sync-standards.sh"
  FACTORY_REPO="$FACTORY_ROOT" "$FACTORY_ROOT/scripts/sync-standards.sh" "$TARGET"
else
  echo "==> [1/5] sync-standards ATLA (hedef = fabrika şablon reposu)"
fi

cd "$TARGET"

# 2. Script izinleri
echo "==> [2/5] Script izinleri"
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x scripts/governance/*.sh 2>/dev/null || true
chmod +x scripts/ceo/*.sh 2>/dev/null || true

# 3. Gradle wrapper (AI Studio projesinde varsa dokunma; yoksa template'ten)
if [[ ! -f "$TARGET/gradlew" ]] && [[ -f "$FACTORY_ROOT/templates/android/project/gradlew" ]]; then
  echo "==> [3/5] gradlew yok — bootstrap-gradle-wrapper (dikkat: AI Studio yapısını kontrol edin)"
  bash "$FACTORY_ROOT/scripts/bootstrap-gradle-wrapper.sh" "$TARGET" 2>/dev/null || true
else
  echo "==> [3/5] gradlew mevcut veya atlandı"
fi

# 4. Executive OS + YAPILACAKLAR
echo "==> [4/5] init-governance + YAPILACAKLAR"
mkdir -p "$TARGET/.factory"
cat > "$TARGET/.factory/project.json" <<EOF
{
  "app_name": "$APP_NAME",
  "package_name": "$PACKAGE",
  "source": "aistudio-import",
  "factory_root": "$FACTORY_ROOT",
  "initialized_at": "$(date +%Y-%m-%d)"
}
EOF

bash "$TARGET/scripts/governance/init-governance.sh" "$APP_NAME" "$PACKAGE"

if [[ -n "$PROMPT" ]]; then
  bash "$TARGET/scripts/governance/init-yapilacaklar.sh" "$PROMPT"
else
  bash "$TARGET/scripts/governance/init-yapilacaklar.sh" "AI Studio import — $APP_NAME — fabrika standartlarına yükseltme"
fi

# 5. Bootstrap manifest (Cursor /baslat kapısı)
echo "==> [5/5] bootstrap_manifest.json"
cat > "$TARGET/.factory/bootstrap_manifest.json" <<EOF
{
  "status": "initialized",
  "source": "bootstrap-external-project",
  "app_name": "$APP_NAME",
  "package_name": "$PACKAGE",
  "factory_root": "$FACTORY_ROOT",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

python3 "$TARGET/scripts/governance/validate-yapilacaklar.py" 2>/dev/null || true

# Proje INDEX kısa güncelleme
if [[ -f "$TARGET/docs/00-INDEX.md" ]]; then
  sed -i.bak "s/Aktif Proje | .*/Aktif Proje | **$APP_NAME** |/" "$TARGET/docs/00-INDEX.md" 2>/dev/null \
    || sed -i '' "s/Aktif Proje | .*/Aktif Proje | **$APP_NAME** |/" "$TARGET/docs/00-INDEX.md" 2>/dev/null \
    || true
  rm -f "$TARGET/docs/00-INDEX.md.bak" 2>/dev/null || true
fi

echo ""
echo "✅ Bootstrap tamamlandı."
echo "   Sonraki: Cursor'da /baslat veya /import-aistudio"
echo "   Rehber: docs/AI_STUDIO_IMPORT.md"
