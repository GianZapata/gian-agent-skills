# Audit output

```text
PHP STYLE AUDIT

[FAIL] path/file.php:LINE
Rule: rule-id

Actual:
...

Expected:
...

Reason:
Violates Gian PHP Style.
```

When one site breaks several rules, prefer one finding with multiple IDs (less noise) over separate FAILs:

```text
[FAIL] path/file.php:LINE
Rules:
- negation-spacing
- single-statement-if
```

Deprecated alias: `single-return` in old reports means `single-statement-if`. Do not emit `single-return` in new AUDIT.

Rule ids: `indent-spaces`, `construct-spacing`, `negation-spacing`, `single-statement-if`, `boolean-operator-position`, `brace-same-line`, `multiline-delimiter-indent`, `array-arrow-alignment`, `named-argument-colon`, `chain-arrow-position`, `concat-spacing`, `ternary-break`, `null-coalesce-break`, `vertical-spacing`, `class-method-separation`, `comments-phpdoc`, `elseif-keyword`, `control-continuation`, `switch-case-spacing`, `arrow-fn-spacing`, `arrow-fn-break`, `closure-use-geometry`, `multiline-params`, `single-param-signature`, `promoted-constructor-multiline`, `empty-promoted-constructor`, `multiline-trailing-comma`, `modifier-keyword-order`, `attribute-empty-parentheses`, `single-class-element-per-statement`, `match-arrow-alignment`, `compound-type-operator-position`, `attribute-one-per-line`, `parameter-attribute-inline`, `property-hook-geometry`, `empty-class-compact`, `import-groups`, `unused-imports`, `grouped-imports`, `laravel-validation-rule-array`, `heredoc-nowdoc-preserve`, `strict-types-preserve`, `alternative-syntax-preserve`.

Do not FAIL: Blade/HTML/`wire:*`/`{{ }}`/`@if`; adding missing `declare(strict_types=1)`; compact `if/else` chains (GAP); dangling-else (do not recommend unsafe compact); grouped-import conversion when ungrouped (GAP); pipe-string validation lists; single-line trailing comma (out of scope for `multiline-trailing-comma`).

`comments-phpdoc`: FAIL on file/class/method/property PHPDoc and on `//` `/* */` outside a function/method/closure body. FAIL obvious intra-body noise. Keep intra-body comments that explain a non-obvious why. Dubious intra-body relevance: GAP. WRITE must not add comments. `@var` inside a body is PHPDoc → FAIL/strip.

`boolean-operator-position` applies to every multiline boolean expression regardless of context. Leading `&&` / `||`: FAIL. Wrap geometry of `(` `)` around a group in `return`/assignment: GAP. Distinct from `compound-type-operator-position` (`|` / `&`).

`multiline-delimiter-indent` on a multiline **control** condition: first operand on the next line; `)` aligned with the keyword; then `{` or the compact statement. Indented `) {` or hanging `if ($a &&` is FAIL, not GAP.

`single-param-signature`: exactly one parameter without constructor promotion must stay on one line. Does not apply to promoted constructors. GAP only if the one parameter is unreadably long.

`promoted-constructor-multiline`: `__construct` with ≥ 1 promoted parameter must be multiline (including mixed promoted + non-promoted). FAIL inline promoted ctor. Does not apply to normal methods or ctors without promotion.

`multiline-trailing-comma`: multiline lists (arrays, arguments, parameters, match, destructuring) must have trailing comma. Does not govern single-line lists.

`class-method-separation`: exactly one blank line between consecutive class methods. PHPDoc/attributes belong to the next method. Not between individual properties.

`laravel-validation-rule-array`: 2+ rules inline → FAIL. One rule inline OK. Do not FAIL Blade markup.

`single-statement-if`: decide by **body geometry**, not only statement count. FAIL braced standalone `if` with one approved **single-line** statement (should be compact). FAIL unbraced `if` whose controlled statement spans multiple physical lines (braces required). Do not FAIL braced standalone `if` with one approved **multiline** statement. Do not FAIL else-chains, nested-if, unspecified statements. Multiline **condition** + one-line body may stay compact.

Group repeated identical violations. Prefer high-confidence findings. Skip dubious inline-vs-multiline wrapping (GAP). PREFERENCE FAILs only when objectively determinable.

Enforcement tags: `references/overrides.md`.
