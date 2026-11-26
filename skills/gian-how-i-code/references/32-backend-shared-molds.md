# 32 — Moldes backend compartidos (Laravel)

Cargar cuando: `CustomException`, envelope de error, activity log, traits/concerns, state machines, jobs con tenant, infra copiada entre repos (backup, Dropbox, `FilterHelper`, `AttachmentService`, `SyncPermissions`).

Estas piezas existen en casi todos los repos y cada uno tiene su variante. La variante equivocada produce bugs (worker con el tenant equivocado, `status()` que pierde el modelo, dos envelopes de error). Regla general (HARD): si el repo no tiene la pieza, se crea con el molde de aquí. Si tiene otra forma, la auditoría la marca PROP para alinearla; no se reescribe sin pedirlo. Moldes de referencia: `elcaba-api` / `fortezza-api`.

## 1. Error: `ApiErrorResponse` + `CustomException` (HARD)

`App\Http\Responses\ApiErrorResponse::make(message, code, status, params, errors)` es lo único que arma el JSON de error. Lo usan el handler (`bootstrap/app.php` → `withExceptions`) y `CustomException::render`. Shape fijo: `{ message, code, params, errors }`; `params` y `errors` vacíos salen como `{}` (`new \stdClass`), no `[]`.

```php
class CustomException extends Exception implements ShouldntReport {
    public function __construct(
        string $message,
        private readonly int $statusCode = 400,
        public readonly array $errors = [],
        public readonly ?string $errorCode = null,
        public readonly array $params = [],
        ?Throwable $previous = null,
    ) {
        parent::__construct($message, $statusCode, $previous);
    }

    public function render($request): JsonResponse {
        return ApiErrorResponse::make(
            message: $this->getMessage(),
            code: $this->errorCode,
            status: $this->statusCode,
            params: $this->params,
            errors: $this->errors,
        );
    }
}
```

- Para un error de negocio esperado (regla del dominio, estado inválido, recurso ajeno). Se lanza con argumentos con nombre: `throw new CustomException('El contrato ya está firmado.', 409, errorCode: 'contract_already_signed')`.
- `errorCode` es `snake_case` estable: el front lo consume (`14`), no se renombra. El mensaje se traduce; el código no.
- Un fallo técnico traducido a `CustomException` pasa `previous:` y decide cómo se reporta (`ShouldntReport` no reporta solo; `05` §Transacción y error).
- Lo inesperado sale con `throw` normal al handler. El handler traduce las excepciones del framework (401, 403, 404, 405, 422, tenant no encontrado) con el mismo `ApiErrorResponse`.

Auditoría:

| Señal | Severidad |
|---|---|
| `CustomException` mínima (`response()->json` a mano, sin `errorCode` ni `ShouldntReport`) | Media |
| Excepción HTTP propia sin `render` ni envelope (`App\Core\Exception\HttpException` de un framework legacy) | Media |
| `response()->json(['message' => ...], 4xx)` en controller o Action | Media |
| `abort()` en Action o Service (el `abort` es del borde HTTP) | Baja |
| Dos shapes de error en el mismo repo | Alta |

## 2. Activity log: `ActivityLogName` + `LogsModelActivity` (HARD con `spatie/laravel-activitylog`)

- `App\Enums\ActivityLogName: string`, un case por área (`User = 'user'`, `ContractTemplate = 'contract_template'`). El nombre del log nunca es un string suelto.
- Trait `App\Models\Concerns\LogsModelActivity`:

```php
trait LogsModelActivity {
    use LogsActivity;

    public function getActivitylogOptions(): LogOptions {
        return LogOptions::defaults()
            ->logOnly($this->activityLogAttributes())
            ->useLogName($this->activityLogName()->value)
            ->logOnlyDirty()
            ->dontLogEmptyChanges();
    }

    abstract protected function activityLogAttributes(): array;

    abstract protected function activityLogName(): ActivityLogName;
}
```

- El modelo usa el trait e implementa los dos métodos. No reimplementa `getActivitylogOptions`.
- `activityLogAttributes()` lista campos de negocio. Nunca password, tokens, secretos ni datos sensibles completos (`29`).
- Log manual (evento sin modelo): `activity(ActivityLogName::X->value)->performedOn($m)->event('...')->log('...')`.

Auditoría: `useLogName('literal')` (Media), `getActivitylogOptions` copiado en 2+ modelos (Media), `activity('literal')` (Baja), atributo sensible en `logOnly` (Alta).

## 3. Traits = `Concerns/` por capa (HARD)

- Un trait vive en el `Concerns/` de la capa que lo usa: `app/Models/Concerns`, `app/Http/Requests/Concerns`, `app/Http/Controllers/Concerns`, `app/Queries/Concerns`, `app/Jobs/Concerns`. Nunca `app/Traits/`.
- Un concern por responsabilidad en todo el repo. Si el mismo trait aparece en dos capas o dos carpetas (`Controllers/Concerns/ResolvesScope` y `Controllers/Api/Concerns/ResolvesScope`), es hallazgo Media: una sola copia, en la capa más baja que lo necesita.
- Un trait no es una bolsa de helpers: tiene una responsabilidad y su nombre la dice (`HasPersonName`, `LogsModelActivity`, `FiltersDateRange`). Lo que no lee `$this` es un helper (`08`), no un trait. Criterio de diseño en `22`.

## 4. State machines: `HasManagedStateMachines` (HARD con `asantibanez/laravel-eloquent-state-machines`)

`App\Models\Concerns\HasManagedStateMachines` (molde elcaba):

```php
trait HasManagedStateMachines {
    use HasStateMachines {
        HasStateMachines::bootHasStateMachines as protected bootHasStateMachinesTrait;
    }

    public static function bootHasStateMachines(): void {
        static::whenBooted(fn() => static::bootHasStateMachinesTrait());
    }

    /**
     * Resuelve `status()` / `fooBar()` directamente desde $stateMachines, sin depender
     * de los macros globales de MacroableModels (que pueden perder el modelo en workers de larga vida).
     */
    public function __call($method, $parameters) {
        foreach ($this->stateMachines ?? [] as $field => $machineClass) {
            if ($method === $field || $method === Str::camel($field)) {
                $stateMachine = new $machineClass($field, $this);

                return new State($this->{$stateMachine->field}, $stateMachine);
            }
        }

        return parent::__call($method, $parameters);
    }
}
```

- Todo modelo con `$stateMachines` usa este trait, no `HasStateMachines` directo.
- Prohibido registrar el accessor con `MacroableModels::addMacro` propio (recupago, soccer-survivor, medesa, todoempleos): en un worker de Horizon/Octane el macro queda atado a una instancia vieja y `status()` responde con otro modelo. Es Alta en auditoría.
- Historial: `recordHistory()` del paquete (`05` §Historial). Prohibido un trait propio que duplique `state_histories` (`RecordsStateMachineHistory`).
- El resto (transiciones, consts, prohibido `update` de `status`) sigue en `05` §State machines y `07`.

## 5. Jobs con tenant: `TenantHelper::run` (HARD con tenancy)

`App\Helpers\TenantHelper` (molde fortezza/elcaba) inicializa el tenant solo si cambia y restaura el original en `finally`:

```php
final class TenantHelper {
    public function run(Tenant $tenant, Closure $callback): mixed {
        $original = tenant();

        if (!$this->isSame($original, $tenant)) tenancy()->initialize($tenant);

        try {
            return $callback();
        } finally {
            $this->restore($original);
        }
    }
    // restore(): end() si no había tenant; initialize($original) si cambió. isSame() compara getTenantKey().
}
```

- Un job tenant guarda `public readonly string $tenantId` (escalar) y los IDs del caso; no serializa el `Tenant` ni modelos tenant si el `QueueTenancyBootstrapper` no está activo en la conexión.
- `handle()` corre todo dentro de `TenantHelper::run(Tenant::findOrFail($this->tenantId), fn () => ...)`, o el job confía en `QueueTenancyBootstrapper` y la auditoría verifica que esté en `config/tenancy.php`. Uno de los dos, declarado; nunca los dos a medias.
- Prohibido `tenancy()->initialize()` sin restaurar en `finally`: el siguiente job del mismo worker corre en ese tenant (Alta).
- Comando que recorre tenants: `Tenant::query()->each(fn ($t) => $helper->run($t, ...))` o despacha un job por tenant con `tenantId`.
- El resto del job (afterCommit, tries, backoff, unique, failed) sigue en `28`.

## 6. Infra copiada entre repos (PROP)

`DatabaseBackupRunner`, `BackupRunResultCache`, `ValidateDropboxToken`, `FilterHelper`, `AttachmentService`, `SyncPermissions`, `TenantHelper` están copiados en 4 a 8 repos con 4 a 8 variantes. Un fix en uno no llega a los demás.

- Antes de tocar una de estas piezas: compararla con la variante de referencia (la más completa y reciente; elcaba/fortezza si la tienen) y decir qué difiere.
- Un bug encontrado en una copia se reporta como hallazgo en las demás copias conocidas (PROP: "mismo bug en X, Y").
- Propuesta de fondo (PROP, `19`): extraer la pieza a un paquete compartido. No se hace sin OK.
- No se crea una variante nueva: se copia la de referencia.
