#!/usr/bin/env python3
"""SessionStart hook shared by Claude Code and Codex.

Prepares the workspace (Engram, CodeGraph, skill registry) and reminds the
agent to load gian-development-workflow. Silent outside a dev workspace.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BOOTSTRAP = Path(__file__).resolve().with_name("workspace-bootstrap.py")
REMINDER = (
    "Workspace root: {root}. Engram project `{name}`; CodeGraph and .atl/skill-registry.md live at this root. "
    "Before the first edit on development work, read gian-development-workflow SKILL.md, classify the task, "
    "then read gian-how-i-code SKILL.md and the references its routing matrix marks."
)
MEMORY_PREFIXES = ("Convention:", "Decision:")
MEMORY_LIMIT = 10
RESULT_LINE = re.compile(r"^\[\d+\] #(\d+) \([^)]*\) — (.+)$")


def memory_index(project: str) -> list[str]:
    """Titles saved under the Memoria rule, newest first, as `#id title`."""
    engram = shutil.which("engram")
    if engram is None:
        return []
    entries: dict[str, str] = {}
    for prefix in MEMORY_PREFIXES:
        try:
            result = subprocess.run(
                [engram, "search", prefix.rstrip(":"), "--project", project, "--limit", str(MEMORY_LIMIT)],
                timeout=5,
                capture_output=True,
                text=True,
            )
        except (subprocess.TimeoutExpired, OSError):
            continue
        for line in result.stdout.splitlines():
            match = RESULT_LINE.match(line.strip())
            if match and match.group(2).startswith(MEMORY_PREFIXES):
                entries.setdefault(match.group(1), match.group(2))
    return [f"#{obs_id} {title}" for obs_id, title in list(entries.items())[:MEMORY_LIMIT]]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    cwd = Path(payload.get("cwd") or Path.cwd())
    sys.path.insert(0, str(BOOTSTRAP.parent))
    import importlib.util

    spec = importlib.util.spec_from_file_location("workspace_bootstrap", BOOTSTRAP)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = module.find_root(cwd)
    if root is None:
        return 0
    try:
        subprocess.run(
            [sys.executable, str(BOOTSTRAP), str(root), "--apply", "--quiet"],
            timeout=25,
            capture_output=True,
        )
    except subprocess.TimeoutExpired:
        pass
    print(REMINDER.format(root=root, name=root.name))
    index = memory_index(root.name)
    if index:
        print(
            "Saved project memory (open with mem_get_observation before deciding on these topics): "
            + "; ".join(index)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
