#!/usr/bin/env python3
"""Cross-type memory query with related-entry graph expansion (V3.1)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

TYPE_PREFIX = {
    "failures": "FAIL",
    "successes": "WIN",
    "lessons": "LESSON",
    "adr_index": "ADR",
}
FILES = ["failures.json", "successes.json", "lessons.json", "adr_index.json"]


def _mem_dir() -> Path:
    return factory_dir("memory")


def _load_all() -> list[tuple[str, dict]]:
    out = []
    mem = _mem_dir()
    for fname in FILES:
        path = mem / fname
        if not path.exists():
            continue
        kind = fname.replace(".json", "")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for entry in data.get("entries", []):
                out.append((kind, entry))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def _tokens(query: str) -> list[str]:
    return [t for t in re.split(r"[\s,_-]+", query.lower()) if len(t) > 1]


def _score(entry: dict, tokens: list[str]) -> int:
    hay = " ".join([
        entry.get("id", ""),
        entry.get("title", ""),
        entry.get("cause", ""),
        entry.get("resolution", ""),
        entry.get("decision", ""),
        " ".join(entry.get("tags", [])),
        " ".join(entry.get("affected_modules", [])),
    ]).lower()
    return sum(2 if t in entry.get("tags", []) else 1 for t in tokens if t in hay)


def _expand_related(entries: list[tuple[str, dict]], all_entries: list[tuple[str, dict]]) -> list[tuple[str, dict]]:
    by_id = {e.get("id"): (k, e) for k, e in all_entries if e.get("id")}
    seen = {e.get("id") for _, e in entries}
    expanded = list(entries)
    for _, e in entries:
        for rel in e.get("related", []):
            if rel in by_id and rel not in seen:
                seen.add(rel)
                expanded.append(by_id[rel])
    return expanded


def main() -> int:
    parser = argparse.ArgumentParser(description="Query factory memory (all types + related)")
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--id", dest="by_id", action="store_true")
    parser.add_argument("--graph", action="store_true", help="Expand related IDs")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return 1

    mem = _mem_dir()
    if not mem.exists():
        print("Memory not initialized. Run: ./scripts/runtime/init-runtime.sh", file=sys.stderr)
        return 1

    all_entries = _load_all()
    if args.by_id:
        hits = [(k, e) for k, e in all_entries if e.get("id", "").lower() == args.query.lower()]
    else:
        tokens = _tokens(args.query)
        scored = [(k, e, _score(e, tokens)) for k, e in all_entries if _score(e, tokens) > 0]
        scored.sort(key=lambda x: (-x[2], x[1].get("id", "")))
        hits = [(k, e) for k, e, _ in scored]

    if args.graph and hits:
        hits = _expand_related(hits, all_entries)

    if not hits:
        print(f"No matches for: {args.query}")
        return 0

    # Group output by type — ID-first lines as requested
    for kind, e in hits:
        prefix = TYPE_PREFIX.get(kind, kind.upper())
        eid = e.get("id", "?")
        title = e.get("title", e.get("decision", ""))
        print(f"{eid}")
        print(f"  [{kind}] {title}")
        if e.get("resolution"):
            print(f"  → {e['resolution'][:100]}")
        rel = e.get("related", [])
        if rel:
            print(f"  related: {', '.join(rel)}")
    print(f"\n{len(hits)} match(es) across {len(set(k for k, _ in hits))} type(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
