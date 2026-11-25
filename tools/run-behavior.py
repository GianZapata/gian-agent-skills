#!/usr/bin/env python3
"""Run behavior evals: a coding agent edits a disposable worktree and the diff is graded.

`run-evals.py` checks that a model can describe a rule. This runner checks that it applies
the rule while editing code.

Cases file (JSON, kept outside this repo when it names a client):

    {"repo": "/path/to/git/repo", "base": "<commit>", "link": ["node_modules"],
     "cases": [{"id": "X-1", "prompt": "...",
                "setup_files": {"docs/spec.md": "..."},
                "forbid_added": ["regex on added diff lines"],
                "require_added": ["regex"], "require_removed": ["regex"],
                "require_read": ["substring of a path or command the agent had to touch"],
                "commands": ["npx tsc --noEmit"],
                "expect": ["judged against the diff and the final answer"]}]}

Hosts: `grok` (grok -p), `cursor` (cursor-agent -p --force), `claude` (claude -p).
Each run gets its own `git worktree` in a temp dir that is removed afterwards.
Reports go to `evals-results/` (git-ignored). Exit code 1 when any check fails.
"""

import argparse
import atexit
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "evals-results"

JUDGE_PROMPT = """You grade a coding agent. Be strict: an expectation passes only when the diff
or the final answer clearly shows it. Return one result per expectation, in order.

Task given to the agent:
{prompt}

Expectations:
{expect}

Diff:
{diff}

Final answer:
{answer}

Reply with only a JSON object: {{"results": [{{"expect": "<text>", "pass": true, "reason": "<short>"}}]}}"""


def sh(command: list[str] | str, cwd: Path, timeout: int = 600, shell: bool = False, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout, shell=shell, env=env)


SKILLS = ["gian-how-i-code", "gian-development-workflow"]


def baseline_env(args: argparse.Namespace) -> dict | None:
    """Make the agent see the skills of `--baseline <ref>` instead of the installed ones.

    cursor and claude honour HOME, so they get a throwaway home. grok ignores HOME, so its
    installed skills are swapped in place and restored on exit.
    """
    if not args.baseline:
        return None

    if args.host != "grok":
        home = sh([sys.executable, "-I", str(ROOT / "tools" / "baseline-home.py"), "--ref", args.baseline], ROOT).stdout.strip()
        atexit.register(shutil.rmtree, home, True)

        return {**os.environ, "HOME": home}

    store = Path.home() / ".agents" / "skills"
    backup = Path(tempfile.mkdtemp(prefix="skills-backup-"))
    stage = Path(sh([sys.executable, "-I", str(ROOT / "tools" / "baseline-home.py"), "--ref", args.baseline], ROOT).stdout.strip())

    def restore() -> None:
        for skill in SKILLS:
            if (backup / skill).exists():
                shutil.rmtree(store / skill, ignore_errors=True)
                shutil.move(str(backup / skill), store / skill)

        shutil.rmtree(stage, ignore_errors=True)
        shutil.rmtree(backup, ignore_errors=True)

    atexit.register(restore)

    for skill in SKILLS:
        shutil.move(str(store / skill), backup / skill)
        shutil.copytree(stage / ".agents" / "skills" / skill, store / skill)

    return None


def agent_command(args: argparse.Namespace, prompt: str, wt: Path) -> list[str]:
    model = ["-m", args.model] if args.model and args.host == "grok" else ["--model", args.model] if args.model else []

    if args.host == "grok":
        return ["grok", "-p", prompt, "--cwd", str(wt), "--always-approve", "--no-memory", "--max-turns", str(args.max_turns),
                "--output-format", "streaming-json", *model]

    if args.host == "cursor":
        return ["cursor-agent", "-p", "--force", "--trust", "--output-format", "stream-json", *model, prompt]

    return ["claude", "-p", prompt, "--permission-mode", "bypassPermissions", "--output-format", "stream-json", "--verbose", *model]


def parse_stream(raw: str) -> tuple[str, str]:
    """Return (tool-call blob, final answer text) from a host's JSON-lines stream."""
    tools, text = [], []

    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        kind = event.get("type")

        if kind == "tool_call" and event.get("subtype") in (None, "started"):
            tools.append(json.dumps(event, ensure_ascii=False))
        elif kind == "text" and isinstance(event.get("data"), str):
            text.append(event["data"])
        elif kind == "assistant":
            for part in event.get("message", {}).get("content", []):
                if part.get("type") == "tool_use":
                    tools.append(json.dumps(part, ensure_ascii=False))
                elif part.get("type") == "text":
                    text.append(part.get("text", "") + "\n")

    return "\n".join(tools), "".join(text).strip()


def diff_lines(patch: str) -> tuple[list[str], list[str]]:
    added = [line[1:] for line in patch.splitlines() if line.startswith("+") and not line.startswith("+++")]
    removed = [line[1:] for line in patch.splitlines() if line.startswith("-") and not line.startswith("---")]

    return added, removed


def judge(case: dict, patch: str, answer: str, args: argparse.Namespace) -> list[dict]:
    prompt = JUDGE_PROMPT.format(
        prompt=case["prompt"],
        expect="\n".join(f"- {item}" for item in case["expect"]),
        diff=patch[:60000],
        answer=answer[:6000],
    )

    if args.judge_model:
        command = ["cursor-agent", "-p", "--mode", "ask", "--trust", "--model", args.judge_model, "--output-format", "text", prompt]
    else:
        command = ["claude", "-p", prompt, "--tools", ""]

    out = sh(command, ROOT, args.timeout).stdout
    start, end = out.find("{"), out.rfind("}")

    if start < 0 or end < 0:
        raise RuntimeError(f"judge returned no JSON: {out[:200]}")

    return json.loads(out[start:end + 1])["results"]


def check(label: str, passed: bool, reason: str = "") -> dict:
    return {"check": label, "pass": passed, "reason": reason}


def run_once(case: dict, spec: dict, args: argparse.Namespace) -> dict:
    repo = Path(spec["repo"]).expanduser()
    scratch = Path(tempfile.mkdtemp(prefix="behavior-"))
    wt = scratch / "wt"
    checks, patch, answer, error = [], "", "", None

    try:
        added = sh(["git", "worktree", "add", "--detach", str(wt), spec["base"]], repo)

        if added.returncode:
            raise RuntimeError(f"git worktree add failed: {added.stderr.strip()[:300]}")

        for name in spec.get("link", []):
            if (repo / name).exists():
                (wt / name).symlink_to(repo / name)

        for rel, content in case.get("setup_files", {}).items():
            target = wt / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)

        sh("git add -A", wt, shell=True)
        sh(["git", "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "seed", "--allow-empty"], wt)
        seed = sh(["git", "rev-parse", "HEAD"], wt).stdout.strip()

        run = sh(agent_command(args, case["prompt"], wt), wt, args.timeout, env=args.env)
        raw = run.stdout
        tools, answer = parse_stream(raw)

        if not raw.strip():
            raise RuntimeError(run.stderr.strip()[:400] or f"{args.host} exit {run.returncode}, no output")

        sh("git add -A", wt, shell=True)
        patch = sh(["git", "diff", "--cached", seed, "--", ".", ":(exclude)node_modules"], wt).stdout
        added, removed = diff_lines(patch)

        for rx in case.get("forbid_added", []):
            hits = [line.strip()[:100] for line in added if re.search(rx, line)]
            checks.append(check(f"forbid_added {rx}", not hits, "; ".join(hits[:3])))

        for rx in case.get("require_added", []):
            checks.append(check(f"require_added {rx}", any(re.search(rx, line) for line in added)))

        for rx in case.get("require_removed", []):
            checks.append(check(f"require_removed {rx}", any(re.search(rx, line) for line in removed)))

        for needle in case.get("require_read", []):
            checks.append(check(f"require_read {needle}", needle in tools))

        for command in case.get("commands", []):
            done = sh(command, wt, 900, shell=True)
            checks.append(check(f"command {command}", done.returncode == 0, (done.stdout + done.stderr).strip()[-200:]))

        if case.get("expect") and (patch.strip() or answer.strip()):
            for item in judge(case, patch or "(the agent made no file changes)", answer, args):
                checks.append(check(f"expect {item['expect']}", bool(item["pass"]), item.get("reason", "")))
        elif case.get("expect"):
            checks.extend(check(f"expect {item}", False, "no diff and no answer") for item in case["expect"])

        if args.keep:
            print(f"kept {scratch}", file=sys.stderr)
    except Exception as exc:  # one failed run must not stop the matrix
        error = str(exc)
    finally:
        if not args.keep:
            sh(["git", "worktree", "remove", "--force", str(wt)], repo)
            shutil.rmtree(scratch, ignore_errors=True)

    return {"checks": checks, "patch": patch, "answer": answer, "error": error}


def report(rows: list[dict], args: argparse.Namespace) -> str:
    lines = [f"# Behavior evals ({args.host} {args.model or 'default'})", ""]
    total = failed = 0

    for row in rows:
        stats: dict[str, list[bool]] = {}

        for run in row["runs"]:
            for item in run["checks"]:
                stats.setdefault(item["check"], []).append(item["pass"])

        lines.append(f"## {row['id']}")

        for index, run in enumerate(row["runs"], 1):
            if run["error"]:
                lines.append(f"- run {index}: ERROR {run['error']}")

        for label, results in stats.items():
            total += len(results)
            failed += results.count(False)
            lines.append(f"- {'PASS' if all(results) else 'FAIL'} {sum(results)}/{len(results)} {label}")

        for index, run in enumerate(row["runs"], 1):
            for item in run["checks"]:
                if not item["pass"] and item["reason"]:
                    lines.append(f"  - run {index} {item['check']}: {item['reason']}")

        lines.append("")

    lines.append(f"Checks failed: {failed}/{total}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cases", required=True, help="cases JSON file")
    parser.add_argument("--case", help="only this case id")
    parser.add_argument("--host", choices=["grok", "cursor", "claude"], default="grok")
    parser.add_argument("--model", help="model id for the host")
    parser.add_argument("--judge-model", help="grade `expect` through cursor-agent with this model (default: claude)")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--max-turns", type=int, default=40)
    parser.add_argument("--timeout", type=int, default=1500, help="seconds per agent run")
    parser.add_argument("--baseline", metavar="REF", help="run with the skills of this git ref of this repo instead of the installed ones")
    parser.add_argument("--keep", action="store_true", help="keep the worktrees")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec = json.loads(Path(args.cases).read_text())
    cases = [case for case in spec["cases"] if not args.case or case["id"] == args.case]

    if args.dry_run:
        for case in cases:
            print(f"{case['id']}: {case['prompt'][:80]}")

        return 0

    args.env = baseline_env(args)
    rows = []

    for case in cases:
        runs = []

        for number in range(args.repeat):
            print(f"{case['id']} run {number + 1}/{args.repeat}", file=sys.stderr, flush=True)
            runs.append(run_once(case, spec, args))

        rows.append({"id": case["id"], "runs": runs})

    text = report(rows, args)
    RESULTS.mkdir(exist_ok=True)
    tag = f"{args.host}-{(args.model or 'default').replace('/', '_')}" + ("-baseline" if args.baseline else "")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (RESULTS / f"behavior-{tag}-{stamp}.md").write_text(text)
    (RESULTS / f"behavior-{tag}-{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    print(text)

    return 1 if "FAIL" in text or "ERROR" in text else 0


if __name__ == "__main__":
    sys.exit(main())
