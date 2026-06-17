#!/usr/bin/env python3
"""Seed portfolio registry templates into runtime/factory/portfolio/."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / "templates" / "factory" / "portfolio"
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import ensure_runtime_tree, factory_dir  # noqa: E402

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    ensure_runtime_tree()
    dest = factory_dir("portfolio")
    dest.mkdir(parents=True, exist_ok=True)
    created = 0
    for tpl in TPL.glob("*.template.json"):
        name = tpl.name.replace(".template.json", ".json")
        out = dest / name
        if out.exists():
            continue
        text = tpl.read_text(encoding="utf-8").replace("{{DATE}}", NOW)
        out.write_text(text, encoding="utf-8")
        created += 1
        print(f"   ✅ {out.relative_to(ROOT)}")
    print(f"   Portfolio seeded ({created} new)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
