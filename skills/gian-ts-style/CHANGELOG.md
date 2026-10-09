# Changelog

## 2.1.0 — 2026-10-09

- `react-component-fc-props` (HARD, solo React): props en `interface Props` local y componente `export const X: FC<Props> = ({ … }) => { return … }`; sin props, `FC`. `import type { FC }`, no `React.FC`. Aplica al componente nuevo o tocado. GAP en genérico, `forwardRef`, `memo` con comparador y lint que prohíbe `FC`. Reemplaza el GAP match-file.

## 2.0.2 — 2026-10-05

- `vertical-spacing`: los slots siguen en `04`. Los casos dentro de cada slot, y el orden de una función plana, los decide `26`. Esta reference solo inserta la línea en blanco.

## 2.0.1 — 2026-10-05

- `vertical-spacing`: la cita del orden sigue a `04`. Efectos al final. Si el edit entra en el cuerpo, `04` reordena esa función. La línea en blanco sigue en el hunk.

## 2.0.0 — 2026-09-30

- Renombrada desde `gian-react-ts-style`. El núcleo es TypeScript y vale en React, Vue, Angular y Node. JSX queda como sección solo React.
- `vertical-spacing`: una línea en blanco entre secciones. Declaraciones cortas del mismo tipo juntas. Sin comentarios de sección.

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
