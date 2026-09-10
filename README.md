# gian-agent-skills

Personal coding skills for Laravel, React, and TypeScript agents.

This repository is **code-only**. It does not include daily work reports, email drafts, CV, LinkedIn, or resume skills.

## Skills

| Skill | Role |
| --- | --- |
| `gian-development-workflow` | Process router (how to approach a task) |
| `gian-how-i-code` | Laravel / React / TypeScript implementation policy |
| `gian-php-style` | Visual PHP formatting (not architecture) |
| `gian-react-ts-style` | Visual TypeScript / TSX formatting (not architecture) |

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

Global install for your user:

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills \
  --skill gian-development-workflow \
  --skill gian-how-i-code \
  --skill gian-php-style \
  --skill gian-react-ts-style \
  -g
```

The repo is installable as soon as it is public. Appearance on [skills.sh](https://skills.sh/GianZapata/gian-agent-skills) is a separate catalog index and may lag or never show up.

## Update

After the first `npx skills add` (so the CLI lock records provenance):

```bash
npx --yes skills@latest update
```

Add a later skill from this repo:

```bash
npx --yes skills@latest add GianZapata/gian-agent-skills --skill <name>
```

## License

Apache-2.0
