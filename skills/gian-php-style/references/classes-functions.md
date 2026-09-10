# Classes and functions

OVERRIDE vs PSR-12 Allman braces.

## Class (HARD OVERRIDE)

```php
final class UserService {
    //
}
```

No:

```php
final class UserService
{
}
```

## Empty class (PREFERENCE)

`empty-class-compact`. Clase realmente vacía:

```php
final class CustomException {}
```

No: `final class CustomException {\n}`. No extrapolar a enum/interface/trait si no es sintácticamente apropiado. No forzar en clases no vacías.

## Method (HARD OVERRIDE)

```php
public function execute(): void {
    //
}
```

No brace en línea siguiente.

## Empty methods (PREFERENCE)

```php
public function reset(): void {}
```

No expandir un cuerpo vacío solo por estética.

## Single-parameter signature (HARD)

`single-param-signature`. Exactamente un parámetro **sin** constructor property promotion → firma **en una línea**. Cuerpo vacío → `{}` en esa línea. Gana a `multiline-params` cuando hay un solo param (no verticalizar).

**No aplica** si `__construct` tiene al menos un parámetro promovido — ver `promoted-constructor-multiline`.

```php
public function __construct(UserRepository $users) {}

public function handle(User $user): void {
}
```

No:

```php
public function handle(
    User $user
): void {
}
```

GAP: un parámetro tan largo que partirlo es la única lectura (attribute largo, union DNF) — no FAIL; no inventar wrap.

## Promoted constructor multiline (HARD OVERRIDE)

`promoted-constructor-multiline` (AUTOFIXABLE). Si `__construct` tiene **≥ 1** parámetro promovido (`private`/`protected`/`public`, con o sin `readonly`), **todo** el constructor va multilínea — aunque haya un solo promoted param o parámetros mixtos (promoted + no promoted).

Gana sobre `single-param-signature`.

```php
public function __construct(
    private readonly WhatsAppGateway $gateway,
) {}

public function __construct(
    UserRepository $users,
    private readonly WhatsAppGateway $gateway,
) {}
```

No:

```php
public function __construct(private readonly WhatsAppGateway $gateway) {}

public function __construct(UserRepository $users, private readonly WhatsAppGateway $gateway) {}
```

No aplica a métodos normales ni constructores sin promotion.

## Promoted empty constructor (HARD OVERRIDE)

`empty-promoted-constructor`. Parámetros multilínea + promotion + empty body:

```php
public function __construct(
    private UserRepository $users,
    private LoggerInterface $logger,
) {}
```

No: `) {\n}`.

## Class elements (HARD)

`single-class-element-per-statement` (AUTOFIXABLE). Una property o constant por sentencia.

```php
private string $name;
private string $email;

public const ACTIVE = 'active';
public const INACTIVE = 'inactive';
```

No:

```php
private string $name, $email;

public const ACTIVE = 'active', INACTIVE = 'inactive';
```

## Anonymous class (HARD OVERRIDE)

`brace-same-line` aplica a `new class`. Brace same-line cuando la declaración cabe así. Wrap de params/interfaces: geometría de delimitadores; wrap subjetivo → GAP.

```php
$service = new class($dependency) implements Contract {
    public function execute(): void {
    }
};
```

## Control structures and try/catch/finally

Opening `{` stays on the same line (`if` / `foreach` / `while` / `for` / `try` / `catch` / `finally`). Continuations: `references/conditions.md` (`control-continuation`).

## match

Follow expression and multiline delimiter rules. Arms are `=>` expressions, not braced control blocks. Alignment: `references/delimiters-arrays.md`.

## Attributes

Ver `references/attributes.md` (`attribute-one-per-line`, `attribute-empty-parentheses`, `parameter-attribute-inline`).

## Property hooks (PREFERENCE)

`property-hook-geometry`. Short hook inline cuando es corto:

```php
public string $name { get => $this->name; }
```

Hook con body: braces same-line; una línea en blanco entre hooks. Short-vs-long dudoso → GAP.

```php
public string $name {
    get {
        return $this->name;
    }

    set(string $value) {
        $this->name = trim($value);
    }
}
```

No: `get\n{`.
