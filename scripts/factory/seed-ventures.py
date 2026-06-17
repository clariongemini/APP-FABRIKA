#!/usr/bin/env python3
"""Seed ventures registry into runtime/factory/ventures/."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / "templates" / "factory" / "ventures" / "ventures.template.json"
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import ensure_runtime_tree, factory_dir  # noqa: E402

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ensure_runtime_tree()
    dest = factory_dir("ventures", "ventures.json")
    if dest.exists():
        print("   ventures.json exists — skip seed")
        return 0
    text = TPL.read_text(encoding="utf-8").replace("{{DATE}}", NOW)
    dest.write_text(text, encoding="utf-8")
    print(f"   ✅ {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
