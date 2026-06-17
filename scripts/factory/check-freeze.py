#!/usr/bin/env python3
"""Verify factory development freeze — block new meta-system expansion."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / ".factory" / "freeze.json"
PORT = ROOT / "runtime" / "factory" / "portfolio" / "apps.json"


def main() -> int:
    if not FREEZE.exists():
        print("   ⚠️  freeze.json missing")
        return 0

    policy = json.loads(FREEZE.read_text(encoding="utf-8"))
    released = 0
    if PORT.exists():
        try:
            apps = json.loads(PORT.read_text(encoding="utf-8")).get("apps", [])
            released = sum(
                1 for a in apps
                if a.get("status") in ("released", "profitable") or a.get("released_at")
            )
        except json.JSONDecodeError:
            pass

    need = policy.get("until_apps_released", 3)
    active = released < need

    mode = policy.get("mode", "MAINTENANCE")
    status = policy.get("status", "FROZEN")
    print(f"   Factory: {status} · {mode} ({released}/{need} apps released)")
    if active:
        print(f"   Next: {policy.get('next_objective', 'validate_through_products')}")
        print(f"   Motto: {policy.get('motto', 'Build less, ship more')}")
        required = policy.get("required_apps") or []
        if required:
            print(f"   Required slugs: {', '.join(required)}")
        else:
            print(f"   Unlock: {need} production releases in runtime/factory/portfolio/apps.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
