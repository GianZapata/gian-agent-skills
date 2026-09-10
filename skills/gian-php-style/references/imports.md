# Imports

## Blocks (PREFERENCE)

`import-groups`. Orden:

```text
class imports
blank
function imports
blank
const imports
```

Sólo crear bloques que existan. Dentro de cada bloque: alfabético.

```php
use App\Models\User;
use Illuminate\Support\Collection;

use function Illuminate\Support\defer;

use const PHP_VERSION;
```

## Unused (`unused-imports`)

PREFERENCE. Quitar imports no usados. AST-SENSITIVE: skip si el uso es dudoso (atributos, strings, names dinámicos).

## Grouped form (`grouped-imports`)

Forma preferida cuando se agrupa:

```php
use App\Models\{
    Offer,
    User,
    Vacancy
};
```

Nunca convertir un **único** import a grouped syntax.

**When** to convert 2+ ungrouped same-namespace imports → **GAP**. AUDIT/FIX MUST NOT rewrite ungrouped siblings into `Ns\{}` until that threshold is decided. NEVER AUTOFIX conversion.
