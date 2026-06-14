#!/usr/bin/env python3
"""Split docs/33-LAYER-MANIFEST.yaml into per-layer slices for on-demand Cursor loading."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "33-LAYER-MANIFEST.yaml"
OUT_DIR = ROOT / "docs" / "33-LAYER-MANIFEST"
LAYER_RE = re.compile(r"^  (\d+):\n((?:    .+\n)+)", re.MULTILINE)


def parse_layers(text: str) -> dict[int, str]:
    layers: dict[int, str] = {}
    for m in LAYER_RE.finditer(text):
        num = int(m.group(1))
        block = m.group(2)
        layers[num] = block
    return layers


def write_slice(num: int, block: str) -> None:
    name_m = re.search(r"name: (.+)", block)
    group_m = re.search(r"group: (.+)", block)
    agent_m = re.search(r"agent: (\w+)", block)
    components = re.findall(r"^      - (.+)$", block, re.MULTILINE)

    lines = [
        f"# KATMAN {num} — on-demand slice (do not load full 33-LAYER-MANIFEST.yaml)",
        f"layer: {num}",
        f"name: {name_m.group(1) if name_m else 'UNKNOWN'}",
        f"group: {group_m.group(1) if group_m else ''}",
        f"agent: {agent_m.group(1) if agent_m else ''}",
        "source: docs/33-LAYER-MANIFEST.yaml",
        "components:",
    ]
    lines.extend(f"  - {c}" for c in components)
    lines.append("")
    path = OUT_DIR / f"layer-{num:02d}.yaml"
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not MANIFEST.exists():
        print(f"HATA: {MANIFEST} missing")
        return 1

    text = MANIFEST.read_text(encoding="utf-8")
    layers = parse_layers(text)
    if len(layers) != 33:
        print(f"HATA: expected 33 layers, parsed {len(layers)}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for num in range(33):
        if num not in layers:
            print(f"HATA: layer {num} missing in manifest")
            return 1
        write_slice(num, layers[num])

    readme = OUT_DIR / "README.md"
    readme.write_text(
        """# 33 Katman — On-Demand Dilimler

Cursor context budget için **tam manifest okunmaz**. Yalnızca ilgili katman dilimini oku:

| Ajan | Dilimler |
|------|----------|
| CPO | `layer-00` … `02`, `25`, `26`, `30` |
| Android | `layer-03` … `06`, `22` |
| Architect | `layer-07` … `15`, `20`, `23`, `24`, `27` … `29` |
| Auditor | `layer-16` … `19`, `21`, `31`, `32` |

Üretim: `python3 scripts/split-layer-manifest.py`  
Kaynak doğruluk: `docs/33-LAYER-MANIFEST.yaml`  
Rehber: `docs/CURSOR_CONTEXT_BUDGET.md`
""",
        encoding="utf-8",
    )
    print(f"==> {len(layers)} layer slices → {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
