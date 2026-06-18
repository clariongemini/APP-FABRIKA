"""AI Dispatch v0 — file queue materialization (no provider SDK in core)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

ULAS_ROOT = Path(__file__).resolve().parent.parent
SVOS_ROOT = ULAS_ROOT.parent
REPO_ROOT = SVOS_ROOT.parent


def dispatch_queue_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "dispatch" / "queue"
    d.mkdir(parents=True, exist_ok=True)
    return d


def queue_card_path(dispatch_id: str) -> Path:
    safe = dispatch_id.replace("/", "_")
    return dispatch_queue_dir() / f"{safe}.md"


def queue_result_path(dispatch_id: str) -> Path:
    safe = dispatch_id.replace("/", "_")
    return dispatch_queue_dir() / f"{safe}.result.json"


def build_queue_card(envelope: dict, codebase: Path) -> str:
    invoke = envelope.get("invoke", {})
    ctx = invoke.get("capability_context", {})
    refs = invoke.get("context_refs", [])
    decision_id = envelope.get("decision_id", "")
    dispatch_id = envelope.get("dispatch_id", "")
    try:
        codebase_label = str(codebase.relative_to(REPO_ROOT))
    except ValueError:
        codebase_label = str(codebase)
    lines = [
        f"# Dispatch: {dispatch_id}",
        "",
        f"- **Decision:** `{decision_id}`",
        f"- **Work package:** `{envelope.get('work_package_id', '')}`",
        f"- **Capability:** `{envelope.get('capability_id', '')}`",
        f"- **Provider:** `{envelope.get('provider_id', '')}`",
        f"- **Codebase:** `{codebase_label}`",
        "",
        "## Instruction",
        "",
        invoke.get("instruction", "").strip() or "(none)",
        "",
        "## Acceptance",
        "",
        invoke.get("acceptance", "").strip() or "(none)",
        "",
        "## Capability context (tier 2)",
        "",
        "```json",
        json.dumps(
            {
                k: ctx[k]
                for k in ("capability_id", "antipatterns", "playbooks", "knowledge", "injected_ids", "injection_stats")
                if k in ctx
            },
            indent=2,
            ensure_ascii=False,
        ),
        "```",
        "",
        "## Context refs",
        "",
    ]
    for ref in refs:
        lines.append(f"- `{ref}`")
    lines.extend([
        "",
        "## Complete",
        "",
        "When done:",
        "",
        "```bash",
        f"ulas dispatch complete --decision-id {decision_id} "
        f"--dispatch-id {dispatch_id} --result success",
        "```",
        "",
    ])
    return "\n".join(lines)


def write_queue_card(envelope: dict, codebase: Path) -> Path:
    path = queue_card_path(envelope["dispatch_id"])
    path.write_text(build_queue_card(envelope, codebase), encoding="utf-8")
    return path


def write_complete_result(
    envelope: dict,
    *,
    success: bool,
    transcript_path: Path | None = None,
    note: str = "",
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "success": success,
        "provider": envelope.get("provider_id"),
        "dispatch_id": envelope.get("dispatch_id"),
        "note": note,
    }
    out = queue_result_path(envelope["dispatch_id"])
    if transcript_path and transcript_path.is_file():
        dest = dispatch_queue_dir() / f"{envelope['dispatch_id'].replace('/', '_')}.transcript.txt"
        shutil.copy2(transcript_path, dest)
        result["transcript_ref"] = str(dest.relative_to(REPO_ROOT))
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result["result_ref"] = str(out.relative_to(REPO_ROOT))
    return result
