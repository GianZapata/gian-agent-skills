# Overrides and enforcement metadata

## Equation

```text
gian-php-style ≠ Laravel preset ≠ PER-CS

gian-php-style = PHP baseline + decisiones Gian + deliberate overrides + autofixers compatibles
```

## Enforcement tags

| Tag | Meaning |
|---|---|
| `AUTOFIXABLE` | Pint/PHP-CS-Fixer can enforce; agent must not contradict |
| `AGENT-ENFORCED` | No reliable fixer or safety gate; agent applies in WRITE/AUDIT/FIX |
| `DELIBERATE-OVERRIDE` | Intentionally differs from PER-CS/PSR; do not "correct" toward the standard |

## Rule registry (1.2)

| Rule id | Layer | Enforcement | PHP-CS-Fixer | Notes |
|---|---|---|---|---|
| `promoted-constructor-multiline` | HARD | AUTOFIXABLE | `multiline_promoted_properties` | experimental |
| `multiline-trailing-comma` | HARD | AUTOFIXABLE | `trailing_comma_in_multiline` | multiline only; does not govern single-line |
| `modifier-keyword-order` | HARD | AUTOFIXABLE | `modifier_keywords` | |
| `attribute-empty-parentheses` | HARD | AUTOFIXABLE | `attribute_empty_parentheses` | |
| `single-class-element-per-statement` | HARD | AUTOFIXABLE | `single_class_element_per_statement` | |
| `class-method-separation` | HARD | AUTOFIXABLE | `class_attributes_separation` | |
| `single-statement-if` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs PER-CS |
| `boolean-operator-position` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs PER-CS |
| `compound-type-operator-position` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs PER-CS |
| `parameter-attribute-inline` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs PER-CS |
| `brace-same-line` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs Laravel preset |
| `null-coalesce-break` | HARD | AGENT-ENFORCED | — | DELIBERATE-OVERRIDE vs PER-CS |

Pint overlay: `assets/pint-enforcement-overlay.json`. Partial enforcement only — see `references/tooling.md`.

## Deliberate overrides (do not correct toward PER-CS)

### `single-statement-if`

```php
if (!$user) return;
```

PER-CS requires braces on all control structures. Gian keeps compact single-line bodies.

### `boolean-operator-position`

```php
if (
    $user->isActive() &&
    $user->hasRole('admin')
) {
}
```

PER-CS puts `&&` / `||` at line start. Gian puts them at line end.

### `compound-type-operator-position`

```php
function handle(
    User|
        Admin|
        Guest $user,
): void {
}
```

PER-CS puts `|` / `&` at line start. Gian puts them at line end.

### `parameter-attribute-inline`

```php
public function execute(
    #[Authenticated] User $user,
    #[CurrentTenant] Tenant $tenant,
): void {
}
```

PER-CS puts the attribute on its own line when the parameter list is multiline. Gian keeps attribute and parameter on the same line.

### `brace-same-line`

```php
final class UserService {
    public function execute(): void {
    }
}
```

Laravel preset and PSR-12 use next-line braces. Gian uses same-line braces.

### `null-coalesce-break`

```php
$value = $this->findSomethingVeryLong() ??
    $this->getFallbackValue();
```

When split, `??` ends the previous line.
