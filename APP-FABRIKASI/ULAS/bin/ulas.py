#!/usr/bin/env python3
"""
ULAS Decision Execution Engine — Phase 2–5
Operationalizes policies/workflows/gates/scoring/memory.
Phase 3: effectiveness instrumentation.
Phase 4: feedback closure audit.
Phase 5: adaptive propagation (outcome → behavior change).
Phase 6: predictive risk (observation → prediction → decision), gated by evidence.

Usage:
  ulas.py risk-gate | risk --venture SLUG --class B --reviewers architect,qa
  ulas.py decide --venture SLUG --class B --title "..." --reviewers architect,qa
  ulas.py outcome --decision-id ID --result correct_block [--propagate]
  ulas.py propagate --decision-id ID [--dry-run] [--apply-memory]
  ulas.py propagation-audit | feedback-audit
  ulas.py calibrate --reviewer architect --outcome good|missed [--decision-id ID] [--reason "..."]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ULAS_ROOT = Path(__file__).resolve().parent.parent
SVOS_ROOT = ULAS_ROOT.parent
REPO_ROOT = SVOS_ROOT.parent
_ENGINE_DIR = Path(__file__).resolve().parent
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))
import capability_memory_engine as cmem
import dispatch_queue as dqueue
import adapter_loader as aload
import gradle_test_parser as gtp
import maturity_audit as mat


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


def runtime_metrics_path() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "metrics"
    d.mkdir(parents=True, exist_ok=True)
    return d / "aggregates.json"


def readiness_history_path() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "metrics"
    d.mkdir(parents=True, exist_ok=True)
    return d / "readiness-history.json"


def readiness_schema_path() -> Path:
    return ULAS_ROOT / "scoring" / "self-improvement-readiness.json"


def adaptations_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "adaptations"
    d.mkdir(parents=True, exist_ok=True)
    return d


def policy_overrides_path() -> Path:
    return adaptations_dir() / "policy-overrides.json"


def default_policy_overrides() -> dict:
    return {
        "version": "1.0",
        "review_matrix": {},
        "decision_classes": {},
        "confidence_weight_deltas": {},
        "changelog": [],
    }


def load_policy_overrides() -> dict:
    path = policy_overrides_path()
    if not path.exists():
        return default_policy_overrides()
    data = _load(path)
    base = default_policy_overrides()
    for key in ("review_matrix", "decision_classes", "confidence_weight_deltas", "changelog"):
        if key in data:
            base[key] = data[key]
    return base


def save_policy_overrides(data: dict) -> None:
    _save(policy_overrides_path(), data)


def load_all_decisions() -> list[dict]:
    records = []
    for f in sorted(runtime_decisions_dir().glob("*.json")):
        try:
            records.append(_load(f))
        except (json.JSONDecodeError, OSError):
            continue
    return records


def rebuild_metrics() -> dict:
    schema_path = ULAS_ROOT / "scoring" / "metrics-schema.json"
    metrics = _load(schema_path)
    dm = metrics["decision_metrics"]
    tm = metrics["token_metrics"]
    mm = metrics["memory_metrics"]
    reviewer_metrics: dict[str, dict] = {}
    by_class: dict[str, int] = {}
    by_band: dict[str, int] = {}
    tier_budgets: list[int] = []

    for rec in load_all_decisions():
        dm["total_decisions"] += 1
        status = rec.get("status", "")
        if status == "APPROVED":
            dm["approved"] += 1
        elif status == "BLOCKED":
            dm["blocked"] += 1

        dc = rec.get("decision_class", "?")
        by_class[dc] = by_class.get(dc, 0) + 1

        band = rec.get("confidence", {}).get("band", "unknown")
        by_band[band] = by_band.get(band, 0) + 1

        tier = str(rec.get("context", {}).get("tier", "2"))
        budget = rec.get("context", {}).get("token_budget_hint", 0)
        if budget:
            tier_budgets.append(int(budget))
        if tier == "1":
            tm["tier1_usage"] += 1
        elif tier == "2":
            tm["tier2_usage"] += 1
        elif tier == "critical":
            tm["critical_usage"] += 1
        else:
            tm["tier3_usage"] += 1

        mm["never_again_hits"] += len(rec.get("never_again_hits", []))

        blocked_reasons = rec.get("blocked_reasons", [])
        is_low_conf = any("LOW_CONFIDENCE" in r for r in blocked_reasons)
        if is_low_conf:
            dm["low_confidence_blocks"] += 1

        eff = rec.get("effectiveness", {})
        outcome = eff.get("outcome")
        if outcome:
            dm["outcomes_evaluated"] += 1
            if outcome in dm:
                dm[outcome] += 1
            if outcome == "overturned":
                dm["overturned"] += 1
            if outcome == "approved_failed":
                dm["failed_after_approval"] += 1
            if is_low_conf:
                if outcome == "correct_block":
                    dm["low_confidence_correct"] += 1
                elif outcome == "false_block":
                    dm["low_confidence_false"] += 1
            for rev in rec.get("review", {}).get("provided_reviewers", []):
                if rev not in reviewer_metrics:
                    reviewer_metrics[rev] = {"reviews": 0, "accurate": 0, "missed": 0, "accuracy": None}
                reviewer_metrics[rev]["reviews"] += 1
                if outcome in ("approved_success", "correct_block"):
                    reviewer_metrics[rev]["accurate"] += 1
                elif outcome in ("approved_failed", "false_block"):
                    reviewer_metrics[rev]["missed"] += 1

    evaluated_blocks = dm["low_confidence_correct"] + dm["low_confidence_false"]
    if evaluated_blocks > 0:
        dm["low_confidence_precision"] = round(dm["low_confidence_correct"] / evaluated_blocks, 3)

    for rev, rm in reviewer_metrics.items():
        total = rm["accurate"] + rm["missed"]
        rm["accuracy"] = round(rm["accurate"] / total, 3) if total > 0 else None
        metrics["reviewer_metrics"][rev] = rm

    if tier_budgets:
        tm["average_context_budget"] = round(sum(tier_budgets) / len(tier_budgets))

    metrics["by_class"] = by_class
    metrics["by_confidence_band"] = by_band
    metrics["last_rebuilt"] = now_iso()
    _save(runtime_metrics_path(), metrics)
    return metrics


def find_decision(decision_id: str) -> Path | None:
    exact = runtime_decisions_dir() / f"{decision_id}.json"
    if exact.exists():
        return exact
    for f in runtime_decisions_dir().glob(f"*{decision_id}*.json"):
        return f
    return None


def load_decision_record(decision_id: str) -> tuple[Path, dict] | tuple[None, None]:
    path = find_decision(decision_id)
    if not path:
        return None, None
    return path, _load(path)


def validate_decision_id(decision_id: str) -> tuple[Path, dict]:
    if not decision_id or decision_id.strip() in ("test", "fake", "unknown"):
        raise ValueError(f"Invalid decision_id: {decision_id!r}")
    path, rec = load_decision_record(decision_id)
    if not path or not rec:
        raise ValueError(f"Decision not found: {decision_id}")
    return path, rec


OUTCOME_REQUIRES_APPROVED = frozenset({"approved_success", "approved_failed"})
OUTCOME_REQUIRES_BLOCKED = frozenset({"correct_block", "false_block"})


def validate_outcome_for_record(rec: dict, result: str) -> None:
    status = rec.get("status", "")
    if result in OUTCOME_REQUIRES_APPROVED and status != "APPROVED":
        raise ValueError(
            f"Outcome {result!r} requires status APPROVED; got {status!r} "
            f"({rec.get('decision_id')})"
        )
    if result in OUTCOME_REQUIRES_BLOCKED and status != "BLOCKED":
        raise ValueError(
            f"Outcome {result!r} requires status BLOCKED; got {status!r} "
            f"({rec.get('decision_id')})"
        )


OUTCOME_CHOICES = (
    "correct_block", "false_block", "approved_success",
    "approved_failed", "overturned", "unknown", "prevented_failure",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_class(decision_class: str) -> dict:
    classes = _load(ULAS_ROOT / "policies" / "decision-classes.json")["classes"]
    key = decision_class.upper()
    if key not in classes:
        default = _load(ULAS_ROOT / "policies" / "decision-classes.json").get("default_class", "B")
        key = default.upper()
    info = classes[key] | {"id": key}
    return apply_class_adaptations(info)


def apply_class_adaptations(class_info: dict) -> dict:
    overrides = load_policy_overrides()
    dc = class_info["id"]
    class_ov = overrides.get("decision_classes", {}).get(dc, {})
    if class_ov.get("min_reviews_delta"):
        class_info = dict(class_info)
        class_info["min_reviews"] = class_info.get("min_reviews", 2) + int(class_ov["min_reviews_delta"])
    tier_floor = class_ov.get("tier_floor")
    if tier_floor is not None:
        class_info = dict(class_info)
        current = class_info.get("tier", 2)
        if current != "critical":
            try:
                if int(current) < int(tier_floor):
                    class_info["tier"] = int(tier_floor)
            except (TypeError, ValueError):
                pass
        elif tier_floor == "critical":
            class_info["tier"] = "critical"
    return class_info


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
    w = dict(weights["weights"])
    for factor, delta in load_policy_overrides().get("confidence_weight_deltas", {}).items():
        if factor in w:
            w[factor] = round(max(0.0, min(1.0, w[factor] + float(delta))), 4)
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
    required = list(matrix["by_decision_class"].get(dc, []))
    overrides = load_policy_overrides()
    rm_ov = overrides.get("review_matrix", {}).get(dc, {})
    for cap in rm_ov.get("additional_required", []):
        if cap not in required:
            required.append(cap)
    min_count = class_def.get("min_reviews", matrix["minimum_review_count"])
    min_count += int(overrides.get("decision_classes", {}).get(dc, {}).get("min_reviews_delta", 0))

    provided = [r.strip().lower() for r in reviewers]
    missing = [r for r in required if r not in provided]
    trust_data = _load(ULAS_ROOT / "scoring" / "trust-scores.json")
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
        "adaptations_applied": bool(rm_ov or overrides.get("decision_classes", {}).get(dc)),
    }


def _apply_trust_delta(
    cap: str,
    outcome: str,
    decision_id: str,
    reason: str,
    evidence: str = "",
    source: str = "calibrate",
) -> dict | None:
    path = ULAS_ROOT / "scoring" / "trust-scores.json"
    data = _load(path)
    cap = cap.lower()
    if cap not in data["capabilities"]:
        return None
    cal = data["calibration"]
    entry = data["capabilities"][cap]
    previous_trust = entry["trust"]
    delta = cal["good_outcome_delta"] if outcome == "good" else cal["missed_risk_delta"]
    new_trust = max(cal["floor"], min(cal["ceiling"], previous_trust + delta))
    entry["trust"] = new_trust
    entry["reviews"] = entry.get("reviews", 0) + 1
    entry["calibration_delta"] = round(entry.get("calibration_delta", 0) + delta, 2)
    entry["last_calibrated"] = now_iso()
    log_entry = {
        "at": now_iso(),
        "previous_trust": previous_trust,
        "new_trust": new_trust,
        "delta": delta,
        "outcome": outcome,
        "decision_id": decision_id or None,
        "reason": reason,
        "evidence": evidence,
        "source": source,
    }
    entry.setdefault("calibration_log", []).append(log_entry)
    _save(path, data)
    return log_entry


def find_similar_decisions(rec: dict, limit: int = 5) -> list[dict]:
    similar: list[dict] = []
    dc = rec.get("decision_class")
    venture = rec.get("venture_slug")
    reviewers = set(rec.get("review", {}).get("provided_reviewers", []))
    for other in load_all_decisions():
        if other.get("decision_id") == rec.get("decision_id"):
            continue
        score = 0
        if other.get("decision_class") == dc:
            score += 2
        if other.get("venture_slug") == venture:
            score += 2
        other_revs = set(other.get("review", {}).get("provided_reviewers", []))
        if reviewers & other_revs:
            score += 1
        if score >= 2:
            similar.append({
                "decision_id": other.get("decision_id"),
                "title": other.get("title"),
                "status": other.get("status"),
                "outcome": other.get("effectiveness", {}).get("outcome"),
                "similarity_score": score,
            })
    return sorted(similar, key=lambda x: -x["similarity_score"])[:limit]


def build_propagation_plan(rec: dict, outcome: str) -> dict:
    dc = rec.get("decision_class", "B")
    reviewers = rec.get("review", {}).get("provided_reviewers", [])
    title = rec.get("title", "")
    plan: dict[str, Any] = {
        "decision_id": rec.get("decision_id"),
        "outcome": outcome,
        "at": now_iso(),
        "questions_answered": {},
        "trust_updates": [],
        "policy_adaptations": [],
        "memory_candidate": None,
        "similar_decisions": find_similar_decisions(rec),
    }
    plan["questions_answered"] = {
        "failure_detected": outcome in ("approved_failed", "overturned", "false_block"),
        "reviewers_who_approved": reviewers if rec.get("status") == "APPROVED" else [],
        "why_approved": rec.get("review", {}),
        "similar_decisions": [s["decision_id"] for s in plan["similar_decisions"]],
        "policy_gap": outcome in ("approved_failed", "overturned"),
        "review_matrix_gap": outcome in ("approved_failed", "overturned") and "auditor" not in reviewers,
        "trust_should_change": outcome in (
            "approved_failed", "overturned", "false_block",
            "approved_success", "correct_block", "prevented_failure",
        ),
        "never_again_candidate": outcome in ("approved_failed", "overturned"),
        "context_should_escalate": outcome in ("approved_failed", "overturned"),
    }

    if outcome in ("approved_failed", "overturned"):
        for rev in reviewers:
            plan["trust_updates"].append({
                "reviewer": rev,
                "outcome": "missed",
                "reason": f"{outcome}: approved decision failed in reality",
            })
        if "auditor" not in reviewers and dc in ("B", "C"):
            plan["policy_adaptations"].append({
                "type": "review_matrix",
                "class": dc,
                "capability": "auditor",
                "reason": f"{outcome}: add auditor to class {dc} chain",
            })
        plan["policy_adaptations"].append({
            "type": "confidence_weight_delta",
            "factor": "evidence_present",
            "delta": 0.05,
            "reason": "approval failed — weight evidence higher",
        })
        if dc == "B":
            plan["policy_adaptations"].append({
                "type": "tier_floor",
                "class": dc,
                "value": 3,
                "reason": "escalate context depth after approval failure",
            })
        plan["memory_candidate"] = {
            "id": f"NA-{rec.get('decision_id', 'unknown')[:24]}",
            "summary": title[:240] or f"Failure from {rec.get('decision_id')}",
            "venture_slug": rec.get("venture_slug", ""),
            "severity": "critical",
            "tags": [dc.lower(), rec.get("venture_slug", ""), outcome],
            "source_decision_id": rec.get("decision_id"),
        }
    elif outcome in ("approved_success", "correct_block", "prevented_failure"):
        for rev in reviewers:
            plan["trust_updates"].append({
                "reviewer": rev,
                "outcome": "good",
                "reason": f"{outcome}: decision quality confirmed",
            })
    elif outcome == "false_block":
        for rev in reviewers:
            plan["trust_updates"].append({
                "reviewer": rev,
                "outcome": "good",
                "reason": "false_block: reviewers were right to challenge",
            })
        plan["policy_adaptations"].append({
            "type": "confidence_weight_delta",
            "factor": "evidence_present",
            "delta": -0.03,
            "reason": "false_block: reduce over-blocking from evidence weight",
        })

    return plan


def apply_policy_adaptation(overrides: dict, adaptation: dict, decision_id: str) -> dict:
    changelog_entry = {
        "at": now_iso(),
        "decision_id": decision_id,
        "adaptation": adaptation,
    }
    atype = adaptation["type"]
    dc = adaptation.get("class", "B")

    if atype == "review_matrix":
        cap = adaptation["capability"]
        rm = overrides.setdefault("review_matrix", {}).setdefault(dc, {"additional_required": []})
        if cap not in rm["additional_required"]:
            rm["additional_required"].append(cap)
    elif atype == "confidence_weight_delta":
        factor = adaptation["factor"]
        delta = float(adaptation["delta"])
        current = float(overrides.setdefault("confidence_weight_deltas", {}).get(factor, 0))
        overrides.setdefault("confidence_weight_deltas", {})[factor] = round(current + delta, 4)
    elif atype == "tier_floor":
        class_ov = overrides.setdefault("decision_classes", {}).setdefault(dc, {})
        new_floor = adaptation["value"]
        old = class_ov.get("tier_floor")
        if old is None or (isinstance(old, int) and isinstance(new_floor, int) and new_floor > old):
            class_ov["tier_floor"] = new_floor
    elif atype == "min_reviews_delta":
        class_ov = overrides.setdefault("decision_classes", {}).setdefault(dc, {})
        class_ov["min_reviews_delta"] = int(class_ov.get("min_reviews_delta", 0)) + int(adaptation.get("delta", 1))

    overrides.setdefault("changelog", []).append(changelog_entry)
    return overrides


def apply_memory_candidate(candidate: dict) -> dict:
    reg = memory_registry()
    entry = {
        "id": candidate["id"],
        "category": "process",
        "summary": candidate["summary"],
        "venture_slug": candidate.get("venture_slug", ""),
        "tags": candidate.get("tags", []),
        "severity": candidate.get("severity", "critical"),
        "source_decision_id": candidate.get("source_decision_id"),
        "created": now_iso()[:10],
        "level": "critical",
    }
    existing_ids = {e.get("id") for e in reg.get("entries", [])}
    if entry["id"] not in existing_ids:
        reg.setdefault("entries", []).append(entry)
        _save(ULAS_ROOT / "memory" / "never-again.json", reg)
    return entry


def propagate_decision(
    rec: dict,
    *,
    dry_run: bool = False,
    apply_memory: bool = False,
) -> dict:
    outcome = rec.get("effectiveness", {}).get("outcome")
    if not outcome:
        raise ValueError("outcome not recorded")
    validate_outcome_for_record(rec, outcome)
    plan = build_propagation_plan(rec, outcome)
    result: dict[str, Any] = {
        "propagated_at": now_iso(),
        "dry_run": dry_run,
        "plan": plan,
        "applied": {"trust": [], "policy": [], "memory": None},
    }

    if not dry_run:
        for tu in plan["trust_updates"]:
            log = _apply_trust_delta(
                tu["reviewer"],
                tu["outcome"],
                rec.get("decision_id", ""),
                tu["reason"],
                source="propagate",
            )
            if log:
                result["applied"]["trust"].append(log)

        overrides = load_policy_overrides()
        for adaptation in plan["policy_adaptations"]:
            overrides = apply_policy_adaptation(overrides, adaptation, rec.get("decision_id", ""))
            result["applied"]["policy"].append(adaptation)
        if plan["policy_adaptations"]:
            save_policy_overrides(overrides)

        if apply_memory and plan.get("memory_candidate"):
            result["applied"]["memory"] = apply_memory_candidate(plan["memory_candidate"])

        rebuild_metrics()

    rec["adaptation"] = {
        "propagated_at": result["propagated_at"],
        "dry_run": dry_run,
        "outcome": outcome,
        "trust_updates": len(plan["trust_updates"]),
        "policy_adaptations": len(plan["policy_adaptations"]),
        "memory_applied": bool(result["applied"]["memory"]),
        "similar_decisions": plan["similar_decisions"],
    }
    return result


def load_risk_engine() -> dict:
    return _load(ULAS_ROOT / "scoring" / "risk-engine.json")


def _risk_band(score: int, engine: dict) -> str:
    for name, band in engine["bands"].items():
        if band["min"] <= score <= band["max"]:
            return name
    return "low"


def _count_evidence_bundles() -> int:
    evidence_root = SVOS_ROOT / "07-evidence"
    if not evidence_root.exists():
        return 0
    count = 0
    for d in evidence_root.iterdir():
        if d.is_dir() and not d.name.startswith("_"):
            if (d / "manifest.json").exists() or (d / "EVIDENCE.md").exists():
                count += 1
    return count


def _count_shipped_ventures() -> int:
    shipped = 0
    for vpath in (SVOS_ROOT / "08-ventures").glob("*/venture.json"):
        try:
            v = _load(vpath)
            if v.get("phase") == "shipped" or v.get("stage") == "shipped" or v.get("status") == "shipped":
                shipped += 1
        except (json.JSONDecodeError, OSError):
            continue
    return shipped


def check_risk_activation() -> dict:
    engine = load_risk_engine()
    gate = engine.get("activation_gate", {})
    reqs = gate.get("auto_enable_when", {})
    metrics = rebuild_metrics() if runtime_metrics_path().exists() else _load(
        ULAS_ROOT / "scoring" / "metrics-schema.json"
    )
    dm = metrics.get("decision_metrics", metrics)
    snapshots = 0
    if readiness_history_path().exists():
        snapshots = len(_load(readiness_history_path()).get("snapshots", []))

    current = {
        "decisions": dm.get("total_decisions", 0),
        "outcomes_evaluated": dm.get("outcomes_evaluated", 0),
        "readiness_snapshots": snapshots,
        "evidence_bundles": _count_evidence_bundles(),
        "shipped_ventures": _count_shipped_ventures(),
    }
    criteria = {}
    all_met = True
    field_map = {
        "min_decisions": "decisions",
        "min_outcomes_evaluated": "outcomes_evaluated",
        "min_readiness_snapshots": "readiness_snapshots",
        "min_evidence_bundles": "evidence_bundles",
        "min_shipped_ventures": "shipped_ventures",
    }
    for req_key, required in reqs.items():
        field = field_map.get(req_key, req_key.replace("min_", ""))
        val = current.get(field, 0)
        met = val >= required
        criteria[field] = {"required": required, "current": val, "met": met}
        if not met:
            all_met = False

    force = gate.get("enabled", False)
    active = force or all_met
    return {
        "active": active,
        "mode": "enforce" if active else "observe",
        "force_enabled": force,
        "criteria": criteria,
        "all_criteria_met": all_met,
        "bottleneck": "evidence" if current["evidence_bundles"] == 0 else (
            "outcomes" if current["outcomes_evaluated"] < reqs.get("min_outcomes_evaluated", 10) else None
        ),
    }


def _estimate_complexity(title: str, proposal: str, class_info: dict) -> float:
    text = f"{title} {proposal}".lower()
    score = 0.0
    keywords = (
        "auth", "security", "migration", "monetization", "release", "ship",
        "database", "architecture", "refactor", "breaking", "payment", "encrypt",
    )
    hits = sum(1 for k in keywords if k in text)
    score += min(0.6, hits * 0.12)
    score += min(0.3, len(text) / 400)
    tier = class_info.get("tier", 2)
    if tier == 3:
        score += 0.25
    elif tier == "critical":
        score += 0.45
    return round(min(1.0, score), 3)


def _similar_failure_count(venture: str, decision_class: str, title: str) -> int:
    count = 0
    title_l = title.lower()
    for rec in load_all_decisions():
        if rec.get("effectiveness", {}).get("outcome") not in ("approved_failed", "overturned"):
            continue
        if rec.get("venture_slug") == venture and rec.get("decision_class") == decision_class:
            count += 1
        elif rec.get("title", "").lower()[:30] == title_l[:30]:
            count += 1
    return count


def compute_risk_prediction(
    *,
    venture: str,
    class_info: dict,
    reviewers: list[str],
    context: dict,
    evidence_status: str,
    never_again_hits: list[dict],
    title: str = "",
    proposal: str = "",
) -> dict:
    engine = load_risk_engine()
    dc = class_info["id"]
    base = engine["class_base"].get(dc, 32)
    fw = engine["factor_weights"]
    factors: dict[str, float] = {}

    trust_data = _load(ULAS_ROOT / "scoring" / "trust-scores.json")
    provided = [r.strip().lower() for r in reviewers if r.strip()]
    if provided:
        trusts = [
            trust_data["capabilities"].get(r, {}).get("trust", trust_data["initial_trust"])
            for r in provided
        ]
        avg_trust = sum(trusts) / len(trusts)
        factors["reviewer_trust"] = round(max(0, (92 - avg_trust) / 42), 3)
    else:
        factors["reviewer_trust"] = 0.5

    metrics = rebuild_metrics() if runtime_metrics_path().exists() else None
    history_risk = 0.0
    if metrics and provided:
        rm = metrics.get("reviewer_metrics", {})
        missed_rates = []
        for r in provided:
            if r in rm and rm[r].get("accuracy") is not None:
                missed_rates.append(1.0 - rm[r]["accuracy"])
        if missed_rates:
            history_risk = sum(missed_rates) / len(missed_rates)
    factors["reviewer_history"] = round(history_risk, 3)

    tier_key = str(context.get("tier", "2"))
    factors["context_tier"] = engine["tier_risk"].get(tier_key, 0.25)

    factors["evidence_level"] = engine["evidence_risk"].get(evidence_status, 1.0)

    factors["memory_hits"] = 1.0 if never_again_hits else 0.0

    overrides = load_policy_overrides()
    has_ov = bool(
        overrides.get("review_matrix", {}).get(dc)
        or overrides.get("decision_classes", {}).get(dc)
        or overrides.get("confidence_weight_deltas")
    )
    factors["policy_overrides"] = 1.0 if has_ov else 0.0

    factors["complexity"] = _estimate_complexity(title, proposal, class_info)

    factors["similar_failures"] = min(1.0, _similar_failure_count(venture, dc, title) * 0.5)

    weighted = sum(factors[k] * fw[k] for k in fw if k in factors)
    score = round(min(100, max(0, base + weighted * 55)))
    band = _risk_band(score, engine)
    activation = check_risk_activation()

    escalation = dict(engine["escalation"].get(band, {}))
    return {
        "risk_score": score,
        "band": band,
        "factors": factors,
        "class_base": base,
        "weighted_signal": round(weighted, 3),
        "escalation": escalation,
        "activation": {
            "active": activation["active"],
            "mode": activation["mode"],
        },
        "computed_at": now_iso(),
    }


def apply_risk_escalation(review: dict, prediction: dict, reviewers: list[str]) -> dict:
    if not prediction["activation"]["active"]:
        return {**review, "risk_escalation": None, "risk_enforced": False}

    band = prediction["band"]
    esc = prediction.get("escalation", {})
    required = list(review["required_capabilities"])
    provided = list(review["provided_reviewers"])

    for cap in esc.get("required_capabilities", []):
        if cap not in required:
            required.append(cap)
    for cap in esc.get("additional_capabilities", []):
        if cap not in required and cap not in provided:
            required.append(cap)

    missing = [r for r in required if r not in provided]
    min_count = review["minimum_review_count"]
    if band in ("medium", "high", "critical") and len(provided) < min_count + 1 and missing:
        min_count = max(min_count, len(required))

    satisfied = len(missing) == 0 and len(provided) >= min_count
    founder_required = bool(esc.get("founder_approval"))
    if founder_required:
        satisfied = False

    return {
        **review,
        "required_capabilities": required,
        "missing_capabilities": missing,
        "minimum_review_count": min_count,
        "satisfied": satisfied,
        "risk_escalation": band,
        "risk_enforced": True,
        "founder_approval_required": founder_required,
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

    prediction = compute_risk_prediction(
        venture=venture,
        class_info=class_info,
        reviewers=reviewers,
        context=context,
        evidence_status=evidence_status,
        never_again_hits=na_hits,
        title=title,
        proposal=args.proposal or "",
    )
    review = apply_risk_escalation(review, prediction, reviewers)

    decision_id = f"{venture}-{class_info['id'].lower()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    blocked_reasons = []

    if context["state"] == "READ_MORE_REQUIRED":
        blocked_reasons.append(f"READ_MORE_REQUIRED: {context['missing_reads']}")
    if confidence["blocked"]:
        blocked_reasons.append(f"LOW_CONFIDENCE: {confidence['band']} ({confidence['confidence']})")
    if not never_again_clear:
        blocked_reasons.append(f"NEVER_AGAIN_CONFLICT: {[h.get('id') for h in na_hits]}")
    if not review["satisfied"]:
        if review.get("founder_approval_required"):
            blocked_reasons.append(f"FOUNDER_GATE: risk={prediction['band']} score={prediction['risk_score']}")
        elif review.get("risk_escalation"):
            blocked_reasons.append(
                f"RISK_ESCALATION_{review['risk_escalation'].upper()}: missing {review['missing_capabilities']}"
            )
        else:
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
        "prediction": prediction,
        "review": review,
        "never_again_hits": na_hits,
        "status": status,
        "blocked_reasons": blocked_reasons,
        "effectiveness": {
            "outcome_recorded": False,
            "outcome": None,
            "note": None,
            "outcome_at": None,
        },
        "created_at": now_iso(),
    }

    out = runtime_decisions_dir() / f"{decision_id}.json"
    _save(out, record)
    rebuild_metrics()

    print(json.dumps({
        "status": status,
        "decision_id": decision_id,
        "path": str(out.relative_to(REPO_ROOT)),
        "risk_score": prediction["risk_score"],
        "risk_band": prediction["band"],
        "risk_mode": prediction["activation"]["mode"],
    }, indent=2))
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
    if not args.decision_id:
        print("ERROR: --decision-id required (blocks fake calibration)", file=sys.stderr)
        return 1
    try:
        validate_decision_id(args.decision_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    log = _apply_trust_delta(
        args.reviewer,
        args.outcome,
        args.decision_id or "",
        args.reason or "",
        args.evidence or "",
    )
    if not log:
        print(f"Unknown capability: {args.reviewer}", file=sys.stderr)
        return 1
    rebuild_metrics()
    print(json.dumps({
        "capability": args.reviewer.lower(),
        "trust": log["new_trust"],
        "delta": log["delta"],
        "log": log,
    }, indent=2))
    return 0


def cmd_outcome(args: argparse.Namespace) -> int:
    path = find_decision(args.decision_id)
    if not path:
        print(f"Decision not found: {args.decision_id}", file=sys.stderr)
        return 1
    rec = _load(path)
    try:
        validate_outcome_for_record(rec, args.result)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    rec["effectiveness"] = {
        "outcome_recorded": True,
        "outcome": args.result,
        "note": args.note or "",
        "outcome_at": now_iso(),
    }
    _save(path, rec)
    if args.result == "prevented_failure":
        m = rebuild_metrics()
        m["memory_metrics"]["prevented_failures"] += 1
        _save(runtime_metrics_path(), m)
    else:
        rebuild_metrics()
    if getattr(args, "propagate", False):
        try:
            result = propagate_decision(rec, dry_run=False, apply_memory=getattr(args, "apply_memory", False))
            _save(path, rec)
            print(json.dumps({
                "decision_id": rec["decision_id"],
                "outcome": args.result,
                "propagation": result,
            }, indent=2, ensure_ascii=False))
            return 0
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    print(json.dumps({"decision_id": rec["decision_id"], "outcome": args.result}, indent=2))
    return 0


def cmd_propagate(args: argparse.Namespace) -> int:
    path = find_decision(args.decision_id)
    if not path:
        print(f"Decision not found: {args.decision_id}", file=sys.stderr)
        return 1
    rec = _load(path)
    try:
        result = propagate_decision(rec, dry_run=args.dry_run, apply_memory=args.apply_memory)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not args.dry_run:
        _save(path, rec)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def audit_propagation_terminations() -> list[dict]:
    overrides = load_policy_overrides()
    na_count = len(memory_registry().get("entries", []))
    propagated = sum(1 for r in load_all_decisions() if r.get("adaptation", {}).get("propagated_at"))

    chains = [
        {
            "chain": "Failure → Postmortem → Lesson → Policy",
            "terminates_at": "Lesson (06-learning/postmortems/)",
            "manual_steps": ["postmortem write", "ADR"],
            "automated_steps": [],
            "measurable": _count_files("*.md", SVOS_ROOT / "06-learning" / "postmortems") > 0,
            "influences_future_decide": bool(overrides.get("changelog")),
        },
        {
            "chain": "Lesson → Policy → Review Matrix → Trust → Future Decision",
            "terminates_at": "Policy (if no propagate)" if not overrides.get("changelog") else "Future Decision (runtime overrides active)",
            "manual_steps": [] if overrides.get("changelog") else ["policy JSON edit", "calibrate"],
            "automated_steps": ["propagate → trust", "propagate → policy-overrides"] if overrides.get("changelog") else ["propagate available"],
            "measurable": len(overrides.get("changelog", [])) > 0,
            "influences_future_decide": bool(overrides.get("changelog")),
        },
        {
            "chain": "Review → Accuracy → Trust → Calibration",
            "terminates_at": "Calibration (auto via propagate)" if propagated else "Accuracy metrics only",
            "manual_steps": [] if propagated else ["calibrate"],
            "automated_steps": ["propagate trust_updates"] if propagated else [],
            "measurable": propagated > 0,
            "influences_future_decide": propagated > 0,
        },
        {
            "chain": "Outcome → Pattern → Intelligence → Future Decision",
            "terminates_at": "Pattern (scripts/factory/promote-pattern.py — manual)",
            "manual_steps": ["promote-pattern.py", "intelligence-engine.py"],
            "automated_steps": [],
            "measurable": _count_files("*.md", SVOS_ROOT / "06-learning" / "patterns" / "proven") > 0,
            "influences_future_decide": False,
        },
        {
            "chain": "Decision → Outcome → Learning → Adaptation → Improved Decision",
            "terminates_at": "Adaptation" if propagated == 0 else "Improved Decision (overrides + trust wired)",
            "manual_steps": ["outcome record"] if propagated == 0 else [],
            "automated_steps": ["outcome --propagate", "propagate command"],
            "measurable": propagated > 0,
            "influences_future_decide": propagated > 0,
        },
        {
            "chain": "Failure → NEVER_AGAIN → Prevention",
            "terminates_at": "NEVER_AGAIN candidate" if na_count == 0 else "Future decide() block",
            "manual_steps": [] if na_count else ["propagate --apply-memory or manual entry"],
            "automated_steps": ["scan at decide", "propagate --apply-memory"],
            "measurable": na_count > 0,
            "influences_future_decide": na_count > 0,
        },
    ]
    for c in chains:
        if c["influences_future_decide"] and c["automated_steps"]:
            c["status"] = "partially_closed"
        elif c["measurable"] and not c["influences_future_decide"]:
            c["status"] = "open"
        elif c["influences_future_decide"]:
            c["status"] = "partially_closed"
        else:
            c["status"] = "open"
    return chains


def cmd_propagation_audit(args: argparse.Namespace) -> int:
    chains = audit_propagation_terminations()
    overrides = load_policy_overrides()
    propagated = sum(1 for r in load_all_decisions() if r.get("adaptation", {}).get("propagated_at"))
    lines = [
        "=== ULAS Phase 5 — Propagation Audit ===",
        f"Decisions propagated: {propagated}",
        f"Policy override changelog entries: {len(overrides.get('changelog', []))}",
        f"Active review adaptations: {list(overrides.get('review_matrix', {}).keys())}",
        f"Confidence deltas: {overrides.get('confidence_weight_deltas', {})}",
        "",
        "## Where feedback stops",
    ]
    for c in chains:
        lines.append(f"  [{c['status'].upper()}] {c['chain']}")
        lines.append(f"    terminates: {c['terminates_at']}")
        if c["manual_steps"]:
            lines.append(f"    manual: {', '.join(c['manual_steps'])}")
        if c["automated_steps"]:
            lines.append(f"    automated: {', '.join(c['automated_steps'])}")
        lines.append(f"    influences future decide(): {'yes' if c['influences_future_decide'] else 'no'}")
    lines.extend([
        "",
        "Close loop: ulas outcome --decision-id ID --result approved_failed --propagate",
        "Doc: APP-FABRIKASI/ULAS/PHASE5_ADAPTIVE_DECISION.md",
    ])
    print("\n".join(lines))
    if getattr(args, "json", False):
        print(json.dumps({"chains": chains, "overrides": overrides}, indent=2, ensure_ascii=False))
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    metrics = rebuild_metrics()
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return 0


def cmd_maturity_audit(args: argparse.Namespace) -> int:
    report = mat.run_maturity_audit(SVOS_ROOT, REPO_ROOT)
    out_path = SVOS_ROOT / "10-runtime" / "maturity-report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(mat.format_report(report))
        print(f"\nRapor: {out_path.relative_to(REPO_ROOT)}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    m = rebuild_metrics()
    dm = m["decision_metrics"]
    tm = m["token_metrics"]
    mm = m["memory_metrics"]
    lines = [
        "=== ULAS Effectiveness Report ===",
        f"Last rebuilt: {m.get('last_rebuilt', '—')}",
        "",
        "## Decision Metrics",
        f"  total_decisions:     {dm['total_decisions']}",
        f"  approved:            {dm['approved']}",
        f"  blocked:             {dm['blocked']}",
        f"  outcomes_evaluated:  {dm['outcomes_evaluated']}",
        f"  overturned:          {dm['overturned']}",
        f"  failed_after_approval: {dm['failed_after_approval']}",
        "",
        "## LOW_CONFIDENCE (6-month question)",
        f"  low_confidence_blocks:  {dm['low_confidence_blocks']}",
        f"  correct_block:          {dm['low_confidence_correct']}",
        f"  false_block:            {dm['low_confidence_false']}",
        f"  precision:              {dm.get('low_confidence_precision', 'insufficient data (need evaluated blocks)')}",
        "",
        "## Token Metrics",
        f"  tier1: {tm['tier1_usage']}  tier2: {tm['tier2_usage']}  tier3: {tm['tier3_usage']}  critical: {tm['critical_usage']}",
        f"  avg_context_budget: {tm.get('average_context_budget', 0)}",
        "",
        "## Memory Metrics",
        f"  never_again_hits:    {mm['never_again_hits']}",
        f"  prevented_failures:  {mm['prevented_failures']}",
        "",
        "## Reviewer Accuracy",
    ]
    for rev, rm in m.get("reviewer_metrics", {}).items():
        lines.append(f"  {rev}: reviews={rm['reviews']} accuracy={rm.get('accuracy', '—')}")
    if not m.get("reviewer_metrics"):
        lines.append("  (no outcome-tagged reviews yet)")
    lines.extend([
        "",
        "## By Class",
        f"  {m.get('by_class', {})}",
        "",
        "Record outcomes: ulas outcome --decision-id ID --result correct_block|...",
    ])
    print("\n".join(lines))
    return 0


def _count_files(glob_pattern: str, base: Path) -> int:
    return len(list(base.glob(glob_pattern))) if base.exists() else 0


def _classify_loop(exists: bool, measurable: bool, automated: bool, actionable: bool) -> str:
    if not exists:
        return "missing"
    if measurable and automated and actionable:
        return "closed"
    if exists and (measurable or automated):
        return "partially_closed"
    if exists:
        return "open"
    return "missing"


def compute_readiness_scores(metrics: dict) -> dict[str, Any]:
    dm = metrics["decision_metrics"]
    mm = metrics["memory_metrics"]
    na = memory_registry()
    trust_data = _load(ULAS_ROOT / "scoring" / "trust-scores.json")

    learning_scripts = all(
        (REPO_ROOT / p).exists()
        for p in (
            "scripts/factory/record-outcome.py",
            "scripts/factory/record-postmortem.py",
            "scripts/factory/promote-pattern.py",
        )
    )
    postmortems = _count_files("*.md", SVOS_ROOT / "06-learning" / "postmortems")
    adrs = _count_files("ADR-*.md", SVOS_ROOT / "06-learning" / "adr")
    ventures = len(list((SVOS_ROOT / "08-ventures").glob("*/venture.json")))
    shipped = 0
    for vdir in (SVOS_ROOT / "08-ventures").glob("*/venture.json"):
        try:
            if _load(vdir).get("phase") == "shipped":
                shipped += 1
        except (json.JSONDecodeError, OSError):
            continue

    cal_log_entries = sum(len(c.get("calibration_log", [])) for c in trust_data["capabilities"].values())
    history_path = readiness_history_path()
    snapshot_count = 0
    if history_path.exists():
        snapshot_count = len(_load(history_path).get("snapshots", []))

    learning = 35
    if learning_scripts:
        learning += 15
    if dm["outcomes_evaluated"] > 0:
        learning += 12
    if postmortems > 0:
        learning += 15
    if shipped > 0:
        learning += 18
    learning = min(100, learning)

    adaptation = 20
    if cal_log_entries > 0:
        adaptation += 18
    if trust_data["capabilities"]:
        adaptation += min(20, sum(1 for c in trust_data["capabilities"].values() if c.get("reviews", 0) > 0) * 5)
    adaptation = min(100, adaptation)

    explainability = 30
    if dm["total_decisions"] > 0:
        explainability += 20
    if cal_log_entries > 0:
        explainability += 20
    with_outcome = sum(1 for r in load_all_decisions() if r.get("effectiveness", {}).get("outcome_recorded"))
    if with_outcome and dm["total_decisions"]:
        explainability += int(30 * with_outcome / dm["total_decisions"])
    explainability = min(100, explainability)

    auditability = 40
    if dm["total_decisions"] >= 1:
        auditability += 25
    if metrics.get("last_rebuilt"):
        auditability += 17
    auditability = min(100, auditability)

    drift = 15 + min(40, snapshot_count * 8)
    if snapshot_count >= 4:
        drift += 15
    drift = min(100, drift)

    policy = 25
    if adrs > 0:
        policy += min(30, adrs * 10)
    if (ULAS_ROOT / "policies").exists():
        policy += 17
    policy = min(100, policy)

    memory = 15
    entries = len(na.get("entries", []))
    if entries:
        memory += min(25, entries * 8)
    if mm["never_again_hits"] > 0:
        memory += 20
    if mm["prevented_failures"] > 0:
        memory += 25
    memory = min(100, memory)

    weights = {
        "learning_capability": 0.18,
        "adaptation_capability": 0.18,
        "explainability": 0.14,
        "auditability": 0.14,
        "drift_resistance": 0.12,
        "policy_evolution": 0.12,
        "memory_effectiveness": 0.12,
    }
    scores = {
        "learning_capability": learning,
        "adaptation_capability": adaptation,
        "explainability": explainability,
        "auditability": auditability,
        "drift_resistance": drift,
        "policy_evolution": policy,
        "memory_effectiveness": memory,
    }
    composite = round(sum(scores[k] * weights[k] for k in weights))
    return {
        "composite_score": composite,
        "dimensions": {
            k: {"score": scores[k], "weight": weights[k]}
            for k in scores
        },
        "signals": {
            "learning_scripts": learning_scripts,
            "postmortems": postmortems,
            "adrs": adrs,
            "ventures": ventures,
            "shipped_ventures": shipped,
            "calibration_log_entries": cal_log_entries,
            "readiness_snapshots": snapshot_count,
            "never_again_entries": entries,
        },
    }


def audit_feedback_loops(metrics: dict) -> list[dict]:
    dm = metrics["decision_metrics"]
    mm = metrics["memory_metrics"]
    na_entries = len(memory_registry().get("entries", []))
    evidence_dirs = _count_files("*", SVOS_ROOT / "07-evidence") if (SVOS_ROOT / "07-evidence").exists() else 0
    portfolio_exists = (SVOS_ROOT / "09-portfolio").exists()

    loops = [
        {
            "chain": "Decision → Outcome → Lesson → Policy Update",
            "exists": dm["total_decisions"] > 0 and (REPO_ROOT / "scripts/factory/record-adr.py").exists(),
            "measurable": dm["outcomes_evaluated"] > 0,
            "automated": False,
            "actionable": False,
        },
        {
            "chain": "Decision → Failure → Memory → Prevention",
            "exists": na_entries >= 0 and "prevented_failure" in OUTCOME_CHOICES,
            "measurable": mm["never_again_hits"] > 0 or mm["prevented_failures"] > 0,
            "automated": False,
            "actionable": mm["prevented_failures"] > 0 or na_entries > 0,
        },
        {
            "chain": "Review → Accuracy → Trust → Calibration",
            "exists": bool(metrics.get("reviewer_metrics")),
            "measurable": dm["outcomes_evaluated"] > 0,
            "automated": False,
            "actionable": any(
                c.get("reviews", 0) > 0
                for c in _load(ULAS_ROOT / "scoring" / "trust-scores.json")["capabilities"].values()
            ),
        },
        {
            "chain": "Context → Usage → Token Metrics → Optimization",
            "exists": dm["total_decisions"] > 0,
            "measurable": metrics["token_metrics"]["tier2_usage"] + metrics["token_metrics"]["tier1_usage"] > 0,
            "automated": True,
            "actionable": False,
        },
        {
            "chain": "Evidence → Insight → Pattern → Decision",
            "exists": (SVOS_ROOT / "07-evidence").exists() and (REPO_ROOT / "scripts/factory/promote-pattern.py").exists(),
            "measurable": evidence_dirs > 0,
            "automated": False,
            "actionable": False,
        },
        {
            "chain": "Venture → Outcome → Portfolio → Capital Allocation",
            "exists": portfolio_exists and (REPO_ROOT / "scripts/factory/build-portfolio-outcomes.py").exists(),
            "measurable": False,
            "automated": False,
            "actionable": False,
        },
    ]
    for loop in loops:
        loop["status"] = _classify_loop(loop["exists"], loop["measurable"], loop["automated"], loop["actionable"])
    return loops


def append_readiness_snapshot(metrics: dict, readiness: dict) -> dict:
    path = readiness_history_path()
    history = _load(path) if path.exists() else {"version": "1.0", "snapshots": []}
    dm = metrics["decision_metrics"]
    snap = {
        "at": now_iso(),
        "self_improvement_score": readiness["composite_score"],
        "total_decisions": dm["total_decisions"],
        "outcomes_evaluated": dm["outcomes_evaluated"],
        "low_confidence_precision": dm.get("low_confidence_precision"),
        "never_again_hits": metrics["memory_metrics"]["never_again_hits"],
        "prevented_failures": metrics["memory_metrics"]["prevented_failures"],
        "dimensions": {k: v["score"] for k, v in readiness["dimensions"].items()},
    }
    history.setdefault("snapshots", []).append(snap)
    _save(path, history)
    return history


def cmd_feedback_audit(args: argparse.Namespace) -> int:
    metrics = rebuild_metrics()
    readiness = compute_readiness_scores(metrics)
    loops = audit_feedback_loops(metrics)
    history = append_readiness_snapshot(metrics, readiness)

    counts = {"closed": 0, "partially_closed": 0, "open": 0, "missing": 0}
    for loop in loops:
        counts[loop["status"]] = counts.get(loop["status"], 0) + 1

    report = {
        "audited_at": now_iso(),
        "composite_score": readiness["composite_score"],
        "verdict": "partially_capable_not_proven" if readiness["composite_score"] < 70 else "improving",
        "dimensions": readiness["dimensions"],
        "signals": readiness["signals"],
        "feedback_loops": loops,
        "loop_counts": counts,
        "trend_snapshots": len(history.get("snapshots", [])),
        "trend_ready": len(history.get("snapshots", [])) >= 4,
        "doc": "ULAS/PHASE4_FEEDBACK_CLOSURE_AUDIT.md",
    }
    _save(readiness_schema_path(), {
        "version": "1.0",
        "audited_at": report["audited_at"][:10],
        "composite_score": report["composite_score"],
        "verdict": report["verdict"],
        "dimensions": {
            k: {**v, "evidence": "computed by feedback-audit"}
            for k, v in readiness["dimensions"].items()
        },
        "feedback_loops": counts,
        "critical_gaps": [
            g for g, cond in [
                ("no_venture_outcomes", readiness["signals"]["shipped_ventures"] == 0),
                ("zero_fully_closed_loops", counts["closed"] == 0),
                ("no_trend_analysis", not report["trend_ready"]),
                ("policy_evolution_manual_only", readiness["signals"]["adrs"] == 0),
            ]
            if cond
        ],
        "next_proof": "first venture: charter → ship → evidence → outcome → one closed learning loop",
    })

    lines = [
        "=== ULAS Phase 4 — Feedback Closure Audit ===",
        f"Audited: {report['audited_at']}",
        f"Self-Improvement Readiness: {readiness['composite_score']} / 100",
        f"Verdict: {report['verdict']}",
        "",
        "## Dimensions",
    ]
    for name, dim in readiness["dimensions"].items():
        lines.append(f"  {name}: {dim['score']} (w={dim['weight']})")
    lines.extend(["", "## Feedback Loops"])
    for loop in loops:
        flags = []
        if loop["exists"]:
            flags.append("exists")
        if loop["measurable"]:
            flags.append("measurable")
        if loop["automated"]:
            flags.append("automated")
        if loop["actionable"]:
            flags.append("actionable")
        lines.append(f"  [{loop['status'].upper()}] {loop['chain']}")
        lines.append(f"    {' · '.join(flags) if flags else 'not wired'}")
    lines.extend([
        "",
        f"Loop counts: closed={counts['closed']} partial={counts['partially_closed']} "
        f"open={counts['open']} missing={counts['missing']}",
        f"Trend snapshots: {report['trend_snapshots']} (trend analysis: {'ready' if report['trend_ready'] else 'need ≥4'})",
        "",
        f"Full report: APP-FABRIKASI/ULAS/PHASE4_FEEDBACK_CLOSURE_AUDIT.md",
        f"Snapshot: {readiness_history_path().relative_to(REPO_ROOT)}",
    ])
    print("\n".join(lines))
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    audit_path = ULAS_ROOT / "AUDIT.md"
    if audit_path.exists():
        print(audit_path.read_text(encoding="utf-8"))
    else:
        print("AUDIT.md not found", file=sys.stderr)
        return 1
    return 0


def cmd_risk(args: argparse.Namespace) -> int:
    class_info = resolve_class(args.class_)
    venture = args.venture
    context = assemble_context(venture, class_info)
    na_hits = scan_never_again(args.proposal or args.title or "") if (args.proposal or args.title) else []
    evidence_status = "none"
    vp = venture_path(venture)
    if vp.exists():
        evidence_status = _load(vp).get("evidence_status", "none")
    reviewers = [r.strip() for r in args.reviewers.split(",") if r.strip()]
    prediction = compute_risk_prediction(
        venture=venture,
        class_info=class_info,
        reviewers=reviewers,
        context=context,
        evidence_status=evidence_status,
        never_again_hits=na_hits,
        title=args.title or "",
        proposal=args.proposal or "",
    )
    review = validate_review_chain(class_info["id"], reviewers)
    escalated = apply_risk_escalation(review, prediction, reviewers)
    gate = check_risk_activation()
    result = {
        "prediction": prediction,
        "current_review": review,
        "if_gate_active_review": escalated,
        "activation_gate": gate,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_risk_gate(args: argparse.Namespace) -> int:
    gate = check_risk_activation()
    engine = load_risk_engine()
    lines = [
        "=== ULAS Phase 6 — Risk Activation Gate ===",
        f"Mode: {gate['mode'].upper()} ({'escalation enforced' if gate['active'] else 'preview only'})",
        f"Bottleneck hint: {gate.get('bottleneck') or '—'}",
        "",
        "## Criteria",
    ]
    for name, c in gate["criteria"].items():
        mark = "✓" if c["met"] else "✗"
        lines.append(f"  {mark} {name}: {c['current']} / {c['required']}")
    lines.extend([
        "",
        f"Gate active: {gate['active']}",
        "",
        "Preview risk: ulas risk --venture SLUG --class B --reviewers architect,qa",
        "Doc: APP-FABRIKASI/ULAS/PHASE6_PREDICTIVE_DECISION.md",
    ])
    print("\n".join(lines))
    if getattr(args, "json", False):
        print(json.dumps({"gate": gate, "engine": engine.get("activation_gate")}, indent=2))
    return 0


def reset_policy_overrides(reason: str = "manual reset") -> dict:
    data = default_policy_overrides()
    data["changelog"] = [{
        "at": now_iso(),
        "decision_id": None,
        "adaptation": {"type": "reset", "reason": reason},
    }]
    save_policy_overrides(data)
    return data


def cmd_overrides_reset(args: argparse.Namespace) -> int:
    data = reset_policy_overrides(getattr(args, "reason", "") or "ulas overrides-reset")
    print(json.dumps({
        "reset": True,
        "path": str(policy_overrides_path().relative_to(REPO_ROOT)),
        "changelog_entries": len(data.get("changelog", [])),
    }, indent=2))
    rebuild_metrics()
    return 0


def work_runtime_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "work"
    d.mkdir(parents=True, exist_ok=True)
    return d


def work_chain_path(decision_id: str) -> Path:
    return work_runtime_dir() / f"{decision_id}.json"


def load_evidence_manifest(venture_slug: str) -> dict | None:
    path = SVOS_ROOT / "07-evidence" / venture_slug / "manifest.json"
    if path.exists():
        return _load(path)
    return None


def load_venture_record(venture_slug: str) -> dict:
    vp = venture_path(venture_slug)
    if vp.exists():
        return _load(vp)
    return {}


def _wp(
    seq: int,
    capability: str,
    task: str,
    acceptance: str,
    platform: str = "android",
) -> dict:
    return {
        "id": f"wp-{seq}",
        "sequence": seq,
        "capability": capability,
        "platform": platform,
        "task": task,
        "status": "pending",
        "acceptance": acceptance,
    }


def generate_work_chain(rec: dict) -> dict:
    decision_id = rec["decision_id"]
    venture = rec.get("venture_slug", "")
    venture_data = load_venture_record(venture)
    evidence = load_evidence_manifest(venture)
    platform = (venture_data.get("platform") or ["android"])[0]
    codebase = venture_data.get("codebase_resolved") or venture_data.get("codebase_path", "")
    title = rec.get("title", "")
    packages: list[dict] = []
    seq = 1

    for reason in rec.get("blocked_reasons", []):
        if "LOW_CONFIDENCE" in reason:
            packages.append(_wp(
                seq, "planner",
                "collect evidence and update venture evidence_status",
                "evidence_status is partial or collected",
                platform,
            ))
            seq += 1
        if "REVIEW_CHAIN" in reason or "RISK_ESCALATION" in reason:
            missing = rec.get("review", {}).get("missing_capabilities", [])
            packages.append(_wp(
                seq, "auditor",
                f"complete review chain: add {missing or 'required reviewers'}",
                "review.satisfied is true on re-decide",
                platform,
            ))
            seq += 1
        if "FOUNDER_GATE" in reason:
            packages.append(_wp(
                seq, "planner",
                "founder approval for critical-risk decision",
                "founder sign-off recorded",
                platform,
            ))
            seq += 1

    tests_failed = 0
    if evidence:
        for src in evidence.get("sources", []):
            if src.get("type") == "unit_test":
                tests_failed = int(src.get("failed", 0))
    validation = venture_data.get("validation", {})
    if validation.get("tests", {}).get("failed"):
        tests_failed = max(tests_failed, int(validation["tests"]["failed"]))

    if tests_failed > 0 or "test" in title.lower() or "fail" in title.lower():
        report_path = SVOS_ROOT / "10-runtime" / "evidence" / venture / "test-failure-report.json"
        clusters: list[dict] = []
        if report_path.exists():
            clusters = _load(report_path).get("clusters", [])
        if not clusters and evidence:
            ft = []
            for src in evidence.get("sources", []):
                ft.extend(src.get("failed_tests", []))
            if ft:
                clusters = gtp.cluster_failures([{"test": t} for t in ft])

        if clusters:
            cap_task = {
                "architecture": ("fix architecture / module boundary failures", "architecture cluster tests pass"),
                "test_env": ("fix test runtime (JDK, Robolectric, sandbox)", "affected tests pass"),
                "jvm_android_api": ("add Robolectric or refactor JVM tests using Android APIs", "affected tests pass"),
                "ui": ("fix UI / visual regression test failures", "affected tests pass"),
                "other": ("fix remaining unit test failures", "all listed tests pass"),
            }
            for cl in clusters:
                cid = cl.get("id", "other")
                cap_role = {
                    "android.architecture": "architect",
                    "android.library": "architect",
                    "android.ui": "architect",
                    "android.testing": "qa",
                }.get(cl.get("capability", ""), "architect")
                task_tpl = cap_task.get(cid, (f"fix cluster {cid}", "cluster tests pass"))
                names = ", ".join(f["test"].split(".")[-1] for f in cl.get("failures", [])[:4])
                packages.append(_wp(
                    seq, cap_role,
                    f"{task_tpl[0]} [{names}]",
                    task_tpl[1],
                    platform,
                ))
                seq += 1
        else:
            packages.append(_wp(
                seq, "architect",
                f"investigate {tests_failed or 'failing'} unit test(s) in codebase",
                "root cause documented per failure cluster",
                platform,
            ))
            seq += 1
            packages.append(_wp(
                seq, "architect",
                "implement fixes per failure cluster",
                "targeted tests pass locally",
                platform,
            ))
            seq += 1
        bridge_cfg = gtp.load_bridge_config(SVOS_ROOT, venture_data)
        test_task = bridge_cfg.get("unit_test_task", ":app:testDebugUnitTest")
        packages.append(_wp(
            seq, "qa",
            "run full unit test suite and confirm zero failures",
            f"./gradlew {test_task} — 0 failed",
            platform,
        ))
        seq += 1

    if not packages:
        packages = [
            _wp(1, "planner", f"confirm scope: {title}", "scope note in decision or ADR", platform),
            _wp(2, "architect", "execute approved change in codebase", "build succeeds", platform),
            _wp(3, "qa", "verify change against acceptance criteria", "verification checks pass", platform),
        ]

    packages.append(_wp(
        seq, "auditor",
        "record evidence via bridge and close work chain",
        "07-evidence manifest updated; outcome recorded",
        platform,
    ))

    bridge_cfg = gtp.load_bridge_config(SVOS_ROOT, venture_data)
    build_task = bridge_cfg.get("build_task", ":app:assembleDebug")
    test_task = bridge_cfg.get("unit_test_task", ":app:testDebugUnitTest")
    build_task_name = build_task.split(":")[-1] if ":" in build_task else build_task
    test_task_name = test_task.split(":")[-1] if ":" in test_task else test_task

    execution_manifest = {
        "codebase_path": codebase,
        "codebase_resolved": venture_data.get("codebase_resolved", codebase),
        "platform": platform,
        "commands": [
            {
                "id": "build",
                "cwd": codebase,
                "cmd": f"./gradlew {build_task}",
            },
            {
                "id": "unit_test",
                "cwd": codebase,
                "cmd": f"./gradlew {test_task}",
            },
        ],
        "bridge": "APP-FABRIKASI/scripts/bridge-venture.sh",
    }

    verification_manifest = {
        "checks": [
            {"id": "build_ok", "type": "gradle", "task": build_task_name, "expect": "success"},
            {"id": "tests_zero_fail", "type": "gradle", "task": test_task_name, "expect": {"failures": 0}},
            {"id": "docs_audit", "type": "script", "cmd": "bash scripts/docs_audit.sh", "optional": True},
        ],
        "retry_policy": {"max_attempts": 3, "on_fail": "return to architect wp"},
    }

    evidence_manifest = {
        "venture_evidence_ref": f"07-evidence/{venture}/manifest.json",
        "update_via": "APP-FABRIKASI/scripts/bridge-venture.sh",
        "required_fields": ["sources.build.status", "sources.unit_test.failed"],
        "outcome_command": "ulas outcome --decision-id {id} --result approved_success",
    }

    state = "ready" if rec.get("status") == "APPROVED" else "blocked"

    return {
        "work_id": f"{decision_id}-work",
        "decision_id": decision_id,
        "decision_title": title,
        "decision_status": rec.get("status"),
        "venture_slug": venture,
        "codebase_path": codebase,
        "platform": platform,
        "generated_at": now_iso(),
        "state": state,
        "work_packages": packages,
        "execution_manifest": execution_manifest,
        "verification_manifest": verification_manifest,
        "evidence_manifest": evidence_manifest,
    }


def cmd_work_generate(args: argparse.Namespace) -> int:
    path, rec = load_decision_record(args.decision_id)
    if not path or not rec:
        print(f"Decision not found: {args.decision_id}", file=sys.stderr)
        return 1
    chain = generate_work_chain(rec)
    out = work_chain_path(rec["decision_id"])
    _save(out, chain)
    rec["work"] = {"work_id": chain["work_id"], "generated_at": chain["generated_at"], "state": chain["state"]}
    _save(path, rec)
    print(json.dumps({
        "work_id": chain["work_id"],
        "path": str(out.relative_to(REPO_ROOT)),
        "packages": len(chain["work_packages"]),
        "state": chain["state"],
    }, indent=2))
    if getattr(args, "verbose", False):
        print(json.dumps(chain, indent=2, ensure_ascii=False))
    return 0


def cmd_work_show(args: argparse.Namespace) -> int:
    out = work_chain_path(args.decision_id)
    if not out.exists():
        alt = find_decision(args.decision_id)
        if alt:
            rec = _load(alt)
            did = rec.get("decision_id", args.decision_id)
            out = work_chain_path(did)
    if not out.exists():
        print(f"No work chain for {args.decision_id}. Run: ulas work generate --decision-id ID", file=sys.stderr)
        return 1
    print(json.dumps(_load(out), indent=2, ensure_ascii=False))
    return 0


def cmd_work_list(args: argparse.Namespace) -> int:
    items = []
    for f in sorted(work_runtime_dir().glob("*.json")):
        try:
            w = _load(f)
            items.append({
                "work_id": w.get("work_id"),
                "decision_id": w.get("decision_id"),
                "state": w.get("state"),
                "packages": len(w.get("work_packages", [])),
                "generated_at": w.get("generated_at"),
            })
        except (json.JSONDecodeError, OSError):
            continue
    print(json.dumps({"work_chains": items, "count": len(items)}, indent=2))
    return 0


# --- Capability Router (P3 — registry + policy; no hardcoded role→provider) ---

ROUTING_ROOT = ULAS_ROOT / "routing"


def load_capability_registry() -> dict:
    mp_path = ULAS_ROOT / "marketplace" / "capability-marketplace.json"
    if mp_path.exists():
        mp = _load(mp_path)
        return {
            "version": mp.get("version"),
            "capabilities": mp.get("capabilities", {}),
            "role_platform_map": mp.get("role_platform_map", {}),
        }
    return _load(ROUTING_ROOT / "capability-registry.json")


def load_provider_registry() -> dict:
    return _load(ROUTING_ROOT / "provider-registry.json")


def load_routing_policy() -> dict:
    policy = _load(ROUTING_ROOT / "routing-policy.json")
    override_path = SVOS_ROOT / "10-runtime" / "ulas" / "routing" / "policy-overrides.json"
    if override_path.exists():
        overrides = _load(override_path)
        merged = dict(policy.get("defaults", {}))
        merged.update(overrides.get("defaults", {}))
        policy["defaults"] = merged
        policy["policy_source"] = str(override_path.relative_to(REPO_ROOT))
    else:
        policy["policy_source"] = str((ROUTING_ROOT / "routing-policy.json").relative_to(REPO_ROOT))
    return policy


def resolve_capability_id(role: str, platform: str, registry: dict | None = None) -> str:
    reg = registry or load_capability_registry()
    role_map = reg.get("role_platform_map", {}).get(role, {})
    cap_id = role_map.get(platform) or role_map.get("*")
    if cap_id:
        return cap_id
    generic = {"planner": "generic.planning", "architect": "generic.architecture",
               "qa": "generic.qa", "auditor": "generic.audit"}
    return generic.get(role, f"generic.{role}")


def select_provider_for_capability(capability_id: str, cap_reg: dict, policy: dict) -> tuple[str, dict]:
    prov_reg = load_provider_registry()
    provider_id = policy.get("defaults", {}).get(capability_id)
    cap = cap_reg.get("capabilities", {}).get(capability_id, {})
    if not provider_id:
        provider_id = cap.get("default_provider")
    if not provider_id:
        exec_class = cap.get("execution_class", "implementation")
        provider_id = policy.get("fallback_by_execution_class", {}).get(exec_class, "human")
    provider = prov_reg.get("providers", {}).get(provider_id, prov_reg["providers"]["human"])
    return provider_id, provider


def build_routing_manifest(chain: dict) -> dict:
    cap_reg = load_capability_registry()
    policy = load_routing_policy()
    bindings: list[dict] = []
    capabilities_needed: list[str] = []
    seen: set[str] = set()

    for wp in chain.get("work_packages", []):
        role = wp.get("capability", "")
        platform = wp.get("platform", "android")
        cap_id = resolve_capability_id(role, platform, cap_reg)
        if cap_id not in seen:
            capabilities_needed.append(cap_id)
            seen.add(cap_id)
        provider_id, provider = select_provider_for_capability(cap_id, cap_reg, policy)
        cap_meta = cap_reg.get("capabilities", {}).get(cap_id, {})
        bindings.append({
            "work_package_id": wp.get("id"),
            "capability_id": cap_id,
            "label": cap_meta.get("label", cap_id),
            "role": role,
            "platform": platform,
            "provider_id": provider_id,
            "provider_type": provider.get("type"),
            "dispatch": provider.get("dispatch", "manual"),
            "wired": bool(provider.get("wired", False)),
        })
        wp["capability_id"] = cap_id
        wp["provider_id"] = provider_id

    return {
        "routing_id": f"{chain['decision_id']}-routing",
        "decision_id": chain["decision_id"],
        "generated_at": now_iso(),
        "policy_version": policy.get("version"),
        "policy_source": policy.get("policy_source"),
        "capabilities_needed": capabilities_needed,
        "bindings": bindings,
    }


def ensure_routing_manifest(chain: dict) -> dict:
    if chain.get("routing_manifest"):
        return chain["routing_manifest"]
    rm = build_routing_manifest(chain)
    chain["routing_manifest"] = rm
    return rm


def binding_for_capability(chain: dict, capability_id: str) -> dict | None:
    rm = ensure_routing_manifest(chain)
    for b in rm.get("bindings", []):
        if b.get("capability_id") == capability_id:
            return b
    return None


def binding_is_automated(binding: dict) -> bool:
    return binding.get("dispatch") == "automated" and binding.get("wired", False)


def manual_bindings(chain: dict) -> list[dict]:
    rm = ensure_routing_manifest(chain)
    return [b for b in rm.get("bindings", []) if not binding_is_automated(b)]


def cmd_capability_route(args: argparse.Namespace) -> int:
    wc_path, chain = load_work_chain(args.decision_id)
    if not chain or not wc_path:
        print(f"No work chain for {args.decision_id}", file=sys.stderr)
        return 1
    rm = build_routing_manifest(chain)
    chain["routing_manifest"] = rm
    _save(wc_path, chain)
    print(json.dumps({
        "routing_id": rm["routing_id"],
        "capabilities_needed": rm["capabilities_needed"],
        "bindings": len(rm["bindings"]),
        "policy_source": rm["policy_source"],
    }, indent=2))
    if getattr(args, "verbose", False):
        print(json.dumps(rm, indent=2, ensure_ascii=False))
    return 0


def cmd_capability_show(args: argparse.Namespace) -> int:
    wc_path, chain = load_work_chain(args.decision_id)
    if not chain or not wc_path:
        print(f"No work chain for {args.decision_id}", file=sys.stderr)
        return 1
    rm = ensure_routing_manifest(chain)
    if not chain.get("routing_manifest"):
        chain["routing_manifest"] = rm
        _save(wc_path, chain)
    lines = ["Capabilities Needed"]
    shown: set[str] = set()
    for b in rm.get("bindings", []):
        cap_id = b["capability_id"]
        if cap_id in shown:
            continue
        shown.add(cap_id)
        status = "automated" if binding_is_automated(b) else "delegated"
        wired = "wired" if b.get("wired") else "not wired"
        lines.append(
            f"  ✓ {b.get('label', cap_id)}  →  {b['provider_id']} ({status}, {wired})"
        )
    print("\n".join(lines))
    if getattr(args, "json", False):
        print(json.dumps(rm, indent=2, ensure_ascii=False))
    return 0


def cmd_capability_policy(args: argparse.Namespace) -> int:
    policy = load_routing_policy()
    print(json.dumps({
        "version": policy.get("version"),
        "policy_source": policy.get("policy_source"),
        "defaults": policy.get("defaults"),
        "fallback_by_execution_class": policy.get("fallback_by_execution_class"),
    }, indent=2, ensure_ascii=False))
    return 0


# --- Provider Dispatch (contract-based; no API SDK) ---

def dispatch_runtime_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "dispatch"
    d.mkdir(parents=True, exist_ok=True)
    return d


def dispatch_log_path(decision_id: str) -> Path:
    return dispatch_runtime_dir() / f"{decision_id}.json"


def record_dispatch_utilization(chain: dict, envelopes: list[dict]) -> None:
    decision_id = chain["decision_id"]
    seen: set[str] = set()
    for env in envelopes:
        cap_id = env.get("capability_id", "")
        ctx = env.get("invoke", {}).get("capability_context", {})
        injected = ctx.get("injected_ids", [])
        if not cap_id or not injected:
            continue
        key = f"{cap_id}:{','.join(i['id'] for i in injected)}"
        if key in seen:
            continue
        seen.add(key)
        cmem.record_utilization(decision_id, cap_id, injected, source="dispatch")


def build_dispatch_envelope(binding: dict, wp: dict, chain: dict) -> dict:
    prov_reg = load_provider_registry()
    provider = prov_reg.get("providers", {}).get(binding["provider_id"], {})
    ptype = provider.get("type", "manual")
    if ptype == "local_shell":
        schema = "shell_invoke"
    elif ptype == "manual":
        schema = "manual_invoke"
    else:
        schema = "ai_invoke"
    return {
        "contract_version": "1.0",
        "dispatch_id": f"{chain['decision_id']}-{wp['id']}-{now_iso().replace(':', '')}",
        "decision_id": chain["decision_id"],
        "work_package_id": wp["id"],
        "capability_id": binding["capability_id"],
        "provider_id": binding["provider_id"],
        "provider_type": ptype,
        "invoke": {
            "schema": schema,
            "context_refs": [
                f"10-runtime/ulas/work/{chain['decision_id']}.json#{wp['id']}",
                cmem.memory_context_ref(binding["capability_id"], 2),
            ],
            "capability_context": cmem.build_capability_context(
                binding["capability_id"], 2, task_hint=wp.get("task", ""),
            ),
            "instruction": wp.get("task", ""),
            "acceptance": wp.get("acceptance", ""),
        },
        "status": "pending",
        "created_at": now_iso(),
    }


def build_dispatch_plan(chain: dict) -> list[dict]:
    rm = ensure_routing_manifest(chain)
    wp_by_id = {wp["id"]: wp for wp in chain.get("work_packages", [])}
    envelopes: list[dict] = []
    for binding in rm.get("bindings", []):
        if binding_is_automated(binding):
            continue
        wp = wp_by_id.get(binding.get("work_package_id", ""))
        if wp:
            envelopes.append(build_dispatch_envelope(binding, wp, chain))
    return envelopes


def ensure_dispatch_log(chain: dict) -> dict:
    path = dispatch_log_path(chain["decision_id"])
    if path.exists():
        return _load(path)
    envelopes = build_dispatch_plan(chain)
    log = {
        "decision_id": chain["decision_id"],
        "envelopes": envelopes,
        "created_at": now_iso(),
    }
    _save(path, log)
    record_dispatch_utilization(chain, envelopes)
    return log


def dispatch_envelope(envelope: dict, codebase: Path) -> dict:
    out = dict(envelope)
    out["status"] = "dispatched"
    invoke = out.get("invoke", {})
    schema = invoke.get("schema", "ai_invoke")
    if schema == "shell_invoke":
        result = invoke_provider(out["provider_id"], invoke, codebase)
    elif schema == "manual_invoke":
        result = invoke_provider("human", invoke, codebase)
    else:
        result = invoke_ai_envelope(out["provider_id"], out, codebase)
    if result.get("skipped"):
        out["status"] = "skipped"
    elif result.get("success"):
        out["status"] = "completed"
    else:
        out["status"] = "failed"
    out["result"] = {**result, "completed_at": now_iso()}
    return out


def build_repair_plan(failed_checks: list[dict], chain: dict, attempt: int) -> dict:
    retry = chain.get("verification_manifest", {}).get("retry_policy", {})
    repair_role = retry.get("repair_capability", "architect")
    repair_cap_id = resolve_capability_id(repair_role, chain.get("platform", "android"))
    binding = binding_for_capability(chain, repair_cap_id)
    triggered = [
        c.get("id") for c in failed_checks
        if not c.get("optional") and not c.get("passed")
    ]
    failed_tests: list[str] = []
    fail_count = None
    for c in failed_checks:
        if c.get("id") == "tests_zero_fail":
            failed_tests = c.get("failed_tests", [])
            fail_count = c.get("failures")
    plan_item: dict = {
        "target_capability_id": repair_cap_id,
        "target_provider_id": binding["provider_id"] if binding else "human",
        "action": "address verification failures",
        "failed_checks": triggered,
        "failed_tests": failed_tests,
        "failures": fail_count,
    }
    if binding:
        plan_item["dispatch_ref"] = f"10-runtime/ulas/dispatch/{chain['decision_id']}.json"
    return {"attempt": attempt, "triggered_by": triggered, "plans": [plan_item]}


def record_chain_memory_impact(chain: dict, outcome: str, failed_tags: list[str]) -> None:
    decision_id = chain["decision_id"]
    path = dispatch_log_path(decision_id)
    if not path.exists():
        return
    for env in _load(path).get("envelopes", []):
        cap_id = env.get("capability_id")
        if not cap_id:
            continue
        injected = env.get("invoke", {}).get("capability_context", {}).get("injected_ids", [])
        cmem.record_memory_impact(decision_id, cap_id, outcome, failed_tags, injected)


def cmd_dispatch_audit(args: argparse.Namespace) -> int:
    report = cmem.dispatch_adapter_audit()
    out_path = ULAS_ROOT / "dispatch" / "PROVIDER_DISPATCH_ADAPTER_AUDIT.json"
    _save(out_path, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if getattr(args, "verbose", False):
        print(f"\nWrote {out_path.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


def cmd_dispatch_plan(args: argparse.Namespace) -> int:
    wc_path, chain = load_work_chain(args.decision_id)
    if not chain or not wc_path:
        print(f"No work chain for {args.decision_id}", file=sys.stderr)
        return 1
    ensure_routing_manifest(chain)
    envelopes = build_dispatch_plan(chain)
    log = {
        "decision_id": chain["decision_id"],
        "envelopes": envelopes,
        "created_at": now_iso(),
        "policy_source": chain.get("routing_manifest", {}).get("policy_source"),
    }
    _save(dispatch_log_path(chain["decision_id"]), log)
    record_dispatch_utilization(chain, envelopes)
    _save(wc_path, chain)
    print(json.dumps({
        "decision_id": chain["decision_id"],
        "envelopes": len(envelopes),
        "path": str(dispatch_log_path(chain["decision_id"]).relative_to(REPO_ROOT)),
    }, indent=2))
    if getattr(args, "verbose", False):
        print(json.dumps(log, indent=2, ensure_ascii=False))
    return 0


def load_dispatch_log(decision_id: str) -> dict | None:
    path = dispatch_log_path(decision_id)
    return _load(path) if path.exists() else None


def save_dispatch_log(log: dict) -> Path:
    path = dispatch_log_path(log["decision_id"])
    _save(path, log)
    return path


def find_dispatch_envelope(log: dict, dispatch_id: str) -> tuple[int, dict | None]:
    for i, env in enumerate(log.get("envelopes", [])):
        if env.get("dispatch_id") == dispatch_id:
            return i, env
    return -1, None


def cmd_dispatch_log(args: argparse.Namespace) -> int:
    path = dispatch_log_path(args.decision_id)
    if not path.exists():
        print(f"No dispatch log for {args.decision_id}. Run: ulas dispatch plan --decision-id ID", file=sys.stderr)
        return 1
    print(json.dumps(_load(path), indent=2, ensure_ascii=False))
    return 0


def cmd_dispatch_execute(args: argparse.Namespace) -> int:
    wc_path, chain = load_work_chain(args.decision_id)
    if not chain or not wc_path:
        print(f"No work chain for {args.decision_id}", file=sys.stderr)
        return 1
    codebase = resolve_codebase_path(chain)
    log = load_dispatch_log(chain["decision_id"])
    if not log:
        ensure_routing_manifest(chain)
        envelopes = build_dispatch_plan(chain)
        log = {
            "decision_id": chain["decision_id"],
            "envelopes": envelopes,
            "created_at": now_iso(),
            "policy_source": chain.get("routing_manifest", {}).get("policy_source"),
        }
        save_dispatch_log(log)
        record_dispatch_utilization(chain, envelopes)
        _save(wc_path, chain)
    dry_run = getattr(args, "dry_run", False)
    mode = getattr(args, "mode", "queue") or "queue"
    only_dispatch = getattr(args, "dispatch_id", "") or ""
    materialized: list[dict] = []
    prov_reg = load_provider_registry()
    for env in log.get("envelopes", []):
        if only_dispatch and env.get("dispatch_id") != only_dispatch:
            continue
        if env.get("status") not in ("pending", "dispatched"):
            continue
        schema = env.get("invoke", {}).get("schema", "")
        if schema not in ("ai_invoke", "manual_invoke"):
            continue
        rec = {
            "dispatch_id": env["dispatch_id"],
            "work_package_id": env.get("work_package_id"),
            "provider_id": env.get("provider_id"),
            "schema": schema,
            "mode": mode,
        }
        if dry_run:
            rec["dry_run"] = True
            materialized.append(rec)
            continue
        if mode == "sdk" and schema == "ai_invoke":
            provider = prov_reg.get("providers", {}).get(env.get("provider_id", ""), {})
            if not provider.get("adapter"):
                rec["error"] = "no adapter configured"
                materialized.append(rec)
                continue
            env["status"] = "dispatched"
            env["dispatched_at"] = now_iso()
            result = invoke_ai_envelope(env["provider_id"], env, codebase)
            env["result"] = {**result, "completed_at": now_iso()}
            if result.get("skipped"):
                env["status"] = "skipped"
            elif result.get("success"):
                env["status"] = "completed"
                env["completed_at"] = now_iso()
            else:
                env["status"] = "failed"
                env["completed_at"] = now_iso()
            rec["status"] = env["status"]
            rec["result_ref"] = result.get("stdout_ref")
            materialized.append(rec)
            continue
        card_path = dqueue.write_queue_card(env, codebase)
        env["status"] = "dispatched"
        env["dispatched_at"] = now_iso()
        env["queue_ref"] = str(card_path.relative_to(REPO_ROOT))
        rec["queue_ref"] = env["queue_ref"]
        materialized.append(rec)
    log["last_execute_at"] = now_iso()
    save_dispatch_log(log)
    summary = {
        "decision_id": chain["decision_id"],
        "dry_run": dry_run,
        "mode": mode,
        "materialized": len(materialized),
        "items": materialized,
        "queue_dir": str(dqueue.dispatch_queue_dir().relative_to(REPO_ROOT)),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


def cmd_dispatch_next(args: argparse.Namespace) -> int:
    """IDE-native: print next actionable dispatch queue card (no API key)."""
    log = load_dispatch_log(args.decision_id)
    if not log:
        print(f"No dispatch log. Run: ulas dispatch plan && ulas dispatch execute --decision-id {args.decision_id}", file=sys.stderr)
        return 1
    target = None
    for env in log.get("envelopes", []):
        if env.get("status") in ("pending", "dispatched"):
            schema = env.get("invoke", {}).get("schema", "")
            if schema in ("ai_invoke", "manual_invoke"):
                target = env
                break
    if not target:
        print(json.dumps({"decision_id": args.decision_id, "next": None, "message": "no pending dispatch"}, indent=2))
        return 0
    queue_ref = target.get("queue_ref")
    if not queue_ref:
        wc_path, chain = load_work_chain(args.decision_id)
        if chain:
            codebase = resolve_codebase_path(chain)
            card = dqueue.write_queue_card(target, codebase)
            target["status"] = "dispatched"
            target["dispatched_at"] = now_iso()
            target["queue_ref"] = str(card.relative_to(REPO_ROOT))
            queue_ref = target["queue_ref"]
            idx, _ = find_dispatch_envelope(log, target["dispatch_id"])
            if idx >= 0:
                log["envelopes"][idx] = target
            save_dispatch_log(log)
    card_path = REPO_ROOT / queue_ref if queue_ref else None
    out = {
        "decision_id": args.decision_id,
        "dispatch_id": target["dispatch_id"],
        "work_package_id": target.get("work_package_id"),
        "capability_id": target.get("capability_id"),
        "provider_id": target.get("provider_id"),
        "status": target.get("status"),
        "queue_ref": queue_ref,
        "instruction": target.get("invoke", {}).get("instruction"),
        "acceptance": target.get("invoke", {}).get("acceptance"),
        "complete_command": (
            f"ulas dispatch complete --decision-id {args.decision_id} "
            f"--dispatch-id {target['dispatch_id']} --result success"
        ),
    }
    if getattr(args, "open", False) and card_path and card_path.is_file():
        out["card_preview"] = card_path.read_text(encoding="utf-8")[:4000]
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def cmd_dispatch_complete(args: argparse.Namespace) -> int:
    log = load_dispatch_log(args.decision_id)
    if not log:
        print(f"No dispatch log for {args.decision_id}", file=sys.stderr)
        return 1
    idx, env = find_dispatch_envelope(log, args.dispatch_id)
    if env is None or idx < 0:
        print(f"Dispatch id not found: {args.dispatch_id}", file=sys.stderr)
        return 1
    success = args.result == "success"
    transcript = getattr(args, "transcript", "") or ""
    transcript_path = Path(transcript) if transcript else None
    if transcript_path and not transcript_path.is_absolute():
        transcript_path = REPO_ROOT / transcript_path
    result_body = dqueue.write_complete_result(
        env,
        success=success,
        transcript_path=transcript_path if transcript_path and transcript_path.exists() else None,
        note=getattr(args, "note", "") or "",
    )
    env["status"] = "completed" if success else "failed"
    env["completed_at"] = now_iso()
    env["result"] = {**result_body, "completed_at": env["completed_at"]}
    log["envelopes"][idx] = env
    save_dispatch_log(log)
    wc_path, chain = load_work_chain(args.decision_id)
    if chain and wc_path:
        for wp in chain.get("work_packages", []):
            if wp.get("id") == env.get("work_package_id"):
                wp["status"] = "completed" if success else "failed"
                break
        _save(wc_path, chain)
    print(json.dumps({
        "decision_id": args.decision_id,
        "dispatch_id": args.dispatch_id,
        "status": env["status"],
        "work_package_id": env.get("work_package_id"),
        "result": env["result"],
    }, indent=2, ensure_ascii=False))
    return 0 if success else 1


def cmd_dispatch_reset(args: argparse.Namespace) -> int:
    """Reset skipped/failed AI dispatch envelopes to pending for IDE re-run."""
    log = load_dispatch_log(args.decision_id)
    if not log:
        print(f"No dispatch log for {args.decision_id}", file=sys.stderr)
        return 1
    only = getattr(args, "dispatch_id", "") or ""
    reset: list[str] = []
    for env in log.get("envelopes", []):
        if only and env.get("dispatch_id") != only:
            continue
        if env.get("status") in ("skipped", "failed", "dispatched"):
            env["status"] = "pending"
            env.pop("result", None)
            env.pop("completed_at", None)
            env.pop("dispatched_at", None)
            reset.append(env["dispatch_id"])
    save_dispatch_log(log)
    print(json.dumps({"decision_id": args.decision_id, "reset": reset, "count": len(reset)}, indent=2))
    return 0


def cmd_evidence_collect(args: argparse.Namespace) -> int:
    """Run bridge + failure report for venture."""
    venture = args.venture
    bridge = SVOS_ROOT / "scripts" / "bridge-venture.sh"
    if not bridge.is_file():
        print(f"Bridge not found: {bridge}", file=sys.stderr)
        return 1
    proc = subprocess.run(
        ["bash", str(bridge), venture],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=shell_env(),
    )
    vp = venture_path(venture)
    if not vp.exists():
        print(f"Venture not found: {venture}", file=sys.stderr)
        return 1
    meta = _load(vp)
    cr = meta.get("codebase_resolved") or meta.get("codebase_path", "")
    if not cr:
        print(f"codebase_path missing in {vp}", file=sys.stderr)
        return 1
    codebase = Path(cr) if Path(cr).is_absolute() else REPO_ROOT / cr
    coll = subprocess.run(
        [sys.executable, str(SVOS_ROOT / "scripts" / "collect-test-failures.py"), venture, "", str(codebase)],
        capture_output=True,
        text=True,
    )
    print(proc.stdout[-2000:] if proc.stdout else "")
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
    print(coll.stdout)
    return 0 if proc.returncode == 0 else proc.returncode


def sync_failure_report(venture: str, codebase: Path, log_path: Path | None = None) -> dict | None:
    """Refresh test-failure-report.json + manifest failed_tests from JUnit / gradle log."""
    script = SVOS_ROOT / "scripts" / "collect-test-failures.py"
    if not script.is_file():
        return None
    log_arg = str(log_path) if log_path and log_path.is_file() else ""
    proc = subprocess.run(
        [sys.executable, str(script), venture, log_arg, str(codebase)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def repair_next_action(decision_id: str) -> dict:
    log = load_dispatch_log(decision_id)
    pending = [
        e for e in (log or {}).get("envelopes", [])
        if e.get("status") in ("pending", "dispatched")
    ]
    return {
        "dispatch_next": f"ulas dispatch next --decision-id {decision_id}",
        "dispatch_complete": "ulas dispatch complete --decision-id ID --dispatch-id DID --result success",
        "re_verify": f"ulas execute run --decision-id {decision_id}",
        "pending_dispatches": len(pending),
        "hint": "IDE: open queue card from dispatch next, apply fixes, dispatch complete, then re-verify",
    }


def ensure_pending_dispatch_queued(chain: dict, codebase: Path) -> int:
    """Auto materialize queue cards for pending AI envelopes before verify."""
    log = load_dispatch_log(chain["decision_id"])
    if not log:
        return 0
    n = 0
    for env in log.get("envelopes", []):
        if env.get("status") != "pending":
            continue
        if env.get("invoke", {}).get("schema") not in ("ai_invoke", "manual_invoke"):
            continue
        card_path = dqueue.write_queue_card(env, codebase)
        env["status"] = "dispatched"
        env["dispatched_at"] = now_iso()
        env["queue_ref"] = str(card_path.relative_to(REPO_ROOT))
        n += 1
    if n:
        save_dispatch_log(log)
    return n


# --- Capability Memory v2 (cmem engine) ---


def load_knowledge_store(capability_id: str) -> dict:
    return cmem.load_store(capability_id)


def save_knowledge_store(capability_id: str, data: dict) -> Path:
    return cmem.save_store(capability_id, data)


def knowledge_store_path(capability_id: str) -> Path:
    return cmem.store_path(capability_id)


def memory_context_ref(capability_id: str, tier: int = 2) -> str:
    return cmem.memory_context_ref(capability_id, tier)


def query_capability_memory(capability_id: str, tier: int = 2) -> dict:
    return cmem.build_capability_context(capability_id, tier)


def detect_regressions(capability_id: str, failed_tags: list[str], venture_slug: str, decision_id: str) -> list[dict]:
    return cmem.detect_regressions(capability_id, failed_tags, venture_slug, decision_id)


def ingest_from_execution(decision_id: str) -> list[dict]:
    log_path = execution_log_path(decision_id)
    if not log_path.exists():
        return []
    elog = _load(log_path)
    _, chain = load_work_chain(decision_id)
    if not chain:
        return []
    venture = chain.get("venture_slug", "")
    created: list[dict] = []
    for attempt in elog.get("attempts", []):
        if attempt.get("verification_passed"):
            continue
        rp = attempt.get("repair_plan")
        if not rp:
            legacy = attempt.get("repair", {})
            if legacy:
                rp = {"plans": [{
                    "target_capability_id": legacy.get("capability_id", "android.architecture"),
                    "action": legacy.get("message", "repair"),
                    "failed_checks": attempt.get("triggered_by", []),
                    "failures": None,
                }]}
        if not rp:
            continue
        for plan in rp.get("plans", []):
            cap_id = plan.get("target_capability_id", "generic.architecture")
            failed = plan.get("failed_checks", [])
            failures = plan.get("failures")
            title = f"Verification fail: {', '.join(failed) or 'unknown'}"
            body = (
                f"Decision {decision_id} attempt {attempt.get('attempt')}: "
                f"checks failed {failed}. failures={failures}."
            )
            tags = list(failed)
            if failures is not None:
                tags.append(f"failures:{failures}")
            entry = cmem.append_antipattern(
                cap_id, title=title, body=body,
                source={"type": "execution", "venture_slug": venture, "decision_id": decision_id,
                        "ref": str(log_path.relative_to(REPO_ROOT))},
                tags=tags, severity="high", venture_slug=venture,
            )
            created.append(entry)
    return created


def cmd_memory_stats(args: argparse.Namespace) -> int:
    report = cmem.quality_report()
    caps = [{
        "capability_id": c["capability_id"],
        "memory_quality": c.get("memory_quality"),
        "proven_patterns": c.get("proven_patterns", 0),
        "active_antipatterns": c.get("active_antipatterns", 0),
        "playbooks": c.get("playbook_count", 0),
        "benchmarks": c.get("benchmark_count", 0),
    } for c in report["capabilities"]]
    print(json.dumps({"capabilities": caps, "count": len(caps)}, indent=2))
    return 0


def cmd_memory_query(args: argparse.Namespace) -> int:
    tier = int(getattr(args, "tier", 2))
    print(json.dumps(cmem.build_capability_context(args.capability, tier), indent=2, ensure_ascii=False))
    return 0


def cmd_memory_ingest(args: argparse.Namespace) -> int:
    created: list[dict] = []
    if args.from_source == "execution":
        if not args.decision_id:
            print("--decision-id required", file=sys.stderr)
            return 1
        created = ingest_from_execution(args.decision_id)
    elif args.from_source == "evidence":
        if not args.venture:
            print("--venture required for evidence ingest", file=sys.stderr)
            return 1
        venture = args.venture
        created = cmem.ingest_from_evidence(venture)
    elif args.from_source == "manual":
        layer = getattr(args, "layer", "knowledge") or "knowledge"
        if not args.capability or not args.title:
            print("--capability and --title required", file=sys.stderr)
            return 1
        if layer == "antipattern":
            created = [cmem.append_antipattern(
                args.capability, title=args.title, body=args.body or args.title,
                source={"type": "manual", "ref": "cli"},
                tags=args.tags.split(",") if getattr(args, "tags", None) else [],
                severity=getattr(args, "severity", "medium") or "medium",
            )]
        else:
            created = [cmem.append_knowledge(
                args.capability, kind=getattr(args, "kind", "pattern") or "pattern",
                title=args.title, body=args.body or args.title,
                source={"type": "manual", "ref": "cli"},
                tags=args.tags.split(",") if getattr(args, "tags", None) else [],
            )]
    else:
        print(f"ingest --from {args.from_source}: use execution|evidence|manual", file=sys.stderr)
        return 1
    print(json.dumps({"ingested": len(created), "entries": created}, indent=2, ensure_ascii=False))
    return 0


def cmd_memory_promote(args: argparse.Namespace) -> int:
    store = cmem.load_store(args.capability)
    entry = None
    layer = "knowledge"
    for e in store.get("knowledge", {}).get("entries", []):
        if e.get("id") == args.entry:
            entry, layer = e, "knowledge"
            break
    if not entry:
        for e in store.get("antipatterns", {}).get("entries", []):
            if e.get("id") == args.entry:
                entry, layer = e, "antipattern"
                break
    if not entry:
        print(f"Entry not found: {args.entry}", file=sys.stderr)
        return 1
    entry["status"] = "proven"
    entry["promoted_at"] = now_iso()
    cmem.save_store(args.capability, store)
    print(json.dumps({"promoted": args.entry, "layer": layer, "capability": args.capability}, indent=2))
    return 0


def cmd_memory_compress(args: argparse.Namespace) -> int:
    store = cmem.compress_store(cmem.load_store(args.capability))
    path = cmem.save_store(args.capability, store)
    print(json.dumps({"capability": args.capability, "path": str(path.relative_to(REPO_ROOT))}, indent=2))
    return 0


def cmd_memory_health(args: argparse.Namespace) -> int:
    store = cmem.load_store(args.capability)
    print(json.dumps(store.get("health", cmem.compute_health(store)), indent=2))
    return 0


def cmd_memory_quality_report(args: argparse.Namespace) -> int:
    report = cmem.quality_report()
    out = SVOS_ROOT / "10-runtime" / "capability-memory" / "MEMORY_QUALITY_REPORT.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    _save(out, report)
    md_path = MEMORY_ROOT / "MEMORY_QUALITY_REPORT.md"
    lines = ["# Memory Quality Report", "", f"Generated: {report['generated_at']}", ""]
    for c in report["capabilities"]:
        lines.append(f"## {c['capability_id']}")
        lines.append(f"- memory_quality: **{c.get('memory_quality')}**")
        lines.append(f"- proven_patterns: {c.get('proven_patterns', 0)}")
        lines.append(f"- active_antipatterns: {c.get('active_antipatterns', 0)}")
        lines.append(f"- playbooks: {c.get('playbook_count', 0)}")
        lines.append(f"- benchmarks: {c.get('benchmark_count', 0)}")
        lines.append(f"- trend: {c.get('trend')}")
        lines.append(f"- last_regression: {c.get('last_regression')}")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"json": str(out.relative_to(REPO_ROOT)), "md": str(md_path.relative_to(REPO_ROOT))}, indent=2))
    if getattr(args, "verbose", False):
        print(json.dumps(report, indent=2))
    return 0


def cmd_memory_migrate(args: argparse.Namespace) -> int:
    n = cmem.migrate_all()
    print(json.dumps({"migrated": n}, indent=2))
    return 0


def cmd_memory_test_regression(args: argparse.Namespace) -> int:
    result = cmem.test_regression_scenario(args.capability, args.tag)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


def cmd_memory_utilization(args: argparse.Namespace) -> int:
    cap = args.capability or None
    report = cmem.utilization_audit(cap)
    out_path = SVOS_ROOT / "10-runtime" / "capability-memory" / "MEMORY_UTILIZATION_REPORT.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _save(out_path, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if getattr(args, "verbose", False):
        print(f"\nWrote {out_path.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


MEMORY_ROOT = cmem.MEMORY_ROOT


# --- Execution Engine (reads routing_manifest; no hardcoded role→provider) ---


def execution_runtime_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "execution"
    d.mkdir(parents=True, exist_ok=True)
    return d


def execution_log_path(decision_id: str) -> Path:
    return execution_runtime_dir() / f"{decision_id}.json"


def execution_logs_dir() -> Path:
    d = execution_runtime_dir() / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def resolve_codebase_path(chain: dict) -> Path:
    em = chain.get("execution_manifest", {})
    raw = em.get("codebase_resolved") or em.get("codebase_path") or chain.get("codebase_path") or ""
    if not raw:
        venture = load_venture_record(chain.get("venture_slug", ""))
        raw = venture.get("codebase_resolved") or venture.get("codebase_path") or ""
    if not raw:
        raise FileNotFoundError(
            f"No codebase_path for venture '{chain.get('venture_slug', '')}' — run init-venture.sh"
        )
    p = Path(raw)
    if not p.is_absolute():
        p = REPO_ROOT / raw
    return p.resolve()


def provider_for_capability(chain: dict, role: str) -> str:
    """Resolve provider via routing manifest — policy swap changes result, not code."""
    rm = ensure_routing_manifest(chain)
    for b in rm.get("bindings", []):
        if b.get("role") == role:
            return b["provider_id"]
    policy = load_routing_policy()
    cap_id = resolve_capability_id(role, chain.get("platform", "android"))
    return select_provider_for_capability(cap_id, load_capability_registry(), policy)[0]


def invoke_ai_envelope(provider_id: str, envelope: dict, codebase: Path) -> dict:
    """AI dispatch — adapter swap via provider-registry.json."""
    prov_reg = load_provider_registry()
    provider = prov_reg.get("providers", {}).get(provider_id, {})
    adapter_rel = provider.get("adapter")
    if provider.get("wired") and adapter_rel:
        try:
            mod = aload.load_adapter(adapter_rel)
            return mod.handle_ai_invoke(envelope, codebase)
        except (FileNotFoundError, ImportError, AttributeError) as exc:
            return {
                "provider": provider_id,
                "success": False,
                "skipped": True,
                "reason": f"adapter load failed: {exc}",
            }
    ptype = provider.get("type", "ai_ide")
    return {
        "provider": provider_id,
        "skipped": True,
        "reason": f"provider type {ptype} not wired — ulas dispatch execute (queue) or configure adapter",
        "wired": provider.get("wired", False),
    }


def invoke_provider(provider_id: str, invoke: dict, codebase: Path) -> dict:
    """Single dispatch entry — execution engine never names Cursor/Claude directly."""
    prov_reg = load_provider_registry()
    provider = prov_reg.get("providers", {}).get(provider_id, prov_reg["providers"]["human"])
    ptype = provider.get("type", "manual")

    if ptype == "local_shell":
        return run_local_shell(invoke.get("cmd", ""), codebase, int(invoke.get("timeout_sec", 600)))

    if ptype == "manual":
        return {
            "provider": provider_id,
            "skipped": True,
            "reason": "manual capability — dispatch to human",
        }

    return {
        "provider": provider_id,
        "skipped": True,
        "reason": f"provider type {ptype} not wired",
        "wired": provider.get("wired", False),
    }


def shell_env() -> dict[str, str]:
    """Prefer JDK 21 (Robolectric SDK 36), then 17 — match bridge-venture.sh."""
    env = os.environ.copy()
    if env.get("JAVA_HOME"):
        return env
    candidates = [
        Path("/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"),
        Path("/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"),
        Path("/usr/local/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"),
        Path("/usr/local/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"),
    ]
    for candidate in candidates:
        if candidate.is_dir():
            env["JAVA_HOME"] = str(candidate)
            env["PATH"] = f"{candidate}/bin:{env.get('PATH', '')}"
            break
    return env


def run_local_shell(cmd: str, cwd: Path, timeout_sec: int = 600) -> dict:
    log_file = execution_logs_dir() / f"{cwd.name}-{now_iso().replace(':', '')}.log"
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=shell_env(),
        )
        log_file.write_text((proc.stdout or "") + (proc.stderr or ""), encoding="utf-8")
        return {
            "provider": "local_shell",
            "exit_code": proc.returncode,
            "success": proc.returncode == 0,
            "stdout_ref": str(log_file.relative_to(REPO_ROOT)),
            "stdout_tail": (proc.stdout or "")[-2000:],
            "stderr_tail": (proc.stderr or "")[-1000:],
        }
    except subprocess.TimeoutExpired:
        return {
            "provider": "local_shell",
            "exit_code": -1,
            "success": False,
            "error": f"timeout after {timeout_sec}s",
        }


def parse_gradle_test_failures(output: str) -> int | None:
    summary = gtp.parse_gradle_summary(output)
    return summary["failed"] if summary else None


def enrich_test_check_result(run: dict, codebase: Path) -> tuple[int | None, list[dict]]:
    text = gtp.read_log_text(run, REPO_ROOT)
    summary = gtp.parse_gradle_summary(text)
    failures = gtp.parse_failed_from_gradle_log(text)
    if not failures:
        failures = gtp.collect_junit_failures(codebase)
    count = summary["failed"] if summary else None
    if count is None and failures:
        count = len(failures)
    return count, failures


def run_execution_commands(chain: dict, codebase: Path) -> list[dict]:
    results: list[dict] = []
    for spec in chain.get("execution_manifest", {}).get("commands", []):
        provider_id = spec.get("provider")
        if not provider_id:
            cap_id = spec.get("capability_id")
            if cap_id:
                b = binding_for_capability(chain, cap_id)
                provider_id = b["provider_id"] if b else "local_shell"
            else:
                provider_id = "local_shell"
        prov_reg = load_provider_registry()
        provider = prov_reg.get("providers", {}).get(provider_id, {})
        if provider.get("type") != "local_shell":
            results.append({
                "id": spec.get("id"),
                "provider": provider_id,
                "skipped": True,
                "reason": "execution manifest command requires local_shell provider",
            })
            continue
        cwd_raw = spec.get("cwd") or str(codebase.relative_to(REPO_ROOT))
        cwd = REPO_ROOT / cwd_raw if not Path(cwd_raw).is_absolute() else Path(cwd_raw)
        timeout = int(spec.get("timeout_sec", 600))
        result = invoke_provider(provider_id, {"cmd": spec["cmd"], "timeout_sec": timeout}, cwd.resolve())
        result["id"] = spec.get("id")
        results.append(result)
    return results


def run_verification_check(check: dict, chain: dict, codebase: Path) -> dict:
    check_id = check.get("id", "?")
    optional = bool(check.get("optional"))
    expect = check.get("expect")
    ctype = check.get("type")

    if ctype == "gradle":
        task = check.get("task", "")
        gradle_cmd = f"./gradlew :app:{task}"
        if "test" in task.lower():
            gradle_cmd += " --no-daemon"
        run = run_local_shell(gradle_cmd, codebase, 900)
        fail_count, failed_tests = enrich_test_check_result(run, codebase)
        if fail_count is None and run["success"]:
            fail_count = 0
        if isinstance(expect, str) and expect == "success":
            ok = run["success"]
        elif isinstance(expect, dict) and "failures" in expect:
            ok = fail_count is not None and fail_count <= int(expect["failures"])
        else:
            ok = run["success"]
        result = {
            "id": check_id,
            "type": ctype,
            "optional": optional,
            "passed": ok,
            "failures": fail_count,
            "run": run,
        }
        if failed_tests:
            result["failed_tests"] = [f["test"] for f in failed_tests]
            result["failure_details"] = failed_tests[:20]
        return result

    if ctype == "script":
        cmd = check.get("cmd", "")
        run = run_local_shell(cmd, codebase, 300)
        ok = run["success"] if expect == "success" else run["success"]
        return {"id": check_id, "type": ctype, "optional": optional, "passed": ok, "run": run}

    if ctype == "json_field":
        venture = chain.get("venture_slug", "")
        evidence = load_evidence_manifest(venture) or {}
        field = check.get("field", "")
        value: Any = evidence
        for part in field.split("."):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break
        ok = value == expect
        return {
            "id": check_id,
            "type": ctype,
            "optional": optional,
            "passed": ok,
            "field": field,
            "value": value,
            "expect": expect,
        }

    if ctype == "file_exists":
        target = codebase / check.get("path", "")
        ok = target.exists()
        return {"id": check_id, "type": ctype, "optional": optional, "passed": ok, "path": str(target)}

    return {"id": check_id, "optional": optional, "passed": False, "error": f"unknown check type: {ctype}"}


def run_verification_manifest(chain: dict, codebase: Path) -> tuple[bool, list[dict]]:
    checks_out: list[dict] = []
    all_required_pass = True
    for check in chain.get("verification_manifest", {}).get("checks", []):
        result = run_verification_check(check, chain, codebase)
        checks_out.append(result)
        if not result.get("optional") and not result.get("passed"):
            all_required_pass = False
    return all_required_pass, checks_out


def run_bridge(chain: dict) -> dict:
    em = chain.get("evidence_manifest", {})
    bridge = em.get("update_via") or chain.get("execution_manifest", {}).get("bridge")
    venture = chain.get("venture_slug", "")
    if not bridge:
        return {"skipped": True, "reason": "no bridge configured"}
    bridge_path = REPO_ROOT / bridge if not Path(bridge).is_absolute() else Path(bridge)
    if not bridge_path.exists():
        return {"skipped": True, "reason": f"bridge not found: {bridge}"}
    run = run_local_shell(f"bash {bridge_path} {venture}", REPO_ROOT, 1200)
    return {"bridge": str(bridge_path.relative_to(REPO_ROOT)), "venture": venture, **run}


def _set_wp_status(chain: dict, capability: str, status: str) -> None:
    for wp in chain.get("work_packages", []):
        if wp.get("capability") == capability and wp.get("status") != "done":
            wp["status"] = status


def _mark_automated_wps(chain: dict, verify_ok: bool) -> None:
    if verify_ok:
        _set_wp_status(chain, "qa", "done")
        _set_wp_status(chain, "auditor", "done")
    else:
        _set_wp_status(chain, "architect", "repair_needed")


def load_work_chain(decision_id: str) -> tuple[Path | None, dict | None]:
    out = work_chain_path(decision_id)
    if not out.exists():
        alt = find_decision(decision_id)
        if alt:
            rec = _load(alt)
            did = rec.get("decision_id", decision_id)
            out = work_chain_path(did)
    if not out.exists():
        return None, None
    return out, _load(out)


def cmd_execute_verify(args: argparse.Namespace) -> int:
    path, chain = load_work_chain(args.decision_id)
    if not chain:
        print(f"No work chain for {args.decision_id}", file=sys.stderr)
        return 1
    codebase = resolve_codebase_path(chain)
    if not codebase.is_dir():
        print(f"Codebase not found: {codebase}", file=sys.stderr)
        return 1
    ok, checks = run_verification_manifest(chain, codebase)
    print(json.dumps({
        "decision_id": chain.get("decision_id"),
        "codebase": str(codebase.relative_to(REPO_ROOT)),
        "verification_passed": ok,
        "checks": checks,
    }, indent=2, ensure_ascii=False))
    return 0 if ok else 1


def cmd_execute_status(args: argparse.Namespace) -> int:
    log_path = execution_log_path(args.decision_id)
    if not log_path.exists():
        print(f"No execution log for {args.decision_id}", file=sys.stderr)
        return 1
    print(json.dumps(_load(log_path), indent=2, ensure_ascii=False))
    return 0


def cmd_execute_run(args: argparse.Namespace) -> int:
    wc_path, chain = load_work_chain(args.decision_id)
    if not chain or not wc_path:
        print(f"No work chain for {args.decision_id}. Run: ulas work generate --decision-id ID", file=sys.stderr)
        return 1
    if chain.get("decision_status") != "APPROVED":
        print(f"Decision not APPROVED ({chain.get('decision_status')})", file=sys.stderr)
        return 1

    codebase = resolve_codebase_path(chain)
    if not codebase.is_dir():
        print(f"Codebase not found: {codebase}", file=sys.stderr)
        return 1

    rm = ensure_routing_manifest(chain)
    _save(wc_path, chain)
    ensure_dispatch_log(chain)
    queued = ensure_pending_dispatch_queued(chain, codebase)
    if queued:
        print(f"Auto-queued {queued} dispatch card(s) for IDE", file=sys.stderr)

    vm = chain.get("verification_manifest", {})
    retry = vm.get("retry_policy", {})
    max_attempts = int(retry.get("max_attempts", 3))
    decision_id = chain["decision_id"]

    log_path = execution_log_path(decision_id)
    log: dict = _load(log_path) if log_path.exists() else {
        "decision_id": decision_id,
        "work_id": chain.get("work_id"),
        "started_at": now_iso(),
        "attempts": [],
        "state": "executing",
    }

    chain["state"] = "executing"
    _save(wc_path, chain)

    skip_commands = getattr(args, "skip_commands", False)
    final_ok = False
    prior_attempts = len(log.get("attempts", []))

    for offset in range(max_attempts):
        attempt = prior_attempts + offset + 1
        attempt_rec: dict = {
            "attempt": attempt,
            "started_at": now_iso(),
            "execution_results": [],
            "verification_results": [],
            "bridge": None,
        }

        if not skip_commands:
            attempt_rec["execution_results"] = run_execution_commands(chain, codebase)

        verify_ok, checks = run_verification_manifest(chain, codebase)
        attempt_rec["verification_results"] = checks
        attempt_rec["verification_passed"] = verify_ok
        attempt_rec["ended_at"] = now_iso()

        if verify_ok:
            attempt_rec["bridge"] = run_bridge(chain)
            _mark_automated_wps(chain, True)
            chain["state"] = "verified"
            log["state"] = "verified"
            log["completed_at"] = now_iso()
            final_ok = True
            log["attempts"].append(attempt_rec)
            break

        _mark_automated_wps(chain, False)
        attempt_rec["repair_plan"] = build_repair_plan(checks, chain, attempt)
        sync_failure_report(chain.get("venture_slug", ""), codebase)
        failed_tags = [
            c.get("id", "") for c in checks
            if not c.get("optional") and not c.get("passed")
        ]
        repair_cap_id = resolve_capability_id(
            retry.get("repair_capability", "architect"),
            chain.get("platform", "android"),
        )
        failed_test_tags: list[str] = []
        for c in checks:
            if c.get("id") == "tests_zero_fail":
                failed_test_tags = c.get("failed_tests", [])
        detect_regressions(
            repair_cap_id, failed_test_tags or failed_tags,
            chain.get("venture_slug", ""), decision_id,
        )
        repair_binding = binding_for_capability(chain, repair_cap_id)
        attempt_rec["repair"] = attempt_rec["repair_plan"]["plans"][0] if attempt_rec["repair_plan"]["plans"] else {
            "capability_id": repair_cap_id,
            "provider_id": repair_binding["provider_id"] if repair_binding else "human",
        }
        chain["state"] = "repair" if offset + 1 < max_attempts else "failed"
        log["state"] = chain["state"]
        log["attempts"].append(attempt_rec)

        if offset + 1 >= max_attempts:
            log["completed_at"] = now_iso()
            break

    _save(wc_path, chain)
    _save(log_path, log)

    last_failed_tags: list[str] = []
    if log.get("attempts"):
        last = log["attempts"][-1]
        last_failed_tags = [
            c.get("id", "") for c in last.get("verification_results", [])
            if not c.get("optional") and not c.get("passed")
        ]
    record_chain_memory_impact(chain, "success" if final_ok else "failure", last_failed_tags)

    # Sync decision record work state
    dec_path, dec_rec = load_decision_record(decision_id)
    if dec_path and dec_rec:
        dec_rec.setdefault("work", {})["state"] = chain["state"]
        dec_rec["work"]["last_execution_at"] = now_iso()
        _save(dec_path, dec_rec)

    summary = {
        "decision_id": decision_id,
        "state": chain["state"],
        "attempts": len(log["attempts"]),
        "verification_passed": final_ok,
        "execution_log": str(log_path.relative_to(REPO_ROOT)),
        "routing_policy": rm.get("policy_source"),
        "capabilities_needed": rm.get("capabilities_needed", []),
        "manual_bindings": [
            {"capability_id": b["capability_id"], "label": b.get("label"), "provider_id": b["provider_id"]}
            for b in manual_bindings(chain)
        ],
    }
    if not final_ok and chain["state"] in ("repair", "failed"):
        summary["next_action"] = repair_next_action(decision_id)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if getattr(args, "verbose", False):
        print(json.dumps(log, indent=2, ensure_ascii=False))
    return 0 if final_ok else 1


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
    p_cal.add_argument("--decision-id", required=True, help="Decision that triggered calibration")
    p_cal.add_argument("--reason", default="", help="Why trust changed")
    p_cal.add_argument("--evidence", default="", help="Supporting evidence note")

    p_route = sub.add_parser("route", help="Show routing for decision class")
    p_route.add_argument("--class", dest="class_", default="B")

    p_out = sub.add_parser("outcome", help="Record decision outcome for effectiveness")
    p_out.add_argument("--decision-id", required=True)
    p_out.add_argument("--result", choices=list(OUTCOME_CHOICES), required=True)
    p_out.add_argument("--note", default="")
    p_out.add_argument("--propagate", action="store_true", help="Auto-propagate feedback after outcome")
    p_out.add_argument("--apply-memory", action="store_true", help="With --propagate: append NEVER_AGAIN candidate")

    p_prop = sub.add_parser("propagate", help="Propagate outcome → trust/policy/memory adaptations")
    p_prop.add_argument("--decision-id", required=True)
    p_prop.add_argument("--dry-run", action="store_true", help="Plan only, do not apply")
    p_prop.add_argument("--apply-memory", action="store_true", help="Append NEVER_AGAIN candidate to registry")

    p_pa = sub.add_parser("propagation-audit", help="Phase 5 — where feedback terminates")
    p_pa.add_argument("--json", action="store_true")

    p_work = sub.add_parser("work", help="Work Engine — packages & manifests")
    work_sub = p_work.add_subparsers(dest="work_command", required=True)
    p_wg = work_sub.add_parser("generate", help="Decision → work packages + manifests")
    p_wg.add_argument("--decision-id", required=True)
    p_wg.add_argument("--verbose", action="store_true")
    p_ws = work_sub.add_parser("show", help="Show work chain JSON")
    p_ws.add_argument("--decision-id", required=True)
    work_sub.add_parser("list", help="List work chains")

    p_exec = sub.add_parser("execute", help="Execution Engine — verify/repair/evidence loop")
    exec_sub = p_exec.add_subparsers(dest="execute_command", required=True)
    p_er = exec_sub.add_parser("run", help="Run execution + verification + repair + bridge")
    p_er.add_argument("--decision-id", required=True)
    p_er.add_argument("--skip-commands", action="store_true", help="Skip execution manifest; verify only")
    p_er.add_argument("--verbose", action="store_true")
    p_ev = exec_sub.add_parser("verify", help="Verification manifest only")
    p_ev.add_argument("--decision-id", required=True)
    p_es = exec_sub.add_parser("status", help="Show execution log")
    p_es.add_argument("--decision-id", required=True)

    p_cap = sub.add_parser("capability", help="Capability Router — capability→provider matching")
    cap_sub = p_cap.add_subparsers(dest="capability_command", required=True)
    p_cr = cap_sub.add_parser("route", help="Bind work packages to capability IDs + providers")
    p_cr.add_argument("--decision-id", required=True)
    p_cr.add_argument("--verbose", action="store_true")
    p_cs = cap_sub.add_parser("show", help="Show capabilities needed and provider bindings")
    p_cs.add_argument("--decision-id", required=True)
    p_cs.add_argument("--json", action="store_true")
    cap_sub.add_parser("policy", help="Show effective routing policy (incl. runtime overrides)")

    p_disp = sub.add_parser("dispatch", help="Provider Dispatch — contract envelopes")
    disp_sub = p_disp.add_subparsers(dest="dispatch_command", required=True)
    p_dp = disp_sub.add_parser("plan", help="Build dispatch envelopes for delegated bindings")
    p_dp.add_argument("--decision-id", required=True)
    p_dp.add_argument("--verbose", action="store_true")
    p_dl = disp_sub.add_parser("log", help="Show dispatch runtime log")
    p_dl.add_argument("--decision-id", required=True)
    p_da = disp_sub.add_parser("audit", help="Provider Dispatch Adapter readiness audit")
    p_da.add_argument("--verbose", action="store_true")
    p_de = disp_sub.add_parser("execute", help="Materialize pending AI/manual dispatch queue cards")
    p_de.add_argument("--decision-id", required=True)
    p_de.add_argument("--dry-run", action="store_true")
    p_de.add_argument("--mode", choices=["queue", "sdk"], default="queue", help="queue=file cards (v0); sdk=Cursor adapter (v1)")
    p_de.add_argument("--dispatch-id", default="", help="SDK/queue: single envelope only")
    p_dc = disp_sub.add_parser("complete", help="Mark dispatch envelope completed after provider work")
    p_dc.add_argument("--decision-id", required=True)
    p_dc.add_argument("--dispatch-id", required=True)
    p_dc.add_argument("--result", choices=["success", "failed"], required=True)
    p_dc.add_argument("--transcript", default="", help="Optional transcript file path")
    p_dc.add_argument("--note", default="", help="Completion note")
    p_dn = disp_sub.add_parser("next", help="IDE: next pending dispatch task (no API key)")
    p_dn.add_argument("--decision-id", required=True)
    p_dn.add_argument("--open", action="store_true", help="Include queue card preview in JSON")
    p_dr = disp_sub.add_parser("reset", help="Reset skipped/failed dispatch envelopes to pending")
    p_dr.add_argument("--decision-id", required=True)
    p_dr.add_argument("--dispatch-id", default="", help="Single envelope only")

    p_ev = sub.add_parser("evidence", help="Venture evidence collection")
    ev_sub = p_ev.add_subparsers(dest="evidence_command", required=True)
    p_ec = ev_sub.add_parser("collect", help="bridge-venture + test failure report")
    p_ec.add_argument("--venture", required=True)

    p_mem = sub.add_parser("memory", help="Capability Memory — operational knowledge per capability")
    mem_sub = p_mem.add_subparsers(dest="memory_command", required=True)
    mem_sub.add_parser("stats", help="Capability memory statistics")
    p_mq = mem_sub.add_parser("query", help="Query capability knowledge (tiered)")
    p_mq.add_argument("--capability", required=True)
    p_mq.add_argument("--tier", type=int, default=2, choices=[1, 2, 3])
    p_mi = mem_sub.add_parser("ingest", help="Ingest into capability memory")
    p_mi.add_argument("--from", dest="from_source", required=True, choices=["execution", "outcome", "postmortem", "evidence", "manual"])
    p_mi.add_argument("--decision-id", default="")
    p_mi.add_argument("--venture", default="")
    p_mi.add_argument("--capability", default="")
    p_mi.add_argument("--title", default="")
    p_mi.add_argument("--body", default="")
    p_mi.add_argument("--kind", default="pattern")
    p_mi.add_argument("--layer", default="knowledge", choices=["knowledge", "antipattern"])
    p_mi.add_argument("--severity", default="medium")
    p_mi.add_argument("--tags", default="")
    p_mp = mem_sub.add_parser("promote", help="Promote entry experimental → proven")
    p_mp.add_argument("--capability", required=True)
    p_mp.add_argument("--entry", required=True)
    p_mp.add_argument("--force", action="store_true")
    p_mc = mem_sub.add_parser("compress", help="Compress capability knowledge tiers")
    p_mc.add_argument("--capability", required=True)
    p_mh = mem_sub.add_parser("health", help="Capability memory health (not trust score)")
    p_mh.add_argument("--capability", required=True)
    p_mqr = mem_sub.add_parser("quality-report", help="Write MEMORY_QUALITY_REPORT")
    p_mqr.add_argument("--verbose", action="store_true")
    mem_sub.add_parser("migrate", help="Migrate all stores to schema v2")
    p_mtr = mem_sub.add_parser("test-regression", help="Simulate regression detection")
    p_mtr.add_argument("--capability", required=True)
    p_mtr.add_argument("--tag", required=True)
    p_mu = mem_sub.add_parser("utilization", help="Memory Utilization Audit — used vs dead knowledge")
    p_mu.add_argument("--capability", default="")
    p_mu.add_argument("--verbose", action="store_true")

    sub.add_parser("metrics", help="Rebuild and print effectiveness metrics JSON")
    p_mat = sub.add_parser("maturity", help="SVOS olgunluk denetimi (README tablosu)")
    mat_sub = p_mat.add_subparsers(dest="maturity_command", required=True)
    p_ma = mat_sub.add_parser("audit", help="Tüm boyutları skorla + gap listesi")
    p_ma.add_argument("--json", action="store_true")

    sub.add_parser("report", help="Human-readable effectiveness report")
    sub.add_parser("audit", help="Print ULAS component audit")
    p_fb = sub.add_parser("feedback-audit", help="Phase 4 self-improvement & loop closure audit")
    p_fb.add_argument("--json", action="store_true", help="Also print JSON report")

    p_risk = sub.add_parser("risk", help="Phase 6 — predictive risk preview (always available)")
    p_risk.add_argument("--venture", required=True)
    p_risk.add_argument("--class", dest="class_", default="B")
    p_risk.add_argument("--title", default="")
    p_risk.add_argument("--proposal", default="")
    p_risk.add_argument("--reviewers", required=True)

    p_rg = sub.add_parser("risk-gate", help="Phase 6 — evidence activation gate status")
    p_rg.add_argument("--json", action="store_true")

    p_or = sub.add_parser("overrides-reset", help="Reset runtime policy adaptations (P1)")
    p_or.add_argument("--reason", default="adaptation reset")

    args = parser.parse_args()

    if args.command == "maturity":
        return cmd_maturity_audit(args)

    if args.command == "work":
        work_handlers = {
            "generate": cmd_work_generate,
            "show": cmd_work_show,
            "list": cmd_work_list,
        }
        return work_handlers[args.work_command](args)

    if args.command == "execute":
        exec_handlers = {
            "run": cmd_execute_run,
            "verify": cmd_execute_verify,
            "status": cmd_execute_status,
        }
        return exec_handlers[args.execute_command](args)

    if args.command == "capability":
        cap_handlers = {
            "route": cmd_capability_route,
            "show": cmd_capability_show,
            "policy": cmd_capability_policy,
        }
        return cap_handlers[args.capability_command](args)

    if args.command == "dispatch":
        disp_handlers = {
            "plan": cmd_dispatch_plan,
            "log": cmd_dispatch_log,
            "audit": cmd_dispatch_audit,
            "execute": cmd_dispatch_execute,
            "complete": cmd_dispatch_complete,
            "next": cmd_dispatch_next,
            "reset": cmd_dispatch_reset,
        }
        return disp_handlers[args.dispatch_command](args)

    if args.command == "evidence":
        ev_handlers = {"collect": cmd_evidence_collect}
        return ev_handlers[args.evidence_command](args)

    if args.command == "memory":
        mem_handlers = {
            "stats": cmd_memory_stats,
            "query": cmd_memory_query,
            "ingest": cmd_memory_ingest,
            "promote": cmd_memory_promote,
            "compress": cmd_memory_compress,
            "health": cmd_memory_health,
            "quality-report": cmd_memory_quality_report,
            "migrate": cmd_memory_migrate,
            "test-regression": cmd_memory_test_regression,
            "utilization": cmd_memory_utilization,
        }
        return mem_handlers[args.memory_command](args)

    handlers = {
        "decide": cmd_decide,
        "assemble": cmd_assemble,
        "calibrate": cmd_calibrate,
        "route": cmd_route,
        "outcome": cmd_outcome,
        "propagate": cmd_propagate,
        "propagation-audit": cmd_propagation_audit,
        "overrides-reset": cmd_overrides_reset,
        "risk": cmd_risk,
        "risk-gate": cmd_risk_gate,
        "metrics": cmd_metrics,
        "report": cmd_report,
        "audit": cmd_audit,
        "feedback-audit": cmd_feedback_audit,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
