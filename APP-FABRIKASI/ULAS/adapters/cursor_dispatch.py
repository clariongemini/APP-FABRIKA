"""Cursor provider adapter — local SDK agent (v1).

Requires:
  pip install cursor-sdk   # or: pip install -r ULAS/adapters/requirements-cursor.txt
  export CURSOR_API_KEY=...

Swap: routing-policy.json only — core ulas.py unchanged.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

ULAS_ROOT = Path(__file__).resolve().parent.parent
SVOS_ROOT = ULAS_ROOT.parent
REPO_ROOT = SVOS_ROOT.parent


def _transcript_dir() -> Path:
    d = SVOS_ROOT / "10-runtime" / "ulas" / "dispatch" / "transcripts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def sdk_available() -> bool:
    try:
        import cursor_sdk  # noqa: F401
        return True
    except ImportError:
        return False


def build_prompt(envelope: dict) -> str:
    invoke = envelope.get("invoke", {})
    ctx = invoke.get("capability_context", {})
    parts = [
        "# ULAS Dispatch Task",
        "",
        f"Decision: {envelope.get('decision_id')}",
        f"Work package: {envelope.get('work_package_id')}",
        f"Capability: {envelope.get('capability_id')}",
        "",
        "## Instruction",
        invoke.get("instruction", ""),
        "",
        "## Acceptance criteria",
        invoke.get("acceptance", ""),
        "",
        "## Capability memory (injected)",
        "```json",
        json.dumps(
            {k: ctx[k] for k in ("antipatterns", "playbooks", "knowledge", "injected_ids") if k in ctx},
            indent=2,
            ensure_ascii=False,
        ),
        "```",
        "",
        "## Rules",
        "- Edit files in the workspace only; minimal focused diff.",
        "- Do not add governance/docs unless required for the fix.",
        "- After changes, ensure acceptance criteria can be verified.",
    ]
    return "\n".join(parts)


def capture_git_diff(codebase: Path) -> str:
    if not (codebase / ".git").exists():
        return ""
    try:
        proc = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=str(codebase),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except (subprocess.TimeoutExpired, OSError):
        return ""


def handle_ai_invoke(envelope: dict, codebase: Path) -> dict[str, Any]:
    """Provider contract entry — called only via adapter_loader."""
    provider_id = envelope.get("provider_id", "cursor")
    dispatch_id = envelope.get("dispatch_id", "unknown")
    api_key = os.environ.get("CURSOR_API_KEY", "").strip()

    if not api_key:
        return {
            "provider": provider_id,
            "success": False,
            "skipped": True,
            "reason": "CURSOR_API_KEY not set — use queue mode: ulas dispatch execute",
            "adapter_mode": "sdk_local",
        }

    if not sdk_available():
        return {
            "provider": provider_id,
            "success": False,
            "skipped": True,
            "reason": "cursor-sdk not installed — pip install cursor-sdk",
            "adapter_mode": "sdk_local",
        }

    from cursor_sdk import Agent, AgentOptions, LocalAgentOptions

    prompt = build_prompt(envelope)
    model = os.environ.get("CURSOR_DISPATCH_MODEL", "composer-2.5")
    transcript_path = _transcript_dir() / f"{dispatch_id.replace('/', '_')}.log"
    diff_before = capture_git_diff(codebase)

    try:
        result = Agent.prompt(
            prompt,
            AgentOptions(
                api_key=api_key,
                model=model,
                local=LocalAgentOptions(cwd=str(codebase.resolve())),
            ),
        )
    except Exception as exc:  # CursorAgentError or network
        body = f"SDK invoke failed: {exc}\n"
        transcript_path.write_text(body, encoding="utf-8")
        return {
            "provider": provider_id,
            "success": False,
            "skipped": False,
            "error": str(exc),
            "adapter_mode": "sdk_local",
            "stdout_ref": str(transcript_path.relative_to(REPO_ROOT)),
        }

    status = getattr(result, "status", None) or "unknown"
    text_out = getattr(result, "result", None) or getattr(result, "output", "") or ""
    diff_after = capture_git_diff(codebase)
    transcript = "\n".join([
        f"status={status}",
        f"model={model}",
        f"codebase={codebase}",
        "",
        "--- agent output ---",
        str(text_out)[:50000],
        "",
        "--- git diff stat (before) ---",
        diff_before or "(none)",
        "",
        "--- git diff stat (after) ---",
        diff_after or "(none)",
    ])
    transcript_path.write_text(transcript, encoding="utf-8")

    success = status not in ("error", "failed", "cancelled")
    return {
        "provider": provider_id,
        "success": success,
        "skipped": False,
        "adapter_mode": "sdk_local",
        "run_status": status,
        "stdout_ref": str(transcript_path.relative_to(REPO_ROOT)),
        "git_diff_stat": diff_after[:2000] if diff_after else "",
        "exit_code": 0 if success else 1,
    }
