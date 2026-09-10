# AGENTS.md

This clone is the source of what is published. Installed copies of these four skills must use the **same wording** as `skills/` here.

## Scope

Publish only:

- `gian-development-workflow`
- `gian-how-i-code`
- `gian-php-style`
- `gian-react-ts-style`

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

## Flow

1. Edit files under `skills/` in this clone.
2. Apply the same edit to the installed copy of that skill.
3. Commit and push.
4. After provenance is in the CLI lock: `npx --yes skills@latest update`.
5. New skill name: `npx --yes skills@latest add GianZapata/gian-agent-skills --skill <name>`.

Do not maintain a hand-made symlink tree between agent skill directories and this clone. Let the CLI install.
