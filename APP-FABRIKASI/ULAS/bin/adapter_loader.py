"""Load provider adapters from ULAS/adapters/ without hardcoding in ulas.py."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ULAS_ROOT = Path(__file__).resolve().parent.parent
_ADAPTERS_ROOT = ULAS_ROOT / "adapters"


def load_adapter(relative_path: str) -> ModuleType:
    """relative_path e.g. adapters/cursor_dispatch.py"""
    rel = relative_path.replace("\\", "/")
    if rel.startswith("ULAS/"):
        rel = rel[len("ULAS/") :]
    if rel.startswith("adapters/"):
        path = ULAS_ROOT / rel
    else:
        path = _ADAPTERS_ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(f"Adapter not found: {path}")
    name = f"ulas_adapter_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load adapter: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "handle_ai_invoke"):
        raise AttributeError(f"{path} missing handle_ai_invoke(envelope, codebase)")
    return mod
