#!/usr/bin/env python3
"""Promote runtime failure entry to permanent knowledge/failures markdown."""
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

FAILURES_JSON = factory_dir("memory", "failures.json")
OUT_DIR = ROOT / "knowledge" / "failures"
TEMPLATE = ROOT / "knowledge" / "failures" / "TEMPLATE.md"


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "failure"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, help="FAIL-YYYY-NNN")
    parser.add_argument("--project", default="unknown", help="Portfolio slug or project name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing markdown")
    args = parser.parse_args()

    if not FAILURES_JSON.exists():
        print("Run: ./scripts/runtime/init-runtime.sh", file=sys.stderr)
        return 1

    data = json.loads(FAILURES_JSON.read_text(encoding="utf-8"))
    entry = next((e for e in data.get("entries", []) if e.get("id") == args.id), None)
    if entry is None:
        print(f"Not found: {args.id}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = _slugify(entry.get("title", args.id))
    out = OUT_DIR / f"{args.id}-{slug}.md"
    if out.exists() and not args.force:
        print(f"Already exists: {out.relative_to(ROOT)} (use --force)", file=sys.stderr)
        return 1

    tags = ", ".join(entry.get("tags", []))
    modules = ", ".join(entry.get("affected_modules", []))
    recorded = entry.get("recorded_at", datetime.now(timezone.utc).isoformat())[:10]

    body = f"""# {args.id}: {entry.get('title', '')}

| Field | Value |
|-------|-------|
| Project | {args.project} |
| Recorded | {recorded} |
| Tags | {tags or '—'} |
| Modules | {modules or '—'} |

## What failed

{entry.get('title', '')}

## Root cause

{entry.get('cause', '—')}

## What we tried

*(Add manual notes if needed)*

## Resolution

{entry.get('resolution', '—')}

## Reusable fix pattern

```
{entry.get('fix_pattern', entry.get('resolution', ''))}
```

## Preventive check

`{entry.get('preventive_check', '')}`

## Related

- Runtime: `runtime/factory/memory/failures.json`
- Query: `./scripts/factory/query-memory.sh --id {args.id}`
"""
    out.write_text(body, encoding="utf-8")
    entry["knowledge_file"] = str(out.relative_to(ROOT))
    entry["promoted_at"] = datetime.now(timezone.utc).isoformat()
    data["updated_at"] = entry["promoted_at"]
    FAILURES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
