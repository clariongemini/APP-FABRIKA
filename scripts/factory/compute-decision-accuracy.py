#!/usr/bin/env python3
"""Compute PDC decision accuracy from reviewed decisions."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir, governance_runtime  # noqa: E402

REG = factory_dir("decision_accuracy", "registry.json")


def main() -> int:
    if not REG.exists():
        print("Run: ./scripts/factory/init-intelligence.sh", file=sys.stderr)
        return 1

    data = json.loads(REG.read_text(encoding="utf-8"))
    reviewed = [d for d in data.get("decisions", []) if d.get("accuracy_score") is not None]
    if reviewed:
        avg = round(sum(d["accuracy_score"] for d in reviewed) / len(reviewed) * 100)
        data["pdc_accuracy_pct"] = avg
    else:
        data["pdc_accuracy_pct"] = None

    data["computed_at"] = datetime.now(timezone.utc).isoformat()
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pct = data.get("pdc_accuracy_pct")
    print(f"   PDC Accuracy: {pct}%" if pct is not None else "   PDC Accuracy: n/a (no reviewed decisions)")

    egc_payload = {
        "pdc_accuracy_pct": pct,
        "factory_decision_accuracy_ref": "runtime/factory/decision_accuracy/registry.json",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "review_rule_days": 90,
    }
    for egc_path in (
        governance_runtime("egc", "PDC_DECISION_QUALITY.json"),
        ROOT / "governance" / "egc" / "PDC_DECISION_QUALITY.json",
    ):
        egc_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {}
        if egc_path.exists():
            try:
                existing = json.loads(egc_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        existing.update(egc_payload)
        egc_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("   ✅ synced → PDC_DECISION_QUALITY.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
