#!/usr/bin/env python3
"""Run prompt evals of the skills through `claude -p` and grade them with a judge call.

Reads every `skills/<skill>/evals/*.json` file with a `cases` list whose items have
`id`, `prompt` and `expect`. For each case:

1. Answer: `claude -p` in plan mode (no edits), told to load the skill and describe
   what it would do for the prompt. With `--answer-model <id>` the answer comes from
   `cursor-agent -p --mode ask --model <id>` instead (plan mode hides the text in a CreatePlan call); the judge stays `claude -p`.
2. Judge: a second `claude -p` with a JSON schema grades each `expect` item as
   pass / fail with a short reason.

Writes a Markdown report to `evals-results/` (git-ignored) and exits 1 when any
expectation fails. Use `--dry-run` to list cases without calling the model.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "evals-results"

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "expect": {"type": "string"},
                    "pass": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "required": ["expect", "pass", "reason"],
            },
        },
    },
    "required": ["results"],
}

ANSWER_PROMPT = """Load and follow the skill `{skill}` (read its SKILL.md and the references it routes to).
Do not edit files. Describe concretely, step by step, how you would handle this request:
what you read first, which mode or route you choose, which rules apply, and what you produce.

Request:
{prompt}"""

JUDGE_PROMPT = """You grade an agent answer against expectations. Be strict: an expectation
passes only when the answer clearly shows it. Return one result per expectation, in order,
copying the expectation text verbatim.

Request:
{prompt}

Expectations:
{expect}

Answer:
{answer}"""


def load_cases(skill_filter: str | None, case_filter: str | None) -> list[dict]:
    cases = []

    for path in sorted(ROOT.glob("skills/*/evals/*.json")):
        skill = path.parts[-3]

        if skill_filter and skill != skill_filter:
            continue

        data = json.loads(path.read_text())

        for case in data.get("cases", []):
            if not {"id", "prompt", "expect"} <= case.keys():
                continue

            if case_filter and case["id"] != case_filter:
                continue

            cases.append({**case, "skill": skill, "file": path.relative_to(ROOT).as_posix()})

    return cases


def parse_payload(stdout: str) -> dict:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("claude returned no JSON") from error

    if isinstance(payload, list):
        found = None

        for event in reversed(payload):
            if isinstance(event, dict) and event.get("type") == "result":
                found = event
                break

        if found is None:
            raise RuntimeError("claude JSON had no result event")

        payload = found

    if not isinstance(payload, dict):
        raise RuntimeError("claude JSON result was not an object")

    return payload


def claude(prompt: str, args: argparse.Namespace, extra: list[str]) -> dict:
    command = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--max-budget-usd",
        str(args.budget),
        *extra,
    ]

    if args.model:
        command += ["--model", args.model]

    result = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True, timeout=args.timeout)
    raw = result.stdout.strip()

    if not raw:
        raise RuntimeError(result.stderr.strip()[:500] or f"exit {result.returncode}, no JSON output")

    payload = parse_payload(raw)

    if payload.get("is_error") or result.returncode != 0:
        raise RuntimeError(f"{payload.get('subtype')}: {str(payload.get('result'))[:500]}")

    return payload


def judge_results(payload: dict) -> list[dict]:
    structured = payload.get("structured_output")

    if structured is None:
        text = payload.get("result", "")
        structured = json.loads(text[text.find("{"):text.rfind("}") + 1])

    return structured["results"]


def cursor_agent_text(prompt: str, model: str, args: argparse.Namespace) -> str:
    command = ["cursor-agent", "-p", "--mode", "ask", "--trust", "--model", model, "--output-format", "text", prompt]
    result = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True, timeout=args.timeout)
    text = result.stdout.strip()

    if result.returncode != 0 or not text:
        raise RuntimeError(result.stderr.strip()[:500] or f"cursor-agent exit {result.returncode}, no output")

    return text


def cursor_answer(prompt: str, args: argparse.Namespace) -> str:
    return cursor_agent_text(prompt, args.answer_model, args)


JUDGE_JSON_HINT = """

Reply with only a JSON object: {"results": [{"expect": "<text>", "pass": true, "reason": "<short>"}]}"""


def cursor_judge(prompt: str, args: argparse.Namespace) -> dict:
    return {"result": cursor_agent_text(prompt + JUDGE_JSON_HINT, args.judge_model, args)}


def run_case(case: dict, args: argparse.Namespace) -> dict:
    answer_prompt = ANSWER_PROMPT.format(skill=case["skill"], prompt=case["prompt"])

    if args.answer_model:
        answer = cursor_answer(answer_prompt, args)
    else:
        answer = claude(answer_prompt, args, ["--permission-mode", "plan"])["result"]

    judge_prompt = JUDGE_PROMPT.format(
        prompt=case["prompt"],
        expect="\n".join(f"- {item}" for item in case["expect"]),
        answer=answer,
    )

    if args.judge_model:
        judged = cursor_judge(judge_prompt, args)
    else:
        judged = claude(judge_prompt, args, ["--json-schema", json.dumps(JUDGE_SCHEMA), "--tools", ""])

    return {**case, "answer": answer, "results": judge_results(judged)}


def report(outcomes: list[dict]) -> str:
    passed = sum(item["pass"] for outcome in outcomes for item in outcome.get("results", []))
    total = sum(len(outcome["expect"]) for outcome in outcomes)
    lines = [f"# Skill evals — {datetime.now():%Y-%m-%d %H:%M}", "", f"**{passed}/{total} expectations passed.**", ""]

    for outcome in outcomes:
        lines += [f"## {outcome['skill']} · {outcome['id']}", "", f"`{outcome['file']}`", ""]

        if "error" in outcome:
            lines += [f"ERROR: {outcome['error']}", ""]

            continue

        for item in outcome["results"]:
            lines.append(f"- {'PASS' if item['pass'] else 'FAIL'} {item['expect']} — {item['reason']}")

        lines += ["", "<details><summary>Answer</summary>", "", outcome["answer"], "", "</details>", ""]

    return "\n".join(lines)


def self_test() -> None:
    event = {"type": "result", "result": "ok", "is_error": False}
    assert parse_payload(json.dumps(event))["result"] == "ok"
    assert parse_payload(json.dumps([{"type": "system"}, event]))["result"] == "ok"

    try:
        parse_payload(json.dumps([{"type": "system"}]))
    except RuntimeError as error:
        if "no result event" not in str(error):
            raise
    else:
        raise RuntimeError("a stream without a result event was accepted")

    graded = judge_results({
        "structured_output": {"results": [{"expect": "a", "pass": True, "reason": "shown"}]},
    })
    assert graded[0]["pass"] is True

    embedded = judge_results({
        "result": 'noise {"results": [{"expect": "a", "pass": false, "reason": "no"}]} tail',
    })
    assert embedded[0]["pass"] is False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill", help="only this skill directory name")
    parser.add_argument("--case", help="only this case id")
    parser.add_argument("--model", help="model for both calls (default: claude default)")
    parser.add_argument("--answer-model", help="answer with this model through `cursor-agent` (judge stays claude)")
    parser.add_argument("--judge-model", help="grade with this model through `cursor-agent` instead of claude")
    parser.add_argument("--cwd", default=str(ROOT), help="directory the answer runs in (a fixture repo)")
    parser.add_argument("--budget", type=float, default=3.0, help="max USD per claude call")
    parser.add_argument("--timeout", type=int, default=600, help="seconds per claude call")
    parser.add_argument("--dry-run", action="store_true", help="list cases without calling claude")
    parser.add_argument("--self-test", action="store_true", help="check payload parsing without calling claude")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("self-test ok")

        return 0

    cases = load_cases(args.skill, args.case)

    if not cases:
        print("No cases matched.")

        return 2

    if args.dry_run:
        for case in cases:
            print(f"{case['skill']}\t{case['id']}\t{len(case['expect'])} expectations")

        print(f"{len(cases)} cases, {2 * len(cases)} claude calls")

        return 0

    outcomes = []

    for case in cases:
        print(f"→ {case['skill']} · {case['id']}", flush=True)

        try:
            outcomes.append(run_case(case, args))
        except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as error:
            outcomes.append({**case, "error": str(error)})

    RESULTS.mkdir(exist_ok=True)
    tag = f"-{args.answer_model}" if args.answer_model else ""
    tag += f"-judge-{args.judge_model}" if args.judge_model else ""
    path = RESULTS / f"{datetime.now():%Y%m%d-%H%M%S}{tag}.md"
    path.write_text(report(outcomes))

    failed = [
        outcome for outcome in outcomes
        if "error" in outcome or not all(item["pass"] for item in outcome["results"])
    ]

    print(report(outcomes).splitlines()[2])
    print(f"Report: {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
