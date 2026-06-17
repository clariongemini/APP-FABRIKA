#!/usr/bin/env python3
"""Record searchable memory entries (failure, success, lesson, adr)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

MEM = factory_dir("memory")
NOW = datetime.now(timezone.utc)


def _next_id(prefix: str, entries: list) -> str:
    year = NOW.strftime("%Y")
    nums = []
    for e in entries:
        m = re.match(rf"{prefix}-{year}-(\d+)", e.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    n = max(nums, default=0) + 1
    return f"{prefix}-{year}-{n:03d}"


def _load(name: str) -> dict:
    path = MEM / name
    if not path.exists():
        sys.stderr.write("Run: ./scripts/factory/init-intelligence.sh\n")
        raise SystemExit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def _save(name: str, data: dict) -> None:
    data["updated_at"] = NOW.isoformat()
    (MEM / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["failure", "success", "lesson", "adr"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--cause", default="")
    parser.add_argument("--resolution", default="")
    parser.add_argument("--modules", default="", help="Comma-separated module names")
    parser.add_argument("--fix-pattern", default="", help="Reusable fix pattern for regression DB")
    parser.add_argument("--preventive-check", default="", help="Grep token for quality gate scan")
    parser.add_argument("--related", default="", help="Comma-separated related entry IDs")
    args = parser.parse_args()

    file_map = {
        "failure": ("failures.json", "FAIL"),
        "success": ("successes.json", "WIN"),
        "lesson": ("lessons.json", "LESSON"),
        "adr": ("adr_index.json", "ADR"),
    }
    fname, prefix = file_map[args.type]
    data = _load(fname)
    entries = data.setdefault("entries", [])
    entry = {
        "id": _next_id(prefix, entries),
        "title": args.title,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "related": [r.strip() for r in args.related.split(",") if r.strip()],
        "recorded_at": NOW.isoformat(),
    }
    if args.type == "failure":
        entry.update({
            "cause": args.cause,
            "resolution": args.resolution,
            "fix_pattern": args.fix_pattern or args.resolution,
            "preventive_check": args.preventive_check,
            "affected_modules": [m.strip() for m in args.modules.split(",") if m.strip()],
        })
    elif args.type == "adr":
        entry["decision"] = args.cause or args.title
    entries.append(entry)
    _save(fname, data)
    print(f"   ✅ {entry['id']} — {args.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
