#!/usr/bin/env python3
"""Promote experimental pattern to proven with evidence from a shipped app."""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXP = ROOT / "knowledge" / "patterns" / "experimental"
PROV = ROOT / "knowledge" / "patterns" / "proven"
NOW = datetime.now(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Pattern dir name e.g. offline_first")
    parser.add_argument("--evidence", required=True, help="Evidence summary e.g. app-slug D30 32%")
    parser.add_argument("--slug", default="", help="Portfolio app slug")
    args = parser.parse_args()

    src = EXP / args.name / "PATTERN.md"
    if not src.exists():
        print(f"Experimental pattern not found: {src.relative_to(ROOT)}", file=sys.stderr)
        return 1

    dest_dir = PROV / args.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "PATTERN.md"

    if dest.exists():
        text = dest.read_text(encoding="utf-8")
    else:
        shutil.copy2(src, dest)
        text = dest.read_text(encoding="utf-8")

    stamp = NOW.strftime("%Y-%m-%d")
    block = f"\n\n## Proven evidence ({stamp})\n\n- App: `{args.slug or 'n/a'}`\n- {args.evidence}\n"
    if "## Proven evidence" not in text:
        text = text.rstrip() + block
    else:
        text = text.rstrip() + f"\n- ({stamp}) App `{args.slug or 'n/a'}`: {args.evidence}\n"

    # Mark status at top if missing
    if "Status: proven" not in text:
        text = f"> **Status:** proven (promoted {stamp})\n\n" + text.lstrip()

    dest.write_text(text, encoding="utf-8")
    print(f"   ✅ proven → {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
