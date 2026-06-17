#!/usr/bin/env python3
"""Record PDC decision with expected outcomes for later accuracy review."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir, governance_runtime  # noqa: E402

REG = factory_dir("decision_accuracy", "registry.json")


def _load() -> dict:
    if not REG.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(REG.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _next_id(decisions: list) -> str:
    year = datetime.now(timezone.utc).strftime("%Y")
    nums = []
    for d in decisions:
        m = re.match(rf"DEC-{year}-(\d+)", d.get("decision_id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"DEC-{year}-{max(nums, default=0) + 1:03d}"


def _find(data: dict, feature: str) -> dict | None:
    for d in data.get("decisions", []):
        if d.get("feature") == feature and d.get("status") != "reviewed":
            return d
    return None


def _score(expected: dict, actual: dict) -> float | None:
    pairs = []
    for key in expected:
        if key in actual and expected[key] is not None and actual[key] is not None:
            exp = float(expected[key])
            act = float(actual[key])
            if exp == 0:
                pairs.append(1.0 if act == 0 else max(0.0, 1.0 - abs(act) / 10))
            else:
                pairs.append(max(0.0, min(1.0, act / exp)))
    return round(sum(pairs) / len(pairs), 2) if pairs else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", "-f", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--expected-retention", type=float)
    parser.add_argument("--expected-conversion", type=float)
    parser.add_argument("--actual-retention", type=float)
    parser.add_argument("--actual-conversion", type=float)
    parser.add_argument("--review", action="store_true")
    args = parser.parse_args()

    data = _load()
    dec = _find(data, args.feature)

    if args.review or args.actual_retention is not None or args.actual_conversion is not None:
        if dec is None:
            dec = next((d for d in data.get("decisions", []) if d.get("feature") == args.feature), None)
        if dec is None:
            print(f"No decision for {args.feature}", file=sys.stderr)
            return 1
        actual = dec.setdefault("actual", {})
        if args.actual_retention is not None:
            actual["retention_delta_pct"] = args.actual_retention
        if args.actual_conversion is not None:
            actual["trial_conversion_delta_pct"] = args.actual_conversion
        score = _score(dec.get("expected", {}), actual)
        if score is not None:
            dec["accuracy_score"] = score
        dec["status"] = "reviewed"
        dec["reviewed_at"] = datetime.now(timezone.utc).isoformat()
        _save(data)
        print(f"   ✅ {dec['decision_id']} reviewed — accuracy {dec.get('accuracy_score', 'n/a')}")
        return 0

    if dec is None:
        dec = {
            "decision_id": _next_id(data.get("decisions", [])),
            "feature": args.feature,
            "title": args.title or f"{args.feature} priority decision",
            "decided_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "review_due": (datetime.now(timezone.utc) + timedelta(days=90)).strftime("%Y-%m-%d"),
            "expected": {},
            "actual": {},
            "status": "pending_review",
        }
        data.setdefault("decisions", []).append(dec)
    if args.expected_retention is not None:
        dec.setdefault("expected", {})["retention_delta_pct"] = args.expected_retention
    if args.expected_conversion is not None:
        dec.setdefault("expected", {})["trial_conversion_delta_pct"] = args.expected_conversion
    _save(data)
    print(f"   ✅ {dec['decision_id']} recorded for {args.feature}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
