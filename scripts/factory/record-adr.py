#!/usr/bin/env python3
"""Record ADR with full lifecycle metadata → knowledge/adr + memory index + LAST_DECISION."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

ADR_DIR = ROOT / "knowledge" / "adr" / "decisions"
LAST_DECISION = ROOT / ".factory" / "context" / "LAST_DECISION.md"
TEMPLATE = ROOT / "knowledge" / "adr" / "ADR.template.md"
MEM_ADR = factory_dir("memory", "adr_index.json")
NOW = datetime.now(timezone.utc)
VALID_STATUS = {"proposed", "accepted", "deprecated", "superseded"}


def _next_id(entries: list) -> str:
    year = NOW.strftime("%Y")
    nums = []
    for e in entries:
        m = re.match(rf"ADR-{year}-(\d+)", e.get("id", ""))
        if m:
            nums.append(int(m.group(1)))
    return f"ADR-{year}-{max(nums, default=0) + 1:03d}"


def _load_mem() -> dict:
    if not MEM_ADR.exists():
        sys.stderr.write("Run: ./scripts/runtime/init-runtime.sh\n")
        raise SystemExit(1)
    return json.loads(MEM_ADR.read_text(encoding="utf-8"))


def _save_mem(data: dict) -> None:
    data["updated_at"] = NOW.isoformat()
    MEM_ADR.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_adr_md(adr_id: str, args: argparse.Namespace, review_due: str) -> Path:
    ADR_DIR.mkdir(parents=True, exist_ok=True)
    path = ADR_DIR / f"{adr_id}.md"
    alt_rows = []
    for i, alt in enumerate(args.alternatives):
        reason = args.alternative_reasons[i] if i < len(args.alternative_reasons) else ""
        alt_rows.append(f"| {alt} | rejected | {reason} |")
    if not alt_rows:
        alt_rows.append("| — | — | — |")

    modules = ", ".join(args.modules) if args.modules else "—"
    risks = "\n".join(f"- {r}" for r in args.risks) if args.risks else "- "

    body = f"""# {adr_id}: {args.title}

| Field | Value |
|-------|-------|
| Status | {args.status} |
| Date | {NOW.strftime('%Y-%m-%d')} |
| Review due | {review_due} |
| Supersedes | {args.supersedes or '—'} |
| Superseded by | — |

## Context

{args.context or args.title}

## Decision

{args.decision or args.title}

## Alternatives considered

| Option | Outcome | Reason |
|--------|---------|--------|
{chr(10).join(alt_rows)}

## Consequences

### Positive

{args.positive or '- '}

### Risks

{risks}

### Affected modules

- {modules.replace(', ', chr(10) + '- ') if modules != '—' else '—'}

## Follow-up

- [ ] Review on {review_due}
- Related patterns: `knowledge/patterns/`
"""
    path.write_text(body, encoding="utf-8")
    return path


def _write_last_decision(adr_id: str, args: argparse.Namespace, review_due: str) -> None:
    LAST_DECISION.parent.mkdir(parents=True, exist_ok=True)
    alts = "\n".join(
        f"{i + 1}. **{a}** — {(args.alternative_reasons[i] if i < len(args.alternative_reasons) else '')}"
        for i, a in enumerate(args.alternatives)
    ) or "1. *(none recorded)*"
    risks = "\n".join(f"- {r}" for r in args.risks) or "- —"
    text = f"""# Last Decision

| Field | Value |
|-------|-------|
| ID | {adr_id} |
| Date | {NOW.strftime('%Y-%m-%d')} |
| Status | {args.status} |
| Decider | {args.decider} |

## Decision

{args.decision or args.title}

## Context

{args.context or '—'}

## Alternatives considered

{alts}

## Consequences

- Positive: {args.positive or '—'}
- Risks:
{risks}
- Review date: {review_due}

## Links

- Full ADR: `knowledge/adr/decisions/{adr_id}.md`
"""
    LAST_DECISION.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Record ADR with lifecycle")
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", default="accepted", choices=sorted(VALID_STATUS))
    parser.add_argument("--context", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--positive", default="")
    parser.add_argument("--alternative", action="append", default=[], dest="alternatives")
    parser.add_argument("--alternative-reason", action="append", default=[], dest="alternative_reasons")
    parser.add_argument("--risk", action="append", default=[], dest="risks")
    parser.add_argument("--modules", default="", help="Comma-separated modules")
    parser.add_argument("--review-days", type=int, default=90)
    parser.add_argument("--supersedes", default="")
    parser.add_argument("--decider", default="Architect")
    args = parser.parse_args()

    if args.status not in VALID_STATUS:
        print(f"Invalid status: {args.status}", file=sys.stderr)
        return 1

    modules = [m.strip() for m in args.modules.split(",") if m.strip()]
    review_due = (NOW + timedelta(days=args.review_days)).strftime("%Y-%m-%d")

    mem = _load_mem()
    entries = mem.setdefault("entries", [])
    adr_id = _next_id(entries)

    adr_path = _write_adr_md(adr_id, args, review_due)
    _write_last_decision(adr_id, args, review_due)

    entry = {
        "id": adr_id,
        "title": args.title,
        "decision": args.decision or args.title,
        "status": args.status,
        "tags": modules,
        "review_due": review_due,
        "supersedes": args.supersedes or None,
        "file": str(adr_path.relative_to(ROOT)),
        "recorded_at": NOW.isoformat(),
    }
    entries.append(entry)
    _save_mem(mem)

    print(f"   ✅ {adr_id} → {adr_path.relative_to(ROOT)}")
    print(f"   ✅ LAST_DECISION.md updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
