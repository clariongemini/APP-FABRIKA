#!/usr/bin/env python3
"""Enforce 90-day mandatory PDC decision outcome review (V3.1)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

REG = factory_dir("decision_accuracy", "registry.json")
REVIEW_DAYS = 90


def main() -> int:
    if not REG.exists():
        print("Decision registry not initialized.", file=sys.stderr)
        return 1

    data = json.loads(REG.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc).date()
    overdue = []
    pending_review = []

    for d in data.get("decisions", []):
        due = d.get("review_due")
        status = d.get("status", "pending_review")
        if not due:
            continue
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            continue
        if status != "reviewed" and now >= due_date:
            overdue.append(d)
            d["status"] = "OVERDUE_REVIEW"
        elif status == "pending_review":
            pending_review.append(d)

    out_path = factory_dir("decision_accuracy", "review_enforcement.json")
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rule": f"Every PDC decision must receive actual outcome within {REVIEW_DAYS} days",
        "overdue_count": len(overdue),
        "overdue": [{"decision_id": d.get("decision_id"), "feature": d.get("feature"), "review_due": d.get("review_due")} for d in overdue],
        "pending_review_count": len(pending_review),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if overdue:
        print(f"   ❌ {len(overdue)} decision(s) OVERDUE for 90-day actual outcome review:")
        for d in overdue:
            print(f"      {d.get('decision_id')} ({d.get('feature')}) due {d.get('review_due')}")
        return 1
    print(f"   ✅ Decision review enforcement OK ({len(pending_review)} pending, 0 overdue)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
