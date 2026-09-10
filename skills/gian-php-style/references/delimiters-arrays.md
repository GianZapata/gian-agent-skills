# Delimiters and arrays

## Universal multiline geometry (HARD)

Para `[]` `()` `{}` multilínea:

```text
content = opener indent + 1 level (4 spaces)
closing delimiter = same indent as the expression that opened
```

Aplica a arrays, argumentos, parámetros, condiciones, named arguments, closures, match, anidados.

```php
$this->execute(
    $user,
    $conversation,
);

$data = [
    'foo' => $foo,
    'bar' => $bar,
];
```

No:

```php
$this->execute(
        $user,
        $conversation
    );

$data = [
        'foo' => $foo,
        'bar' => $bar
    ];
```

## Arrays (PREFERENCE)

Varias entradas cuya lectura mejora en vertical → multilínea. No forzar un array trivial a multilínea.

**Excepción HARD:** listas de validation Laravel — `laravel-validation-rule-array` más abajo. Esa regla gana a esta heurística.

## `=>` alignment (HARD)

En arrays **multilínea**, alinear `=>` entre hermanos del mismo nivel. Cada nivel se alinea **independiente**.

```php
$data = [
    'id'         => $id,
    'first_name' => $firstName,
    'email'      => $email,
];

$data = [
    'user'   => [
        'id'    => $id,
        'email' => $email,
    ],
    'active' => true,
];
```

No alinear `=>` interno con el externo.

No pad artificial de `=` ni `:` (asignaciones ni named arguments).

## Match `=>` (HARD)

`match-arrow-alignment`. Cada `match` es su propia región. No mezclar columnas con arrays externos. El texto visible del arm completo (incl. `'draft', 'pending'`) cuenta para alinear `=>`. Wrapping corto/largo dudoso → GAP.

```php
return match ($status) {
    'active'  => true,
    'pending' => false,
    default   => null,
};

return match ($status) {
    'draft', 'pending' => false,
    'active'           => true,
};
```

## Laravel validation rule arrays (HARD)

`laravel-validation-rule-array`. Lista Laravel de validation rules con **más de una** regla → multiline, **una regla por línea**. Una sola regla puede permanecer inline.

Gana a la PREFERENCE genérica de arrays.

```php
'name' => ['required'],

'newSessionName' => [
    'required',
    'string',
    'max:60',
    'regex:/^[a-z0-9-]+$/',
],
```

No:

```php
'newSessionName' => ['required', 'string', 'max:60', 'regex:/^[a-z0-9-]+$/'],
```

Aplica a: `FormRequest::rules()`, Livewire `rules()`, Livewire Form `rules()`, `$request->validate([...])`, `$this->validate([...])`, `Validator::make($data, [...])`.

`Rule` objects son un ítem de la lista:

```php
'email' => [
    'required',
    'email',
    Rule::unique('users')->ignore($user),
],
```

No modificar el **contenido** de reglas/regexes. Sólo representación del array.

Outer map: `array-arrow-alignment`. Inner list: values only, no pad de `=>`.

Multiline lists: `multiline-trailing-comma` (`references/principles.md`).

Pipe-string `'required|string'`: UNSPECIFIED. No convertir a array. NEVER AUTOFIX.

No aplicar esta regla a arrays que no sean listas de validation rules (field => list of rule strings/objects).
