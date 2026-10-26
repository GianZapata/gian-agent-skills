# 05 — Molde backend (Laravel)

Cargar cuando: endpoints, Actions, Queries, Resources, Form Requests, state machines.

## Alcance

- **Núcleo:** la responsabilidad de cada capa (validación en el borde, caso de uso, contrato de lectura, enum y estado) vive en la matriz de `01`.
- **Adaptador Laravel:** este archivo. En Python o Node, la fila de su stack en `01`.

Formato visual PHP (indent, braces, `=>`, guards): `gian-php-style`. Esta reference no duplica esas reglas.

Orden del cuerpo del método tocado: `26`. Si el edit entra en el método, se reordena ese método. El otro método del archivo no. Esta reference no duplica ese orden.

## Flujo HTTP

```text
Route → FormRequest → Controller (delgado) → Action → Resource
Job o comando → Action
Lectura compleja → Query (Spatie QueryBuilder) → Resource
```

Laravel valida el FormRequest antes de invocar el método del controller.

| Capa | Garantiza |
|---|---|
| FormRequest | Entrada HTTP: requerido, formato, tipo, límite. Puede adelantar un rechazo |
| Controller | Datos y contexto, llama a la Action, arma la respuesta. No decide el negocio |
| Action | Condiciones del caso, escrituras, transacción si hace falta, errores conocidos. Sigue siendo válida si la llaman un Job u otra Action, sin ese Request |
| Resource | Serializa. No carga relaciones ni dispara queries |
| Policy | Permiso. Si no hay HTTP, se reutiliza con el actor explícito |
| Modelo | Invariante cohesiva de esa entidad |
| Base | Constraint, índice único o bloqueo. Protege la escritura. No reemplaza a la Action |

La Action coordina esas garantías. No las duplica por rutina. Una comprobación en el Request mejora la respuesta temprana. No sustituye la garantía junto a la escritura.

Al crear, modificar o auditar un caso, se recorre el flujo aunque la Action tenga una línea. En implementación autorizada, se ponen las protecciones que el contrato ya exige. Si falta una regla de negocio, se plantea esa decisión y se sigue con lo independiente. La ausencia de una regla extra no es, por sí sola, una decisión pendiente. Pendiente solo si una ambigüedad concreta cambia el caso. Auditar no modifica.

Buscar una mejora justificada es obligatorio aunque el caso cumpla. No hay cupo mínimo. No se agrega transacción, `catch`, clase, validación ni idempotencia por rutina. Tener `transaction()` y `CustomException` no demuestra que el flujo sea correcto.

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
| La integración exige o consume la clase | Adaptador. Config, factory, contenedor o `new`. El config puede nombrar la clase. Buscar un `new` literal no basta. No es un helper |
| Lo usa un solo dueño | Método privado de ese dueño. `private static` si no usa `$this` |
| Solo lo usan un test o un seeder | Fixture. No código de producto |
| Solo agrupa variables, sin comportamiento ni invariante | No se crea. Ni en `Support` ni en `Helpers` |
| Reglas y mensajes compartidos por el Store y el Update de una entidad | Clase base abstracta `<Entity>Request` en `app/Http/Requests/<Entity>/` (§Form Requests) |
| Trait horizontal | `app/Traits/<anfitrión>/`. Un solo nivel. Modelos: `app/Traits/Models/`, namespace `App\Traits\Models`. Un bloque de reglas reutilizado por requests de entidades distintas: `app/Traits/Requests/` |

No se crea una clase solo para agrupar variables. Una clase que ya existe y solo declara constructor no se borra por eso: mirar consumidores, herencia, si el constructor valida un invariante, y si el comportamiento viene del padre. Estar en `Support` incumple el molde. Es desviación de convención, no un nivel de severidad. La gravedad depende del impacto, la frecuencia y el riesgo sustentados por evidencia (`18`, `24`). No se migra esa carpeta en silencio.

### Forma a copiar

- Action: clase `final`, método `handle`, sin constructor si el método no usa una dependencia inyectada.
- Query: el cálculo que solo usa esa query es un método privado de la query.
- Valor reutilizado: helper estático en `Helpers`.
- Adaptador: la clase que la integración exige o consume, al lado de esa integración. No en `Support`.
- Trait: `app/Traits/<anfitrión>/Nombre.php`. El anfitrión es el tipo de clase que lo usa (`Models`, `Jobs`, `Actions`). Un trait de modelo es `app/Traits/Models/Nombre.php`, namespace `App\Traits\Models`. No vive en `app/Models` ni en `Concerns`. Un trait que ya está plano en `app/Traits/` no se mueve en silencio. La regla vale para un trait nuevo y para el que se toca.

## Transacción y error

La Action dueña delimita qué se confirma junto. Una Action reutilizable puede abrir transacción si corre sola, y participar en la exterior si la llaman. En la misma conexión, Laravel usa savepoints cuando el motor los soporta. Lo interior se confirma cuando termina la exterior. Otra conexión no entra en ese rollback: mirar la conexión efectiva de cada modelo.

Un `catch` puede traducir o limpiar una causa conocida si el fallo indispensable sale con `throw`. No vale capturar dentro del callback, devolver un valor y seguir: Laravel da la transacción por buena. `CustomException` se lanza, no se retorna. `render()` construye la respuesta HTTP. Si la excepción escapa del callback de una transacción, Laravel revierte esa transacción antes de propagarla. Renderizar una excepción no revierte escrituras por sí mismo. Si el error ocurre fuera de la transacción, o después del commit, no hay rollback.

Si B escribió y falla, A puede seguir con un resultado parcial autorizado solo después de que B haya revertido sus escrituras. El `catch` puede estar en A, fuera del callback de B. Que B sea opcional no basta para conservar escrituras incompletas, ni para seguir si el fallo invalida toda la operación.

Durante la transacción se conserva el error que Laravel usa para reintentar, deadlock incluido. No se traduce a `CustomException` mientras esos reintentos sigan abiertos. Cuando se agotan, puede mapearse a una respuesta controlada, con `previous` y el reporte.

El handler traduce las excepciones del framework al envelope. No se copia dentro de cada Action. El borde ajeno traduce lo conocido a `CustomException` y relanza el resto. Los mensajes visibles, incluidos los errores por campo, usan el idioma soportado del usuario y el fallback del proyecto. `code`, status y claves de campo quedan estables. Se traduce el mensaje, no la clave. La traducción puede ocurrir antes de construir `CustomException`. Se recorre ese camino. Si no existe, se identifica y se propone. No se inventa un sistema de i18n en el mismo corte. `ShouldntReport` no reporta solo: un fallo técnico convertido en `CustomException` conserva la causa y define cómo se reporta.

La idempotencia no es un `catch` ni un default de cada `create`. Cuando el efecto no puede repetirse, se nombran la clave, el alcance de tenant y actor, la adquisición atómica, el resultado guardado, y qué pasa si la misma clave llega con otros datos. No se devuelve el resultado viejo si el payload cambió. Se autoriza antes de devolver un resultado protegido.

Saldo, stock, cupo o disponibilidad se protegen junto con la escritura: índice único, operación atómica o bloqueo. Una comprobación previa, aunque sea de backend, puede quedar vieja. La comprobación previa orienta al sistema. No se publica como "Disponible". Guardar resuelve la colisión.

Los efectos de afuera no los deshace la base. Por flujo se evalúa cuándo correrlos, qué pasa si se repiten, y cómo recuperarse si la base ya confirmó y después fallan: reintento, estado pendiente o compensación. `afterCommit()` espera la transacción exterior. La idempotencia evita repetir el efecto. No se exigen los dos mecanismos iguales en cada integración.

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

### Store y Update de la misma entidad (HARD)

Si existen el Store y el Update de una entidad, sus reglas y mensajes viven una sola vez, en una clase base abstracta `<Entity>Request` en `app/Http/Requests/<Entity>/`. Si solo existe uno, no hay base (`22`: sin abstracta de una sola implementación).

La base declara `authorize()`, `rules()`, `messages()` y, si hace falta, `attributes()`. Store y Update solo implementan `presence(): array`, que se esparce en cada campo obligatorio de la raíz.

```php
use App\Models\Invoice;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

abstract class InvoiceRequest extends FormRequest {
    public function authorize(): bool {
        return true;
    }

    abstract protected function presence(): array;

    public function rules(): array {
        return [
            'number'      => [
                ...$this->presence(),
                'string',
            ],
            'code'        => [
                'string',
                Rule::unique(Invoice::class)->ignore($this->route('invoice')),
            ],
            'note'        => [
                'nullable',
                'string',
            ],
            'items.*.qty' => [
                'required_with:items.*.price',
                'integer',
            ],
        ];
    }
}

final class StoreInvoiceRequest extends InvoiceRequest {
    protected function presence(): array {
        return ['required'];
    }
}

final class UpdateInvoiceRequest extends InvoiceRequest {
    protected function presence(): array {
        return [
            'sometimes',
            'required',
        ];
    }
}
```

- `presence()` va solo en campos obligatorios de la raíz. Un campo opcional no lleva `sometimes`: las reglas no implícitas no corren sobre un campo ausente.
- Una key anidada (`items.*.qty`) nunca lleva `sometimes`: un item enviado sin esa key pasaría el `required_with`.
- Update parcial (PATCH): `['sometimes', 'required']`. Update que reemplaza todo (PUT): `['required']`.
- `unique` vive una vez en la base, con `->ignore($this->route('<param>'))`. En el Store la ruta no trae el parámetro e `ignore(null)` no excluye nada.
- Una diferencia que no es de presencia (por ejemplo, un campo inmutable al editar) se escribe en la subclase: `[...parent::rules(), 'status' => ['prohibited']]`.
- Prohibido: recorrer las reglas para inyectar `sometimes` o `required` (`foreach` + `array_unshift`, filtros por nombre de key con `Str::contains`), redefinir en el Update una regla que ya está en la base, y usar un trait para compartir reglas entre el Store y el Update de una misma entidad.
- Al tocar un Store o Update que comparte reglas con un trait o un loop, se reemplaza por la base en ese par. El trait se borra si queda sin uso. No se conserva el loop por compatibilidad.

### Bloque de reglas en entidades distintas

Si el mismo bloque (dirección, contacto, periodo) se valida en requests de entidades distintas: trait en `app/Traits/Requests/<Eje>Rules.php`, namespace `App\Traits\Requests`. Expone métodos con el nombre del eje (`addressRules(string $prefix = '')`, `addressMessages(string $prefix = '')`). No declara `rules()`, `messages()` ni `authorize()`, y no lee `$this->route()`. Cada request arma su `rules()` con `...$this->addressRules('billing.')` y su `messages()` con `...$this->addressMessages('billing.')`.

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
- [ ] Lugar decidido antes de crear el archivo. `Support` no es el molde. No se creó una clase solo para agrupar variables
- [ ] Includes/filters/sorts explícitos
- [ ] Tipos cerrados: backed Enum **o** constantes SM (no ambos para lo mismo)
- [ ] SM con const + transitions + defaultState + bootHasStateMachines
- [ ] Tests focalizados si cambia comportamiento
- [ ] Joins/SQL: alias `t1`/`t2`; subquery `st1`/`sst1` (no `users u`)
- [ ] User-facing validation (`05`): no done solo con `rules()`; completion gate si toca FormRequest/form
- [ ] Store/Update de la misma entidad: base `<Entity>Request` + `presence()`; sin loop de presencia ni reglas redefinidas

Ver `assets/backend/`.
