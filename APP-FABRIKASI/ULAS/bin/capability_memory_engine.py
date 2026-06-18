"""Capability Memory v2 — knowledge, antipatterns, playbooks, benchmarks."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ULAS_ROOT = Path(__file__).resolve().parent.parent
SVOS_ROOT = ULAS_ROOT.parent
REPO_ROOT = SVOS_ROOT.parent
MEMORY_ROOT = ULAS_ROOT / "capability-memory"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_memory_index() -> dict:
    return _load(MEMORY_ROOT / "index.json")


def store_path(capability_id: str) -> Path:
    idx = load_memory_index()
    cap = idx.get("capabilities", {}).get(capability_id)
    if cap and cap.get("file"):
        return MEMORY_ROOT / "knowledge" / cap["file"]
    return MEMORY_ROOT / "knowledge" / f"{capability_id}.json"


def empty_store(capability_id: str) -> dict:
    label = load_memory_index().get("capabilities", {}).get(capability_id, {}).get("label", capability_id)
    return {
        "capability_id": capability_id,
        "label": label,
        "schema_version": "2.0",
        "updated_at": None,
        "knowledge": {"entries": []},
        "antipatterns": {"entries": []},
        "playbooks": {"entries": []},
        "benchmarks": {"entries": []},
        "regression_signals": [],
        "compression_profile": {"tier1_max_tokens": 200, "tier2_max_tokens": 800, "max_tier2_items": 40},
        "health": {},
    }


def migrate_v1_to_v2(data: dict) -> dict:
    if data.get("schema_version") == "2.0":
        return data
    cap_id = data.get("capability_id", "unknown")
    store = empty_store(cap_id)
    store["label"] = data.get("label", cap_id)
    store["regression_signals"] = data.get("regression_signals", [])
    store["compression_profile"] = data.get("compression_profile", store["compression_profile"])
    for entry in data.get("entries", []):
        kind = entry.get("kind", "")
        if kind in ("anti_pattern", "failure_mode"):
            ap = _legacy_to_antipattern(entry, cap_id)
            store["antipatterns"]["entries"].append(ap)
        else:
            store["knowledge"]["entries"].append(entry)
    return store


def _legacy_to_antipattern(entry: dict, cap_id: str) -> dict:
    n = len(entry.get("id", "0").split("-")[-1]) if entry.get("id") else 1
    try:
        num = int(re.sub(r"\D", "", entry.get("id", "1")) or "1")
    except ValueError:
        num = 1
    return {
        "id": f"{cap_id}.{num:03d}",
        "title": entry.get("title", "Untitled"),
        "status": entry.get("status", "experimental"),
        "severity": "high" if entry.get("regression_watch") else "medium",
        "body": entry.get("body", ""),
        "body_compressed": entry.get("body_compressed", ""),
        "evidence_count": 1,
        "source": entry.get("source", {}),
        "tags": entry.get("tags", []),
        "regression_watch": True,
    }


def load_store(capability_id: str) -> dict:
    path = store_path(capability_id)
    if not path.exists():
        store = empty_store(capability_id)
        save_store(capability_id, store)
        return store
    data = _load(path)
    dirty = False
    if data.get("schema_version") != "2.0" or "entries" in data:
        data = migrate_v1_to_v2(data)
        dirty = True
    before = json.dumps(data.get("antipatterns", {}), sort_keys=True)
    if dirty:
        save_store(capability_id, data)
    return data


def compress_text(body: str, max_words: int = 80) -> str:
    words = body.split()
    if len(words) <= max_words:
        return body.strip()
    return " ".join(words[:max_words]).strip() + "…"


def compute_health(store: dict) -> dict:
    kn = store.get("knowledge", {}).get("entries", [])
    ap = store.get("antipatterns", {}).get("entries", [])
    pb = store.get("playbooks", {}).get("entries", [])
    bm = store.get("benchmarks", {}).get("entries", [])
    proven_p = sum(1 for e in kn if e.get("status") == "proven")
    exp_p = sum(1 for e in kn if e.get("status") == "experimental")
    active_ap = sum(1 for e in ap if e.get("status") in ("experimental", "proven"))
    proven_ap = sum(1 for e in ap if e.get("status") == "proven")
    signals = store.get("regression_signals", [])
    last_reg = signals[-1].get("detected_at") if signals else None
    prevented = store.get("stats", {}).get("prevented_failures", 0)
    total = proven_p + proven_ap + len(pb) + len(bm)
    if total == 0:
        quality, trend = "sparse", "sparse"
    elif total < 10:
        quality, trend = "growing", "stable"
    else:
        quality = "mature"
        trend = "weakening" if len(signals) >= 2 else ("strengthening" if proven_ap > len(signals) else "stable")
    return {
        "computed_at": now_iso(),
        "proven_patterns": proven_p,
        "experimental_patterns": exp_p,
        "active_antipatterns": active_ap,
        "proven_antipatterns": proven_ap,
        "playbook_count": len(pb),
        "benchmark_count": len(bm),
        "prevented_failures": prevented,
        "last_regression": last_reg,
        "trend": trend,
        "memory_quality": quality,
    }


def save_store(capability_id: str, store: dict) -> Path:
    store["schema_version"] = "2.0"
    store["updated_at"] = now_iso()
    store["health"] = compute_health(store)
    path = store_path(capability_id)
    _save(path, store)
    return path


def next_knowledge_id(store: dict) -> str:
    return f"cap-k-{len(store.get('knowledge', {}).get('entries', [])) + 1:03d}"


def next_antipattern_id(capability_id: str, store: dict) -> str:
    n = len(store.get("antipatterns", {}).get("entries", [])) + 1
    return f"{capability_id}.{n:03d}"


def compress_store(store: dict) -> dict:
    profile = store.setdefault("compression_profile", {})
    max_items = int(profile.get("max_tier2_items", 40))
    word_budget = max(50, int(profile.get("tier2_max_tokens", 800)) // 4)
    used = 0
    ranked_ap = sorted(
        store.get("antipatterns", {}).get("entries", []),
        key=lambda e: (0 if e.get("status") == "proven" else 1, -{"critical": 0, "high": 1, "medium": 2, "low": 3}.get(e.get("severity", "medium"), 2)),
    )[:15]
    for entry in ranked_ap:
        entry["body_compressed"] = compress_text(entry.get("body", entry.get("title", "")), 60)
    ranked_kn = sorted(
        store.get("knowledge", {}).get("entries", []),
        key=lambda e: 0 if e.get("status") == "proven" else 1,
    )[:15]
    for entry in ranked_kn:
        t = compress_text(entry.get("body", entry.get("title", "")), 60)
        tags = entry.get("tags", [])
        entry["body_compressed"] = t + (f" ({tags[0]})" if tags else "")
        used += len(entry["body_compressed"].split())
    if used > word_budget:
        for entry in ranked_kn:
            if entry.get("status") != "proven":
                entry["body_compressed"] = entry.get("title", "")[:100]
    profile["last_compressed_at"] = now_iso()
    profile["tier2_item_count"] = min(max_items, len(ranked_ap) + len(ranked_kn))
    return store


def utilization_runtime_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "capability-memory" / "utilization"
    d.mkdir(parents=True, exist_ok=True)
    return d


def utilization_log_path(decision_id: str) -> Path:
    return utilization_runtime_dir() / f"{decision_id}.json"


def impact_log_path() -> Path:
    return utilization_runtime_dir() / "impact-log.jsonl"


def _ensure_usage_fields(entry: dict) -> None:
    entry.setdefault("usage_count", 0)
    entry.setdefault("success_count", 0)
    entry.setdefault("failure_count", 0)
    entry.setdefault("last_used_at", None)
    entry.setdefault("last_impact", None)


def _find_entry(store: dict, entry_id: str) -> tuple[str, dict | None]:
    for layer in ("knowledge", "antipatterns", "playbooks", "benchmarks"):
        for e in store.get(layer, {}).get("entries", []):
            if e.get("id") == entry_id:
                return layer, e
    return "", None


def entry_rank_score(entry: dict, layer: str, task_hint: str) -> float:
    _ensure_usage_fields(entry)
    score = 0.0
    if entry.get("status") == "proven":
        score += 100
    if layer == "antipatterns":
        score += {"critical": 40, "high": 30, "medium": 15, "low": 5}.get(entry.get("severity", "medium"), 10)
    score += int(entry.get("success_count", 0)) * 8
    score -= int(entry.get("failure_count", 0)) * 12
    hint = task_hint.lower()
    for tag in entry.get("tags", []):
        if str(tag).lower() in hint:
            score += 60
    if entry.get("usage_count", 0) == 0 and entry.get("status") in ("proven", "experimental"):
        score += 15
    return score


def select_ranked_entries(entries: list[dict], layer: str, task_hint: str, limit: int) -> list[dict]:
    ranked = sorted(entries, key=lambda e: entry_rank_score(e, layer, task_hint), reverse=True)
    return [e for e in ranked if e.get("status") not in ("deprecated", "superseded")][:limit]


def build_capability_context(capability_id: str, tier: int = 2, task_hint: str = "") -> dict:
    store = load_store(capability_id)
    if tier >= 2:
        store = compress_store(store)
    injected: list[dict] = []
    ctx: dict[str, Any] = {
        "capability_id": capability_id,
        "tier": tier,
        "health": store.get("health", {}),
        "path": str(store_path(capability_id).relative_to(REPO_ROOT)),
        "task_hint": task_hint[:200] if task_hint else "",
    }
    ap_pool = store["antipatterns"]["entries"]
    kn_pool = store["knowledge"]["entries"]
    pb_pool = store["playbooks"]["entries"]
    if tier == 1:
        for e in select_ranked_entries(ap_pool, "antipatterns", task_hint, 8):
            injected.append({"layer": "antipattern", "id": e["id"]})
        for e in select_ranked_entries(kn_pool, "knowledge", task_hint, 5):
            injected.append({"layer": "knowledge", "id": e["id"]})
        ctx["antipatterns"] = [{"id": e["id"], "title": e["title"], "severity": e.get("severity")} for e in select_ranked_entries(ap_pool, "antipatterns", task_hint, 8)]
        ctx["knowledge"] = [{"id": e["id"], "title": e["title"]} for e in select_ranked_entries(kn_pool, "knowledge", task_hint, 5)]
    elif tier == 2:
        ap_sel = select_ranked_entries(ap_pool, "antipatterns", task_hint, 15)
        kn_sel = select_ranked_entries(kn_pool, "knowledge", task_hint, 15)
        pb_sel = select_ranked_entries(pb_pool, "playbooks", task_hint, 3)
        for e in ap_sel:
            injected.append({"layer": "antipattern", "id": e["id"]})
        for e in kn_sel:
            injected.append({"layer": "knowledge", "id": e["id"]})
        for e in pb_sel:
            injected.append({"layer": "playbook", "id": e["id"]})
        ctx["antipatterns"] = [{"id": e["id"], "text": e.get("body_compressed") or e["title"], "severity": e.get("severity")} for e in ap_sel]
        ctx["knowledge"] = [{"id": e["id"], "text": e.get("body_compressed") or e.get("title")} for e in kn_sel]
        ctx["playbooks"] = [{"id": e["id"], "title": e["title"], "when": e.get("when_to_use", "")} for e in pb_sel]
    else:
        ctx["store"] = store
    total_active = len([e for e in ap_pool + kn_pool + pb_pool if e.get("status") not in ("deprecated", "superseded")])
    ctx["injected_ids"] = injected
    ctx["injection_stats"] = {
        "selected": len(injected),
        "pool_active": total_active,
        "utilization_rate": round(len(injected) / total_active, 3) if total_active else 0,
    }
    ctx["token_estimate"] = len(json.dumps(ctx, ensure_ascii=False).split())
    if tier >= 2:
        save_store(capability_id, store)
    return ctx


def record_utilization(decision_id: str, capability_id: str, injected: list[dict], source: str = "dispatch") -> dict:
    store = load_store(capability_id)
    ts = now_iso()
    for item in injected:
        layer, entry = _find_entry(store, item["id"])
        if not entry:
            continue
        _ensure_usage_fields(entry)
        entry["usage_count"] = int(entry.get("usage_count", 0)) + 1
        entry["last_used_at"] = ts
    save_store(capability_id, store)
    log_path = utilization_log_path(decision_id)
    log = _load(log_path) if log_path.exists() else {"decision_id": decision_id, "events": []}
    event = {"at": ts, "source": source, "capability_id": capability_id, "injected": injected}
    log["events"].append(event)
    _save(log_path, log)
    return event


def record_memory_impact(
    decision_id: str,
    capability_id: str,
    outcome: str,
    failed_tags: list[str],
    injected: list[dict] | None = None,
) -> dict:
    """Dispatch → Memory Impact feedback. outcome: success | failure."""
    store = load_store(capability_id)
    ts = now_iso()
    if injected is None:
        log_path = utilization_log_path(decision_id)
        injected = []
        if log_path.exists():
            for ev in reversed(_load(log_path).get("events", [])):
                if ev.get("capability_id") == capability_id:
                    injected = ev.get("injected", [])
                    break
    impacted: list[dict] = []
    tag_set = {t.lower() for t in failed_tags if t}
    for item in injected:
        layer, entry = _find_entry(store, item["id"])
        if not entry:
            continue
        _ensure_usage_fields(entry)
        rec = {"id": entry["id"], "layer": layer, "outcome": outcome}
        if outcome == "success":
            entry["success_count"] = int(entry.get("success_count", 0)) + 1
            entry["last_impact"] = "success"
            if layer == "playbook" and entry.get("status") == "experimental":
                entry["status"] = "proven"
        else:
            entry["failure_count"] = int(entry.get("failure_count", 0)) + 1
            entry["last_impact"] = "failure"
            if layer == "antipattern" and entry.get("status") == "proven":
                entry["status"] = "experimental"
                store.setdefault("regression_signals", []).append({
                    "detected_at": ts,
                    "entry_id": entry["id"],
                    "signal": "injected_but_failed",
                    "decision_id": decision_id,
                    "detail": "Antipattern injected but verification failed",
                })
        impacted.append(rec)
    if outcome == "failure" and tag_set:
        detect_regressions(capability_id, list(failed_tags), "", decision_id)
    save_store(capability_id, store)
    impact_rec = {"at": ts, "decision_id": decision_id, "capability_id": capability_id, "outcome": outcome, "impacted": impacted, "failed_tags": failed_tags}
    with impact_log_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(impact_rec, ensure_ascii=False) + "\n")
    return impact_rec


def utilization_audit(capability_id: str | None = None) -> dict:
    idx = load_memory_index()
    cap_ids = [capability_id] if capability_id else list(idx.get("capabilities", {}))
    report_caps: list[dict] = []
    for cap_id in cap_ids:
        store = load_store(cap_id)
        dead: list[dict] = []
        active: list[dict] = []
        for layer in ("knowledge", "antipatterns", "playbooks"):
            for e in store.get(layer, {}).get("entries", []):
                if e.get("status") in ("deprecated", "superseded"):
                    continue
                _ensure_usage_fields(e)
                row = {
                    "id": e["id"],
                    "layer": layer,
                    "title": e.get("title", "")[:80],
                    "usage_count": e.get("usage_count", 0),
                    "success_count": e.get("success_count", 0),
                    "failure_count": e.get("failure_count", 0),
                    "status": e.get("status"),
                }
                if row["usage_count"] == 0:
                    dead.append(row)
                else:
                    active.append(row)
        pool = len(dead) + len(active)
        report_caps.append({
            "capability_id": cap_id,
            "pool_active": pool,
            "used_entries": len(active),
            "dead_entries": len(dead),
            "utilization_rate": round(len(active) / pool, 3) if pool else 0,
            "dead": dead[:20],
            "top_performers": sorted(active, key=lambda x: x["success_count"], reverse=True)[:10],
            "high_failure": [a for a in active if a["failure_count"] > 0],
        })
    return {"generated_at": now_iso(), "capabilities": report_caps}


def _cursor_sdk_installed() -> bool:
    try:
        import cursor_sdk  # noqa: F401
        return True
    except ImportError:
        return False


def dispatch_adapter_audit() -> dict:
    prov = _load(ULAS_ROOT / "routing" / "provider-registry.json")
    wired = sum(1 for p in prov.get("providers", {}).values() if p.get("wired"))
    total = len(prov.get("providers", {}))
    return {
        "generated_at": now_iso(),
        "contract_schema": "ULAS/dispatch/provider-contract.schema.json",
        "providers_total": total,
        "providers_wired": wired,
        "providers_unwired": total - wired,
        "ai_dispatch_ready": any(
            p.get("wired") and p.get("adapter")
            for p in prov.get("providers", {}).values()
            if p.get("type") in ("ai_ide", "ai_api")
        ),
        "cursor_sdk_installed": _cursor_sdk_installed(),
        "queue_v0_ready": True,
        "queue_v0_cli": "ulas dispatch execute | ulas dispatch complete",
        "local_shell_ready": True,
        "human_ready": True,
        "swap_test": "Change routing-policy.json only — no code change",
        "blocker": "CURSOR_API_KEY + cursor-sdk required for --mode sdk; queue mode always available",
        "next_step": "pip install -r ULAS/adapters/requirements-cursor.txt && ulas dispatch execute --mode sdk",
        "providers": {
            pid: {"type": p.get("type"), "wired": p.get("wired", False), "dispatch": p.get("dispatch")}
            for pid, p in prov.get("providers", {}).items()
        },
    }


def memory_context_ref(capability_id: str, tier: int = 2) -> str:
    return f"ULAS/capability-memory/knowledge/{capability_id}.json?schema=2.0&tier={tier}"


def append_antipattern(capability_id: str, *, title: str, body: str, source: dict, tags: list[str] | None = None, severity: str = "medium", venture_slug: str = "") -> dict:
    store = load_store(capability_id)
    tag_list = tags or []
    for existing in store["antipatterns"]["entries"]:
        if existing.get("title") == title[:120] or (tag_list and tag_list[0] in existing.get("tags", [])):
            existing["evidence_count"] = existing.get("evidence_count", 1) + 1
            save_store(capability_id, store)
            return existing
    entry = {
        "id": next_antipattern_id(capability_id, store),
        "title": title[:120],
        "status": "experimental",
        "severity": severity,
        "body": body,
        "body_compressed": compress_text(body, 40),
        "evidence_count": 1,
        "source": source,
        "tags": tag_list,
        "regression_watch": True,
    }
    store["antipatterns"]["entries"].append(entry)
    if venture_slug:
        store.setdefault("stats", {})["ventures_contributed"] = store.get("stats", {}).get("ventures_contributed", 0) + 1
    save_store(capability_id, store)
    return entry


def append_knowledge(capability_id: str, *, kind: str, title: str, body: str, source: dict, tags: list[str] | None = None, venture_slug: str = "") -> dict:
    store = load_store(capability_id)
    entry = {
        "id": next_knowledge_id(store),
        "kind": kind,
        "status": "experimental",
        "title": title[:120],
        "body": body,
        "body_compressed": compress_text(body, 40),
        "source": source,
        "evidence_refs": source.get("evidence_refs", []),
        "tags": tags or [],
    }
    store["knowledge"]["entries"].append(entry)
    if venture_slug:
        store.setdefault("stats", {})["ventures_contributed"] = store.get("stats", {}).get("ventures_contributed", 0) + 1
    save_store(capability_id, store)
    return entry


def append_benchmark(capability_id: str, *, project_type: str, metrics: dict, source: dict, venture_slug: str = "") -> dict:
    store = load_store(capability_id)
    n = len(store["benchmarks"]["entries"]) + 1
    entry = {
        "id": f"{capability_id}.bm-{n:03d}",
        "project_type": project_type,
        "venture_slug": venture_slug,
        "metrics": metrics,
        "recorded_at": now_iso(),
        "source": source,
    }
    store["benchmarks"]["entries"].append(entry)
    save_store(capability_id, store)
    return entry


def detect_regressions(capability_id: str, failed_tags: list[str], venture_slug: str, decision_id: str) -> list[dict]:
    store = load_store(capability_id)
    tag_set = {t.lower() for t in failed_tags}
    signals: list[dict] = []
    for entry in store["antipatterns"]["entries"]:
        if entry.get("status") != "proven":
            continue
        entry_tags = {t.lower() for t in entry.get("tags", [])}
        if not tag_set.intersection(entry_tags):
            continue
        signal = {
            "detected_at": now_iso(),
            "entry_id": entry["id"],
            "signal": "proven_violated",
            "venture_slug": venture_slug,
            "decision_id": decision_id,
            "detail": f"Proven antipattern '{entry.get('title')}' tag match",
        }
        store["regression_signals"].append(signal)
        entry["status"] = "experimental"
        signals.append(signal)
    if signals:
        save_store(capability_id, store)
    return signals


def ingest_from_evidence(venture_slug: str) -> list[dict]:
    path = SVOS_ROOT / "07-evidence" / venture_slug / "manifest.json"
    if not path.exists():
        return []
    manifest = _load(path)
    created: list[dict] = []
    metrics: dict[str, Any] = {}
    for src in manifest.get("sources", []):
        if src.get("type") == "unit_test":
            metrics["unit_test_total"] = src.get("total", 0)
            metrics["unit_test_failed"] = src.get("failed", 0)
        if src.get("type") == "build":
            metrics["build_status"] = 1 if src.get("status") == "success" else 0
    if metrics:
        bm = append_benchmark(
            "android.testing",
            project_type=venture_slug,
            metrics=metrics,
            source={"type": "evidence", "ref": str(path.relative_to(REPO_ROOT))},
            venture_slug=venture_slug,
        )
        created.append(bm)
    return created


def quality_report() -> dict:
    idx = load_memory_index()
    caps = []
    for cap_id, meta in idx.get("capabilities", {}).items():
        store = load_store(cap_id)
        h = store.get("health", compute_health(store))
        caps.append({"capability_id": cap_id, "label": meta.get("label"), **h})
    return {"generated_at": now_iso(), "schema_version": "2.0", "capabilities": caps}


def migrate_all() -> int:
    count = 0
    for cap_id in load_memory_index().get("capabilities", {}):
        load_store(cap_id)
        count += 1
    return count


def test_regression_scenario(capability_id: str, tag: str) -> dict:
    store = load_store(capability_id)
    for entry in store["antipatterns"]["entries"]:
        if entry.get("id") == "android.architecture.001" or tag in entry.get("tags", []):
            entry["status"] = "proven"
    save_store(capability_id, store)
    signals = detect_regressions(capability_id, [tag], "test-venture", "regression-test")
    return {"simulated_tag": tag, "signals": signals, "health": load_store(capability_id).get("health"), "ok": len(signals) > 0}
