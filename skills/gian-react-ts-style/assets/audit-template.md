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

`exported-arrow-default`, `arrow-implicit-return`, `react-component-explicit-return`, `single-statement-if`, `compact-if-else`, `guard-clause-over-nesting`, `conditional-and-render`, `simple-jsx-ternary`, `no-nested-ternary`, `derived-multi-branch`, `direct-handler-reference`, `inline-argument-handler`, `no-ceremonial-handler-extraction`, `boolean-prop-shorthand`, `fragment-shorthand`, `self-closing-jsx`, `intentional-prop-spread`, `type-only-import`, `interface-object-shape`, `direct-property-access`, `query-data-alias`, `list-data-default`, `comments-noise`.

`single-statement-multiline` is a clause of `single-statement-if` (do not emit as a separate AUDIT id).

## MUST NOT FAIL

PRETTIER_OWNED (quotes, indent, semi, trailing comma, printWidth, JSX wrap, arrowParens); `React.FC`; `disabled={false}`; class `static async`; shadcn `export function cn`; `import/order` of the repo; unused imports already owned by ESLint; `renderFoo` ambiguity; why-comment dudoso.

## GAP omit (FIX)

Report:

```text
GAP — no corregido automáticamente:
posible cambio de asociación/semántica
```

Cases: dangling-else; nested if+else; guard rewrite inseguro; entity/DTO spread; detail `= []`; `count &&`; `renderFoo`; ceremonial vs required JSDoc dudoso.

## WRITE vs AUDIT vs FIX

WRITE/FIX **apply** SAFE FIX on the touched hunk. AUDIT only lists FAIL. Do not say “violates `arrow-implicit-return`” and leave `{ return x }` if the mode is WRITE/FIX.
