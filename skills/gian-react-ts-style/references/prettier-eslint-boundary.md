# Prettier / ESLint boundary

La skill no instala plugins ni modifica configs. ESLint custom rules: no en v1.0.

## PRETTIER_OWNED (MUST NOT FAIL)

Si el repo usa Prettier (`prettier`, `eslint-plugin-prettier`):

- indent / `tabWidth` / tabs vs spaces
- `singleQuote` / `jsxSingleQuote`
- `semi`
- `trailingComma`
- `printWidth` / wrapping de JSX, calls, objects
- `arrowParens` (`x =>` vs `(x) =>`)
- `bracketSpacing`, `endOfLine`, `bracketSameLine`

Test: “¿Prettier lo reimprime inevitablemente?” → sí = no HARD de esta skill.

## ESLint already active (do not duplicate FAIL)

En repos típicos de este stack (no asumir todos):

- `prettier/prettier`
- `unused-imports` / `@typescript-eslint/no-unused-vars`
- `import/order`
- `react/self-closing-comp` (warn en varios)
- `react/jsx-sort-props` (algunos)

Si el repo ya FAIL/fixea `self-closing-comp`, no emitir un segundo FAIL por la misma línea. WRITE igual emite self-closing.

## Equivalents NOT enabled — do not activate in this lote

| Skill rule | ESLint approx | Why not on |
|---|---|---|
| `arrow-implicit-return` | `arrow-body-style: as-needed` | Rompe `react-component-explicit-return` |
| `single-statement-if` | `curly: multi` / `multi-or-nest` | Suele exigir braces en multilínea (regla 5) |
| `boolean-prop-shorthand` | `react/jsx-boolean-value: never` | Equivalente futuro opcional |
| `fragment-shorthand` | `react/jsx-fragments: syntax` | Equivalente futuro opcional |
| `type-only-import` | `@typescript-eslint/consistent-type-imports` | GAP decorators; no instalar |
| `interface-object-shape` | `@typescript-eslint/consistent-type-definitions: interface` | Verificar `z.infer`; no instalar |
| `no-nested-ternary` | `no-nested-ternary` | Lint ≠ FIX useMemo; no instalar |

`direct-handler-reference` no usar `jsx-no-bind` (empuja lo contrario).
