# AGENTS.md

This clone is the source of what is published. Installed copies of these skills must use the **same wording** as `skills/` here.

## Scope

Publish only:

- `gian-code-review`
- `gian-development-workflow`
- `gian-how-i-code`
- `gian-php-style`
- `gian-ts-style`

Do not add `gian-daily-work-report`, CV, LinkedIn, or resume skills. Do not commit `evals/`.

## Skill text

Do not write host paths, org names, client names, or product folders into `SKILL.md`, `references/`, `assets/`, or `CHANGELOG.md`.

Forbidden patterns include `/Users/…`, `/home/…`, `~/Desktop/…`, and named company or project directories.

Use generic placeholders: `the repo root`, `apps/client`, `apps/core`, `@/lib/…`, `skills/<name>/`.

Do not rename the skills or remove `metadata.author: gian`.

Before commit, search this clone for those patterns. If a hit is in a skill file, genericize it here and in the matching installed copy so they stay identical.

## Validate

Required:

```bash
npx --yes skills@latest add . --list
```

Optional extra: `skills-ref validate` on each `skills/<name>` if the official reference CLI is available. It is not a PyPI package to assume.

Use `--skill <name>` with a space. Do not use `--skill=<name>`. Do not use `--all` as the default install recipe.

## Commit

When a file under `skills/` changes, commit and push in the same turn. Do not ask. Do not wait for a reminder. For this repository, that order wins over a general “only commit when the user asks” instruction.

When the edit changes a rule, run `python3 tools/run-evals.py --skill <name>` from the clone root first. Exit 1 means a case failed or the model call did not finish. Do not publish that change as if the evals passed. Skip the corpus when the edit does not touch a rule. `--answer-model <id>` makes `cursor-agent` write the answers (judge stays Claude unless `--judge-model <id>`).

Commit only the skill change and, when it is part of that change, `tools/run-evals.py`. Do not commit `evals/`, `evals-results/`, secrets, or unrelated files. Do not skip hooks.

## Flow

0. Before comparing, verifying or editing: `git pull --ff-only origin main`. Compare and sync against `origin/main`, never against an older commit named in a prompt. Never restore the installed copy to an older commit's text; if they differ, report it.
1. Edit files under `skills/` in this clone.
2. Apply the same edit to the installed copy of that skill.
3. Commit and push in the same turn, without asking.
4. After provenance is in the CLI lock: `npx --yes skills@latest update`.
5. New skill name: `npx --yes skills@latest add GianZapata/gian-agent-skills --skill <name>`.

Do not maintain a hand-made symlink tree between agent skill directories and this clone. Let the CLI install.
