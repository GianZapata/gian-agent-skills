# Expressions

## Multiline booleans

`&&` / `||` en cualquier expresión multilínea: `references/conditions.md` (no solo `if`). No duplicar esa spec aquí. `?` / `:` del ternario no usan esa regla. `|` / `&` de tipos no usan esa regla.

## Arrow functions (PREFERENCE)

`arrow-fn-spacing`: `fn($user)` no `fn ($user)`.

```php
$users->map(fn($user) => $user->email);
```

`arrow-fn-break`: en arrow multilínea, `=>` **termina** la línea de la firma.

```php
$fn = fn($user): bool =>
    $user->isActive();
```

No:

```php
$fn = fn($user): bool
    => $user->isActive();
```

## Compound types (HARD OVERRIDE)

`compound-type-operator-position`. Union / intersection / DNF: cuando hay que partir, `|` y `&` **terminan** la línea anterior. Distinct from `&&` / `||`.

```php
function handle(
    User|
        Admin|
        Guest $user,
): void {
}
```

No leading `|` / `&`.

DNF con paréntesis agrupados: **GAP**. No inventar wrap. NEVER AUTOFIX wrap.

## Concatenation (HARD)

Espacios alrededor de `.`:

```php
$name = $first . ' ' . $last;
```

No: `$first.' '.$last`.

Regex / string composition no es excepción:

```php
$regex = '/^(?:' . $verbs . ')\b/u';
```

No: `'/^(?:'.$verbs.')\b/u'`.

`.=` es otro operador; no tratarlo como concatenación binaria.

## Ternary (PREFERENCE)

Corto:

```php
$value = $active ? 'yes' : 'no';
```

Multilínea: `?` y `:` **inician** la continuación. No aplicar la regla de booleanos aquí.

```php
$value = $active
    ? $this->active()
    : $this->inactive();
```

## Null coalescing `??` (PREFERENCE)

Inline cuando limpia:

```php
$value = $something ?? $fallback;

return $result ?? $data;
```

Si hay que partir: `??` **termina** la línea anterior:

```php
$value = $this->findSomethingVeryLong() ??
    $this->getFallbackValue();
```

No:

```php
$value = $this->findSomethingVeryLong()
    ?? $this->getFallbackValue();
```
