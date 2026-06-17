#!/usr/bin/env python3
"""Aggregate app outcomes → portfolio_outcomes.json + roi_history snapshot."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

OUT_DIR = factory_dir("outcomes")
NOW = datetime.now(timezone.utc)


def _read(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _avg(values: list[float]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def _status(apps: list[dict]) -> str:
    if not apps:
        return "AWAITING_DATA"
    with_users = [a for a in apps if a.get("users")]
    with_revenue = [a for a in apps if (a.get("mrr") or 0) > 0]
    with_roi = [a for a in apps if a.get("roi")]
    if with_roi and with_revenue:
        return "PROVEN"
    if with_users and (with_revenue or any(a.get("retention_d30") for a in apps)):
        return "ACTIVE"
    if apps:
        return "PARTIAL"
    return "AWAITING_DATA"


def main() -> int:
    app_data = _read(OUT_DIR / "app_outcomes.json")
    portfolio_apps = _read(factory_dir("portfolio", "apps.json")).get("apps", [])
    slug_names = {a.get("slug"): a.get("name") for a in portfolio_apps if a.get("slug")}

    apps = app_data.get("apps", [])
    enriched = []
    total_users = 0
    mrr_total = 0.0
    ret_d30 = []
    dev_days = []
    rois = []
    released_with_users = 0

    for app in apps:
        slug = app.get("slug", "")
        row = {
            "slug": slug,
            "name": slug_names.get(slug),
            "released": bool(app.get("released")),
            "users": app.get("users"),
            "retention_d7": app.get("retention_d7"),
            "retention_d30": app.get("retention_d30"),
            "mrr": app.get("mrr"),
            "development_days": app.get("development_days"),
            "development_cost": app.get("development_cost"),
            "roi": app.get("roi"),
            "recorded_at": app.get("recorded_at"),
        }
        enriched.append(row)
        if app.get("users"):
            total_users += int(app["users"])
            if app.get("released"):
                released_with_users += 1
        if app.get("mrr"):
            mrr_total += float(app["mrr"])
        if app.get("retention_d30") is not None:
            ret_d30.append(float(app["retention_d30"]))
        if app.get("development_days") is not None:
            dev_days.append(float(app["development_days"]))
        if app.get("roi") is not None:
            rois.append(float(app["roi"]))

    portfolio = {
        "generated_at": NOW.isoformat(),
        "schema": "factory.outcomes.portfolio.v1",
        "outcome_validation_status": _status(enriched),
        "apps_with_outcomes": len(enriched),
        "apps_released_with_users": released_with_users,
        "total_users": total_users if total_users else None,
        "portfolio_mrr": round(mrr_total, 2) if mrr_total else None,
        "avg_retention_d30": _avg(ret_d30),
        "avg_development_days": _avg(dev_days),
        "avg_roi": _avg(rois),
        "apps": enriched,
    }

    history = _read(OUT_DIR / "roi_history.json")
    snapshots = history.setdefault("snapshots", [])
    snapshots.append({
        "recorded_at": NOW.isoformat(),
        "outcome_validation_status": portfolio["outcome_validation_status"],
        "apps_with_outcomes": portfolio["apps_with_outcomes"],
        "total_users": portfolio["total_users"],
        "portfolio_mrr": portfolio["portfolio_mrr"],
        "avg_roi": portfolio["avg_roi"],
    })
    if len(snapshots) > 120:
        snapshots[:] = snapshots[-120:]
    history["updated_at"] = NOW.isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "portfolio_outcomes.json").write_text(
        json.dumps(portfolio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "roi_history.json").write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"   Outcome validation: {portfolio['outcome_validation_status']}")
    print(f"   Apps with outcomes: {portfolio['apps_with_outcomes']}")
    print(f"   ✅ portfolio_outcomes.json · roi_history.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
