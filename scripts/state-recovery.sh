#!/usr/bin/env bash
# State Recovery — Composer truncation / yarım Gradle edit kurtarma.
#
# Modlar:
#   --checkpoint   Gradle/build edit öncesi git stash veya dosya kopyası
#   --recover      LATEST.gradle.log analizi → etkilenen build dosyalarını geri yükle
#   --status       Son checkpoint + handoff özeti
#
# Ortam:
#   RECOVERY_SKIP_CHECKPOINT=1   gradle-build-loop checkpoint atlar
#   RECOVERY_AUTO=1              recover sonrası gradle-build-loop tekrar dener
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RECOVERY_DIR="$ROOT/.cursor/snapshots/recovery"
CHECKPOINT_META="$RECOVERY_DIR/LATEST.checkpoint.json"
HANDOFF="$RECOVERY_DIR/LATEST.recovery.handoff.json"
BUILD_LOG="$ROOT/.cursor/snapshots/build/LATEST.gradle.log"
ERROR_SIG_FILE="$RECOVERY_DIR/last-error.sig"

BUILD_GLOBS=(
  "gradle/libs.versions.toml"
  "settings.gradle.kts"
  "build.gradle.kts"
)

log() { echo "==> $*"; }

json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/}"
  printf '%s' "$s"
}

is_git_repo() {
  git -C "$ROOT" rev-parse --git-dir &>/dev/null
}

collect_build_files() {
  local rel f
  while IFS= read -r rel; do
    [[ -n "$rel" ]] && echo "$rel"
  done < <(
    for f in "${BUILD_GLOBS[@]}"; do
      [[ -f "$ROOT/$f" ]] && echo "$f"
    done
    find "$ROOT" -name 'build.gradle.kts' -not -path '*/build/*' \
      -not -path '*/.cursor/snapshots/recovery/*' 2>/dev/null \
      | sed "s|^$ROOT/||"
    find "$ROOT" -name 'AndroidManifest.xml' -not -path '*/build/*' \
      -not -path '*/.cursor/snapshots/recovery/*' 2>/dev/null \
      | sed "s|^$ROOT/||"
  ) | sort -u
}

write_checkpoint_meta() {
  local ts="$1"
  local stash_ref="${2:-}"
  local head_commit="${3:-}"
  local copy_dir="${4:-}"
  local method="$5"
  local files_json=""
  local t

  mkdir -p "$RECOVERY_DIR/checkpoints"
  while IFS= read -r t; do
    [[ -z "$t" ]] && continue
    files_json+="\"$(json_escape "$t")\","
  done < <(collect_build_files)
  files_json="[${files_json%,}]"

  cat > "$CHECKPOINT_META" <<EOF
{
  "schema": "factory-recovery-checkpoint-v1",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "timestamp": "$ts",
  "method": "$method",
  "stash_ref": "$(json_escape "$stash_ref")",
  "head_commit": "$(json_escape "$head_commit")",
  "copy_dir": "$(json_escape "$copy_dir")",
  "tracked_build_files": $files_json
}
EOF
  cp "$CHECKPOINT_META" "$RECOVERY_DIR/checkpoints/checkpoint-${ts}.json"
}

cmd_checkpoint() {
  mkdir -p "$RECOVERY_DIR/checkpoints"
  local ts copy_dir head_commit=""
  ts="$(date +%Y%m%d-%H%M%S)"
  copy_dir="$RECOVERY_DIR/checkpoints/files-${ts}"
  mkdir -p "$copy_dir"

  if is_git_repo; then
    head_commit="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo "")"
  fi

  local rel f
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    mkdir -p "$copy_dir/$(dirname "$rel")"
    if is_git_repo && git -C "$ROOT" cat-file -e "HEAD:$rel" 2>/dev/null; then
      git -C "$ROOT" show "HEAD:$rel" > "$copy_dir/$rel"
    elif [[ -f "$ROOT/$rel" ]]; then
      cp "$ROOT/$rel" "$copy_dir/$rel"
    fi
  done < <(collect_build_files)

  log "Checkpoint: HEAD build dosyaları → $copy_dir"
  write_checkpoint_meta "$ts" "" "$head_commit" "$copy_dir" "file-copy-head"
  log "Checkpoint meta: $CHECKPOINT_META"
}

log_is_recoverable() {
  local log_file="$1"
  [[ -f "$log_file" ]] || return 1
  local patterns=(
    'unexpected end of file'
    'Unexpected end of input'
    'unclosed'
    'parse error'
    'Could not parse'
    'Could not compile'
    'EOF'
    'unresolved dependency'
    'unresolved reference'
    'expecting'
    'Truncation'
  )
  local p
  for p in "${patterns[@]}"; do
    if grep -qiE "$p" "$log_file" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}

extract_affected_files() {
  local log_file="$1"
  local found=""

  found="$( {
    grep -oE "Build file '[^']+'" "$log_file" 2>/dev/null | sed "s/Build file '//;s/'$//" || true
    grep -oE "[^ '\"]+\\.(gradle\\.kts|toml)" "$log_file" 2>/dev/null || true
    grep -oE "[^ '\"]+AndroidManifest\\.xml" "$log_file" 2>/dev/null || true
  } | while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local rel="$line"
    if [[ "$rel" == "$ROOT/"* ]]; then rel="${rel#"$ROOT"/}"; fi
    rel="${rel#./}"
    if [[ "$rel" == *.gradle.kts || "$rel" == *.toml || "$rel" == *AndroidManifest.xml ]]; then
      echo "$rel"
    fi
  done | sort -u )"

  if [[ -z "$found" ]]; then
    collect_build_files
  else
    echo "$found"
  fi
}

meta_field() {
  local key="$1"
  grep -o "\"${key}\": \"[^\"]*\"" "$CHECKPOINT_META" 2>/dev/null | head -1 | cut -d'"' -f4
}

restore_file_from_checkpoint() {
  local rel="$1"
  local method stash_ref head_commit copy_dir
  method="$(meta_field method)"
  stash_ref="$(meta_field stash_ref)"
  head_commit="$(meta_field head_commit)"
  copy_dir="$(meta_field copy_dir)"

  case "$method" in
    git-stash|git-head|file-copy|file-copy-head)
      if [[ -f "$copy_dir/$rel" ]]; then
        mkdir -p "$ROOT/$(dirname "$rel")"
        cp "$copy_dir/$rel" "$ROOT/$rel"
        log "Geri yüklendi (checkpoint): $rel"
        return 0
      fi
      if [[ -n "$head_commit" ]] && git -C "$ROOT" checkout "$head_commit" -- "$rel" 2>/dev/null; then
        log "Geri yüklendi (HEAD): $rel"
        return 0
      fi
      ;;
  esac
  log "ATLA (geri yüklenemedi): $rel"
  return 1
}

read_active_phase() {
  local yap="$ROOT/YAPILACAKLAR.md"
  [[ -f "$yap" ]] || { echo "none"; return; }
  grep -E '^## F[0-9]+ .+ · `işleniyor`' "$yap" 2>/dev/null | head -1 | sed -n 's/^## \(F[0-9]\+\).*/\1/p' || echo "none"
}

write_handoff() {
  local reason="$1"
  local restored_json="$2"
  local cleanliness="$3"
  local active_phase="${4:-unknown}"

  cat > "$HANDOFF" <<EOF
{
  "schema": "factory-recovery-handoff-v1",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "reason": "$(json_escape "$reason")",
  "restored_files": $restored_json,
  "cleanliness": "$(json_escape "$cleanliness")",
  "yapilacaklar_active_phase": "$(json_escape "$active_phase")",
  "agent_instruction": "Dosya yarım kesildi veya Gradle parse hatası tespit edildi. Etkilenen build dosyaları son checkpoint'e döndürüldü. YAPILACAKLAR aktif faz korundu. @.cursor/snapshots/recovery/LATEST.recovery.handoff.json ve @.cursor/snapshots/build/LATEST.gradle.log okuyup yalnızca etkilenen dosyayı küçük batch ile yeniden yaz.",
  "next_action": "./scripts/gradle-build-loop.sh"
}
EOF

  echo ""
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║  STATE RECOVERY — Agent Handoff                          ║"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo "  Sebep     : $reason"
  echo "  Handoff   : $HANDOFF"
  echo "  YAPILACAKLAR fazı değiştirilmedi: $active_phase"
  echo ""
  echo "  Cursor Agent: Etkilenen dosyayı küçük parçada yeniden yaz."
  echo "  @.cursor/snapshots/recovery/LATEST.recovery.handoff.json"
  echo "  @.cursor/snapshots/build/LATEST.gradle.log"
}

cmd_recover() {
  if [[ ! -f "$CHECKPOINT_META" ]]; then
    log "Checkpoint yok — önce: ./scripts/state-recovery.sh --checkpoint"
    exit 1
  fi

  if [[ ! -f "$BUILD_LOG" ]]; then
    log "Build log yok: $BUILD_LOG — önce gradle-build-loop çalıştırın"
    exit 1
  fi

  if ! log_is_recoverable "$BUILD_LOG"; then
    log "Log recoverable pattern içermiyor — manuel düzeltme gerekli"
    exit 2
  fi

  local restored_json="" rel count=0
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    if restore_file_from_checkpoint "$rel"; then
      restored_json+="\"$(json_escape "$rel")\","
      count=$((count + 1))
    fi
  done < <(extract_affected_files "$BUILD_LOG")
  restored_json="[${restored_json%,}]"

  local cleanliness="skipped"
  if [[ -f "$ROOT/gradlew" ]] && command -v java &>/dev/null; then
    chmod +x "$ROOT/gradlew" 2>/dev/null || true
    set +e
    "$ROOT/gradlew" help -q >/dev/null 2>&1
    local rc=$?
    set -e
    if [[ $rc -eq 0 ]]; then
      cleanliness="gradlew-help-ok"
      log "Gradle cleanliness: OK (gradlew help)"
    else
      cleanliness="gradlew-help-failed"
    fi
  else
    cleanliness="no-gradlew-or-jdk"
  fi

  write_handoff "gradle-log-recoverable-error" "$restored_json" "$cleanliness" "$(read_active_phase)"
  rm -f "$ERROR_SIG_FILE"

  if [[ "${RECOVERY_AUTO:-0}" == "1" && -f "$ROOT/gradlew" ]]; then
    log "RECOVERY_AUTO=1 → gradle-build-loop yeniden deneniyor"
    "$ROOT/scripts/gradle-build-loop.sh" || true
  fi

  [[ $count -eq 0 ]] && exit 3
  exit 0
}

cmd_status() {
  echo "State Recovery durumu"
  echo "  Checkpoint : $CHECKPOINT_META ($(test -f "$CHECKPOINT_META" && echo mevcut || echo yok))"
  echo "  Handoff    : $HANDOFF ($(test -f "$HANDOFF" && echo mevcut || echo yok))"
  echo "  Build log  : $BUILD_LOG ($(test -f "$BUILD_LOG" && echo mevcut || echo yok))"
  [[ -f "$CHECKPOINT_META" ]] && echo "" && head -20 "$CHECKPOINT_META"
  [[ -f "$HANDOFF" ]] && echo "" && head -25 "$HANDOFF"
}

compute_error_sig() {
  local log_file="$1"
  [[ -f "$log_file" ]] || return
  grep -iE 'error|exception|failed|parse|unclosed|unexpected|unresolved' "$log_file" 2>/dev/null \
    | tail -8 | shasum -a 256 2>/dev/null | awk '{print $1}' || echo "unknown"
}

maybe_auto_recover() {
  local log_file="$1"
  local sig
  sig="$(compute_error_sig "$log_file")"
  if [[ -f "$ERROR_SIG_FILE" ]] && [[ "$(cat "$ERROR_SIG_FILE" 2>/dev/null)" == "$sig" ]]; then
    log "Aynı hata imzası tekrarlandı → --recover tetikleniyor"
    cmd_recover || true
    return 0
  fi
  echo "$sig" > "$ERROR_SIG_FILE"
  return 1
}

main() {
  mkdir -p "$RECOVERY_DIR"
  case "${1:-}" in
    --checkpoint) cmd_checkpoint ;;
    --recover)    cmd_recover ;;
    --status)     cmd_status ;;
    --maybe-auto-recover) maybe_auto_recover "${2:-$BUILD_LOG}" ;;
    -h|--help) echo "Kullanım: $0 --checkpoint | --recover | --status" ;;
    *) echo "HATA: Bilinmeyen mod — $0 --help"; exit 1 ;;
  esac
}

main "$@"
