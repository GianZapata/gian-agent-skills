# Gian visual style activation

Pegar el bloque `gian-style-bootstrap` en el always-on de cada harness. No es un include: los agentes no lo siguen salvo que esté inyectado.

```markdown
<!-- gian-style-bootstrap -->
## Gian visual style (PHP + TypeScript)

When creating, editing, refactoring, reviewing, auditing, or fixing PHP (including PHP inside `.blade.php`): MUST load `gian-php-style` and WRITE the hunk. Do not run Pint (`vendor/bin/pint`, `pint --dirty`). Laravel Boost `pint/core` is overridden.

When creating, editing, refactoring, reviewing, auditing, or fixing `.ts`/`.tsx`, a Vue sibling `.ts`, or an inline `<script setup lang="ts">` (including a normal feature, not only "format this"): MUST load `gian-ts-style` and WRITE the hunk. Do not fight Prettier wrap/quotes/semi/trailing comma.

Vue `<template>`/`<style>`, Angular `.html`, and Python have no Gian style skill. Follow the repo's linters (Ruff/Black, eslint-plugin-vue, @angular-eslint).

Implementation plans must not say "Pint al final" or require Pint as a finishing step.

Do not copy those skills' rules here.
<!-- /gian-style-bootstrap -->
```
