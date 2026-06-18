"""Parse Gradle unit test output and JUnit XML — shared by verify, bridge, evidence."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_gradle_summary(output: str) -> dict | None:
    m = re.search(r"(\d+)\s+tests?\s+completed,\s+(\d+)\s+failed", output)
    if m:
        total, failed = int(m.group(1)), int(m.group(2))
        return {"total": total, "failed": failed, "passed": total - failed}
    if "BUILD SUCCESSFUL" in output and "failed" not in output.lower():
        return {"total": None, "failed": 0, "passed": None}
    return None


def parse_failed_from_gradle_log(output: str) -> list[dict]:
    """Lines like: ClassName > methodName FAILED"""
    failures: list[dict] = []
    for line in output.splitlines():
        m = re.match(r"^(\S+)\s+>\s+(\S+)\s+FAILED\s*$", line.strip())
        if m:
            failures.append({
                "test": f"{m.group(1)}.{m.group(2)}",
                "class": m.group(1),
                "method": m.group(2),
            })
    return failures


def parse_junit_xml(path: Path) -> list[dict]:
    failures: list[dict] = []
    if not path.is_file():
        return failures
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return failures
    for case in root.iter("testcase"):
        fail = case.find("failure")
        if fail is None:
            fail = case.find("error")
        if fail is None:
            continue
        cls = case.get("classname", "")
        name = case.get("name", "")
        failures.append({
            "test": f"{cls}.{name}" if cls else name,
            "class": cls,
            "method": name,
            "message": (fail.get("message") or fail.text or "")[:500],
        })
    return failures


def collect_junit_failures(codebase: Path, variant: str = "testDebugUnitTest") -> list[dict]:
    results_dir = codebase / "app" / "build" / "test-results" / variant
    if not results_dir.is_dir():
        return []
    seen: set[str] = set()
    out: list[dict] = []
    for xml in sorted(results_dir.glob("TEST-*.xml")):
        for f in parse_junit_xml(xml):
            if f["test"] not in seen:
                seen.add(f["test"])
                out.append(f)
    return out


def read_log_text(run: dict, repo_root: Path) -> str:
    ref = run.get("stdout_ref", "")
    if ref:
        p = repo_root / ref
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")
    return (run.get("stdout_tail") or "") + (run.get("stderr_tail") or "")


def cluster_failures(failures: list[dict]) -> list[dict]:
    """Group failures into repair clusters for work packages (project-agnostic heuristics)."""
    clusters: dict[str, dict] = {}

    def add(cid: str, cap: str, item: dict) -> None:
        c = clusters.setdefault(cid, {"id": cid, "capability": cap, "failures": []})
        c["failures"].append(item)

    for f in failures:
        test = f.get("test", "")
        msg = (f.get("message") or "").lower()
        tl = test.lower()
        if any(k in tl for k in ("boundary", "module", "architecture", "gradle")):
            add("architecture", "android.architecture", f)
        elif "java 21" in msg or "robolectric" in msg or "sandbox" in msg:
            add("test_env", "android.testing", f)
        elif "not mocked" in msg:
            add("jvm_android_api", "android.testing", f)
        elif any(k in tl for k in ("ui", "compose", "widget", "screenshot", "roborazzi")):
            add("ui", "android.ui", f)
        else:
            add("other", "android.testing", f)
    return list(clusters.values())


def load_bridge_config(svos_root: Path, venture: dict) -> dict:
    """Resolve Gradle bridge tasks: venture.build overrides platform bridge.defaults.json."""
    platform = (venture.get("platform") or ["android"])[0]
    defaults_path = svos_root / "02-platforms" / platform / "bridge.defaults.json"
    defaults: dict = {}
    if defaults_path.is_file():
        import json
        defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
    custom = venture.get("build") or {}
    return {
        "build_task": custom.get("build_task") or defaults.get("build_task", ":app:assembleDebug"),
        "unit_test_task": custom.get("unit_test_task") or defaults.get("unit_test_task", ":app:testDebugUnitTest"),
        "junit_results_variant": custom.get("junit_results_variant")
        or defaults.get("junit_results_variant", "testDebugUnitTest"),
    }
