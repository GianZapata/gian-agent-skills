# Calls and arguments

## Positional (PREFERENCE + HARD geometry)

Corto y legible → inline:

```php
$this->create($name, $email, true);
```

Multilínea → geometría de delimitadores:

```php
$this->create(
    $name,
    $email,
    true,
);
```

No indentar argumentos +2 niveles ni cerrar `)` más adentro.

## Multiline signatures (HARD)

`multiline-params`. Si hay **2+** parámetros y la lista ya es multilínea: **un parámetro por línea**. Un solo parámetro sin promotion: `single-param-signature` (`references/classes-functions.md`). `__construct` con promotion: `promoted-constructor-multiline`. `): ReturnType {` en la geometría actual.

```php
public function execute(
    User $user,
    Conversation $conversation,
    Context $context,
): Result {
}
```

No:

```php
public function execute(
    User $user, Conversation $conversation,
    Context $context
): Result {
}
```

## Closure `use` (PREFERENCE)

`closure-use-geometry`. Si los parámetros de la closure son multilínea pero `use` sigue corto: no expandir `use`.

```php
$callback = function (
    User $user,
    Context $context
) use ($service, $logger): bool {
    return true;
};
```

Si el propio `use (...)` necesita multilínea: geometría de delimitadores. Wrapping subjetivo → GAP.

## Named arguments (HARD)

```php
$this->create(
    name: $name,
    email: $email,
    active: true,
);
```

Usar `name: $value`. No `name : $value`. No pad de columnas en `:`.
