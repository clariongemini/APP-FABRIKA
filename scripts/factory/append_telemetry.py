#!/usr/bin/env python3
"""Append entry to factory/runtime/telemetry/cycle_log.json."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "factory"))
from runtime_paths import telemetry_path  # noqa: E402

LOG = telemetry_path("cycle_log.json")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle", required=True)
    parser.add_argument("--script", required=True)
    parser.add_argument("--started", required=True)
    parser.add_argument("--motors", default="")
    parser.add_argument("--exit-code", type=int, default=0)
    args = parser.parse_args()

    LOG.parent.mkdir(parents=True, exist_ok=True)
    data = {"version": "1.0", "entries": []}
    if LOG.exists():
        try:
            data = json.loads(LOG.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    motors = [m.strip() for m in args.motors.split(",") if m.strip()]
    data.setdefault("entries", []).append({
        "cycle": args.cycle,
        "script": args.script,
        "started_at": args.started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": args.exit_code,
        "motors_updated": motors,
    })
    LOG.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ {LOG.relative_to(ROOT)} updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
