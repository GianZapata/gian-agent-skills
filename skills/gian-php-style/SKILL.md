---
name: gian-php-style
description: "Mandatory visual PHP/Laravel style. Load whenever creating, editing, refactoring, reviewing, auditing, or fixing PHP (incl. PHP inside .blade.php). Overrides Laravel Boost pint/core: do not run Pint. Governs formatting only, not architecture."
license: Apache-2.0
metadata:
  author: gian
  version: "1.2.0"
when-to-use: "Any PHP create/edit/refactor/review/audit/fix; Laravel Boost pint; format PHP; php-style-audit; php-style-fix. Not for CSS, TypeScript, SQL-only, or conversation without PHP."
---

# gian-php-style

Fuente de verdad única del **estilo visual/formato PHP**. No es arquitectura, tipos, ni molde Laravel (`gian-how-i-code`). No es una skill de Blade/HTML.

## Activation Contract

Cargar al crear, editar, refactorizar, revisar, auditar o corregir **PHP real** (incl. Laravel), también dentro de `.blade.php`: Livewire 4 SFC (`new class extends Component`), `<?php ... ?>`, `@php ... @endphp`. No omitir por extensión.

No reformatear: HTML, Blade (`@if`, `{{ }}`, directives), `wire:*`, Alpine, JavaScript, CSS. Preservar el envelope del template.

No cargar para CSS, TypeScript, React, SQL aislado, o conversación sin PHP.

## Layers

| Layer | Meaning | Audit |
|---|---|---|
| HARD / OVERRIDE | Gian Style; gana a baseline y a convención de proyecto | FAIL |
| PREFERENCE | Gian Style deliberado | FAIL sólo si es objetivamente determinable; heurísticas de wrapping → GAP |
| BASELINE | PHP moderno razonable si esta skill no especifica | FAIL solo si viola HARD |
| NEUTRAL | p. ej. `declare(strict_types=1)` ausente | MUST NOT FAIL / MUST NOT rewrite-only |

Precedencia: **instrucción explícita del usuario > HARD gian-php-style > convención de proyecto > baseline**. Laravel Boost `pint/core` (correr Pint al finalizar) queda anulado: WRITE no corre Pint.

Overrides y enforcement (`AUTOFIXABLE` / `AGENT-ENFORCED` / `DELIBERATE-OVERRIDE`): `references/overrides.md`.

## Hard Rules

- Indent: 4 espacios; nunca tabs. `references/principles.md`
- Constructs: `if ($x)` con espacio tras keyword, sin espacios internos en `()`. `elseif` no `else if`. `references/conditions.md`
- Negación: `!$x` nunca `! $x`. `references/conditions.md`
- Single-statement-if: `if` standalone + una statement aprobada (`return`/`throw`/`continue`/`break`/assignment/call) → sin `{}` **solo si el body cabe en una línea física**. Body multilínea → `{}` obligatorias. OVERRIDE. `references/conditions.md`
- Booleanos multilínea: `&&` / `||` terminan la línea anterior, toda expresión. OVERRIDE. `references/conditions.md`
- Condición de control multilínea: primer operando en la línea siguiente; `)` al nivel de la keyword; luego `{` o la statement compacta. `references/conditions.md`
- Continuación: `} elseif (` / `} else {` / `} catch (` / `} finally {` en la misma línea. `references/conditions.md`
- Braces de clase/método/control/anonymous class en la misma línea; método/clase/ctor vacío `{}` compacto. OVERRIDE. `references/classes-functions.md`
- Delimitadores multilínea: contenido +1; cierre al nivel de quien abrió. Un param sin promotion → una línea (`single-param-signature`). 2+ y ya multilínea → uno por línea. `references/calls-arguments.md` `references/classes-functions.md`
- Promoted constructor: si `__construct` tiene ≥ 1 param promovido → multilínea (`promoted-constructor-multiline`). OVERRIDE sobre `single-param-signature`. `references/classes-functions.md`
- Multiline trailing comma: obligatoria en listas multilínea; no decide single-line. `references/principles.md`
- Modifier order: orden canónico PER-CS. `references/modifiers.md`
- Attributes sin args: `#[Foo]` no `#[Foo()]`. `references/attributes.md`
- Una property/const por sentencia. `references/classes-functions.md`
- Entre métodos de clase: exactamente una línea vacía (metadata del siguiente método incluido). `references/vertical-spacing.md`
- Arrays multilínea: alinear `=>` entre hermanos del mismo nivel. Match: región propia. `references/delimiters-arrays.md`
- Validation Laravel 2+ reglas → una por línea (`laravel-validation-rule-array`). HARD. `references/delimiters-arrays.md`
- Comentarios / PHPDoc: no emitir; strip PHPDoc y comentarios fuera de cuerpo; intra-cuerpo útil se conserva. `references/principles.md`
- Named args: `name: $value` sin pad de `:`. `references/calls-arguments.md`
- Chains largas: `->` inicia continuación. `references/chains.md`
- Concat: espacios alrededor de `.`. Ternario: `?` / `:` inician línea. `??` y union/intersection `|` `&`: operador termina la línea anterior. `references/expressions.md`
- Arrow: `fn($x)` no `fn ($x)`; `=>` multilínea termina la firma. `references/expressions.md`
- Bloques lógicos / switch cases: una línea en blanco. `references/vertical-spacing.md`
- Heredoc/nowdoc, `declare(strict_types=1)` (no añadir), sintaxis alternativa PHP: preservar. `references/principles.md`
- Corto y legible → inline. Largo → multilínea geométrica. Sin límite rígido 80/100/120 salvo el proyecto.

## Decision Gates

| Situación | Acción |
|---|---|
| Escribir PHP nuevo o editar PHP por cualquier motivo | WRITE sobre el **hunk/método tocado** (PHP real, incl. región PHP de `.blade.php`). HARD. Sin comentarios/PHPDoc nuevos. Un parámetro sin promotion → firma en una línea. Promoted ctor → multilínea. No reformatear Blade/HTML. No Pint |
| PHPDoc o comentario fuera de cuerpo | AUDIT FAIL `comments-phpdoc`; FIX/WRITE borrar en el hunk |
| Comentario intra-cuerpo que narra el código | FAIL si es obvio; borrar. Dudoso → GAP; conservar |
| Comentario intra-cuerpo con porqué no obvio | conservar; no FAIL. WRITE no añadir uno nuevo |
| `if` compacto inseguro (else-chain, nested if, dangling-else) | no quitar `{}`; GAP / omitir |
| `if` unbraced con body multilínea (una statement aprobada) | FAIL `single-statement-if`; FIX: añadir `{}` |
| Auditar estilo / php-style-audit | AUDIT: no editar; solo FAIL reales |
| Corregir formato / php-style-fix | FIX: solo estilo; si puede cambiar semántica → no aplicar |
| Lista multilínea sin trailing comma | FAIL `multiline-trailing-comma`; FIX: añadir comma |
| Legibilidad inline vs wrap dudosa | no FAIL (GAP); no verticalizar por costumbre |
| ast-grep útil (if/return/calls) | usarlo; whitespace/`=>`/`!$x`/indent → texto |

## Execution Steps

1. Anunciar modo: WRITE, AUDIT o FIX.
2. Cargar solo `references/` de las reglas tocadas.
3. WRITE: PHP HARD/PREFERENCE en código nuevo y hunk tocado; sin comentarios/PHPDoc nuevos; strip PHPDoc y comentarios externos de ese hunk; no tocar envelope Blade.
4. AUDIT: PHP relevante; alta confianza; agrupar repeticiones; formato `assets/audit-template.md`.
5. FIX: solo estilo; añadir trailing comma en listas multilínea; strip PHPDoc/comentarios externos del hunk; quitar `{}` de `single-statement-if` solo si el body es una línea y pasa el safety gate; añadir `{}` si el body unbraced es multilínea; listar ítems inseguros omitidos.
6. No migrar un repo entero salvo audit+fix pedido.

## Output Contract

- WRITE: PHP formateado; sin correr Pint; Blade/HTML intacto.
- AUDIT: lista `[FAIL] path:line` + `Rule:` o `Rules:` + Actual + Expected + Reason; o "no findings". No emitir `single-return` (alias deprecado de `single-statement-if`).
- FIX: archivos tocados + reglas aplicadas + ítems inseguros omitidos.

## References

- `references/principles.md`
- `references/overrides.md`
- `references/tooling.md`
- `references/conditions.md`
- `references/delimiters-arrays.md`
- `references/calls-arguments.md`
- `references/chains.md`
- `references/classes-functions.md`
- `references/modifiers.md`
- `references/attributes.md`
- `references/expressions.md`
- `references/vertical-spacing.md`
- `references/imports.md`
- `assets/audit-template.md`
- `assets/pint-enforcement-overlay.json`
- `evals/trigger-evals.json`
- `evals/behavioral-evals.json`
