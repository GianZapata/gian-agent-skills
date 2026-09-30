# Changelog

## 1.1.0 — 2026-09-30

- Alcance: cualquier stack TS. Vue (hermano `.ts` y `<script setup lang="ts">`) sin reglas JSX ni `react-component-*`; Angular: clases, decoradores y DI son GAP o `LIBRARY_OWNED`; Node: funciones libres con `exported-arrow-default`, clases Nest/Express GAP. `.js`/`.jsx`/`.mjs`/`.cjs` fuera.
- `access-destructuring`: Vue usa `const props = defineProps<Props>()` y `const emit = defineEmits<Emits>()` sin destructurar.
- `derived-multi-branch`: solo define la forma (cadena de `if` con `return`). `useMemo`/`computed` lo decide `gian-how-i-code` `23`.
- `prettier-eslint-boundary`: no pelear ni instalar `eslint-plugin-vue` ni `@angular-eslint`.

## 1.0.1 — 2026-08-17

- Description: visual-format work vs consult-only architecture/policy. No change to WRITE/AUDIT/FIX rules.

## 1.0.0 — 2026-08-13

- Skill canónica de sintaxis/estilo TS/TSX. Autoridad visual; no arquitectura (`gian-how-i-code`).
- Modos WRITE / AUDIT / FIX espejo de `gian-php-style`: WRITE/FIX corrigen el hunk; AUDIT no edita.
- SAFE FIX vs AST-SENSITIVE (gate) vs NEVER AUTOFIX/GAP.
- Prettier manda wrapping mecánico. No instalar ni reconfigurar ESLint.
