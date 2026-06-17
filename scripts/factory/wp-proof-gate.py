#!/usr/bin/env python3
"""CDID WP closure → Proof Required → Feature PROVEN gate (V3.1 operational)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir, project_meta  # noqa: E402

GENERATED = ROOT / "governance" / "cdid" / "GENERATED_WORK_PACKAGES.json"
QUEUE = ROOT / "governance" / "executive" / "APPROVAL_QUEUE.md"
REGISTRY = factory_dir("proof", "proof_registry.json")
REQUIRED_PROOF = {"commit", "apk", "analytics"}
RELEASE_STEPS = {"release", "qa"}


def _load_registry() -> dict:
    if not REGISTRY.exists():
        return {"features": []}
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _feature_proofs(feature_id: str, reg: dict) -> dict | None:
    for f in reg.get("features", []):
        if f.get("feature_id") == feature_id:
            return f
    return None


def _proof_types(feature: dict) -> set[str]:
    return {p.get("type") for p in feature.get("proofs", []) if p.get("type")}


def _queue_closed_wps() -> list[dict]:
    closed = []
    if not QUEUE.exists():
        return closed
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| WP-"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 8:
            continue
        status = parts[7].strip("` ").lower()
        if status in ("done", "completed", "closed", "released"):
            closed.append({"wp_id": parts[1], "feature_id": parts[2], "status": status})
    return closed


def _wps_by_feature() -> dict[str, list[dict]]:
    if not GENERATED.exists():
        return {}
    data = json.loads(GENERATED.read_text(encoding="utf-8"))
    by_f: dict[str, list] = {}
    for w in data.get("work_packages", []):
        by_f.setdefault(w.get("feature_id", ""), []).append(w)
    return by_f


def _all_release_wps_done(feature_id: str, by_f: dict, queue_closed: set[str]) -> bool:
    wps = by_f.get(feature_id, [])
    release_wps = [w for w in wps if w.get("step") in RELEASE_STEPS or "release" in w.get("title", "").lower()]
    if not release_wps:
        release_wps = wps
    if not release_wps:
        return False
    return all(w.get("wp_id") in queue_closed or w.get("status", "").lower() in ("done", "completed", "closed") for w in release_wps)


def audit() -> dict:
    reg = _load_registry()
    queue_closed = {c["wp_id"] for c in _queue_closed_wps()}
    by_f = _wps_by_feature()
    results = []

    for feature_id, wps in by_f.items():
        if not feature_id:
            continue
        feat = _feature_proofs(feature_id, reg) or {"feature_id": feature_id, "status": "PLANNED", "proofs": []}
        types = _proof_types(feat)
        wps_closed = _all_release_wps_done(feature_id, by_f, queue_closed)
        missing = REQUIRED_PROOF - types

        if wps_closed and feat.get("status") != "PROVEN":
            status = "BLOCKED_PROOF" if missing else "READY_TO_PROVE"
        elif feat.get("status") == "PROVEN":
            status = "PROVEN"
        else:
            status = "IN_PROGRESS"

        results.append({
            "feature_id": feature_id,
            "status": status,
            "wps_closed": wps_closed,
            "missing_proofs": sorted(missing),
            "proof_types": sorted(types),
        })

    blocked = [r for r in results if r["status"] == "BLOCKED_PROOF"]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "principle": "WP Closed → Proof Required → Feature PROVEN",
        "required_proof_types": sorted(REQUIRED_PROOF),
        "features": results,
        "blocked_count": len(blocked),
        "blocked_features": [b["feature_id"] for b in blocked],
    }


def close_wp(wp_id: str, feature_id: str, auto_proof: bool = False) -> int:
    """Mark WP closed in queue metadata and enforce proof on feature."""
    report = audit()
    feat = next((f for f in report["features"] if f["feature_id"] == feature_id), None)
    if feat and feat["status"] == "BLOCKED_PROOF":
        print(f"   ❌ {feature_id}: WP {wp_id} closed but PROOF MISSING: {feat['missing_proofs']}")
        print("   Required: commit + apk + analytics before PROVEN")
        if auto_proof:
            _try_auto_proofs(feature_id)
            report = audit()
            feat = next((f for f in report["features"] if f["feature_id"] == feature_id), None)
        if feat and feat["status"] == "BLOCKED_PROOF":
            return 1
    print(f"   ✅ {wp_id} → {feature_id} proof gate OK (status: {feat['status'] if feat else 'unknown'})")
    return 0


def _try_auto_proofs(feature_id: str) -> None:
    script = ROOT / "scripts" / "factory" / "record-proof.py"
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
        subprocess.run([sys.executable, str(script), "-f", feature_id, "-t", "commit", "-v", sha], check=False)
    except (subprocess.CalledProcessError, OSError):
        pass


def sync_from_cdid() -> int:
    """Called at end of CDID cycle — write proof_gate.json + warn on blocked."""
    out = factory_dir("proof", "proof_gate.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    report = audit()
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["blocked_count"]:
        print(f"   ⚠️  Proof gate: {report['blocked_count']} feature(s) BLOCKED — {report['blocked_features']}")
    else:
        print("   ✅ Proof gate: no blocked features")
    return 1 if report["blocked_count"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="WP → Proof → PROVEN gate")
    parser.add_argument("--audit", action="store_true", help="Write proof_gate.json report")
    parser.add_argument("--sync-cdid", action="store_true", help="CDID cycle hook")
    parser.add_argument("--close-wp", metavar="WP-ID")
    parser.add_argument("--feature", "-f")
    parser.add_argument("--auto-proof", action="store_true")
    args = parser.parse_args()

    if args.sync_cdid or args.audit:
        return sync_from_cdid()
    if args.close_wp and args.feature:
        return close_wp(args.close_wp, args.feature, args.auto_proof)

    report = audit()
    print(json.dumps(report, indent=2))
    return 1 if report["blocked_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
