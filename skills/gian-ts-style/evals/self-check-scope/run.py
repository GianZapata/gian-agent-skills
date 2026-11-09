#!/usr/bin/env python3
"""Local regression runner. Not committed. Creates a temp git repo per case."""

import subprocess
import tempfile
from pathlib import Path

OLD = Path("/tmp/gian-skill-snapshots/clone/skills/gian-ts-style/assets/self-check.mjs")
NEW = Path("/Users/gian/Desktop/Dev/gian-agent-skills/skills/gian-ts-style/assets/self-check.mjs")
NODE_MODULES = Path("/Users/gian/Desktop/Dev/acsyt/elcaba/elcaba-panel-admin/node_modules")


def run_script(repo: Path, script: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["node", str(script), *args],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def init_repo() -> Path:
    root = Path(tempfile.mkdtemp(prefix="self-check-scope-"))
    (root / "package.json").write_text('{"type":"module"}\n')
    (root / "node_modules").symlink_to(NODE_MODULES)
    git(root, "init", "-q")
    git(root, "config", "user.email", "repro@example.com")
    git(root, "config", "user.name", "repro")
    return root


def commit(repo: Path, *files: str) -> None:
    git(repo, "add", *files)
    git(repo, "commit", "-q", "-m", "base")


def show(label: str, before: tuple[int, str], after: tuple[int, str]) -> None:
    print(f"\n## {label}")
    print(f"BEFORE exit={before[0]}")
    print(before[1] or "(empty)")
    print(f"AFTER exit={after[0]}")
    print(after[1] or "(empty)")


def case_pair(name: str, filename: str, base: str, edited: str, args: list[str] | None = None) -> None:
    repo = init_repo()
    path = repo / filename
    path.write_text(base)
    commit(repo, filename)
    path.write_text(edited)
    argv = args if args is not None else [filename]
    show(name, run_script(repo, OLD, argv), run_script(repo, NEW, argv))


def main() -> None:
    component_base = """import type { FC } from 'react';

export const Widget: FC<{ target: string | null }> = ({ target }) => {
  const label = target ?? '';

  if (!target) return null;

  return <p>{label}</p>;
};
"""
    case_pair(
        "component-separated",
        "page.tsx",
        component_base,
        component_base.replace("target ?? ''", "target ?? 'x'"),
    )
    case_pair(
        "component-glued",
        "page.tsx",
        component_base,
        component_base.replace("const label = target ?? '';\n\n  if (!target) return null;", "const label = target ?? '';\n  if (!target) return null;"),
    )

    plain_glued = """export const areaNumber = (value: string | null): number | null => {
  const number = Number(value);
  if (!Number.isFinite(number)) return null;

  return number;
};
"""
    plain_split = """export const areaNumber = (value: string | null): number | null => {
  const number = Number(value);

  if (!Number.isFinite(number)) return null;

  return number;
};
"""
    case_pair("plain-glued", "plain.ts", plain_split, plain_glued)
    case_pair("plain-separated", "plain.ts", plain_glued, plain_split)

    handler_base = """import type { FC } from 'react';

export const Widget: FC = () => {
  const onClick = (event: Event) => {
    const target = event.target;
    if (!target) return;
  };

  return null;
};
"""
    handler_split = handler_base.replace("const target = event.target;\n    if (!target) return;", "const target = event.target;\n\n    if (!target) return;")
    case_pair("handler-glued", "handler.tsx", handler_split, handler_base)
    case_pair("handler-separated", "handler.tsx", handler_base, handler_split)

    memo_base = """import { useMemo } from 'react';

export const useTotal = (value: string) => {
  const total = useMemo(() => {
    const number = Number(value);
    if (!Number.isFinite(number)) return null;

    return number;
  }, [value]);

  return total;
};
"""
    memo_split = memo_base.replace("const number = Number(value);\n    if (!Number.isFinite(number)) return null;", "const number = Number(value);\n\n    if (!Number.isFinite(number)) return null;")
    case_pair("usememo-glued", "memo.ts", memo_split, memo_base)
    case_pair("usememo-separated", "memo.ts", memo_base, memo_split)

    effect_base = """import { useEffect } from 'react';

export const useTitle = (value: string) => {
  useEffect(() => {
    const number = Number(value);
    if (!Number.isFinite(number)) return;

    document.title = String(number);
  }, [value]);
};
"""
    effect_split = effect_base.replace("const number = Number(value);\n    if (!Number.isFinite(number)) return;", "const number = Number(value);\n\n    if (!Number.isFinite(number)) return;")
    case_pair("effect-glued", "effect.ts", effect_split, effect_base)
    case_pair("effect-separated", "effect.ts", effect_base, effect_split)

    class_base = """export class ReportHelper {
  static methodA(value: string): string {
    return value.trim();
  }

  static methodB(value: string): number | null {
    // State


    const number = Number(value);

    if (!Number.isFinite(number)) return null;

    return number;
  }
}
"""
    case_pair(
        "class-touch-A-B-in-HEAD",
        "helper.ts",
        class_base,
        class_base.replace("return value.trim();", "return value.trim().toLowerCase();"),
    )
    case_pair(
        "class-touch-B",
        "helper.ts",
        class_base,
        class_base.replace("return number;", "return number + 0;"),
    )

    members = """export class Box {
  constructor(value: string) {
    const number = Number(value);

    if (!Number.isFinite(number)) return;
  }

  get size(): number | null {
    const number = Number(this.value);
    if (!Number.isFinite(number)) return null;

    return number;
  }

  set size(value: string) {
    const number = Number(value);
    if (!Number.isFinite(number)) return;
  }

  format(value: string): number | null {
    const number = Number(value);
    if (!Number.isFinite(number)) return null;

    return number;
  }

  value = '';
}
"""
    case_pair("member-constructor", "members.ts", members, members.replace("if (!Number.isFinite(number)) return;", "if (!Number.isFinite(number)) return;", 1).replace("const number = Number(value);\n\n    if (!Number.isFinite(number)) return;", "const number = Number(value);\n    if (!Number.isFinite(number)) return;", 1))
    # The constructor case above is messy. Dedicated cases follow.
    for label, old, new in [
        (
            "touch-constructor-only",
            "constructor(value: string) {\n    const number = Number(value);\n\n    if (!Number.isFinite(number)) return;\n  }",
            "constructor(value: string) {\n    const number = Number(value);\n    if (!Number.isFinite(number)) return;\n  }",
        ),
        (
            "touch-getter-only",
            "get size(): number | null {\n    const number = Number(this.value);\n\n    if (!Number.isFinite(number)) return null;\n\n    return number;\n  }",
            "get size(): number | null {\n    const number = Number(this.value);\n    if (!Number.isFinite(number)) return null;\n\n    return number;\n  }",
        ),
        (
            "touch-setter-only",
            "set size(value: string) {\n    const number = Number(value);\n\n    if (!Number.isFinite(number)) return;\n  }",
            "set size(value: string) {\n    const number = Number(value);\n    if (!Number.isFinite(number)) return;\n  }",
        ),
        (
            "touch-method-function-only",
            "format(value: string): number | null {\n    const number = Number(value);\n\n    if (!Number.isFinite(number)) return null;\n\n    return number;\n  }",
            "format(value: string): number | null {\n    const number = Number(value);\n    if (!Number.isFinite(number)) return null;\n\n    return number;\n  }",
        ),
    ]:
        case_pair(label, "members.ts", members, members.replace(old, new, 1))

    ordinary = """export class Fields {
  clean = 1;

  field: { a: string; b: string };
}
"""
    case_pair(
        "ordinary-property",
        "fields.ts",
        ordinary,
        ordinary.replace("{ a: string; b: string }", "{ a: string; b: number }"),
    )
    case_pair(
        "ordinary-property-sibling-untouched",
        "fields.ts",
        ordinary,
        ordinary.replace("clean = 1;", "clean = 2;"),
    )

    const_class = """export const Helper = class {
  static methodA(value: string): string {
    return value.trim();
  }

  static methodB(value: string): number | null {
    const number = Number(value);

    if (!Number.isFinite(number)) return null;

    return number;
  }
};
"""
    case_pair(
        "const-class-touch-A",
        "const-class.ts",
        const_class,
        const_class.replace("return value.trim();", "return value.trim().toLowerCase();"),
    )

    header = """export class Foo extends Bar<{ a: string; b: string }> {
  methodB(value: string): number | null {
    // State


    const number = Number(value);

    if (!Number.isFinite(number)) return null;

    return number;
  }
}
"""
    case_pair(
        "class-header-type",
        "header.ts",
        header,
        header.replace("{ a: string; b: string }", "{ a: string; b: number }"),
    )

    siblings = """import type { FC } from 'react';

export const Widget: FC<{ target: string | null }> = ({ target }) => {
  const label = target ?? '';

  if (!target) return null;

  return <p>{label}</p>;
};

export const Broken: FC = () => {
  const value = 1;
  if (!value) return null;

  return <span>{value}</span>;
};
"""
    case_pair(
        "sibling-component",
        "siblings.tsx",
        siblings,
        siblings.replace("target ?? ''", "target ?? 'z'"),
    )

    nested = """import type { FC } from 'react';

export const Widget: FC<{ target: string | null }> = ({ target }) => {
  const label = target ?? '';

  if (!target) return null;

  return target ? (label ? <p>{label}</p> : null) : null;
};
"""
    case_pair("same-body-nested", "nested.tsx", nested, nested.replace("target ?? ''", "target ?? 'q'"))

    # Two dirty files, no args vs one path.
    repo = init_repo()
    (repo / "helper.ts").write_text(class_base)
    (repo / "plain.ts").write_text(plain_glued)
    commit(repo, "helper.ts", "plain.ts")
    (repo / "helper.ts").write_text(class_base.replace("return value.trim();", "return value.trim().toLowerCase();"))
    (repo / "plain.ts").write_text(plain_split)
    show("two-files-no-args", run_script(repo, OLD, []), run_script(repo, NEW, []))
    show("two-files-one-path", run_script(repo, OLD, ["helper.ts"]), run_script(repo, NEW, ["helper.ts"]))

    # Two methods changed in one file, explicit path: both enter.
    both = class_base.replace("return value.trim();", "return value.trim().toLowerCase();").replace("return number;", "return number + 0;")
    case_pair("same-file-two-methods", "helper.ts", class_base, both, ["helper.ts"])

    # --all and untracked.
    repo = init_repo()
    (repo / "fields.ts").write_text(ordinary)
    (repo / "helper.ts").write_text(class_base)
    commit(repo, "fields.ts", "helper.ts")
    untracked = repo / "extra.ts"
    untracked.write_text(ordinary)
    show("all-explicit", run_script(repo, OLD, ["--all", "fields.ts", "helper.ts"]), run_script(repo, NEW, ["--all", "fields.ts", "helper.ts"]))
    show("untracked", run_script(repo, OLD, ["extra.ts"]), run_script(repo, NEW, ["extra.ts"]))

    meta = """import type { ButtonProps } from '@mui/material/Button';

type Tone = 'recent' | 'critical';

const COLORS: Record<Tone, string> = {
  recent: 'a',
  critical: 'b',
};

const LABELS: Record<Tone, string> = {
  recent: 'Recent label',
  critical: 'Critical label',
};

const button: { a: string; b: string } = { a: '1', b: '2' };

const color: 'warning' | 'error' | 'inherit' = 'warning';
"""
    case_pair("metadata-in-scope", "meta.tsx", meta, meta.replace("recent: 'a'", "recent: 'c'"))
    repo = init_repo()
    (repo / "meta.tsx").write_text(meta)
    show("metadata-all", run_script(repo, OLD, ["--all", "meta.tsx"]), run_script(repo, NEW, ["--all", "meta.tsx"]))


if __name__ == "__main__":
    main()
