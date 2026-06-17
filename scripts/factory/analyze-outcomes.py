#!/usr/bin/env python3
"""Analyze portfolio outcomes → pattern recommendations and optional snapshot export."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

OUTCOMES = factory_dir("outcomes", "app_outcomes.json")
SNAPSHOT_DIR = ROOT / "knowledge" / "outcomes" / "snapshots"

# Heuristic: map tags/signals to pattern paths
PATTERN_HINTS = [
    ("subscription_app", lambda a: (a.get("mrr") or 0) > 0 or "subscription_app" in (a.get("patterns") or [])),
    ("offline_first", lambda a: a.get("offline_first") or "offline_first" in (a.get("patterns") or [])),
    ("media_app", lambda a: "media" in (a.get("tags") or []) or "media_app" in (a.get("patterns") or [])),
    ("chat_app", lambda a: "chat" in (a.get("tags") or []) or "chat_app" in (a.get("patterns") or [])),
    ("ai_assistant", lambda a: "ai" in (a.get("tags") or []) or "ai_assistant" in (a.get("patterns") or [])),
]


def _score(app: dict) -> float:
    """Composite success score for ranking."""
    parts = []
    if app.get("retention_d30") is not None:
        parts.append(float(app["retention_d30"]) * 2.0)
    if app.get("mrr") is not None:
        parts.append(min(float(app["mrr"]) / 10.0, 50.0))
    if app.get("roi") is not None:
        parts.append(min(float(app["roi"]) * 5.0, 30.0))
    if app.get("rating") is not None:
        parts.append(float(app["rating"]) * 5.0)
    if app.get("crash_rate") is not None:
        parts.append(max(0.0, 10.0 - float(app["crash_rate"]) * 100))
    return round(sum(parts) / max(len(parts), 1), 2)


def _patterns_for(app: dict) -> list[str]:
    proven_root = ROOT / "knowledge" / "patterns" / "proven"
    exp_root = ROOT / "knowledge" / "patterns" / "experimental"
    found = []
    for name, pred in PATTERN_HINTS:
        if pred(app):
            if (proven_root / name / "PATTERN.md").exists():
                found.append(f"knowledge/patterns/proven/{name}/PATTERN.md")
            else:
                found.append(f"knowledge/patterns/experimental/{name}/PATTERN.md")
    if not found and app.get("released"):
        found.append("knowledge/patterns/experimental/offline_first/PATTERN.md")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=5, help="Top N apps by composite score")
    parser.add_argument("--export", default="", help="Export JSON snapshot to directory")
    parser.add_argument("--min-users", type=int, default=0)
    args = parser.parse_args()

    if not OUTCOMES.exists():
        print("No outcomes yet. Run record-outcome.py after release.", file=sys.stderr)
        print("   Example: python3 scripts/factory/record-outcome.py --slug my-app --users 100 --mrr 50")
        return 0

    data = json.loads(OUTCOMES.read_text(encoding="utf-8"))
    apps = [a for a in data.get("apps", []) if (a.get("users") or 0) >= args.min_users]
    if not apps:
        print("No apps in app_outcomes.json")
        return 0

    ranked = sorted(apps, key=_score, reverse=True)[: args.top]

    print(f"Outcome intelligence — top {len(ranked)} app(s)\n")
    pattern_votes: dict[str, int] = {}

    for i, app in enumerate(ranked, 1):
        slug = app.get("slug", "?")
        score = _score(app)
        patterns = _patterns_for(app)
        print(f"{i}. {slug} (score {score})")
        print(f"   users={app.get('users')} retention_d30={app.get('retention_d30')} mrr={app.get('mrr')} roi={app.get('roi')}")
        print(f"   crash_rate={app.get('crash_rate')} rating={app.get('rating')} uninstall_rate={app.get('uninstall_rate')}")
        for p in patterns:
            print(f"   → pattern: {p}")
            pattern_votes[p] = pattern_votes.get(p, 0) + 1

    if pattern_votes:
        print("\nRecommended patterns for next project:")
        for p, n in sorted(pattern_votes.items(), key=lambda x: -x[1]):
            print(f"   [{n}x] {p}")

    if args.export:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        snap = {
            "schema": "factory.outcomes.analysis.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "top": ranked,
            "pattern_recommendations": pattern_votes,
        }
        out = Path(args.export) if args.export != "knowledge/outcomes/snapshots/" else SNAPSHOT_DIR
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"analysis-{ts}.json"
        path.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n   ✅ snapshot → {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
