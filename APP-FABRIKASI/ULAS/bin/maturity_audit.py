"""SVOS maturity audit — README olgunluk tablosu ile hizalı, kanıt tabanlı skor."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

SVOS_ROOT = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = SVOS_ROOT.parent


@dataclass
class Check:
    id: str
    label: str
    points: int
    passed: bool
    fix: str = ""


@dataclass
class Dimension:
    id: str
    label: str
    weight: float
    score: int = 0
    max_score: int = 100
    checks: list[Check] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _exists(path: Path) -> bool:
    return path.is_file() or path.is_dir()


def _load_json(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _list_ventures(svos: Path) -> list[Path]:
    vdir = svos / "08-ventures"
    if not vdir.is_dir():
        return []
    return sorted(
        p for p in vdir.glob("*/venture.json")
        if not p.parent.name.startswith("_")
    )


def _primary_venture(svos: Path) -> tuple[str, dict] | tuple[None, None]:
    """En aktif venture: work chain olan, yoksa ilk gerçek charter."""
    work_slugs: set[str] = set()
    for wp in (svos / "10-runtime/ulas/work").glob("*.json"):
        w = _load_json(wp) or {}
        if w.get("venture_slug"):
            work_slugs.add(w["venture_slug"])
    for vpath in _list_ventures(svos):
        if vpath.parent.name in work_slugs:
            return vpath.parent.name, _load_json(vpath) or {}
    ventures = _list_ventures(svos)
    if ventures:
        v = _load_json(ventures[0]) or {}
        return ventures[0].parent.name, v
    return None, None


def _count_glob(root: Path, pattern: str) -> int:
    if not root.is_dir():
        return 0
    return len(list(root.glob(pattern)))


def _venture_count(svos: Path) -> int:
    return len(_list_ventures(svos))


def audit_architecture(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("architecture", "Architecture", 0.14)
    checks = [
        Check(
            "purpose_layers",
            "01–10 PURPOSE.md",
            18,
            all(_exists(svos / f"{i:02d}-{name}/PURPOSE.md") for i, name in [
                (1, "core"), (2, "platforms"), (3, "agents"), (4, "design"),
                (5, "templates"), (6, "learning"), (7, "evidence"), (8, "ventures"),
                (9, "portfolio"), (10, "runtime"),
            ]),
            "./APP-FABRIKASI/scripts/svos-health.sh",
        ),
        Check("architecture_doc", "ARCHITECTURE.md", 14, _exists(svos / "ARCHITECTURE.md"), "docs/ARCHITECTURE.md oluştur"),
        Check("north_star", "NORTH_STAR.md", 10, _exists(svos / "NORTH_STAR.md"), ""),
        Check("ulas_core", "ULAS/bin/ulas.py", 18, _exists(svos / "ULAS/bin/ulas.py"), ""),
        Check("context_schema", "context-manifest.schema.json", 10, _exists(svos / "10-runtime/context-manifest.schema.json"), ""),
        Check("install_script", "install-svos-into-project.sh", 15, _exists(svos / "scripts/install-svos-into-project.sh"), "scripts/install-svos-into-project.sh ekle"),
        Check("assemble_context", "assemble-svos-context.sh", 15, _exists(svos / "scripts/assemble-svos-context.sh"), "scripts/assemble-svos-context.sh ekle"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_governance(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("governance", "Governance", 0.10)
    gov = svos / "01-core/governance/GOVERNANCE_DESIGN.md"
    checks = [
        Check("gov_design", "GOVERNANCE_DESIGN.md", 25, _exists(gov), ""),
        Check("stabilization", "STABILIZATION.md", 15, _exists(svos / "STABILIZATION.md"), ""),
        Check("dispatch_ide", "dispatch-ide.mdc", 20, _exists(svos / ".cursor/rules/dispatch-ide.mdc"), ".cursor/rules/dispatch-ide.mdc"),
        Check("gap_analysis", "GAP_ANALYSIS.md", 15, _exists(svos / "GAP_ANALYSIS.md"), ""),
        Check("maturity_cli", "ulas maturity audit", 15, _exists(svos / "ULAS/bin/maturity_audit.py"), ""),
        Check("no_exec_bloat", "Hafif governance (≤12 top-level governance dirs)", 10,
              not _exists(repo / "governance/egc") or _exists(svos / "STABILIZATION.md"), ""),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_android_adapter(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("android_adapter", "Android adapter", 0.12)
    checks = [
        Check("adapter_doc", "02-platforms/android/ADAPTER.md", 20, _exists(svos / "02-platforms/android/ADAPTER.md"), ""),
        Check("bridge", "bridge-venture.sh", 25, _exists(svos / "scripts/bridge-venture.sh"), ""),
        Check("failure_collect", "collect-test-failures.py", 20, _exists(svos / "scripts/collect-test-failures.py"), ""),
        Check("gradle_parser", "gradle_test_parser.py", 15, _exists(svos / "ULAS/bin/gradle_test_parser.py"), ""),
        Check("factory_templates", "templates/android", 20, _exists(repo / "templates/android"), "Android factory templates"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_learning(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("learning", "Learning", 0.10)
    adrs = _count_glob(svos / "06-learning/adr", "ADR-*.md")
    pms = _count_glob(svos / "06-learning/postmortems", "*.md")
    checks = [
        Check("learning_tree", "06-learning yapısı", 25, _exists(svos / "06-learning/PURPOSE.md"), ""),
        Check("adr_template", "ADR şablonu", 15, _exists(svos / "06-learning/adr") or adrs > 0, ""),
        Check("postmortem_dir", "postmortems/", 15, _exists(svos / "06-learning/postmortems"), ""),
        Check("outcome_script", "record-outcome", 15,
              _exists(repo / "scripts/factory/record-outcome.py") or _exists(svos / "scripts/record-outcome.py"), ""),
        Check("has_adrs", f"ADR kayıtları ({adrs})", min(15, adrs * 5), adrs > 0, "İlk ADR: 06-learning/adr/"),
        Check("has_postmortems", f"postmortem ({pms})", min(15, pms * 8), pms > 0, "Ship sonrası postmortem yaz"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_intelligence(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("intelligence", "Intelligence (ULAS)", 0.14)
    ulas = svos / "ULAS/bin/ulas.py"
    text = ulas.read_text(encoding="utf-8") if ulas.is_file() else ""
    checks = [
        Check("decide", "ulas decide", 12, "cmd_decide" in text or 'add_parser("decide"' in text, ""),
        Check("work", "ulas work generate", 12, "cmd_work_generate" in text, ""),
        Check("dispatch", "ulas dispatch", 15, "cmd_dispatch" in text or "dispatch execute" in text, ""),
        Check("execute", "ulas execute run", 15, "cmd_execute_run" in text, ""),
        Check("memory", "capability memory", 12, _exists(svos / "ULAS/bin/capability_memory_engine.py"), ""),
        Check("routing", "provider-registry.json", 12, _exists(svos / "ULAS/routing/provider-registry.json"), ""),
        Check("dispatch_queue", "dispatch_queue.py", 12, _exists(svos / "ULAS/bin/dispatch_queue.py"), ""),
        Check("maturity", "maturity audit", 10, _exists(svos / "ULAS/bin/maturity_audit.py"), ""),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_evidence(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("evidence", "Evidence", 0.12)
    ventures = _list_ventures(svos)
    collected = 0
    for vpath in ventures:
        v = _load_json(vpath) or {}
        if v.get("evidence_status") in ("collected", "partial", "complete"):
            collected += 1
    checks = [
        Check("evidence_purpose", "07-evidence PURPOSE", 15, _exists(svos / "07-evidence/PURPOSE.md"), ""),
        Check("bridge", "bridge-venture.sh", 25, _exists(svos / "scripts/bridge-venture.sh"), ""),
        Check("failure_report", "test-failure-report.json", 20,
              any((svos / "10-runtime/evidence").glob("*/test-failure-report.json")), "ulas evidence collect --venture SLUG"),
        Check("manifest", "evidence manifest.json", 20,
              any((svos / "07-evidence").glob("*/manifest.json")), "bridge-venture.sh SLUG"),
        Check("venture_collected", f"venture evidence ({collected}/{max(len(ventures),1)})", 20,
              collected > 0, "bridge-venture.sh + evidence collect"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_portfolio(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("portfolio", "Portfolio", 0.08)
    ventures = _venture_count(svos)
    outcomes = 0
    dec_dir = svos / "10-runtime/ulas/decisions"
    if dec_dir.is_dir():
        for f in dec_dir.glob("*.json"):
            d = _load_json(f) or {}
            if d.get("effectiveness", {}).get("outcome_recorded"):
                outcomes += 1
    checks = [
        Check("portfolio_dir", "09-portfolio", 30, _exists(svos / "09-portfolio/PURPOSE.md"), ""),
        Check("multi_venture", f"≥2 venture ({ventures})", 35, ventures >= 2, "İkinci venture charter"),
        Check("outcomes", f"outcome kayıtları ({outcomes})", 35, outcomes >= 1, "ulas outcome --result approved_success"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


def audit_venture_validation(svos: Path, repo: Path) -> Dimension:
    dim = Dimension("venture_validation", "Venture validation", 0.20)
    slug, v = _primary_venture(svos)
    if not slug or not v:
        dim.checks = [Check("charter", "venture charter", 100, False, "./APP-FABRIKASI/scripts/init-venture.sh")]
        dim.score = 0
        dim.gaps = ["Venture charter yok — init-venture.sh çalıştır"]
        return dim

    decision_id = ""
    work_path = None
    dispatch_path = None
    exec_path = None
    for wp in (svos / "10-runtime/ulas/work").glob("*.json"):
        w = _load_json(wp) or {}
        if w.get("venture_slug") == slug:
            decision_id = w.get("decision_id", "")
            work_path = wp
            break
    if decision_id:
        dispatch_path = svos / "10-runtime/ulas/dispatch" / f"{decision_id}.json"
        exec_path = svos / "10-runtime/ulas/execution" / f"{decision_id}.json"

    dispatch = _load_json(dispatch_path) if dispatch_path else None
    execution = _load_json(exec_path) if exec_path else None
    completed_dispatches = 0
    if dispatch:
        completed_dispatches = sum(1 for e in dispatch.get("envelopes", []) if e.get("status") == "completed")

    tests_ok = (v.get("validation", {}).get("tests", {}).get("failed", 1) == 0)
    build_ok = v.get("validation", {}).get("build") == "success"
    verified = execution and execution.get("state") == "verified"
    shipped = v.get("stage") == "shipped" or v.get("phase") == "shipped"

    checks = [
        Check("charter", "venture.json charter", 12, bool(v.get("charter")), ""),
        Check("codebase_link", "codebase_path", 10, bool(v.get("codebase_path")), ""),
        Check("decision", "APPROVED decision + work chain", 15, work_path is not None, "ulas decide + work generate"),
        Check("dispatch", "dispatch plan", 12, dispatch is not None, "ulas dispatch plan"),
        Check("bridge", "build/test bridge", 15, bool(v.get("validation")), "bridge-venture.sh"),
        Check("zero_fail", "tests 0 failed", 18, tests_ok, "dispatch next → düzelt → execute run"),
        Check("dispatch_done", f"dispatch completed ({completed_dispatches})", 10, completed_dispatches > 0, "ulas dispatch complete"),
        Check("verified", "execute verified", 8, bool(verified), "ulas execute run → pass"),
        Check("shipped", "venture shipped", 10, shipped, "Play Store + stage=shipped"),
    ]
    dim.checks = checks
    dim.score = min(100, sum(c.points for c in checks if c.passed))
    dim.gaps = [f"{c.label}: {c.fix}" for c in checks if not c.passed and c.fix]
    return dim


AUDITORS: list[Callable[[Path, Path], Dimension]] = [
    audit_architecture,
    audit_governance,
    audit_android_adapter,
    audit_learning,
    audit_intelligence,
    audit_evidence,
    audit_portfolio,
    audit_venture_validation,
]


def run_maturity_audit(svos_root: Path | None = None, repo_root: Path | None = None) -> dict[str, Any]:
    svos = svos_root or SVOS_ROOT
    repo = repo_root or REPO_ROOT
    dimensions = [fn(svos, repo) for fn in AUDITORS]
    composite = round(sum(d.score * d.weight for d in dimensions))
    all_gaps: list[dict[str, str]] = []
    for d in dimensions:
        for g in d.gaps:
            all_gaps.append({"dimension": d.id, "gap": g, "priority": "P0" if d.id == "venture_validation" else "P1"})

    return {
        "composite_score": composite,
        "target_score": 100,
        "gap_to_target": 100 - composite,
        "audited_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "svos_root": str(svos.relative_to(repo) if svos.is_relative_to(repo) else svos),
        "dimensions": {
            d.id: {
                "label": d.label,
                "score": d.score,
                "weight": d.weight,
                "checks_passed": sum(1 for c in d.checks if c.passed),
                "checks_total": len(d.checks),
                "gaps": d.gaps,
            }
            for d in dimensions
        },
        "open_gaps": all_gaps,
        "next_commands": _next_commands(all_gaps, dimensions),
    }


def _next_commands(gaps: list[dict], dimensions: list[Dimension]) -> list[str]:
    cmds: list[str] = []
    vv = next((d for d in dimensions if d.id == "venture_validation"), None)
    if vv and vv.score < 100:
        cmds.append("./APP-FABRIKASI/scripts/init-venture.sh \"My App\" my-app path/to/codebase/")
        cmds.append("./APP-FABRIKASI/scripts/bridge-venture.sh my-app")
        cmds.append("ulas dispatch next --decision-id <ID>")
        cmds.append("ulas execute run --decision-id <ID>")
        cmds.append("ulas outcome --decision-id <ID> --result approved_success")
    if any(g["dimension"] == "portfolio" for g in gaps):
        cmds.append("./APP-FABRIKASI/scripts/init-venture.sh \"Venture 2\" venture-2 path/to/codebase/")
    if not cmds:
        cmds.append("./APP-FABRIKASI/scripts/svos-health.sh")
    return cmds[:6]


def format_report(report: dict) -> str:
    lines = [
        f"SVOS Maturity: {report['composite_score']} / 100  (hedefe {report['gap_to_target']} puan)",
        "",
        "| Alan | Skor | Ağırlık |",
        "|------|------|---------|",
    ]
    for did, dim in report["dimensions"].items():
        lines.append(f"| {dim['label']} | {dim['score']} | {int(dim['weight']*100)}% |")
    if report["open_gaps"]:
        lines.extend(["", "## Açık gap'ler (öncelikli)", ""])
        for i, g in enumerate(report["open_gaps"][:12], 1):
            lines.append(f"{i}. **[{g['dimension']}]** {g['gap']}")
    lines.extend(["", "## Sonraki komutlar", ""])
    for c in report.get("next_commands", []):
        lines.append(f"- `{c}`")
    return "\n".join(lines)
