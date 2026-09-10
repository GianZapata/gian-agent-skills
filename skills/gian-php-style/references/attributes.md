# Attributes

## One per line (PREFERENCE)

`attribute-one-per-line`. No agrupar automáticamente `#[First, Second]`.

```php
#[First]
#[Second]
public function execute(): void {
}
```

## Empty parentheses (HARD)

`attribute-empty-parentheses` (AUTOFIXABLE). Sin argumentos → sin `()`.

```php
#[WithoutRelations]
#[UseFactory(ClientFactory::class)]
final class Client {
}
```

No:

```php
#[WithoutRelations()]
public function execute(): void {
}
```

## Parameter attributes (HARD, DELIBERATE-OVERRIDE)

`parameter-attribute-inline`. Attribute y parámetro en la **misma** línea. Override vs PER-CS — ver `references/overrides.md`.

```php
public function execute(
    #[Authenticated] User $user,
    #[CurrentTenant] Tenant $tenant,
): void {
}
```

No:

```php
    #[Authenticated]
    User $user,
```
