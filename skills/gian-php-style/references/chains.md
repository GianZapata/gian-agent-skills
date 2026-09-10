# Method chains

Corta y legible → inline:

```php
$user->posts()->get();
```

Larga → `->` inicia cada continuación:

```php
User::query()
    ->where('active', true)
    ->whereNotNull('email')
    ->orderBy('name')
    ->get();
```

No romper una cadena corta sin necesidad. GAP si "larga" es dudoso: no FAIL.
