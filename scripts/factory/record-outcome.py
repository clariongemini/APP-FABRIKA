#!/usr/bin/env python3
"""Record or update per-app outcome metrics (users, retention, revenue, ROI)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

OUTCOMES = factory_dir("outcomes", "app_outcomes.json")
NOW = datetime.now(timezone.utc)


def _load() -> dict:
    if not OUTCOMES.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(OUTCOMES.read_text(encoding="utf-8"))


def _compute_roi(mrr: float | None, cost: float | None, dev_days: float | None) -> float | None:
    if mrr is None or mrr <= 0:
        return None
    basis = cost if cost and cost > 0 else None
    if basis is None and dev_days and dev_days > 0:
        basis = dev_days * 100.0  # placeholder daily burn when cost unknown
    if basis is None or basis <= 0:
        return None
    return round((mrr * 12) / basis, 2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Record app outcome metrics")
    parser.add_argument("--slug", required=True, help="Portfolio slug e.g. my-app")
    parser.add_argument("--released", action="store_true", help="App is released")
    parser.add_argument("--users", type=int)
    parser.add_argument("--retention-d7", type=float, dest="retention_d7")
    parser.add_argument("--retention-d30", type=float, dest="retention_d30")
    parser.add_argument("--mrr", type=float)
    parser.add_argument("--development-days", type=float, dest="development_days")
    parser.add_argument("--development-hours", type=float, dest="development_hours")
    parser.add_argument("--development-cost", type=float, dest="development_cost")
    parser.add_argument("--maintenance-cost", type=float, dest="maintenance_cost", help="Monthly maintenance cost")
    parser.add_argument("--ai-usage-pct", type=float, dest="ai_usage_pct", help="AI-assisted dev percent 0-100")
    parser.add_argument("--launch-duration-days", type=float, dest="launch_duration_days")
    parser.add_argument("--feature-count", type=int, dest="feature_count")
    parser.add_argument("--refund-rate", type=float, dest="refund_rate", help="Refund rate percent")
    parser.add_argument("--roi", type=float, help="Override computed ROI")
    parser.add_argument("--crash-rate", type=float, dest="crash_rate", help="Crash rate 0-1 e.g. 0.02")
    parser.add_argument("--rating", type=float, help="Store rating e.g. 4.6")
    parser.add_argument("--uninstall-rate", type=float, dest="uninstall_rate", help="Uninstall percent e.g. 12.0")
    parser.add_argument("--tags", default="", help="Comma-separated tags for pattern hints")
    parser.add_argument("--patterns", default="", help="Comma-separated pattern names e.g. offline_first,subscription_app")
    parser.add_argument("--onboarding", default="", help="minimal|tutorial|value-first|paywall-first")
    parser.add_argument("--monetization", default="", help="subscription|ads|freemium|one-time|hybrid")
    parser.add_argument("--architecture", default="", help="clean-10-module|feature-heavy|monolith-lite")
    parser.add_argument("--offline-first", action="store_true", dest="offline_first")
    parser.add_argument("--source", default="manual", help="AID | play_console | revenue | manual")
    args = parser.parse_args()

    data = _load()
    apps = data.setdefault("apps", [])
    entry = next((a for a in apps if a.get("slug") == args.slug), None)
    if entry is None:
        entry = {"slug": args.slug, "released": False}
        apps.append(entry)

    if args.released:
        entry["released"] = True
    if args.users is not None:
        entry["users"] = args.users
    if args.retention_d7 is not None:
        entry["retention_d7"] = args.retention_d7
    if args.retention_d30 is not None:
        entry["retention_d30"] = args.retention_d30
    if args.mrr is not None:
        entry["mrr"] = args.mrr
    if args.development_days is not None:
        entry["development_days"] = args.development_days
    if args.development_hours is not None:
        entry["development_hours"] = args.development_hours
    if args.development_cost is not None:
        entry["development_cost"] = args.development_cost
    if args.maintenance_cost is not None:
        entry["maintenance_cost"] = args.maintenance_cost
    if args.ai_usage_pct is not None:
        entry["ai_usage_pct"] = args.ai_usage_pct
    if args.launch_duration_days is not None:
        entry["launch_duration_days"] = args.launch_duration_days
    if args.feature_count is not None:
        entry["feature_count"] = args.feature_count
    if args.refund_rate is not None:
        entry["refund_rate"] = args.refund_rate

    roi = args.roi if args.roi is not None else _compute_roi(
        entry.get("mrr"), entry.get("development_cost"), entry.get("development_days")
    )
    if roi is not None:
        entry["roi"] = roi
    if args.crash_rate is not None:
        entry["crash_rate"] = args.crash_rate
    if args.rating is not None:
        entry["rating"] = args.rating
    if args.uninstall_rate is not None:
        entry["uninstall_rate"] = args.uninstall_rate
    if args.offline_first:
        entry["offline_first"] = True
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        existing = entry.setdefault("tags", [])
        for t in tags:
            if t not in existing:
                existing.append(t)
    if args.patterns:
        patterns = [p.strip() for p in args.patterns.split(",") if p.strip()]
        entry["patterns"] = patterns
    if args.onboarding:
        entry["onboarding"] = args.onboarding
    if args.monetization:
        entry["monetization"] = args.monetization
    if args.architecture:
        entry["architecture"] = args.architecture

    sources = entry.setdefault("sources", [])
    if args.source and args.source not in sources:
        sources.append(args.source)

    entry["recorded_at"] = NOW.isoformat()
    data["updated_at"] = NOW.isoformat()
    OUTCOMES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ Outcome recorded: {args.slug} → {OUTCOMES.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
