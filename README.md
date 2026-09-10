# gian-agent-skills

Personal coding skills for Laravel, React, and TypeScript agents.

This repository is **code-only**. It does not include daily work reports, email drafts, CV, LinkedIn, or resume skills.

Installed copies and this clone must stay the **same wording**. Do not put host paths, org or client names, or product folder names in skill files.

## Skills

| Skill | Role |
| --- | --- |
| `gian-development-workflow` | Process router (how to approach a task) |
| `gian-how-i-code` | Laravel / React / TypeScript implementation policy |
| `gian-php-style` | Visual PHP formatting (not architecture) |
| `gian-react-ts-style` | Visual TypeScript / TSX formatting (not architecture) |

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

Install the four skills (space form of `--skill`; do not use `--skill=name`):

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills \
  --skill gian-development-workflow \
  --skill gian-how-i-code \
  --skill gian-php-style \
  --skill gian-react-ts-style
```

Global install:

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills \
  --skill gian-development-workflow \
  --skill gian-how-i-code \
  --skill gian-php-style \
  --skill gian-react-ts-style \
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

## Update

After the first `npx skills add` (so the CLI lock records provenance):

```bash
npx --yes skills@latest update
```

`evals/` are not in git. An update can wipe local `evals/` under the installed skill folder.

## License

Apache-2.0
