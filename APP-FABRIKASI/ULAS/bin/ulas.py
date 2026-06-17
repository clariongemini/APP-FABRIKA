#!/usr/bin/env python3
"""
ULAS Decision Execution Engine — Phase 2
Operationalizes policies/workflows/gates/scoring/memory.

Usage:
  ulas.py decide --venture SLUG --class B --title "..." --reviewers architect,qa
  ulas.py gate --decision-id ID
  ulas.py calibrate --reviewer architect --outcome good|missed
  ulas.py assemble --venture SLUG --class B
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ULAS_ROOT = Path(__file__).resolve().parent.parent
SVOS_ROOT = ULAS_ROOT.parent
REPO_ROOT = SVOS_ROOT.parent


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_policy(name: str) -> dict:
    return _load(ULAS_ROOT / "policies" / name)


def _load_scoring(name: str) -> dict:
    return _load(ULAS_ROOT / "scoring" / name)


def memory_registry() -> dict:
    return _load(ULAS_ROOT / "memory" / "never-again.json")


def venture_path(slug: str) -> Path:
    return SVOS_ROOT / "08-ventures" / slug / "venture.json"


def runtime_decisions_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "decisions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_class(decision_class: str) -> dict:
    classes = _load(ULAS_ROOT / "policies" / "decision-classes.json")["classes"]
    key = decision_class.upper()
    if key not in classes:
        default = _load(ULAS_ROOT / "policies" / "decision-classes.json").get("default_class", "B")
        key = default.upper()
    return classes[key] | {"id": key}


def resolve_tier(class_info: dict, escalate: bool = False) -> str | int:
    tier = class_info.get("tier", 2)
    if escalate and isinstance(tier, int) and tier < 3:
        return tier + 1
    return tier


def assemble_context(venture_slug: str, class_info: dict) -> dict:
    """Context assembly — returns manifest + required reads."""
    tier = class_info.get("tier", 2)
    escalation = _load(ULAS_ROOT / "policies" / "context-escalation.json")
    tier_key = str(tier) if tier != "critical" else "critical"
    tier_def = escalation["tiers"].get(tier_key, escalation["tiers"]["2"])

    reads: list[dict] = []
    vpath = venture_path(venture_slug)
    if vpath.exists():
        reads.append({"path": str(vpath.relative_to(REPO_ROOT)), "priority": 1, "status": "required"})
    else:
        reads.append({"path": f"APP-FABRIKASI/08-ventures/{venture_slug}/venture.json", "priority": 1, "status": "missing"})

    platform = []
    if vpath.exists():
        v = _load(vpath)
        platform = v.get("platform", [])
    if platform:
        adapter = f"APP-FABRIKASI/02-platforms/{platform[0]}/ADAPTER.md"
        reads.append({"path": adapter, "priority": 2, "status": "required"})

    reads.append({"path": "APP-FABRIKASI/ULAS/memory/never-again.json", "priority": 3, "status": "required"})
    if tier_key in ("3", "critical"):
        reads.append({"path": "APP-FABRIKASI/06-learning/patterns/proven/", "priority": 4, "status": "optional"})

    missing = [r for r in reads if r["status"] == "missing" or not (REPO_ROOT / r["path"]).exists() and not r["path"].endswith("/")]

    state = "READ_MORE_REQUIRED" if missing else "CONTEXT_COMPLETE"
    return {
        "venture_slug": venture_slug,
        "tier": tier_key,
        "tier_name": tier_def.get("name"),
        "token_budget_hint": tier_def.get("token_budget_hint"),
        "context_load": tier_def.get("context_load", []),
        "required_reads": reads,
        "missing_reads": [m["path"] for m in missing],
        "state": state,
        "assembled_at": now_iso(),
    }


def scan_never_again(proposal: str) -> list[dict]:
    reg = memory_registry()
    hits = []
    proposal_lower = proposal.lower()
    for entry in reg.get("entries", []):
        summary = entry.get("summary", "").lower()
        tags = [t.lower() for t in entry.get("tags", [])]
        if summary and summary in proposal_lower:
            hits.append(entry)
        elif any(t in proposal_lower for t in tags if t):
            hits.append(entry)
    return hits


def score_confidence(
    context: dict,
    evidence_status: str = "none",
    never_again_clear: bool = True,
    decision_class: str = "B",
) -> dict:
    weights = _load(ULAS_ROOT / "scoring" / "confidence-weights.json")
    w = weights["weights"]
    factors = {
        "evidence_present": 1.0 if evidence_status in ("collected", "partial") else 0.0,
        "prior_outcomes": 0.0,
        "known_failures_clear": 1.0 if never_again_clear else 0.0,
        "adr_alignment": 0.5,
        "pattern_support": 0.0,
        "context_complete": 1.0 if context["state"] == "CONTEXT_COMPLETE" else 0.0,
    }
    # Class A (documentation): evidence not required for approval
    if decision_class.upper() == "A":
        factors["evidence_present"] = 0.5
        factors["prior_outcomes"] = 0.5
    confidence = sum(factors[k] * w[k] for k in w)
    band = "low"
    for name, b in weights["bands"].items():
        if b["min"] <= confidence <= b["max"]:
            band = name
            break
    blocked = weights["bands"].get(band, {}).get("action") == "block"
    return {
        "confidence": round(confidence, 3),
        "band": band,
        "factors": factors,
        "blocked": blocked,
        "computed_at": now_iso(),
    }


def validate_review_chain(decision_class: str, reviewers: list[str]) -> dict:
    matrix = _load(ULAS_ROOT / "policies" / "review-matrix.json")
    classes = _load(ULAS_ROOT / "policies" / "decision-classes.json")["classes"]
    dc = decision_class.upper()
    class_def = classes.get(dc, classes[classes.get("default_class", "B")])
    required = matrix["by_decision_class"].get(dc, [])
    trust_data = _load(ULAS_ROOT / "scoring" / "trust-scores.json")
    min_count = class_def.get("min_reviews", matrix["minimum_review_count"])

    provided = [r.strip().lower() for r in reviewers]
    missing = [r for r in required if r not in provided]
    effective_weight = sum(
        trust_data["capabilities"].get(r, {}).get("trust", trust_data["initial_trust"]) / 100
        for r in provided
    )
    satisfied = len(provided) >= min_count and len(missing) == 0

    return {
        "required_capabilities": required,
        "provided_reviewers": provided,
        "missing_capabilities": missing,
        "minimum_review_count": min_count,
        "effective_trust_weight": round(effective_weight, 2),
        "satisfied": satisfied,
    }


def cmd_decide(args: argparse.Namespace) -> int:
    class_info = resolve_class(args.class_)
    venture = args.venture
    title = args.title or "untitled decision"

    context = assemble_context(venture, class_info)
    na_hits = scan_never_again(args.proposal or title) if (args.proposal or title) else []
    never_again_clear = len(na_hits) == 0

    evidence_status = "none"
    vp = venture_path(venture)
    if vp.exists():
        evidence_status = _load(vp).get("evidence_status", "none")

    confidence = score_confidence(context, evidence_status, never_again_clear, class_info["id"])
    reviewers = [r.strip() for r in args.reviewers.split(",") if r.strip()]
    review = validate_review_chain(class_info["id"], reviewers)

    decision_id = f"{venture}-{class_info['id'].lower()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    blocked_reasons = []

    if context["state"] == "READ_MORE_REQUIRED":
        blocked_reasons.append(f"READ_MORE_REQUIRED: {context['missing_reads']}")
    if confidence["blocked"]:
        blocked_reasons.append(f"LOW_CONFIDENCE: {confidence['band']} ({confidence['confidence']})")
    if not never_again_clear:
        blocked_reasons.append(f"NEVER_AGAIN_CONFLICT: {[h.get('id') for h in na_hits]}")
    if not review["satisfied"]:
        blocked_reasons.append(f"REVIEW_CHAIN: missing {review['missing_capabilities']}")

    status = "APPROVED" if not blocked_reasons else "BLOCKED"
    record = {
        "decision_id": decision_id,
        "title": title,
        "venture_slug": venture,
        "decision_class": class_info["id"],
        "class_label": class_info.get("label"),
        "lifecycle_state": "APPROVAL" if status == "APPROVED" else "BLOCKED",
        "context": context,
        "confidence": confidence,
        "review": review,
        "never_again_hits": na_hits,
        "status": status,
        "blocked_reasons": blocked_reasons,
        "created_at": now_iso(),
    }

    out = runtime_decisions_dir() / f"{decision_id}.json"
    _save(out, record)

    print(json.dumps({"status": status, "decision_id": decision_id, "path": str(out.relative_to(REPO_ROOT))}, indent=2))
    if blocked_reasons:
        for r in blocked_reasons:
            print(f"  BLOCK: {r}", file=sys.stderr)
        return 1
    return 0


def cmd_assemble(args: argparse.Namespace) -> int:
    class_info = resolve_class(args.class_)
    ctx = assemble_context(args.venture, class_info)
    print(json.dumps(ctx, indent=2, ensure_ascii=False))
    return 0 if ctx["state"] == "CONTEXT_COMPLETE" else 2


def cmd_calibrate(args: argparse.Namespace) -> int:
    path = ULAS_ROOT / "scoring" / "trust-scores.json"
    data = _load(path)
    cap = args.reviewer.lower()
    if cap not in data["capabilities"]:
        print(f"Unknown capability: {cap}", file=sys.stderr)
        return 1
    cal = data["calibration"]
    entry = data["capabilities"][cap]
    delta = cal["good_outcome_delta"] if args.outcome == "good" else cal["missed_risk_delta"]
    entry["trust"] = max(cal["floor"], min(cal["ceiling"], entry["trust"] + delta))
    entry["reviews"] = entry.get("reviews", 0) + 1
    entry["calibration_delta"] = round(entry.get("calibration_delta", 0) + delta, 2)
    entry["last_calibrated"] = now_iso()
    _save(path, data)
    print(json.dumps({"capability": cap, "trust": entry["trust"], "delta": delta}, indent=2))
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    """Print full routing: class → tier → chain → gates."""
    class_info = resolve_class(args.class_)
    matrix = _load(ULAS_ROOT / "policies" / "review-matrix.json")
    chain = matrix["by_decision_class"].get(class_info["id"], [])
    print(json.dumps({
        "decision_class": class_info["id"],
        "label": class_info.get("label"),
        "tier": class_info.get("tier"),
        "risk": class_info.get("risk"),
        "review_chain": chain,
        "min_reviews": class_info.get("min_reviews"),
        "full_review": class_info.get("full_review", False),
        "founder_approval": class_info.get("founder_approval", False),
    }, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ULAS Decision Execution Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    p_decide = sub.add_parser("decide", help="Run full decision lifecycle gate")
    p_decide.add_argument("--venture", required=True)
    p_decide.add_argument("--class", dest="class_", default="B")
    p_decide.add_argument("--title", default="")
    p_decide.add_argument("--proposal", default="", help="Text scanned against NEVER_AGAIN")
    p_decide.add_argument("--reviewers", required=True, help="Comma-separated capabilities")

    p_asm = sub.add_parser("assemble", help="Context assembly only")
    p_asm.add_argument("--venture", required=True)
    p_asm.add_argument("--class", dest="class_", default="B")

    p_cal = sub.add_parser("calibrate", help="Update trust score after outcome")
    p_cal.add_argument("--reviewer", required=True)
    p_cal.add_argument("--outcome", choices=["good", "missed"], required=True)

    p_route = sub.add_parser("route", help="Show routing for decision class")
    p_route.add_argument("--class", dest="class_", default="B")

    args = parser.parse_args()
    handlers = {
        "decide": cmd_decide,
        "assemble": cmd_assemble,
        "calibrate": cmd_calibrate,
        "route": cmd_route,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
