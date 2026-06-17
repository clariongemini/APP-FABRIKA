#!/usr/bin/env python3
"""
Factory Intelligence Engine — Knowledge → Insight → (human/AI) Decision.

No new agents. Correlates outcomes, ventures, patterns, failures, ADRs.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import factory_dir  # noqa: E402

OUTCOMES = factory_dir("outcomes", "app_outcomes.json")
VENTURES = factory_dir("ventures", "ventures.json")
FAILURES = factory_dir("memory", "failures.json")
INSIGHT_DIR = ROOT / "knowledge" / "outcomes" / "snapshots"
PATTERNS_ROOT = ROOT / "knowledge" / "patterns"

ASK_QUERIES = {
    "retention-by-pattern": "En yüksek retention hangi pattern'lerde?",
    "uninstall-by-onboarding": "En düşük uninstall hangi onboarding'de?",
    "revenue-by-monetization": "En yüksek gelir hangi monetization modelinde?",
    "crash-by-architecture": "En yüksek crash hangi mimaride?",
    "feature-count-vs-rating": "Özellik sayısı rating ile ilişkili mi?",
    "ai-usage-vs-launch": "AI kullanımı launch süresini etkiliyor mu?",
    "portfolio-summary": "Portföy özeti — son uygulamalar",
}


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _apps(last: int) -> list[dict]:
    data = _load_json(OUTCOMES) or {}
    apps = list(data.get("apps", []))
    apps.sort(key=lambda a: a.get("recorded_at", ""), reverse=True)
    return apps[:last] if last else apps


def _pattern_names(app: dict) -> list[str]:
    explicit = app.get("patterns") or []
    if explicit:
        return list(explicit)
    tags = app.get("tags") or []
    known = {
        "offline_first", "subscription_app", "media_app",
        "chat_app", "ai_assistant", "local_database",
    }
    return [t for t in tags if t in known]


def _avg(values: list[float]) -> float | None:
    return round(statistics.mean(values), 2) if values else None


def _group_metric(apps: list[dict], key: str, metric: str) -> dict[str, dict]:
    groups: dict[str, list[float]] = defaultdict(list)
    for app in apps:
        val = app.get(metric)
        if val is None:
            continue
        group_val = app.get(key) or "unknown"
        if isinstance(group_val, list):
            for g in group_val:
                groups[str(g)].append(float(val))
        else:
            groups[str(group_val)].append(float(val))
    return {
        g: {"count": len(v), "avg": _avg(v), "min": min(v), "max": max(v)}
        for g, v in groups.items()
    }


def _retention_by_pattern(apps: list[dict]) -> dict:
    groups: dict[str, list[float]] = defaultdict(list)
    for app in apps:
        r = app.get("retention_d30") or app.get("retention_d7")
        if r is None:
            continue
        for p in _pattern_names(app) or ["unspecified"]:
            groups[p].append(float(r))
    ranked = sorted(
        [(p, _avg(v), len(v)) for p, v in groups.items()],
        key=lambda x: (x[1] or 0, x[2]),
        reverse=True,
    )
    return {
        "question": ASK_QUERIES["retention-by-pattern"],
        "metric": "retention_d30|d7",
        "ranking": [{"pattern": p, "avg_retention": a, "apps": n} for p, a, n in ranked],
        "winner": ranked[0][0] if ranked else None,
    }


def _uninstall_by_onboarding(apps: list[dict]) -> dict:
    groups = _group_metric(apps, "onboarding", "uninstall_rate")
    ranked = sorted(groups.items(), key=lambda x: x[1].get("avg") or 999)
    return {
        "question": ASK_QUERIES["uninstall-by-onboarding"],
        "metric": "uninstall_rate (lower is better)",
        "by_onboarding": dict(groups),
        "winner": ranked[0][0] if ranked else None,
    }


def _revenue_by_monetization(apps: list[dict]) -> dict:
    groups = _group_metric(apps, "monetization", "mrr")
    ranked = sorted(groups.items(), key=lambda x: x[1].get("avg") or 0, reverse=True)
    return {
        "question": ASK_QUERIES["revenue-by-monetization"],
        "metric": "mrr",
        "by_monetization": dict(groups),
        "winner": ranked[0][0] if ranked else None,
    }


def _crash_by_architecture(apps: list[dict]) -> dict:
    groups = _group_metric(apps, "architecture", "crash_rate")
    ranked = sorted(groups.items(), key=lambda x: x[1].get("avg") or 0, reverse=True)
    return {
        "question": ASK_QUERIES["crash-by-architecture"],
        "metric": "crash_rate (lower is better)",
        "by_architecture": dict(groups),
        "worst": ranked[0][0] if ranked else None,
        "best": ranked[-1][0] if ranked else None,
    }


def _feature_count_vs_rating(apps: list[dict]) -> dict:
    pairs = [
        (float(a["feature_count"]), float(a["rating"]))
        for a in apps
        if a.get("feature_count") is not None and a.get("rating") is not None
    ]
    insight = "insufficient_data"
    if len(pairs) >= 3:
        fc = [p[0] for p in pairs]
        rt = [p[1] for p in pairs]
        # Simple trend: compare avg rating above/below median feature count
        med = statistics.median(fc)
        high_fc = [r for f, r in pairs if f >= med]
        low_fc = [r for f, r in pairs if f < med]
        ah, al = _avg(high_fc), _avg(low_fc)
        if ah is not None and al is not None:
            if ah < al - 0.2:
                insight = "more_features_correlates_with_lower_rating"
            elif ah > al + 0.2:
                insight = "more_features_correlates_with_higher_rating"
            else:
                insight = "no_clear_correlation"
    return {
        "question": ASK_QUERIES["feature-count-vs-rating"],
        "pairs": len(pairs),
        "insight": insight,
        "data": [{"feature_count": f, "rating": r} for f, r in pairs],
    }


def _ai_usage_vs_launch(apps: list[dict]) -> dict:
    pairs = [
        {
            "slug": a.get("slug"),
            "ai_usage_pct": a.get("ai_usage_pct"),
            "launch_duration_days": a.get("launch_duration_days"),
            "development_hours": a.get("development_hours"),
        }
        for a in apps
        if a.get("ai_usage_pct") is not None and a.get("launch_duration_days") is not None
    ]
    return {
        "question": ASK_QUERIES["ai-usage-vs-launch"],
        "pairs": len(pairs),
        "data": pairs,
        "note": "Correlate manually until N>=5; engine lists raw pairs",
    }


def _portfolio_summary(apps: list[dict], ventures: list[dict]) -> dict:
    return {
        "question": ASK_QUERIES["portfolio-summary"],
        "apps_analyzed": len(apps),
        "released": sum(1 for a in apps if a.get("released")),
        "total_mrr": sum(a.get("mrr") or 0 for a in apps),
        "avg_retention_d30": _avg([float(a["retention_d30"]) for a in apps if a.get("retention_d30") is not None]),
        "ventures": len(ventures),
        "successful_ventures": sum(1 for v in ventures if v.get("result") in ("successful", "başarılı", "success")),
        "slugs": [a.get("slug") for a in apps],
    }


def _pattern_inventory() -> dict:
    inv = {"proven": [], "experimental": []}
    for tier in ("proven", "experimental"):
        base = PATTERNS_ROOT / tier
        if not base.exists():
            continue
        for p in sorted(base.iterdir()):
            if p.is_dir() and (p / "PATTERN.md").exists():
                inv[tier].append(p.name)
    return inv


def _failure_top_tags(limit: int = 5) -> list[tuple[str, int]]:
    data = _load_json(FAILURES) or {}
    counts: dict[str, int] = defaultdict(int)
    for e in data.get("entries", []):
        for t in e.get("tags", []):
            counts[t] += 1
    return sorted(counts.items(), key=lambda x: -x[1])[:limit]


def run_analysis(last: int) -> dict:
    apps = _apps(last)
    vdata = _load_json(VENTURES) or {}
    ventures = vdata.get("ventures", [])

    insights = {
        "schema": "factory.intelligence.report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "apps_in_scope": len(apps),
        "pattern_inventory": _pattern_inventory(),
        "queries": {
            "retention_by_pattern": _retention_by_pattern(apps),
            "uninstall_by_onboarding": _uninstall_by_onboarding(apps),
            "revenue_by_monetization": _revenue_by_monetization(apps),
            "crash_by_architecture": _crash_by_architecture(apps),
            "feature_count_vs_rating": _feature_count_vs_rating(apps),
            "ai_usage_vs_launch": _ai_usage_vs_launch(apps),
            "portfolio_summary": _portfolio_summary(apps, ventures),
        },
        "failure_hot_tags": _failure_top_tags(),
        "adr_count": len(list((ROOT / "knowledge" / "adr" / "decisions").glob("ADR-*.md"))),
        "postmortem_count": len([
            p for p in (ROOT / "knowledge" / "postmortems").glob("*.md")
            if p.name not in ("README.md", "TEMPLATE.md")
        ]),
    }
    return insights


def _print_human(report: dict, ask: str | None) -> None:
    q = report["queries"]
    if ask is None or ask == "portfolio-summary":
        s = q["portfolio_summary"]
        print(f"\n=== {s['question']} ===")
        print(f"Apps: {s['apps_analyzed']} · Released: {s['released']} · MRR sum: {s['total_mrr']}")
        print(f"Avg retention D30: {s['avg_retention_d30']} · Ventures: {s['ventures']}")

    mapping = {
        "retention-by-pattern": "retention_by_pattern",
        "uninstall-by-onboarding": "uninstall_by_onboarding",
        "revenue-by-monetization": "revenue_by_monetization",
        "crash-by-architecture": "crash_by_architecture",
        "feature-count-vs-rating": "feature_count_vs_rating",
        "ai-usage-vs-launch": "ai_usage_vs_launch",
        "portfolio-summary": "portfolio_summary",
    }
    keys = [mapping[ask]] if ask and ask in mapping else list(mapping.values())

    for k in keys:
        block = q[k]
        print(f"\n=== {block.get('question', k)} ===")
        if "ranking" in block:
            for row in block["ranking"][:5]:
                print(f"  {row}")
            if block.get("winner"):
                print(f"  → Winner: {block['winner']}")
        elif "by_onboarding" in block:
            for name, stats in block["by_onboarding"].items():
                print(f"  {name}: avg={stats.get('avg')} (n={stats.get('count')})")
            if block.get("winner"):
                print(f"  → Lowest uninstall: {block['winner']}")
        elif "by_monetization" in block:
            for name, stats in block["by_monetization"].items():
                print(f"  {name}: avg MRR={stats.get('avg')} (n={stats.get('count')})")
            if block.get("winner"):
                print(f"  → Highest revenue model: {block['winner']}")
        elif "by_architecture" in block:
            for name, stats in block["by_architecture"].items():
                print(f"  {name}: avg crash={stats.get('avg')} (n={stats.get('count')})")
            if block.get("worst"):
                print(f"  → Highest crash: {block['worst']} · Best: {block.get('best')}")
        elif "insight" in block:
            print(f"  Insight: {block['insight']} (n={block.get('pairs', 0)})")
        elif "data" in block and k == "ai_usage_vs_launch":
            for row in block["data"][:10]:
                print(f"  {row}")

    inv = report.get("pattern_inventory", {})
    print(f"\n=== Patterns ===")
    print(f"  Proven: {inv.get('proven') or '(none yet)'}")
    print(f"  Experimental: {inv.get('experimental', [])}")
    if report.get("failure_hot_tags"):
        print(f"\n=== Failure hot tags ===")
        for tag, n in report["failure_hot_tags"]:
            print(f"  {tag}: {n}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Factory Intelligence Engine")
    parser.add_argument("--last", type=int, default=10, help="Analyze last N apps by recorded_at")
    parser.add_argument(
        "--ask",
        choices=list(ASK_QUERIES.keys()),
        help="Single insight query",
    )
    parser.add_argument("--analyze", action="store_true", help="Run full analysis (default)")
    parser.add_argument("--export", action="store_true", help="Write JSON snapshot to knowledge/outcomes/snapshots/")
    parser.add_argument("--json", action="store_true", help="Print full JSON to stdout")
    args = parser.parse_args()

    if not OUTCOMES.exists():
        print("No outcomes data. Initialize runtime and record outcomes:", file=sys.stderr)
        print("  ./scripts/runtime/init-runtime.sh", file=sys.stderr)
        print("  python3 scripts/factory/record-outcome.py --slug my-app --users 100 ...", file=sys.stderr)
        return 0

    report = run_analysis(args.last)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_human(report, args.ask)

    if args.export or (args.analyze and not args.ask):
        INSIGHT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = INSIGHT_DIR / f"intelligence-{ts}.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if not args.json:
            print(f"\n   ✅ insight snapshot → {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
