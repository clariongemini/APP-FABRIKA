#!/usr/bin/env python3
"""Issue CERTIFIED_BY_FACTORY for an app before release."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

META = ROOT / ".factory" / "meta.json"
OUT_DIR = factory_dir("certification")


def _run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
    return r.returncode, r.stdout + r.stderr


def _audit_score() -> int | None:
    _, out = _run(["bash", "scripts/run-factory-audit.sh"])
    m = re.search(r"Audit:\s*✅\s*(\d+)", out)
    if not m:
        return None
    passed = int(m.group(1))
    m2 = re.search(r"❌\s*(\d+)", out)
    failed = int(m2.group(1)) if m2 else 0
    total = passed + failed
    return round(passed * 100 / total) if total else None


def _quality_gate_ok() -> bool:
    code, _ = _run(["bash", "scripts/factory-quality-gate.sh"])
    return code == 0


def _level(audit: int | None, qg_ok: bool, regression_ok: bool) -> str:
    if not qg_ok or audit is None:
        return "NONE"
    if audit >= 95 and regression_ok:
        return "GOLD"
    if audit >= 90:
        return "SILVER"
    if audit >= 80:
        return "BRONZE"
    return "NONE"


def main() -> int:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--name", required=True)
    args = p.parse_args()

    meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}
    qg_ok = _quality_gate_ok()
    audit = _audit_score()
    _, reg_out = _run([sys.executable, "scripts/factory/scan-regression.py"])
    regression_ok = "REGRESSION WARN" not in reg_out and "REGRESSION FAIL" not in reg_out

    level = _level(audit, qg_ok, regression_ok)
    cert = {
        "certified_by_factory": level != "NONE",
        "factory_version": meta.get("v4_target") or meta.get("version", "unknown"),
        "app": args.name,
        "slug": args.slug,
        "certification_level": level,
        "audit_score": audit,
        "quality_gate": 100 if qg_ok else 0,
        "regression_scan_clean": regression_ok,
        "release_ready": level in ("GOLD", "SILVER"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{args.slug}.json").write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")

    index_path = OUT_DIR / "index.json"
    index = {"apps": []}
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    apps = [a for a in index.get("apps", []) if a.get("slug") != args.slug]
    apps.append({"slug": args.slug, "name": args.name, "level": level, "release_ready": cert["release_ready"]})
    index["apps"] = apps
    index["updated_at"] = cert["generated_at"]
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    print(f"   CERTIFIED_BY_FACTORY: {args.name} → {level} (audit {audit}, qg {'pass' if qg_ok else 'fail'})")
    return 0 if cert["certified_by_factory"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
