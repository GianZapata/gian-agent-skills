#!/usr/bin/env python3
"""Prepare a development workspace for the agent toolchain.

The workspace root is the folder that holds one or more git repositories
(for example `tienda/` with `tienda-client/` and `tienda-back/`), or the
repository itself when it stands alone. Everything lives at that root:
Engram project, CodeGraph index, `.atl/skill-registry.md` and `.vscode/`.

Usage:
  workspace-bootstrap.py [DIR] [--apply] [--quiet]
  workspace-bootstrap.py --all [SCAN_DIR] [--apply]

--all scans SCAN_DIR (default: $WORKSPACE_SCAN_ROOT, else the current
directory) for workspace roots.

Without --apply it only reports. Every step is idempotent and limited to the
Capability Bootstrap allowlist: no dependency installs, no Serena onboarding,
no CodeGraph upgrade or reindex.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
IGNORE_ENTRIES = (".codegraph/", ".engram/", ".atl/", ".serena/", "graphify-out/")
GLOBAL_IGNORE = HOME / ".config/git/ignore"
MANIFESTS = ("composer.json", "package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml")
SKIP_DIRS = {"node_modules", "vendor", ".git", ".worktrees", "dist", "build"}


def is_repo(path: Path) -> bool:
    return (path / ".git").exists()


def has_manifest(path: Path) -> bool:
    return any((path / name).exists() for name in MANIFESTS)


def child_repos(path: Path) -> list[Path]:
    if not path.is_dir():
        return []
    return sorted(
        child for child in path.iterdir()
        if child.is_dir() and child.name not in SKIP_DIRS and not child.name.startswith(".") and is_repo(child)
    )


def is_submodule(repo: Path) -> bool:
    modules = repo.parent / ".gitmodules"
    if not is_repo(repo.parent) or not modules.exists():
        return False
    return any(line.strip() == f"path = {repo.name}" for line in modules.read_text().splitlines())


def is_workspace(folder: Path) -> bool:
    """A non-repo folder is a workspace only when marked or named after its repos."""
    if folder == HOME or is_repo(folder):
        return False
    repos = child_repos(folder)
    if not repos:
        return False
    marked = (folder / ".engram/config.json").exists() or (folder / ".codegraph").exists()
    if marked or any(folder.glob("*.code-workspace")):
        return True
    prefix = folder.name.lower().removesuffix("-launcher")
    named = [repo for repo in repos if repo.name.lower().startswith((prefix + "-", prefix + "_"))]
    return bool(named) and len(named) * 2 >= len(repos)


def find_root(start: Path) -> Path | None:
    """Return the workspace root that owns `start`, or None outside a project."""
    start = start.resolve()
    if start in (HOME, Path("/")) or HOME not in start.parents:
        return None
    current = start
    while current != HOME and current != current.parent:
        if is_repo(current):
            parent = current.parent
            if is_submodule(current):
                current = parent  # submodule: resolve from the superproject
                continue
            return parent if is_workspace(parent) else current
        if is_workspace(current):
            return current
        current = current.parent
    return None


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    if shutil.which(cmd[0]) is None:
        return 127, f"{cmd[0]} not installed"
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


class Report:
    def __init__(self, root: Path, apply: bool):
        self.root, self.apply, self.lines = root, apply, []

    def add(self, step: str, state: str, detail: str = "") -> None:
        self.lines.append(f"  {step:<10} {state}{(' - ' + detail) if detail else ''}")


def alias_project(output: str) -> str | None:
    try:
        data, _ = json.JSONDecoder().raw_decode(output[output.index("{"):])
        return data.get("aliases", {}).get("project")
    except (ValueError, AttributeError, IndexError):
        return None


def step_engram(root: Path, repos: list[Path], rep: Report) -> None:
    config = root / ".engram/config.json"
    want = {"project_name": root.name}
    current = json.loads(config.read_text()) if config.exists() else None
    if current and current.get("project_name") == root.name:
        rep.add("engram", "ok", root.name)
    elif rep.apply:
        config.parent.mkdir(exist_ok=True)
        config.write_text(json.dumps({**(current or {}), **want}, indent=2) + "\n")
        rep.add("engram", "created", root.name)
    else:
        rep.add("engram", "missing", f"would write {config}")
    for repo in repos:
        if repo == root:
            continue
        code, out = run(["engram", "projects", "alias", "resolve", "--cwd", str(repo)])
        if code == 0 and alias_project(out) == root.name:
            continue
        if rep.apply:
            code, out = run(["engram", "projects", "alias", "set", "--cwd", str(repo), "--project", root.name])
            rep.add("engram", "aliased" if code == 0 else "alias-failed", f"{repo.name} -> {root.name}")
        else:
            rep.add("engram", "unaliased", f"{repo.name} -> {root.name}")


def step_codegraph(root: Path, rep: Report) -> None:
    if (root / ".codegraph").exists():
        rep.add("codegraph", "ok")
    elif shutil.which("codegraph") is None:
        rep.add("codegraph", "skip", "binary missing")
    elif rep.apply:
        log = root / ".codegraph-init.log"
        subprocess.Popen(
            ["codegraph", "init", "--yes"], cwd=root,
            stdout=open(log, "w"), stderr=subprocess.STDOUT, start_new_session=True,
        )
        rep.add("codegraph", "init-started", f"background, log {log.name}")
    else:
        rep.add("codegraph", "missing")


def step_registry(root: Path, rep: Report) -> None:
    if (root / ".atl/skill-registry.md").exists():
        rep.add("registry", "ok")
    elif rep.apply:
        (root / ".atl").mkdir(exist_ok=True)
        code, out = run(["gentle-ai", "skill-registry", "refresh", "--no-gitignore", "--cwd", str(root)])
        code = 0 if (root / ".atl/skill-registry.md").exists() else 1
        rep.add("registry", "created" if code == 0 else "failed", "" if code == 0 else out[-200:])
    else:
        rep.add("registry", "missing")


def step_vscode(root: Path, repos: list[Path], rep: Report) -> None:
    settings = root / ".vscode/settings.json"
    if settings.exists():
        rep.add("vscode", "ok", "existing settings kept")
        return
    if root in repos:
        rep.add("vscode", "skip", "single repo")
        return
    names = [repo.name for repo in repos]
    data = {
        "git.autoRepositoryDetection": True,
        "git.repositoryScanMaxDepth": 1,
        "git.scanRepositories": names,
        "search.exclude": {"**/.worktrees": True, "**/.codegraph": True, "**/graphify-out": True},
        "files.watcherExclude": {"**/.worktrees/**": True, "**/.codegraph/**": True},
    }
    if any((repo / "composer.json").exists() for repo in repos):
        php = next(repo for repo in repos if (repo / "composer.json").exists())
        data["intelephense.environment.includePaths"] = [f"{php.name}/vendor"]
    eslint = [repo.name for repo in repos if (repo / "package.json").exists()]
    if eslint:
        data["eslint.workingDirectories"] = [{"directory": name, "changeProcessCWD": True} for name in eslint]
    if rep.apply:
        settings.parent.mkdir(exist_ok=True)
        settings.write_text(json.dumps(data, indent=2) + "\n")
        rep.add("vscode", "created")
    else:
        rep.add("vscode", "missing")


def step_ignore(repos: list[Path], rep: Report) -> None:
    wanted = list(IGNORE_ENTRIES)
    current = GLOBAL_IGNORE.read_text().splitlines() if GLOBAL_IGNORE.exists() else []
    missing = [entry for entry in wanted if entry not in current]
    if missing and rep.apply:
        GLOBAL_IGNORE.parent.mkdir(parents=True, exist_ok=True)
        prefix = "" if not current or current[-1] == "" else "\n"
        GLOBAL_IGNORE.write_text("\n".join(current) + prefix + "\n".join(missing) + "\n")
        rep.add("gitignore", "global-updated", ", ".join(missing))
    elif missing:
        rep.add("gitignore", "global-missing", ", ".join(missing))
    for repo in repos:
        ignored = []
        for entry in wanted:
            probe = entry.replace("**/", "").rstrip("/") + ("/probe" if entry.endswith("/") else "")
            code, _ = run(["git", "-C", str(repo), "check-ignore", "-q", "--no-index", probe])
            if code != 0:
                ignored.append(entry)
        if ignored and not rep.apply:
            rep.add("gitignore", "not-ignored", f"{repo.name}: {', '.join(ignored)}")


def bootstrap(root: Path, apply: bool) -> Report:
    repos = child_repos(root) or ([root] if is_repo(root) else [])
    rep = Report(root, apply)
    step_engram(root, repos, rep)
    step_codegraph(root, rep)
    step_registry(root, rep)
    step_vscode(root, repos, rep)
    step_ignore(repos, rep)
    return rep


def all_roots(scan: Path) -> list[Path]:
    roots = set()
    for manifest in scan.rglob("*"):
        if manifest.name not in MANIFESTS or any(part in SKIP_DIRS or part.startswith(".") for part in manifest.relative_to(scan).parts[:-1]):
            continue
        if len(manifest.relative_to(scan).parts) > 5:
            continue
        root = find_root(manifest.parent)
        if root:
            roots.add(root)
    return sorted(roots)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    scan = Path(args.dir if args.dir != "." else os.environ.get("WORKSPACE_SCAN_ROOT", ".")).expanduser().resolve()
    roots = all_roots(scan) if args.all else [r for r in [find_root(Path(args.dir))] if r]
    if not roots:
        if not args.quiet:
            print("no workspace root here")
        return 0
    for root in roots:
        rep = bootstrap(root, args.apply)
        if not args.quiet:
            print(root)
            print("\n".join(rep.lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
