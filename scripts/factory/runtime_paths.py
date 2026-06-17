#!/usr/bin/env python3
"""Canonical runtime path resolver — V3.1 consolidation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def runtime_root() -> Path:
    return ROOT / "runtime"


def ensure_runtime_tree() -> None:
    for sub in (
        "governance/memory", "governance/execution", "governance/egc",
        "factory/proof", "factory/memory", "factory/decision_accuracy",
        "factory/revenue", "factory/benchmark", "factory/portfolio",
        "factory/certification", "factory/regression", "factory/outcomes",
        "factory/ventures", "analytics", "telemetry",
    ):
        (runtime_root() / sub).mkdir(parents=True, exist_ok=True)


def factory_dir(*parts: str) -> Path:
    ensure_runtime_tree()
    return runtime_root() / "factory" / Path(*parts)


def telemetry_path(name: str) -> Path:
    ensure_runtime_tree()
    return runtime_root() / "telemetry" / name


def analytics_output_dir() -> Path:
    ensure_runtime_tree()
    d = runtime_root() / "analytics"
    d.mkdir(parents=True, exist_ok=True)
    return d


def governance_runtime(*parts: str) -> Path:
    ensure_runtime_tree()
    return runtime_root() / "governance" / Path(*parts)


def project_meta() -> dict:
    meta_path = ROOT / ".factory" / "project.json"
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"app_name": "Factory", "package_name": "com.ulas.factory", "slug": "factory"}


def legacy_factory_dir(*parts: str) -> Path:
    """Read-only fallback during migration."""
    p = ROOT / "factory" / "runtime" / Path(*parts)
    return p
