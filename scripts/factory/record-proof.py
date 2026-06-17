#!/usr/bin/env python3
"""Record execution proof for a feature — Feature Proven gate."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

REGISTRY = factory_dir("proof", "proof_registry.json")
REQUIRED_FOR_PROVEN = {"commit", "apk", "analytics"}


def _load() -> dict:
    if not REGISTRY.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _find_feature(data: dict, feature_id: str) -> dict | None:
    for f in data.get("features", []):
        if f.get("feature_id") == feature_id:
            return f
    return None


def _maybe_proven(feature: dict) -> None:
    types = {p.get("type") for p in feature.get("proofs", [])}
    if REQUIRED_FOR_PROVEN.issubset(types):
        feature["status"] = "PROVEN"
        feature["proven_at"] = datetime.now(timezone.utc).isoformat()
    elif feature.get("status") != "PROVEN":
        feature["status"] = "COMPLETED" if feature.get("proofs") else "IN_PROGRESS"


def cmd_status(data: dict) -> None:
    print(f"{'Feature':<12} {'Status':<12} {'Proofs'}")
    print("-" * 50)
    for f in data.get("features", []):
        proofs = ", ".join(p.get("type", "?") for p in f.get("proofs", []))
        print(f"{f.get('feature_id', '?'):<12} {f.get('status', '?'):<12} {proofs or '—'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Record feature execution proof")
    parser.add_argument("--feature", "-f", help="Feature id e.g. F002")
    parser.add_argument("--wp", help="Work package id e.g. WP-25")
    parser.add_argument("--type", "-t", choices=["commit", "apk", "analytics", "test", "audit"])
    parser.add_argument("--value", "-v", help="Proof value")
    parser.add_argument("--status", action="store_true", help="Print proof registry summary")
    args = parser.parse_args()

    data = _load()

    if args.status:
        cmd_status(data)
        return 0

    if not args.feature or not args.type or not args.value:
        parser.error("--feature, --type, --value required (or --status)")

    feature = _find_feature(data, args.feature)
    if feature is None:
        feature = {
            "feature_id": args.feature,
            "wp_id": args.wp,
            "status": "IN_PROGRESS",
            "proofs": [],
        }
        data.setdefault("features", []).append(feature)
    if args.wp:
        feature["wp_id"] = args.wp

    feature.setdefault("proofs", []).append({
        "type": args.type,
        "value": args.value,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    })
    _maybe_proven(feature)
    _save(data)
    print(f"   ✅ {args.feature} → {feature['status']} (+{args.type}: {args.value})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
