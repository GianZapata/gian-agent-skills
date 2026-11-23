#!/usr/bin/env python3
"""SessionStart hook shared by Claude Code and Codex.

Prepares the workspace (Engram, CodeGraph, skill registry) and reminds the
agent to load gian-development-workflow. Silent outside a dev workspace.
"""
import json
import subprocess
import sys
from pathlib import Path

BOOTSTRAP = Path(__file__).resolve().with_name("workspace-bootstrap.py")
REMINDER = (
    "Workspace root: {root}. Engram project `{name}`; CodeGraph and .atl/skill-registry.md live at this root. "
    "Before the first edit on development work, read gian-development-workflow SKILL.md, classify the task, "
    "then read gian-how-i-code SKILL.md and the references its routing matrix marks."
)


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
    return 0


if __name__ == "__main__":
    sys.exit(main())
