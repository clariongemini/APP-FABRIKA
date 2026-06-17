#!/usr/bin/env bash
# V3.1 — Consolidated runtime tree + legacy migration hints.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "==> Runtime consolidation (V3.1)"

mkdir -p "$ROOT/runtime"/{governance/memory,governance/execution,governance/egc}
mkdir -p "$ROOT/runtime/factory"/{proof,memory,decision_accuracy,revenue,benchmark,portfolio,certification,regression,outcomes,ventures}
mkdir -p "$ROOT/runtime/analytics"
mkdir -p "$ROOT/runtime/telemetry"

# Seed factory intelligence into runtime/factory/
FACTORY_RUNTIME="$ROOT/runtime/factory"
export RUNTIME_FACTORY_ROOT="$FACTORY_RUNTIME"
python3 "$ROOT/scripts/factory/seed-intelligence.py"
python3 "$ROOT/scripts/factory/seed-portfolio.py"
python3 "$ROOT/scripts/factory/seed-outcomes.py"
python3 "$ROOT/scripts/factory/seed-ventures.py"

# Migrate legacy factory/runtime → runtime/factory if newer legacy exists
LEG="$ROOT/factory/runtime"
if [[ -d "$LEG" ]]; then
  for sub in proof memory decision_accuracy revenue benchmark telemetry; do
    if [[ -d "$LEG/$sub" ]] && [[ "$(ls -A "$LEG/$sub" 2>/dev/null)" ]]; then
      cp -Rn "$LEG/$sub/"* "$ROOT/runtime/factory/$sub/" 2>/dev/null || true
    fi
  done
fi

echo "   ✅ runtime/ tree ready"
echo "   Docs: runtime/README.md"
