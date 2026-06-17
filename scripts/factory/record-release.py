#!/usr/bin/env python3
"""Record a portfolio app release event."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

HISTORY = factory_dir("portfolio", "release_history.json")
APPS = factory_dir("portfolio", "apps.json")
NOW = datetime.now(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--track", default="internal", choices=["internal", "beta", "production"])
    parser.add_argument("--apk-proof", default="", help="Path or build id")
    args = parser.parse_args()

    if not HISTORY.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        return 1

    hist = json.loads(HISTORY.read_text(encoding="utf-8"))
    hist.setdefault("releases", []).append({
        "slug": args.slug,
        "version": args.version,
        "track": args.track,
        "apk_proof": args.apk_proof or None,
        "released_at": NOW.isoformat(),
    })
    hist["updated_at"] = NOW.isoformat()
    HISTORY.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if APPS.exists():
        apps = json.loads(APPS.read_text(encoding="utf-8"))
        for app in apps.get("apps", []):
            if app.get("slug") == args.slug:
                if not app.get("first_apk_at"):
                    app["first_apk_at"] = NOW.isoformat()
                if args.track == "production":
                    app["status"] = "released"
                    app["released_at"] = NOW.isoformat()
        apps["updated_at"] = NOW.isoformat()
        APPS.write_text(json.dumps(apps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"   ✅ Release {args.slug}@{args.version} ({args.track})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
