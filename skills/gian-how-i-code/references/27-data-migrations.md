# 27 — Migraciones, índices y rendimiento de queries

Cargar cuando: migración nueva o editada, columna, índice, FK, seed de datos, query de listado, paginación, `with()` / eager load, reporte o export.

## Alcance

- **Núcleo:** el esquema cambia hacia adelante, sin perder datos y sin bloquear producción. Cada query de lectura declara lo que carga.
- **Adaptador Laravel:** este archivo. En Python (Alembic, Django) o Node (Prisma, Knex, TypeORM), aplican las mismas reglas con la API de su ORM.
- Transacciones e idempotencia del caso de uso: `05` §Transacciones. Esta reference no las duplica.

## Migraciones

1. **Nunca editar una migración que ya corrió en un entorno compartido.** El cambio va en una migración nueva. Una migración local sin push sí se puede editar.
2. `down()` revierte lo que hizo `up()`. Si el cambio destruye datos (drop de columna o tabla), `down()` recrea la estructura y la migración lo dice en un comentario. No se inventa un rollback de datos que no existe.
3. **Cambios destructivos en dos pasos.** Renombrar o borrar una columna en uso: (a) agregar la nueva, escribir en ambas, backfill; (b) en un deploy posterior, dejar de leer la vieja y borrarla. En el mismo deploy, solo si el usuario confirma que no hay tráfico ni otra app leyendo.
4. **Columna nueva en tabla con datos:** `nullable()` o `default(...)`. Un `NOT NULL` sin default falla o bloquea.
5. **Backfill de datos fuera de la migración de esquema.** Va en un comando o un job por lotes (`chunkById`), idempotente. La migración de esquema no recorre filas.
6. FKs con `foreignId(...)->constrained()` y una regla de borrado explícita: `cascadeOnDelete()`, `nullOnDelete()` o `restrictOnDelete()`. Elegirla según el dominio, nunca por defecto.
7. Enums de dominio: columna `string` + enum PHP (`07`), no `enum()` de base de datos. Cambiar los valores de un `enum()` de MySQL reescribe la tabla.
8. Tenancy: la migración va en la carpeta del contexto (central o tenant) que corresponde (`16`).

```php
// Mal: NOT NULL sin default en una tabla con datos, FK sin regla, backfill dentro
$table->string('status');
$table->foreignId('branch_id');
DB::table('orders')->update(['status' => 'pending']);

// Bien
$table->string('status')->default(OrderStatus::Pending->value);
$table->foreignId('branch_id')->constrained()->restrictOnDelete();
```

## Índices

1. Toda FK lleva índice (`constrained()` ya lo crea en MySQL, no en todas las bases: verificarlo).
2. Columna usada en `where`, `orderBy` o filtro de `11` sobre una tabla que crece → índice. Filtro + orden combinados → índice compuesto en ese orden (igualdad primero, rango u orden después).
3. `unique()` cuando el dominio exige unicidad. La validación del FormRequest no reemplaza al índice (carrera entre dos requests).
4. No indexar por si acaso: cada índice cuesta en escritura. Justificarlo con la query que lo usa.

## Rendimiento de lectura

1. **N+1:** toda relación que el Resource o la vista recorre se carga en la Query (`with()`, `withCount()`), nunca dentro de un loop. En desarrollo, el repo debería tener `Model::preventLazyLoading(! app()->isProduction())`. Si no lo tiene, es hallazgo, no se activa sin OK.
2. Seleccionar columnas cuando la tabla es ancha o el listado es grande (`select([...])`, `with('rel:id,name')`).
3. **Listados paginan siempre.** `paginate()` para tablas con número de página. `cursorPaginate()` para scroll infinito, feeds o tablas muy grandes. Nunca `get()` sin límite en un endpoint.
4. **Procesos masivos:** `chunkById()` o `lazyById()`, nunca `all()` o `get()` sobre la tabla completa. `chunk()` + update sobre la misma columna salta filas, por eso se usa `chunkById()`.
5. Conteos y sumas en SQL (`withCount`, `withSum`, `count()`), no en colección después de cargar todo.
6. `whereHas` sobre tablas grandes: revisar el plan. Un `join` o un `whereIn` con subquery puede ser más barato. Medir antes de cambiarlo.

## Verificación

- `php artisan migrate` y luego `migrate:rollback --step=1` y de nuevo `migrate` en la base local o de test: las tres tienen que pasar.
- Query nueva de listado: el test cuenta las queries o el repo tiene `preventLazyLoading` activo en tests.
- En el cierre (`21`), la migración se declara como riesgo de datos si borra, renombra o cambia el tipo de una columna con datos.
