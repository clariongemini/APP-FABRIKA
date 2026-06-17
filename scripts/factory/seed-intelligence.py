#!/usr/bin/env python3
"""Seed factory intelligence JSON — prefers runtime/factory/ (V3.1)."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import ensure_runtime_tree, factory_dir, project_meta, runtime_root  # noqa: E402

TPL = ROOT / "templates" / "factory"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_base() -> Path:
    env = os.environ.get("RUNTIME_FACTORY_ROOT")
    if env:
        return Path(env)
    ensure_runtime_tree()
    return factory_dir()


def subst(text: str, meta: dict) -> str:
    return (
        text.replace("{{DATE}}", NOW)
        .replace("{{APP_NAME}}", meta.get("app_name", "Factory"))
        .replace("{{PACKAGE_NAME}}", meta.get("package_name", "com.ulas.factory"))
    )


def write_from_template(rel_tpl: str, dest: Path, meta: dict) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    tpl = TPL / rel_tpl
    if tpl.exists():
        dest.write_text(subst(tpl.read_text(encoding="utf-8"), meta), encoding="utf-8")
    else:
        dest.write_text(json.dumps({"version": "1.0", "updated_at": NOW}, indent=2) + "\n", encoding="utf-8")


def migrate_governance_memory(run: Path) -> None:
    for gov_path in (
        ROOT / "governance" / "memory" / "FAILURE_HISTORY.json",
        runtime_root() / "governance" / "memory" / "FAILURE_HISTORY.json",
    ):
        dest = run / "memory" / "failures.json"
        if not gov_path.exists() or not dest.exists():
            continue
        try:
            gov = json.loads(gov_path.read_text(encoding="utf-8"))
            fac = json.loads(dest.read_text(encoding="utf-8"))
            existing_ids = {e.get("id") for e in fac.get("entries", [])}
            for i, entry in enumerate(gov.get("entries", []), start=1):
                eid = entry.get("id") or f"FAIL-MIG-{i:03d}"
                if eid in existing_ids:
                    continue
                fac.setdefault("entries", []).append({
                    "id": eid,
                    "title": entry.get("title", entry.get("summary", "Migrated failure")),
                    "tags": entry.get("tags", []),
                    "cause": entry.get("cause", ""),
                    "resolution": entry.get("resolution", entry.get("fix", "")),
                    "affected_modules": entry.get("affected_modules", []),
                    "related": entry.get("related", []),
                    "recorded_at": entry.get("recorded_at", NOW),
                    "migrated_from": str(gov_path.relative_to(ROOT)),
                })
            dest.write_text(json.dumps(fac, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            pass


def main() -> int:
    meta = project_meta()
    app_name = meta.get("app_name", "Factory")
    run = _run_base()
    mappings = [
        ("proof_registry.template.json", run / "proof" / "proof_registry.json"),
        ("memory_failures.template.json", run / "memory" / "failures.json"),
        ("memory_successes.template.json", run / "memory" / "successes.json"),
        ("memory_lessons.template.json", run / "memory" / "lessons.json"),
        ("memory_adr_index.template.json", run / "memory" / "adr_index.json"),
        ("decision_accuracy.template.json", run / "decision_accuracy" / "registry.json"),
        ("revenue_snapshot.template.json", run / "revenue" / "revenue_snapshot.json"),
        ("benchmark_factory.template.json", run / "benchmark" / "factory.json"),
        ("benchmark_product.template.json", run / "benchmark" / "product.json"),
        ("benchmark_market.template.json", run / "benchmark" / "market.json"),
        ("benchmark_summary.template.json", run / "benchmark" / "summary.json"),
        ("benchmark_velocity.template.json", run / "benchmark" / "velocity.json"),
        ("telemetry_cycle.template.json", runtime_root() / "telemetry" / "cycle_log.json"),
    ]
    created = 0
    for tpl, dest in mappings:
        before = dest.exists()
        write_from_template(tpl, dest, meta)
        if not before and dest.exists():
            created += 1
            try:
                print(f"   ✅ {dest.relative_to(ROOT)}")
            except ValueError:
                print(f"   ✅ {dest}")
    migrate_governance_memory(run)
    print(f"   Factory intelligence seeded ({created} new) → {run.relative_to(ROOT) if run.is_relative_to(ROOT) else run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
