# Tooling — Pint enforcement overlay

## What this is

`assets/pint-enforcement-overlay.json` is a **partial enforcement overlay** for the AUTOFIXABLE rules documented in this skill.

It is **not** a complete `gian-php-style` Pint config.

## What it is not

```text
The bundled Pint overlay does not make Laravel's preset fully equivalent to gian-php-style.

Laravel's preset may contain rules that intentionally conflict with DELIBERATE-OVERRIDE
rules such as brace-same-line and single-statement-if.
```

```text
gian-php-style ≠ Laravel preset ≠ PER-CS
```

## Merge into a Laravel project

Pint accepts PHP-CS-Fixer rules on top of a preset. Merge the overlay `rules` into your project `pint.json`:

```json
{
  "preset": "laravel",
  "rules": {
    "multiline_promoted_properties": {
      "minimum_number_of_parameters": 1
    },
    "trailing_comma_in_multiline": {
      "after_heredoc": true,
      "elements": ["arguments", "array_destructuring", "arrays", "match", "parameters"]
    },
    "modifier_keywords": true,
    "attribute_empty_parentheses": true,
    "single_class_element_per_statement": {
      "elements": ["property", "const"]
    },
    "class_attributes_separation": {
      "elements": {
        "method": "one"
      }
    }
  }
}
```

Laravel preset conflicts to expect (do not assume Pint will enforce Gian overrides):

- `braces_position` / `control_structure_braces` → next-line braces vs `brace-same-line`
- control-structure brace requirements vs `single-statement-if`

Optional (not in overlay): `braces_position` with `same_line` values can align brace-same-line — evaluate per project; not required for 1.2.

## Rule mapping

| Gian rule id | PHP-CS-Fixer rule | Notes |
|---|---|---|
| `promoted-constructor-multiline` | `multiline_promoted_properties` | experimental |
| `multiline-trailing-comma` | `trailing_comma_in_multiline` | multiline lists only |
| `modifier-keyword-order` | `modifier_keywords` | |
| `attribute-empty-parentheses` | `attribute_empty_parentheses` | |
| `single-class-element-per-statement` | `single_class_element_per_statement` | |
| `class-method-separation` | `class_attributes_separation` | `method: one` |

`multiline-trailing-comma` does **not** use `no_trailing_comma_in_singleline` — that rule does not cover parameters or match, and single-line trailing comma is out of scope for this rule id.

## Agent policy

WRITE mode: do not run Pint. Apply Gian Style directly.

AUDIT/FIX: agent-enforced rules still require the agent even when a fixer exists, unless the user runs Pint separately.
