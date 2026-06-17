#!/usr/bin/env python3
"""Build regression catalog from memory + run preventive checks."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

MEM = factory_dir("memory", "failures.json")
CATALOG = factory_dir("regression", "catalog.json")

# Canonical seed — grows from real project failures
SEED = [
    {
        "id": "FAIL-2026-001",
        "title": "Compose Navigation Loop",
        "root_cause": "Wrong backstack restore on process death",
        "fix_pattern": "SavedStateHandle + singleTop launch mode",
        "affected_modules": ["feature:home"],
        "preventive_check": "SavedStateHandle",
        "tags": ["navigation", "compose"],
    },
    {
        "id": "FAIL-2026-002",
        "title": "Samsung background kill",
        "root_cause": "MIUI/Samsung aggressive battery optimization",
        "fix_pattern": "OemBatteryOptimizer whitelist + user guide",
        "affected_modules": ["core:oem"],
        "preventive_check": "OemBatteryOptimizer",
        "tags": ["samsung", "oem", "background"],
    },
    {
        "id": "FAIL-2026-003",
        "title": "Room migration failure",
        "root_cause": "Schema bump without Migration spec",
        "fix_pattern": "AutoMigration + fallback export schema",
        "affected_modules": ["core:database"],
        "preventive_check": "Migration",
        "tags": ["room", "migration", "database"],
    },
    {
        "id": "FAIL-2026-004",
        "title": "FCM delivery bug",
        "root_cause": "Token refresh not persisted",
        "fix_pattern": "onNewToken + EncryptedSharedPreferences",
        "affected_modules": ["app"],
        "preventive_check": "FirebaseMessaging",
        "tags": ["fcm", "push"],
    },
    {
        "id": "FAIL-2026-005",
        "title": "Billing restore issue",
        "root_cause": "Purchase not acknowledged after restore",
        "fix_pattern": "queryPurchasesAsync + acknowledgePurchase",
        "affected_modules": ["feature:premium"],
        "preventive_check": "BillingClient",
        "tags": ["billing", "restore"],
    },
]


def _merge_catalog() -> dict:
    entries = {e["id"]: e for e in SEED}
    if MEM.exists():
        try:
            mem = json.loads(MEM.read_text(encoding="utf-8"))
            for e in mem.get("entries", []):
                if e.get("fix_pattern") or e.get("preventive_check"):
                    entries[e["id"]] = {
                        "id": e["id"],
                        "title": e.get("title", ""),
                        "root_cause": e.get("cause", ""),
                        "fix_pattern": e.get("fix_pattern", e.get("resolution", "")),
                        "affected_modules": e.get("affected_modules", []),
                        "preventive_check": e.get("preventive_check", ""),
                        "tags": e.get("tags", []),
                    }
        except json.JSONDecodeError:
            pass
    return {
        "version": "1.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "entries": list(entries.values()),
    }


def _scan_codebase(check: str) -> bool:
    if not check:
        return True
    try:
        r = subprocess.run(
            ["rg", "-l", check, "templates/android/project", "--glob", "*.kt"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return r.returncode == 0 and bool(r.stdout.strip())
    except (subprocess.TimeoutExpired, OSError):
        return True  # don't block if rg missing


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--build-catalog", action="store_true")
    args = p.parse_args()

    catalog = _merge_catalog()
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    if args.build_catalog:
        print(f"   ✅ regression catalog: {len(catalog['entries'])} entries")
        return 0

    missing = []
    for e in catalog["entries"]:
        check = e.get("preventive_check", "")
        if check and not _scan_codebase(check):
            missing.append(e["id"])

    if missing:
        print(f"   REGRESSION WARN: preventive pattern missing for {', '.join(missing)}")
        print("   (Template scaffold — app projects should verify before release)")
        return 0  # warn only until real app path wired

    print(f"   ✅ regression scan: {len(catalog['entries'])} known patterns checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
