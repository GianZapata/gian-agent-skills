# Vertical spacing

Una línea en blanco después de un bloque que ya es multilínea. Lo que cabe en una línea y es el mismo paso se queda junto. Nunca dos líneas en blanco.

El orden de los pasos lo decide `gian-how-i-code` (`26`). Este archivo solo inserta la línea en blanco.

## Mismo paso, una línea

Asignaciones de una línea del mismo paso van juntas, solo entre ellas. Una escalera de `if` que resuelve un solo valor no se abre. Un `if` de una línea no gana su propio blanco.

```php
$record = $this->findRecord($id);
$label = $this->findLabel($id);

if ($status === 'failed') return 'error';
if ($status === 'complete') return 'complete';

return 'start';
```

```php
$term = trim((string) $search);
if ($term === '') return $query;
```

## Cuatro pasos

Al cerrar un paso multilínea, una línea en blanco antes del paso siguiente. Las sentencias de una línea del mismo paso quedan juntas. No se parte un array ni los argumentos de una llamada.

La consulta, el bucle que llena, las reducciones de una línea, el bucle que arma, y el `return`:

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
