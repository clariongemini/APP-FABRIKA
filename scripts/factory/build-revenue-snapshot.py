#!/usr/bin/env python3
"""Build application revenue snapshot — NOT factory revenue (V3.1)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import analytics_output_dir, factory_dir, project_meta  # noqa: E402

OUT = factory_dir("revenue", "revenue_snapshot.json")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", help="Application name override")
    parser.add_argument("--manual-mrr", type=float)
    parser.add_argument("--manual-arpu", type=float)
    parser.add_argument("--manual-churn", type=float)
    parser.add_argument("--manual-trial-conversion", type=float)
    args = parser.parse_args()

    meta = project_meta()
    if OUT.exists():
        snap = json.loads(OUT.read_text(encoding="utf-8"))
    else:
        tpl = ROOT / "templates" / "factory" / "revenue_snapshot.template.json"
        raw = tpl.read_text(encoding="utf-8") if tpl.exists() else "{}"
        raw = raw.replace("{{APP_NAME}}", meta.get("app_name", "App"))
        raw = raw.replace("{{PACKAGE_NAME}}", meta.get("package_name", ""))
        snap = json.loads(raw)

    snap["scope"] = "application"
    snap["app"] = args.app or meta.get("app_name", "App")
    snap["package"] = meta.get("package_name")
    snap["generated_at"] = datetime.now(timezone.utc).isoformat()

    aid_metrics = analytics_output_dir() / "live_metrics.json"
    if not aid_metrics.exists():
        aid_metrics = ROOT / "governance" / "analytics" / "output" / "live_metrics.json"
    if aid_metrics.exists():
        try:
            live = json.loads(aid_metrics.read_text(encoding="utf-8"))
            conv = live.get("conversion", {})
            churn = live.get("churn", {})
            if conv.get("trial_to_paid") is not None:
                snap["trial_conversion_pct"] = conv["trial_to_paid"]
            if churn.get("d7_churn_rate") is not None:
                snap["churn_pct"] = churn["d7_churn_rate"]
            snap["aid_ref"] = str(aid_metrics.relative_to(ROOT))
        except json.JSONDecodeError:
            pass

    if args.manual_mrr is not None:
        snap["mrr"] = args.manual_mrr
        snap["arr"] = round(args.manual_mrr * 12, 2)
        snap["status"] = "PARTIAL"
    if args.manual_arpu is not None:
        snap["arpu"] = args.manual_arpu
    if args.manual_churn is not None:
        snap["churn_pct"] = args.manual_churn
    if args.manual_trial_conversion is not None:
        snap["trial_conversion_pct"] = args.manual_trial_conversion

    if snap.get("mrr") and snap.get("status") == "PIPELINE_READY":
        snap["status"] = "ACTIVE"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Mirror to runtime/analytics for consolidated tree
    mirror = analytics_output_dir() / "revenue_snapshot.json"
    mirror.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"   ✅ app={snap['app']} revenue → {OUT.relative_to(ROOT)} (status: {snap.get('status')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
