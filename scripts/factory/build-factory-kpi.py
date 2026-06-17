#!/usr/bin/env python3
"""Build Factory Success Health KPI from portfolio registry."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

PORT = factory_dir("portfolio")
NOW = datetime.now(timezone.utc)


def _read(name: str) -> dict:
    p = PORT / name
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _days_between(start: str | None, end: str | None) -> float | None:
    if not start or not end:
        return None
    try:
        a = datetime.fromisoformat(start.replace("Z", "+00:00"))
        b = datetime.fromisoformat(end.replace("Z", "+00:00"))
        return round((b - a).total_seconds() / 86400, 1)
    except (ValueError, TypeError):
        return None


def main() -> int:
    apps_data = _read("apps.json")
    apps = apps_data.get("apps", [])
    releases = _read("release_history.json").get("releases", [])

    outcomes_path = factory_dir("outcomes", "portfolio_outcomes.json")
    outcomes = {}
    if outcomes_path.exists():
        try:
            outcomes = json.loads(outcomes_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    created = len(apps)
    released = sum(1 for a in apps if a.get("status") in ("released", "profitable") or a.get("released_at"))
    profitable = sum(1 for a in apps if a.get("status") == "profitable" or (a.get("mrr") or 0) > 0)

    first_apk_days = []
    release_days = []
    ratings = []
    mrr_total = 0.0

    for app in apps:
        reg = app.get("registered_at")
        first = app.get("first_apk_at")
        rel = app.get("released_at")
        d1 = _days_between(reg, first)
        d2 = _days_between(reg, rel)
        if d1 is not None:
            first_apk_days.append(d1)
        if d2 is not None:
            release_days.append(d2)
        if app.get("playstore_rating"):
            ratings.append(float(app["playstore_rating"]))
        if app.get("mrr"):
            mrr_total += float(app["mrr"])

    avg_first = round(sum(first_apk_days) / len(first_apk_days), 1) if first_apk_days else None
    avg_release = round(sum(release_days) / len(release_days), 1) if release_days else None
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

    # Factory Success Health: 0-100 when real data exists
    success = None
    if created > 0:
        components = []
        if released:
            components.append(min(100, released / max(created, 1) * 100))
        if avg_first is not None:
            components.append(max(0, min(100, 100 - (avg_first - 3) * 10)))
        if avg_rating:
            components.append(avg_rating / 5 * 100)
        if components:
            success = round(sum(components) / len(components), 1)

    kpi = {
        "generated_at": NOW.isoformat(),
        "metric": "factory_success_health",
        "apps_created": created,
        "apps_released": released,
        "apps_profitable": profitable,
        "avg_time_to_first_apk_days": avg_first,
        "avg_time_to_release_days": avg_release,
        "avg_playstore_rating": avg_rating,
        "portfolio_mrr": round(mrr_total, 2) if mrr_total else outcomes.get("portfolio_mrr"),
        "portfolio_arr": round(mrr_total * 12, 2) if mrr_total else (
            round(float(outcomes["portfolio_mrr"]) * 12, 2) if outcomes.get("portfolio_mrr") else None
        ),
        "factory_success_health": success,
        "validation_status": "ACTIVE" if released >= 1 else "AWAITING_REAL_APPS",
        "outcome_validation_status": outcomes.get("outcome_validation_status", "AWAITING_DATA"),
        "total_users": outcomes.get("total_users"),
        "avg_retention_d30": outcomes.get("avg_retention_d30"),
        "avg_roi": outcomes.get("avg_roi"),
        "release_count": len(releases),
    }

    scorecard = {
        "generated_at": NOW.isoformat(),
        "factory_success_health": success,
        "factory_success_health_note": "Outcome metric — not factory-health.sh",
        **{k: kpi[k] for k in (
            "apps_created", "apps_released", "apps_profitable",
            "avg_time_to_first_apk_days", "avg_time_to_release_days",
            "avg_playstore_rating", "portfolio_mrr",
        )},
    }

    roi = {
        "generated_at": NOW.isoformat(),
        "dashboard": "factory_roi",
        "apps_created": kpi["apps_created"],
        "apps_released": kpi["apps_released"],
        "apps_profitable": kpi["apps_profitable"],
        "avg_time_to_first_apk_days": avg_first,
        "avg_time_to_release_days": avg_release,
        "portfolio_mrr": kpi["portfolio_mrr"],
        "portfolio_rating": avg_rating,
        "factory_success_health": success,
        "outcome_validation_status": kpi.get("outcome_validation_status"),
        "total_users": kpi.get("total_users"),
        "avg_retention_d30": kpi.get("avg_retention_d30"),
        "avg_roi": kpi.get("avg_roi"),
        "note": "Ship products, not documents.",
    }

    PORT.mkdir(parents=True, exist_ok=True)
    (PORT / "factory_kpi.json").write_text(json.dumps(kpi, indent=2) + "\n", encoding="utf-8")
    (PORT / "roi_dashboard.json").write_text(json.dumps(roi, indent=2) + "\n", encoding="utf-8")
    (PORT / "portfolio_scorecard.json").write_text(json.dumps(scorecard, indent=2) + "\n", encoding="utf-8")

    print(f"   Factory Success Health: {success if success is not None else 'n/a (register apps + releases)'}")
    print(f"   Outcome validation: {kpi.get('outcome_validation_status', 'AWAITING_DATA')}")
    print(f"   Apps: {created} created · {released} released · {profitable} profitable")
    print(f"   ✅ factory_kpi.json · roi_dashboard.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
