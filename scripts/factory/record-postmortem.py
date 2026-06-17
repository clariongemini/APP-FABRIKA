#!/usr/bin/env python3
"""Record project postmortem — deeper than failure log."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "knowledge" / "postmortems"
TEMPLATE = OUT / "TEMPLATE.md"
NOW = datetime.now(timezone.utc)


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:50] or "postmortem"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project name e.g. Offline Music App v1")
    parser.add_argument("--expected", required=True, help="What we expected")
    parser.add_argument("--actual", required=True, help="What happened")
    parser.add_argument("--why", required=True, help="Why it happened")
    parser.add_argument("--retry", required=True, help="What we would do differently")
    parser.add_argument("--result", default="failed", choices=["successful", "failed", "pivoted", "mixed"])
    parser.add_argument("--venture-slug", default="", dest="venture_slug")
    parser.add_argument("--patterns", default="", help="Comma-separated patterns")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    date = NOW.strftime("%Y-%m-%d")
    slug = _slugify(args.project)
    path = OUT / f"{date}-{slug}.md"

    patterns = ", ".join(p.strip() for p in args.patterns.split(",") if p.strip()) or "—"

    body = f"""# Postmortem: {args.project}

| Field | Value |
|-------|-------|
| Date | {date} |
| Result | {args.result} |
| Venture | {args.venture_slug or '—'} |
| Patterns | {patterns} |

## What we expected

{args.expected}

## What happened

{args.actual}

## Why it happened

{args.why}

## If we did it again

{args.retry}

## Links

- Failures: `knowledge/failures/`
- Venture: `knowledge/ventures/`
- Outcomes: `runtime/factory/outcomes/`
"""
    path.write_text(body, encoding="utf-8")
    print(f"   ✅ {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
