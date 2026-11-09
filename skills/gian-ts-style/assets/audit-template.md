# Audit output

```text
TS/TSX STYLE AUDIT

[FAIL] path/file.tsx:LINE
Rule: rule-id

Actual:
...

Expected:
...

Reason:
Violates Gian TS/React Style.
```

When one site breaks several rules, prefer one finding with multiple IDs:

```text
[FAIL] path/file.tsx:LINE
Rules:
- arrow-implicit-return
- single-statement-if
```

## Rule ids

`exported-arrow-default`, `arrow-implicit-return`, `react-component-explicit-return`, `react-component-fc-props`, `classname-cn`, `single-statement-if`, `compact-if-else`, `guard-clause-over-nesting`, `conditional-and-render`, `simple-jsx-ternary`, `no-nested-ternary`, `derived-multi-branch`, `direct-handler-reference`, `inline-argument-handler`, `no-ceremonial-handler-extraction`, `boolean-prop-shorthand`, `fragment-shorthand`, `self-closing-jsx`, `intentional-prop-spread`, `type-only-import`, `interface-object-shape`, `direct-property-access`, `query-data-alias`, `list-data-default`, `comments-noise`, `vertical-spacing`, `read-group`, `slot-order`, `guard-glue`, `data-hook-location`, `no-local-style-constants`, `handler-naming`, `enum-ownership`, `library-shadow-type`, `named-interface`, `display-meta-location`, `parallel-meta`, `derived-multi-branch`, `no-nested-ternary`, `memo-ceremonial`.

`single-statement-multiline` is a clause of `single-statement-if` (do not emit as a separate AUDIT id).

## MUST NOT FAIL

Closed list:

- PRETTIER_OWNED (quotes, indent, semi, trailing comma, printWidth, JSX wrap, arrowParens)
- component signature with generics, `forwardRef` or `memo` (with or without comparator)
- `Cell`, `Header` and library render props
- `disabled={false}`
- class method form (`static async`, arrow field)
- shadcn or generated `export function cn`
- `import/order` and unused imports owned by the repo ESLint
- `function` in the closed exceptions of `exported-arrow-default` (overloads, `function*`, `this`, module-level call before the definition)
- comments in the closed keep list of `comments-noise` and directives
- `{cond ? <X /> : null}` with a `number`, `string` or array condition
- fragment with a single child
- files `*.gen.ts` / `*.gen.tsx`

Everything else that breaks a rule in scope is FAIL.

## GAP omit (FIX)

Only the closed list of `references/principles.md` § NEVER AUTOFIX. One line per case:

```text
GAP <rule-id> path/file.tsx:LINE — <case from the closed list>
```

Cases used by the references: dangling-else and `if` with `else` inside (`single-statement-if`, `compact-if-else`); guard rewrite in the closed list of `guard-clause-over-nesting`; nested ternary in a default param, decorator or type position (`no-nested-ternary`); entity/DTO spread in existing code (`intentional-prop-spread`); object mutated after destructuring (`direct-property-access`); typecheck fails after `react-component-fc-props` or `interface-object-shape`; runtime decorator metadata (`type-only-import`); the repo has no `cn` (`classname-cn`); generic component, `forwardRef`, `memo`, library render props (`react-component-fc-props`).

## WRITE vs AUDIT vs FIX

WRITE/FIX **apply** every rule in scope: the whole function, component or hook that contains an added or changed line, plus the file imports. AUDIT only lists FAIL. WRITE/FIX close with `node <ruta de gian-ts-style>/assets/self-check.mjs` on the touched files: every hit in scope is fixed or reported as GAP. El script cubre `classname-cn`, pero no detecta `clsx`/`classnames`/`twMerge` directo ni `const xClass = '…'`. Esos dos `rg` se siguen corriendo a mano. Do not say “violates `arrow-implicit-return`” and leave `{ return x }` if the mode is WRITE/FIX.
