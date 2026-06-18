#!/usr/bin/env python3
"""Collect test failures into evidence manifest + runtime report."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent.parent / "ULAS" / "bin"
sys.path.insert(0, str(_ENGINE))
import gradle_test_parser as gtp  # noqa: E402

SVOS = Path(__file__).resolve().parent.parent
REPO_ROOT = SVOS.parent


def main() -> int:
    if len(sys.argv) < 2:
        print("Kullanım: collect-test-failures.py <venture-slug> [gradle-log] [codebase-path]", file=sys.stderr)
        return 1
    venture = sys.argv[1]
    log_arg = sys.argv[2] if len(sys.argv) > 2 else ""
    codebase_arg = sys.argv[3] if len(sys.argv) > 3 else ""
    venture_json = SVOS / "08-ventures" / venture / "venture.json"
    if codebase_arg:
        codebase = Path(codebase_arg)
    elif venture_json.is_file():
        meta = json.loads(venture_json.read_text())
        resolved = meta.get("codebase_resolved") or meta.get("codebase_path", "")
        codebase = Path(resolved) if Path(resolved).is_absolute() else REPO_ROOT / resolved
    else:
        print(f"ERROR: venture not found and no codebase path: {venture}", file=sys.stderr)
        return 1

    junit_variant = "testDebugUnitTest"
    if venture_json.is_file():
        meta = json.loads(venture_json.read_text())
        junit_variant = gtp.load_bridge_config(SVOS, meta).get("junit_results_variant", junit_variant)

    log_path: Path | None = None
    if log_arg and log_arg not in ("/dev/null", "-"):
        log_path = Path(log_arg)

    failures: list[dict] = []
    if log_path and log_path.is_file() and log_path.stat().st_size > 0:
        failures = gtp.parse_failed_from_gradle_log(log_path.read_text(encoding="utf-8", errors="replace"))
    junit = gtp.collect_junit_failures(codebase.resolve(), variant=junit_variant)
    if junit:
        by_test = {f["test"]: f for f in failures}
        for j in junit:
            by_test.setdefault(j["test"], j)
            if j.get("message"):
                by_test[j["test"]]["message"] = j["message"]
        failures = list(by_test.values())

    summary = None
    if log_path and log_path.is_file() and log_path.stat().st_size > 0:
        summary = gtp.parse_gradle_summary(log_path.read_text(encoding="utf-8", errors="replace"))

    clusters = gtp.cluster_failures(failures)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "venture_slug": venture,
        "collected_at": ts,
        "summary": summary,
        "failed_count": len(failures),
        "failures": failures,
        "clusters": clusters,
    }

    out_dir = SVOS / "10-runtime" / "evidence" / venture
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "test-failure-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_path = SVOS / "07-evidence" / venture / "manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for src in manifest.get("sources", []):
            if src.get("type") == "unit_test":
                src["failed_tests"] = [f["test"] for f in failures]
                if summary:
                    src["total"] = summary.get("total")
                    src["failed"] = summary.get("failed")
                    src["passed"] = summary.get("passed")
        manifest["failure_report_ref"] = str(report_path.relative_to(SVOS))
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        runtime_manifest = SVOS / "10-runtime" / "evidence" / venture / "manifest.json"
        runtime_manifest.parent.mkdir(parents=True, exist_ok=True)
        runtime_manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"report": str(report_path.relative_to(REPO_ROOT)), "failures": len(failures)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
