# 05 — Molde backend (Laravel)

Cargar cuando: endpoints, Actions, Queries, Resources, Form Requests, state machines.

## Alcance

- **Núcleo:** la responsabilidad de cada capa (validación en el borde, caso de uso, contrato de lectura, enum y estado) vive en la matriz de `01`.
- **Adaptador Laravel:** este archivo. En Python o Node, la fila de su stack en `01`.

Formato visual PHP (indent, braces, `=>`, guards): `gian-php-style`. Esta reference no duplica esas reglas.

## Flujo HTTP

```text
Route → Controller (delgado) → FormRequest → Action → Resource
Lectura compleja → Query (Spatie QueryBuilder) → Resource
```

- Actions: mutaciones, transacciones, dominio
- Queries: includes, filters, sorts, counts
- Resources: serializan; **no** cargan relaciones ni disparan queries; `whenLoaded` al ctor del Resource (`06`)
- Lista: `Resource::collection` o el `ResourceCollection` de la feature si la lista necesita envoltura propia. No una clase aparte para el arreglo.
- Services Laravel: solo integraciones externas

## Dónde va un valor, no en Support

Antes de crear el archivo, nombrar qué es. No agregarlo a `Support` o `Supports` porque la carpeta ya existe. Una feature nueva no abre esa carpeta ni le suma archivos. Si el repo ya la tiene, no es el molde y no se migra en silencio.

| Qué es | Dónde |
|---|---|
| Cableado de un paquete, o un tope que cambia por entorno | `config`. El config puede nombrar una clase; no es el lugar del comportamiento |
| Regla o valor de una entidad | El modelo dueño |
| Conjunto cerrado de nombres | Enum. No una clase con `const VALUES` |
| Transformación reutilizada de un solo eje | Helper `final` en `Helpers`, `public static`, como un eje ya cohesivo. Si ese eje existe, se extiende. No uno nuevo por un solo arreglo |
| El paquete hace `new` de la clase | Adaptador. No es un helper. El config solo guarda el nombre de la clase |
| Lo usa un solo dueño | Método privado de ese dueño. `private static` si no usa `$this` |
| Solo lo usan un test o un seeder | Fixture. No código de producto |
| Solo `__construct` | No se crea. Ni en `Support` ni en `Helpers` |

Al implementar, si se toca una clase que solo tiene constructor, se borra y el paso vuelve al dueño. No se renombra a `Support`. Auditoría: hallazgo Alto, sin editar.

### Forma a copiar

- Action: clase `final`, método `handle`, sin constructor si el método no usa una dependencia inyectada.
- Query: el cálculo que solo usa esa query es un método privado de la query.
- Valor reutilizado: helper estático en `Helpers`.
- Adaptador de paquete: la clase que el paquete instancia, al lado de esa integración. No en `Support`.

## Query table aliases

Cuando Query Builder, `DB::table`, `from`/`join` o SQL crudo **necesita** alias de tabla:

- Nivel 0 (query raíz): `t1`, `t2`, `t3`, … en orden de aparición (`from` = `t1`, primer join = `t2`).
- Subquery: un `s` por nivel de anidamiento, luego `t` + índice **en ese nivel** (el índice reinicia por subquery).
  - profundidad 1 → `st1`, `st2`
  - profundidad 2 → `sst1`, `sst2`
  - profundidad 3 → `ssst1`, …
- No mnemonicos: no `u`, `o`, `users u`, `orders o`.

```php
DB::table('users as t1')
    ->join('orders as t2', 't2.user_id', '=', 't1.id')
    ->select('t1.id', 't2.total');

DB::table('users as t1')
    ->whereIn('t1.id', function ($q) {
        $q->from('orders as st1')
            ->select('st1.user_id');
    });
```

No:

```php
DB::table('users as u')
    ->join('orders as o', 'o.user_id', '=', 'u.id');
```

No forzar alias en un from de una sola tabla sin join/self-join: `DB::table('users')`.

No aplica a relaciones Eloquent (`$user->orders()`), nombres de tabla reales ni columnas. Formato visual PHP: `gian-php-style`.

GAP: alias en `with()` / eager load — no FAIL. Lateral joins / CTEs si el nivel no es un subquery claro — GAP.

## Resources y verdad derivada

- Flags/agregados de negocio en Resource, no en FE
- Accessor con relación: `relationLoaded()`; si no cargó → `null` (no `0`)
- Contar colección cargada; **nunca** `$this->rel()->count()` (N+1)
- Conteos filtrables/ordenables en listados → `withCount` / `withExists` en Query (forzado si se filtra/ordena)

## State machines

- Paquete tipo `asantibanez/laravel-eloquent-state-machines`
- Prohibido `update` de `status` a mano
- `bootHasStateMachines()` en `boot()` para jobs async
- Estados como `public const` UPPER_SNAKE en la SM + `values()` (fuente única; ver `07`)
- Nuevo estado = SM (const + transitions) + DB enum/constraint + factories + labels UI (TS string enum)
- No backed Enum PHP paralelo para los mismos estados salvo necesidad demostrada
- Membresía 2+ estados: `in_array(..., true)` / `.includes()` — ver `07`

## Form Requests

Store/Update definen validación y autorización. DTOs FE alineados al Request, no al Resource completo. Status de SM: `Rule::in(EntityStatusStateMachine::values())`.

### User-Facing Validation Contracts (HARD)

Cuando se cree o modifique validación de datos introducidos por un usuario:

1. MUST revisar las reglas **y** los mensajes visibles asociados.
2. En Laravel, revisar explícitamente `rules()`, `messages()`, y `attributes()` **cuando sea útil** (ver abajo).
3. Agregar mensajes específicos para cualquier regla cuyo default exponga implementación, nombres internos, sea ambiguo o no explique qué debe corregir el usuario.
4. Agregar, modificar o eliminar una regla MUST disparar la revisión de su mensaje resultante.
5. **No** considerar un FormRequest terminado solamente porque `rules()` está implementado.

`attributes()` es **condicional**. Revisarlo y usarlo cuando el nombre interno pudiera llegar al usuario vía `:attribute`, o cuando haga falta copy humano. Un Request con mensajes específicos ya human-facing puede ser válido **sin** `attributes()`. No exigir el método por existencia estructural.

### Human-facing language

Los mensajes visibles MUST usar lenguaje del dominio. SHOULD orientar sobre qué ingresar, seleccionar o corregir.

MUST NOT exponer innecesariamente: `boolean`, `regex`, `enum`, `UUID`, tipos internos, nombres de columnas, clases, excepciones, reglas internas de validación.

MAY usar términos técnicos cuando formen parte real de la audiencia o dominio (`URL`, `PDF`, `CSV`, `API key`).

```text
BAD:  El estatus debe ser un valor booleano
GOOD: Selecciona un estatus válido

BAD:  El campo is_active es obligatorio
GOOD: Selecciona el estatus del usuario

BAD:  El teléfono no cumple con el regex
GOOD: Ingresa el teléfono con código de país, por ejemplo +521234567890
```

### Coverage gate (semántico)

Validation message coverage is semantic, not structural.
Do not require one `messages()` entry per validation rule.
Every reachable user-facing validation failure MUST resolve to acceptable human-facing copy.

Cobertura puede existir mediante:

- `messages()` específico;
- mensajes globales/localizados;
- `attributes()` + mensaje global adecuado.

La omisión de un mensaje específico MUST ser deliberada: el agente MUST comprobar el mensaje **resultante** y no asumir que el default es aceptable.

No implementar gates del tipo `count(rules) === count(messages)`.

Revisión conceptual:

```text
rule -> resulting user-facing message
full_name.required      -> covered
email.required          -> covered
email.email             -> covered
email.unique            -> covered
phone.regex             -> covered
is_active.required      -> covered
is_active.boolean       -> covered
```

### Backend → frontend

Si hay UI que consume esa validación: MUST comprobar el camino real del 422; MUST asignar errores por campo a los inputs cuando esa sea la arquitectura del repo; MUST preferir el mensaje human-facing del backend (no sustituirlo por un genérico). Definir buenos mensajes en BE y no mostrarlos en FE **no** cuenta como integración completa. No introducir arquitectura nueva de errores si el proyecto ya tiene patrón — ver `10`/`14`.

### Completion gate

Una tarea que modifica formularios o validación user-facing no puede declararse completa hasta revisar, según aplique:

```text
[ ] rules
[ ] messages
[ ] human-facing terminology
[ ] semantic rule/message coverage
[ ] field names / attributes
[ ] backend 422 contract
[ ] frontend field-error consumption
```

## Checklist BE

- [ ] Controller delgado
- [ ] Request + Action + Resource / Query
- [ ] Sin `Support` ni clase cuyo único miembro es el constructor
- [ ] Includes/filters/sorts explícitos
- [ ] Tipos cerrados: backed Enum **o** constantes SM (no ambos para lo mismo)
- [ ] SM con const + transitions + defaultState + bootHasStateMachines
- [ ] Tests focalizados si cambia comportamiento
- [ ] Joins/SQL: alias `t1`/`t2`; subquery `st1`/`sst1` (no `users u`)
- [ ] User-facing validation (`05`): no done solo con `rules()`; completion gate si toca FormRequest/form

Ver `assets/backend/`.
