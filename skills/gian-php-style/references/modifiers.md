# Modifier keyword order

`modifier-keyword-order` (HARD, AUTOFIXABLE). PHP-CS-Fixer: `modifier_keywords`.

Canonical order (PER-CS 3.1):

```text
abstract / final
→ public / protected / private
→ set visibility (e.g. private(set))
→ static
→ readonly
→ type
→ name
```

```php
final public static function execute(): void {
}

protected private(set) string $name;

private readonly WhatsAppGateway $gateway;

protected static string $name;
```

No reorder inventado. GAP solo si la combinación no existe en PHP de la versión del proyecto.
