---
name: gian-ts-style
description: "Mandatory visual TS/TSX style for any TS stack. Load when creating, editing, refactoring, reviewing, auditing, or fixing .ts/.tsx or a Vue script setup in TS, incl. a normal feature. Not for consult-only architecture questions. Governs syntax/format only; Prettier owns wrap/quotes/semi."
license: Apache-2.0
metadata:
  author: gian
  version: "2.2.0"
when-to-use: "Any .ts/.tsx create/edit/refactor/review/audit/fix in any TS stack (React, Vue sibling .ts or inline script setup lang=ts, Angular, Node); ts-style-audit; ts-style-fix; format TypeScript. Not for .js/.jsx/.mjs/.cjs, Vue template/style, Angular .html, PHP, CSS, SQL-only, or architecture-only consults."
---

# gian-ts-style

Fuente de verdad única del **estilo visual TypeScript**. El núcleo vale en React, Vue, Angular y Node. Las reglas de JSX son solo React. No es arquitectura, enums, React Query, RHF/Zod ni molde de feature (`gian-how-i-code`). No es Prettier.

## Activation Contract

Cargar al crear, editar, refactorizar, revisar, auditar o corregir **TypeScript real** (`.ts` / `.tsx`), también en una tarea normal (“agrega un filtro”) — no solo si el usuario pide format/audit. No omitir por extensión.

Aplica en cualquier stack TS:

- Vue (hermano `.ts` y `<script setup lang="ts">` inline): no aplican las reglas de JSX ni `react-component-*`. `<template>` y `<style>` no son de esta skill.
- Angular: clases, decoradores y DI son GAP o `LIBRARY_OWNED` (`gian-how-i-code` `01`). El `.html` no es de esta skill.
- Node: las funciones libres siguen `exported-arrow-default`; las clases de Nest/Express son GAP.
- No aplica a `.js`, `.jsx`, `.mjs` ni `.cjs`.

No reformatear: PHP, CSS, JSON de i18n, SQL, Markdown. Preservar directives (`@ts-expect-error`, `eslint-disable`, `prettier-ignore`).

No cargar para CSS, PHP, SQL aislado, o conversación sin TS. Arquitectura (“enum o union”, “dónde va la mutation”) → `gian-how-i-code`.

## Layers

| Layer | Meaning | Audit |
|---|---|---|
| HARD / OVERRIDE | Gian Style; gana a baseline | FAIL; WRITE/FIX aplican si SAFE |
| PREFERENCE | Gian Style deliberado | FAIL sólo si es objetivamente determinable |
| BASELINE | TS/React razonable si esta skill no especifica | FAIL solo si viola HARD |
| NEUTRAL | quotes, indent, semi, trailing comma, printWidth | MUST NOT FAIL / MUST NOT rewrite-only |
| GAP | semántica dudosa / heurística frágil | MUST NOT FAIL; NEVER AUTOFIX |

Precedencia: **instrucción explícita del usuario > HARD gian-ts-style > ESLint/Prettier ya activos del repo > PREFERENCE > baseline**.

No vender preferencias de Gian como best practice universal. `references/principles.md`.

## Hard Rules

- WRITE/FIX **corrigen** el hunk; no se limitan a reportar. AUDIT no edita. `references/principles.md`
- Alcance: código nuevo + **hunk/función tocada**. No migrar el archivo ni el repo. `references/principles.md`
- Wrapping mecánico: Prettier manda. No pelear printWidth/quotes/semi/trailing comma/JSX wrap. `references/prettier-eslint-boundary.md`
- Exported arrow default. `function` solo overload/hoisting/API real. `references/functions-arrows.md`
- No-component + una expresión → implicit return (object literal `({ })`). `references/functions-arrows.md`
- Solo React: componente PascalCase → block body + `return` explícito. Props: `interface Props` local + `export const X: FC<Props> = ({ … }) => { return … }`; sin props, `FC`. Boolean JSX `={true}` → shorthand. Fragment sin key → `<>`. Empty JSX → self-closing. `references/react-components-jsx.md`
- Solo React: `className` no estático (template literal, `+`, ternario, join, prop `className`) → `cn()` del repo en el hunk. No crear otro `cn` ni importar `clsx`/`twMerge` directo. `rg` de cierre sobre los `.tsx` tocados. `references/react-components-jsx.md`
- Single-statement-if standalone (return/throw/call/assignment/continue/break) sin `{}`; líneas ≠ statements. `references/conditions-guards.md`
- Solo React: handler con firma 1:1 → referencia directa. `references/callbacks-handlers.md`
- Secciones de un composable, hook o componente: una línea en blanco entre grupos; declaraciones cortas del mismo tipo juntas. Sin comentarios de sección. `references/vertical-spacing.md`
- Type-only import → `import type`. `references/types-imports.md`
- Comentarios: WRITE no emite narración/JSDoc. Strip ruido obvio. Conservar directives. `references/comments.md`

## Decision Gates

| Situación | Acción |
|---|---|
| Crear o editar `.ts`/`.tsx` por cualquier motivo | WRITE sobre el **hunk/función tocada**. HARD. Aplicar HARD/PREFERENCE y SAFE FIX de ese alcance. No recorrer el archivo/repo |
| `arrow { return x }`, boolean `={true}`, fragment, self-closing, type-only import, wrapper `() => onClose()`, if standalone una statement | WRITE/FIX aplicar (SAFE FIX) |
| if/else compacto, single-statement multilínea, ternary→`&&`, nested ternary, `type` object shape → interface | FIX solo con gate; si duda → GAP |
| nested if+else, dangling-else, guard rewrite con side effects, spread entity/DTO, `= []` en detail, why-comment, `renderFoo` ambiguo | NEVER AUTOFIX; registrar GAP |
| Auditar estilo / ts-style-audit | AUDIT: no editar; solo FAIL reales |
| Corregir formato / ts-style-fix | FIX: solo estilo seguro; listar omitidos |
| Wrap/quotes/indent que Prettier reimprime | ignorar (PRETTIER_OWNED) |
| `className` con template literal, `+`, ternario, join o prop `className` | WRITE/FIX `cn()` del repo en el hunk. GAP si el repo no tiene `cn` |
| Firma de componente React | WRITE/FIX `interface Props` + `FC<Props>` en el componente tocado. GAP: genérico, `forwardRef`, `memo` con comparador, lint que prohíbe `FC` |

## Execution Steps

1. Anunciar modo: WRITE, AUDIT o FIX.
2. Cargar solo `references/` de las reglas tocadas.
3. WRITE: HARD/PREFERENCE en código nuevo y hunk tocado; SAFE FIX de inconsistencias **en ese alcance**; no comentarios nuevos; no tocar el resto del archivo.
4. WRITE en `.tsx` React: antes de cerrar, el `rg` de `classname-cn` sobre los archivos tocados; corregir cada coincidencia del hunk.
5. AUDIT: TS/TSX relevante; alta confianza; agrupar repeticiones; formato `assets/audit-template.md`.
6. FIX: solo estilo; SAFE FIX siempre; AST-SENSITIVE solo con gate; NEVER AUTOFIX si puede cambiar semántica; listar GAP omitidos.
7. No migrar un repo entero salvo audit+fix pedido.

## Output Contract

- WRITE: TS/TSX del hunk conforme; Prettier del repo intacto como autoridad de wrap; sin instalar ESLint.
- AUDIT: lista `[FAIL] path:line` + `Rule:` o `Rules:` + Actual + Expected + Reason; o "no findings".
- FIX: archivos tocados + reglas aplicadas + ítems inseguros omitidos (`GAP — no corregido automáticamente: …`).

## References

- `references/principles.md`
- `references/prettier-eslint-boundary.md`
- `references/functions-arrows.md`
- `references/conditions-guards.md`
- `references/react-components-jsx.md`
- `references/expressions-ternaries.md`
- `references/callbacks-handlers.md`
- `references/types-imports.md`
- `references/access-destructuring.md`
- `references/comments.md`
- `references/vertical-spacing.md`
- `assets/audit-template.md`
- `evals/trigger-evals.json`
- `evals/behavioral-evals.json`
