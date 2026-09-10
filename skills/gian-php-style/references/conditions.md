# Conditions

## Constructs (HARD)

Espacio después de `if` / `foreach` / `while` / `for` / `elseif`. Sin espacios internos en los paréntesis.

```php
if ($user) {
    //
}

foreach ($users as $user) {
    //
}
```

No: `if($user)`, `if ( $user )`.

## `elseif` keyword (HARD)

`elseif-keyword`. Usar `elseif`, nunca `else if`.

```php
if ($a) {
} elseif ($b) {
} else {
}
```

## Control continuation (HARD)

`control-continuation`. `} elseif (` / `} else {` / `} catch (` / `} finally {` en la **misma línea** que el `}` de cierre.

```php
try {
} catch (Throwable $e) {
} finally {
}
```

No:

```php
if ($a) {
}
else {
}
```

## Negation (HARD)

```php
!$user
!$enabled
!$conversation->isActive()
```

No: `! $user`.

```php
if (!$user) return null;
```

## Single-statement-if (HARD OVERRIDE)

Canonical id: `single-statement-if`. Deprecated alias: `single-return` (old reports only; do not emit).

La regla se decide por la **geometría del body**, no solo por el número de statements AST.

Si un `if` **standalone** (sin `elseif`/`else` en esa statement) contiene **exactamente una** statement aprobada: omitir `{}` **solo** cuando esa statement controlada completa se representa en **una sola línea física**, inmediatamente después de `)`.

Si el body necesita varias líneas físicas, las `{}` son **obligatorias** aunque a nivel AST siga siendo una sola statement.

Aprobadas: `return`; `throw`; `continue`; `break`; assignment; function/method/static call; una chained call (`$user->profile()->refresh()`).

Compacto (body de una línea):

```php
if (!$user) return;

if (!$user) return null;

if ($blocked) throw new RuntimeException('Blocked');

if ($searchResult === null) throw new InvalidArgumentException('A complete vacancy search did not produce a result.');

if (!$item->isValid()) continue;

if ($finished) break;

if ($user) $this->process($user);

if ($user) $name = $user->name;

if ($user) $user->profile()->refresh();

if (
    $conditionA &&
    $conditionB
) $this->execute();
```

Body multilínea → braces (siguen siendo una statement AST):

```php
if ($x) {
    return [
        'kind'      => $kind,
        'reference' => $reference
    ];
}

if ($allowPhone) {
    $string = preg_replace(
        $pattern,
        '[PHONE_REDACTED]',
        $string,
    );
}

if ($searchResult === null) {
    throw new InvalidArgumentException(
        'A complete vacancy search did not produce a result.'
    );
}
```

No (braces around one approved **single-line** statement):

```php
if (!$user) {
    return null;
}

if ($user) {
    $this->process($user);
}
```

No (unbraced body that spans multiple physical lines):

```php
if ($x) return [
    'kind'      => $kind,
    'reference' => $reference
];

if ($allowPhone) $string = preg_replace(
    $pattern,
    '[PHONE_REDACTED]',
    $string,
);

if ($searchResult === null) throw new InvalidArgumentException(
    'A complete vacancy search did not produce a result.'
);
```

Varias statements → llaves:

```php
if (!$user) {
    $this->logger->warning('User missing');

    return null;
}
```

WRITE: emitir compacto cuando el body sea una línea y sea seguro. Emitir `{}` cuando el body sea multilínea. No inventar `if/else` compacto.

AUDIT:

- FAIL: `if` standalone con `{}` alrededor de una statement aprobada **de una línea**.
- FAIL: `if` unbraced cuyo body aprobado ocupa **varias líneas físicas**.
- No FAIL: `if` standalone con `{}` alrededor de una statement aprobada **multilínea**.
- Condición multilínea + body de una línea puede seguir compacto.

FIX: quitar `{}` solo si el body es una línea y pasa el dangling-else gate. Añadir `{}` a un body unbraced multilínea es SAFE TEXTUAL. `php -l` no basta.

### Dangling-else / association (NEVER AUTOFIX)

1. El `if` tiene `else` o `elseif` → no compactar (GAP).
2. El cuerpo contiene otro `if` → no compactar.
3. Un `else`/`elseif` hermano se asocia a este `if` vía braces → no quitar braces.
4. Permitido compactar: `if (T) { S; }` con S aprobada **de una línea**, sin control anidado, sin else/elseif → `if (T) S`. Si S es multilínea, conservar o añadir `{}`.
5. Si el proyecto ya tiene `nikic/php-parser`, comparar stmts; no instalarlo. Si el árbol de control difiere → skip FIX.

No:

```php
if ($a) {
    if ($b) foo();
} else {
    bar();
}
```

→ compacto inseguro. Conservar braces del `if` exterior.

### GAP — if/elseif/else chain

Aunque cada branch tenga una sola statement: **no** compactar. Conservar braces. AUDIT no FAIL. NEVER AUTOFIX.

```php
if ($a) {
    foo();
} else {
    bar();
}
```

### UNSPECIFIED (keep braces)

`yield`; `yield from`; `goto`; `unset`; `echo`; `include`/`require`; standalone `++`/`--`; nested control as the only statement; `catch` de una sola statement. No inventar.

## Short conditions (PREFERENCE)

Si cabe limpio, una línea:

```php
if ($active && $verified) {
    //
}
```

No expandir sin necesidad. GAP si la legibilidad es dudosa: no FAIL.

## Multiline control condition (HARD)

Si una condición de control (`if` / `elseif` / `while` / `for` / `foreach`) necesita varias líneas: abrir `(` y poner el **primer operando en la línea siguiente**. `)` al mismo indent que la keyword. Luego `{` **o** la statement compacta (`single-statement-if`). Rule: `multiline-delimiter-indent`. FAIL, no GAP.

```php
if (
    $conditionA &&
    $conditionB
) {
    //
}

if (
    $conditionA &&
    $conditionB
) $this->execute();
```

No:

```php
if (
    $conditionA &&
    $conditionB
    ) {
}

if ($conditionA &&
    $conditionB
) {
}
```

Esto no decide wrap de grupos en `return` (sigue GAP más abajo).

## Switch case spacing (PREFERENCE)

`switch-case-spacing`. Una línea en blanco entre cases. No múltiples vacías.

```php
switch ($status) {
    case 'active':
        return true;

    case 'pending':
        return false;

    default:
        return null;
}
```

## Multiline booleans (HARD OVERRIDE)

Boolean operator placement applies to every multiline boolean
expression, regardless of syntactic context.

Includes:
- if / elseif / while
- return expressions
- assignments
- closures / callbacks
- grouped boolean expressions

Cuando hay que partir, el operador **termina** la línea anterior. Distinct from `|` / `&` (`references/expressions.md`).

```php
if (
    $active &&
    $verified &&
    !$blocked
) {
    //
}

if (
    $admin ||
    $owner ||
    $user->can('edit')
) {
    //
}
```

No (leading operator):

```php
if (
    $active
    && $verified
    && !$blocked
) {
}
```

También fuera de `if`:

```php
return $active &&
    $verified ||
    $fallback;
```

No:

```php
return $active
    && $verified
    || $fallback;
```

Si el cuerpo de un `if` es una statement aprobada **de una línea**, combinar con single-statement-if. Si el body es multilínea, usar `{}`.

## GAP — grouped parenthesized booleans

No hay Expected canónico para wrap geométrico de `(` `)` alrededor de un grupo en `return`/asignación. Ejemplo no decidido:

```php
return $normalizedReference !== '' &&
    ($this->contains($title, $normalizedReference) ||
        $this->contains($company, $normalizedReference));
```

versus wrap de delimitadores. AUDIT: reportar **GAP**, no FAIL. FIX/WRITE: no inventar wrap de paréntesis; sí corregir posición de `&&` / `||` cuando sea inequívoca.
