# gian-agent-skills

Personal coding skills. The how-i-code core applies to any stack; Laravel, React, and Vue are documented adapters.

This repository is **code-only**. It does not include daily work reports, email drafts, CV, LinkedIn, or resume skills.

Installed copies and this clone must stay the **same wording**. Do not put host paths, org or client names, or product folder names in skill files.

## Skills

| Skill | Role |
| --- | --- |
| `gian-development-workflow` | Process router (how to approach a task) |
| `gian-how-i-code` | Implementation policy. The core applies to any stack; Laravel, React, and Vue are documented adapters |
| `gian-php-style` | Visual PHP formatting (not architecture) |
| `gian-ts-style` | Visual TypeScript / TSX formatting (not architecture) |
| `gian-code-review` | Read-only review of a diff through parallel lenses; runs alongside RDD |
| `admin-dashboard-architect` | Admin panels, tables, forms and dialogs for a new surface; structure and copy rules elsewhere |
| `modern-ui-architect` | Minimal modern UI for prototypes and new screens without an existing identity |

## Layout

```text
skills/<name>/SKILL.md
```

`name` in frontmatter must match the directory: lowercase, hyphens, at most 64 characters, no leading/trailing hyphen, no consecutive `--`.

Copy into a skill folder only:

- `SKILL.md` (required)
- `scripts/`, `references/`, `assets/` (optional)
- `CHANGELOG.md` if it exists

Do **not** copy `evals/` (local-only; can hold private fixtures). Do not add daily-work-report, CV, LinkedIn, or resume skills here.

## What must not appear in skill text

Omit or replace with generic placeholders (`the repo root`, `apps/client`, `apps/core`, `@/lib/…`, `skills/<name>/`):

- Absolute or home paths (`/Users/…`, `/home/…`, `~/Desktop/…`)
- Org, client, or product directories and names
- Staging URLs, Jira IDs, named tenants, snippets from private repos

Keep skill names (`gian-how-i-code`) and `metadata.author: gian`.

## Install

List what the repo contains:

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills --list
```

Install the skills (space form of `--skill`; do not use `--skill=name`):

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills \
  --skill admin-dashboard-architect \
  --skill gian-code-review \
  --skill gian-development-workflow \
  --skill gian-how-i-code \
  --skill gian-php-style \
  --skill gian-ts-style \
  --skill modern-ui-architect
```

Global install:

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills \
  --skill admin-dashboard-architect \
  --skill gian-code-review \
  --skill gian-development-workflow \
  --skill gian-how-i-code \
  --skill gian-php-style \
  --skill gian-ts-style \
  --skill modern-ui-architect \
  -g
```

`--all` is not “all skills in this repo”: it selects every skill, every detected agent, and skips prompts. Do not use it as the default recipe.

The repo is installable as soon as it is public. Appearance on [skills.sh](https://skills.sh/GianZapata/gian-agent-skills) is a separate catalog index and may lag or never show up.

## Add a skill

1. Add `skills/<name>/SKILL.md` (and optional `scripts/`, `references/`, `assets/`).
2. Sanitize the copy (no host paths or org/client text).
3. Required gate:

```bash
npx --yes skills@latest add . --list
```

That must list only the skills that belong in this repo. `skills-ref validate` is extra if you have the official reference implementation; do not assume it is on PyPI.

4. Commit and push.
5. Register the new skill (first-time or new name):

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills --skill <name>
```

## Agent commits

If you change a skill in this repo, commit and push in the same turn. Do not ask first. Do not leave the edit uncommitted for the user to notice.

When the edit changes a rule, run this from the clone root before the commit:

```bash
python3 tools/run-evals.py --skill <name>
```

To have another model write the answers (for example Grok), add `--answer-model <id>` (ids from `cursor-agent --list-models`). The judge stays `claude -p`; `--model` only changes the Claude calls. `--judge-model <id>` grades through `cursor-agent` too, for when Claude is unavailable.

`tools/run-behavior.py` measures application, not description: an agent edits a disposable `git worktree` and the diff is graded.

```bash
python3 tools/run-behavior.py --cases <cases.json> --host grok|cursor|claude --model <id> --repeat 2 --judge-model <id>
```

The cases file holds `repo`, `base`, optional `link` (for example `node_modules`) and `cases` with `prompt`, optional `setup_files`, and the checks `forbid_added`, `require_added`, `require_removed` (regexes on the diff), `require_read`, `commands` and `expect` (judged). Runs take minutes each, so run cases in parallel and keep the cases file outside this repo when it names a client.

That applies to `skills/<name>/` only. Do not commit `evals/` or `evals-results/`. The same order is in `AGENTS.md`.

## Update

After the first `npx skills add` (so the CLI lock records provenance):

```bash
npx --yes skills@latest update
```

`evals/` are not in git. An update can wipe local `evals/` under the installed skill folder.

## License

Apache-2.0
