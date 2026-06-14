#!/usr/bin/env bash
# Factory Smoke App — test/factory-smoke-app oluşturur (fabrika kökünü değiştirmez).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$REPO_ROOT/test/factory-smoke-app"
APP_NAME="FactorySmoke"
PACKAGE="com.ulas.factory.smoke"
DATE="$(date +%Y-%m-%d)"

echo "==> Factory smoke app bootstrap"

mkdir -p "$REPO_ROOT/test/docs"

# --- Adım 1: test dizini ---
echo "==> [1/8] test/ dizini"
mkdir -p "$REPO_ROOT/test"

# --- Adım 2: Minimal vizyon belgesi (F1 simülasyonu) ---
echo "==> [2/8] Smoke app vizyon belgesi"
cat > "$REPO_ROOT/test/docs/SMOKE_APP_BRIEF.md" <<EOF
# FactorySmoke — Fabrika Denetim Uygulaması

| Alan | Değer |
|------|-------|
| Amaç | Fabrika şablonu özelliklerini uçtan uca doğrulamak |
| Package | \`$PACKAGE\` |
| MVP | Tek ekran, i18n, Liquid Glass kart, offline-first |
| Oluşturulma | $DATE |

## Kabul kriterleri

- Gradle 10 modül derlenir
- \`tr.json\` / \`en.json\` hard-coded string yok
- \`./test/run-factory-audit.sh\` tüm fabrika kapılarından geçer
EOF

# --- Adım 3: Android scaffold (F3) ---
echo "==> [3/8] Android scaffold → test/factory-smoke-app"
if [[ -f "$APP_DIR/settings.gradle.kts" ]]; then
  echo "    ATLA: factory-smoke-app zaten mevcut"
else
  bash "$REPO_ROOT/scripts/scaffold-android-project-to.sh" "$APP_DIR" "$APP_NAME" "$PACKAGE"
fi

# --- Adım 4: Gradle wrapper doğrulama ---
echo "==> [4/8] Gradle wrapper"
[[ -x "$APP_DIR/gradlew" ]] || { echo "HATA: gradlew yok"; exit 1; }

# --- Adım 5: State recovery checkpoint (F3+) ---
echo "==> [5/8] State recovery checkpoint"
if [[ -x "$REPO_ROOT/scripts/state-recovery.sh" ]]; then
  (cd "$APP_DIR" && RECOVERY_ROOT="$APP_DIR" "$REPO_ROOT/scripts/state-recovery.sh" --checkpoint) || true
fi

# --- Adım 6: Proje meta ---
echo "==> [6/8] test/.factory/project.json"
mkdir -p "$REPO_ROOT/test/.factory"
cat > "$REPO_ROOT/test/.factory/project.json" <<EOF
{
  "app_name": "$APP_NAME",
  "package_name": "$PACKAGE",
  "purpose": "factory-smoke-test",
  "factory_version": "1.0.0",
  "initialized_at": "$DATE"
}
EOF

# --- Adım 7: Gradle build (JDK varsa) ---
echo "==> [7/8] Gradle assembleDebug"
if command -v java &>/dev/null; then
  (cd "$APP_DIR" && ./gradlew assembleDebug --quiet) && echo "    ✅ BUILD SUCCESS" || echo "    ⚠️ BUILD FAILED — audit raporuna bakın"
else
  echo "    ATLA: JDK yok"
fi

# --- Adım 8: Audit ---
echo "==> [8/8] Fabrika audit"
bash "$REPO_ROOT/test/run-factory-audit.sh"

echo ""
echo "==> Bootstrap tamamlandı."
echo "    Uygulama : $APP_DIR"
echo "    Audit    : test/AUDIT_REPORT.md"
