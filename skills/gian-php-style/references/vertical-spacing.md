# Vertical spacing

Una línea en blanco después de un bloque que ya es multilínea y después de cada lectura con su complemento. Lo que cabe en una línea y es el mismo paso se queda junto, salvo dos lecturas. Nunca dos líneas en blanco.

El orden de los pasos lo decide `gian-how-i-code` (`26`). Este archivo solo inserta la línea en blanco.

## Mismo paso, una línea

Asignaciones de una línea del mismo paso van juntas, solo entre ellas. Una lectura no entra en ese grupo: abre el suyo (`read-group`). Una escalera de `if` que resuelve un solo valor no se abre. Un `if` de una línea no gana su propio blanco.

```php
$status = strtolower($status);
$attempts = (int) $attempts;

if ($status === 'failed') return 'error';
if ($status === 'complete') return 'complete';

return 'start';
```

```php
$term = trim((string) $search);
if ($term === '') return $query;
```

## Una lectura, un grupo (HARD)

`read-group` (AGENT-ENFORCED). Cada lectura abre su propio grupo. Su complemento va pegado debajo. Una línea en blanco cierra el grupo. Dos lecturas solo van pegadas si la segunda es complemento de la primera, aunque cada una quepa en una línea.

Lectura: lo que trae registros de una fuente de datos. Una query de Eloquent o del Query Builder, un repositorio, un service, un cliente HTTP, la caché, o un método propio que hace eso (`$this->settlementRows()`). Normalizar la entrada, leer config, `now()` o una zona horaria no es lectura: va en el grupo de normalizar.

Complemento: la sentencia de una línea justo debajo que solo lee esa lectura y existe para completarla.

- Una transformación de ella: sus ids, su `keyBy`, su conteo (`$invoiceIds`, `$customerById`).
- Su historial o su detalle, cuyo nombre deriva del de la lectura (`$products` → `$productHistories`).

Otra entidad (`$customer` desde `$invoice->customerId`) es otra lectura y abre su grupo. Una línea que combina dos lecturas es derivar y abre su grupo.

Si la lectura es multilínea, la línea en blanco va al cerrarla, como cualquier bloque multilínea. Su complemento queda en su propio grupo, debajo. Única excepción: el guard que la valida se queda pegado (`gian-how-i-code` `26`).

El orden de las lecturas lo decide `26`. Esta regla solo pone la línea en blanco.

```php
$this->from = $from;
$this->to = $to;
$this->timezone = $this->civilTimezone();

$products = Product::withTrashed()->with('category')->get();
$productHistories = $this->histories(Product::class, $products->modelKeys());

$orders = Order::withTrashed()->with(['customer', 'items'])->get();
$orderHistories = $this->histories(Order::class, $orders->modelKeys());

$settlements = $this->settlementRows();
$invoiceIds = $settlements->pluck('invoice_id')->map(fn($id) => (int) $id)->all();

$invoices = Invoice::query()
    ->with(['order.customer'])
    ->whereIn('id', $invoiceIds)
    ->get();

$invoiceHistories = $this->histories(Invoice::class, $invoices->modelKeys());

$income = $this->income($settlements, $invoices, $invoiceHistories);
$cashRows = $income['rows'];
```

No:

```php
$products = Product::withTrashed()->with('category')->get();
$productHistories = $this->histories(Product::class, $products->modelKeys());
$orders = Order::withTrashed()->with(['customer', 'items'])->get();
$orderHistories = $this->histories(Order::class, $orders->modelKeys());
$settlements = $this->settlementRows();
```

WRITE lo aplica en el método tocado. AUDIT: FAIL si dos lecturas van pegadas y la segunda no es complemento de la primera. Si no es claro que una línea sea lectura o complemento: GAP, sin FAIL.

## Cuatro pasos

Al cerrar un paso multilínea, una línea en blanco antes del paso siguiente. Las sentencias de una línea del mismo paso quedan juntas. No se parte un array ni los argumentos de una llamada.

La consulta, el bucle que llena, las reducciones de una línea, la lectura de etiquetas, el bucle que arma, y el `return`:

```php
$rows = $this->records()
    ->where('active', true)
    ->get();

$counts = [];
foreach ($rows as $row) {
    $key = $row->bucket;
    $counts[$key] = ($counts[$key] ?? 0) + 1;
}

arsort($counts);
$counts = array_slice($counts, 0, 8, true);

$labels = $this->labels(array_keys($counts));

$items = [];
foreach ($counts as $id => $count) {
    $items[] = ['id' => $id, 'label' => $labels[$id] ?? null, 'count' => $count];
}

return $items;
```

WRITE lo aplica en el método tocado. No es un pase posterior.

## Class method separation (HARD)

`class-method-separation` (AUTOFIXABLE). Entre métodos consecutivos a nivel de clase: **exactamente una** línea en blanco. No cero, no dos o más.

PHPDoc y attributes pertenecen al método siguiente. La línea vacía va entre el cierre del método anterior y el metadata del siguiente.

```php
public function foo(): void {
}

/** Something */
#[Transactional]
public function bar(): void {
}
```

No:

```php
public function foo(): void {
}
/** Something */
#[Transactional]
public function bar(): void {
}
```

Ni:

```php
public function foo(): void {
}


/** Something */
#[Transactional]
public function bar(): void {
}
```

**No aplica** entre properties individuales — mantener agrupación visual de properties.

## Switch cases

Una línea en blanco entre `case` / `default` siblings. Ver `references/conditions.md` (`switch-case-spacing`).
