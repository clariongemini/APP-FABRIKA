#!/usr/bin/env python3
"""Record Software Venture — problem/solution/scores for venture factory layer."""
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

REG = factory_dir("ventures", "ventures.json")
KNOW = ROOT / "knowledge" / "ventures"
NOW = datetime.now(timezone.utc)

VALID_RESULTS = {"successful", "failed", "pivoted", "ongoing", "success", "başarılı"}


def _load() -> dict:
    if not REG.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(REG.read_text(encoding="utf-8"))


def _next_id(ventures: list) -> str:
    year = NOW.strftime("%Y")
    nums = []
    for v in ventures:
        m = re.match(rf"VEN-{year}-(\d+)", v.get("venture_id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"VEN-{year}-{max(nums, default=0) + 1:03d}"


def _write_md(entry: dict) -> Path:
    KNOW.mkdir(parents=True, exist_ok=True)
    slug = entry.get("slug", entry["venture_id"])
    path = KNOW / f"{slug}.md"
    scores = entry.get("scores", {})
    body = f"""# {entry.get('solution', entry.get('title', slug))}

| Field | Value |
|-------|-------|
| Venture ID | {entry['venture_id']} |
| Slug | {entry.get('slug', '—')} |
| Result | {entry.get('result', 'ongoing')} |
| Recorded | {entry.get('recorded_at', '')[:10]} |

## Problem

{entry.get('problem', '—')}

## Solution

{entry.get('solution', '—')}

## Scores (1–10)

| Dimension | Score |
|-----------|-------|
| Market | {scores.get('market', '—')} |
| Competition | {scores.get('competition', '—')} |
| Revenue potential | {scores.get('revenue', '—')} |

## Patterns

{', '.join(entry.get('patterns', [])) or '—'}

## Outcome link

Portfolio slug: `{entry.get('portfolio_slug', entry.get('slug', '—'))}`
"""
    path.write_text(body, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="Venture slug e.g. offline-music-v1")
    parser.add_argument("--problem", required=True)
    parser.add_argument("--solution", required=True)
    parser.add_argument("--market", type=int, help="Market score 1-10")
    parser.add_argument("--competition", type=int, help="Competition score 1-10")
    parser.add_argument("--revenue", type=int, help="Revenue potential 1-10")
    parser.add_argument("--result", default="ongoing")
    parser.add_argument("--patterns", default="", help="Comma-separated pattern names")
    parser.add_argument("--portfolio-slug", default="", dest="portfolio_slug")
    parser.add_argument("--no-md", action="store_true", help="Skip knowledge/ventures markdown")
    args = parser.parse_args()

    data = _load()
    ventures = data.setdefault("ventures", [])
    entry = next((v for v in ventures if v.get("slug") == args.slug), None)
    if entry is None:
        entry = {"venture_id": _next_id(ventures), "slug": args.slug}
        ventures.append(entry)

    entry["problem"] = args.problem
    entry["solution"] = args.solution
    entry["scores"] = {
        "market": args.market,
        "competition": args.competition,
        "revenue": args.revenue,
    }
    entry["result"] = args.result
    entry["patterns"] = [p.strip() for p in args.patterns.split(",") if p.strip()]
    if args.portfolio_slug:
        entry["portfolio_slug"] = args.portfolio_slug
    entry["recorded_at"] = NOW.isoformat()
    data["updated_at"] = entry["recorded_at"]
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not args.no_md:
        md = _write_md(entry)
        print(f"   ✅ {md.relative_to(ROOT)}")

    print(f"   ✅ {entry['venture_id']} — {args.solution}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
