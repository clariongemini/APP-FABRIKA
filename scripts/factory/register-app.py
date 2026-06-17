#!/usr/bin/env python3
"""Register a factory-produced app in the portfolio registry."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

APPS = factory_dir("portfolio", "apps.json")
NOW = datetime.now(timezone.utc)


def _load_apps() -> dict:
    if not APPS.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(APPS.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Register app in factory portfolio")
    parser.add_argument("--name", required=True, help='App display name e.g. "My App"')
    parser.add_argument("--package", required=True, help="Android package e.g. com.example.myapp")
    parser.add_argument("--slug", required=True, help="Portfolio slug e.g. my-app")
    parser.add_argument("--repo", default="", help="Optional path or git URL")
    parser.add_argument("--status", default="development", choices=["development", "beta", "released", "profitable"])
    args = parser.parse_args()

    data = _load_apps()
    apps = data.setdefault("apps", [])
    if any(a.get("slug") == args.slug for a in apps):
        print(f"   ⚠️  App already registered: {args.slug}")
        return 0

    apps.append({
        "slug": args.slug,
        "name": args.name,
        "package": args.package,
        "repo": args.repo or None,
        "status": args.status,
        "registered_at": NOW.isoformat(),
        "first_apk_at": None,
        "released_at": None,
        "playstore_rating": None,
        "mrr": None,
    })
    data["updated_at"] = NOW.isoformat()
    APPS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ Registered {args.name} ({args.slug}) → {APPS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
