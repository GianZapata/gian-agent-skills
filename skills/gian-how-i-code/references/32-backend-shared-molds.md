# 32 — Moldes backend compartidos (Laravel)

Cargar cuando: `CustomException`, envelope de error, activity log, traits, state machines, jobs con tenant, una regla de `app/Rules` (`EmailAddress`, `RfcStructural`, `Clabe`, `E164Phone`, `HumanName`, `StrongPassword`), infra copiada entre repos (backup, Dropbox, `FilterHelper`, `AttachmentService`, `SyncPermissions`, `MoneyHelper`), exports XLSX/CSV (`ExportContract` + `OpenSpout`), PDFs con Blade (`barryvdh/laravel-dompdf`), correos en cola, plantillas Blade de correo o colas Horizon.

Estas piezas existen en casi todos los repos y cada uno tiene su variante. La variante equivocada produce bugs (worker con el tenant equivocado, `status()` que pierde el modelo, dos envelopes de error, un refresh de Dropbox que avisa en cada intento). Regla general (HARD): si el repo no tiene la pieza, se crea con el molde de aquí. Si tiene otra forma, la auditoría la marca PROP para alinearla; no se reescribe sin pedirlo. Moldes de referencia: `elcaba-api` / `fortezza-api`. Dropbox y backup: `mrpobox-core` (§8).

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
- Trait `App\Traits\Models\LogsModelActivity` (`app/Traits/Models/`):

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

## 3. Traits = `app/Traits/<anfitrión>/` (HARD)

- La ubicación es la de `05` §Dónde va (`app/Traits/<anfitrión>/Nombre.php`, namespace `App\Traits\<Anfitrión>`): `Traits/Models`, `Traits/Requests`, `Traits/Controllers`, `Traits/Queries`, `Traits/Jobs`. Un solo nivel. Nunca `Concerns/` ni dentro de `app/Models`.
- Un trait en `Concerns/` (`Models/Concerns`, `Http/Controllers/Concerns`) es hallazgo Baja: se mueve al tocarlo, no en silencio.
- Un trait por responsabilidad en todo el repo. Si el mismo trait aparece en dos carpetas (`Controllers/Concerns/ResolvesScope` y `Controllers/Api/Concerns/ResolvesScope`), es hallazgo Media: una sola copia en `app/Traits/Controllers/`, con el diff de lo que difería.
- Un trait no es una bolsa de helpers: tiene una responsabilidad y su nombre la dice (`HasPersonName`, `LogsModelActivity`, `FiltersDateRange`). Lo que no lee `$this` es un helper (`08`), no un trait. Criterio de diseño en `22`.

## 4. State machines: `HasManagedStateMachines` (HARD con `asantibanez/laravel-eloquent-state-machines`)

`App\Traits\Models\HasManagedStateMachines` (molde elcaba; en elcaba/fortezza vive en `Models/Concerns`, se mueve al tocarlo):

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

`DatabaseBackupRunner`, `BackupRunResultCache`, `ValidateDropboxToken`, `AutoRefreshingTokenProvider`, `FilterHelper`, `AttachmentService`, `SyncPermissions`, `TenantHelper`, `MoneyHelper` están copiados en varios repos con variantes distintas. Un fix en uno no llega a los demás. Dropbox y backup no usan "la más completa": su referencia es §8.

- Antes de tocar una de estas piezas: compararla con la variante de referencia (Dropbox y backup, §8; el resto, la más completa y reciente; elcaba/fortezza si la tienen) y decir qué difiere.
- Un bug encontrado en una copia se reporta como hallazgo en las demás copias conocidas (PROP: "mismo bug en X, Y").
- Propuesta de fondo (PROP, `19`): extraer la pieza a un paquete compartido. No se hace sin OK.
- No se crea una variante nueva: se copia la de referencia.

## 7. Reglas de validación copiadas (HARD)

`elcaba-api` y `fortezza-api` comparten, byte a byte, `Clabe`, `E164Phone`, `EmailAddress`, `HumanName`, `KnownContractTemplatePlaceholders`, `PlatformSubdomain`, `RfcStructural`, `Settlement` y `StrongPassword`. Los tests viven en `elcaba-api` (`tests/Unit/Rules/`, trait `tests/Concerns/AssertsValidationRule`). `fortezza-api` es la copia y no trae esos tests. `ActiveClient` no es el mismo archivo. `AssignableWarehouse` y `AssignableApartment` son del producto: no se portan.

- Si el repo ya tiene una de esas clases, el FormRequest la usa. No se reescribe el regex en el request ni se sustituye `EmailAddress` por `'email'` suelto.
- Un repo que valida el correo en el FormRequest (`email`, `email.email`, `email.unique`), sin `app/Rules`, se queda así. No se le impone `EmailAddress` en la misma tarea. Ahí cada regla lleva su mensaje (`05`).
- Un bug en una clase idéntica se reporta en la otra copia (PROP). No se reescribe la otra sin pedirlo.
- El ejemplo del mensaje sale de `CompanyEmailHelper` (el dominio del producto), no de un dominio escrito en la regla. El test no afirma el dominio de otro producto.

Test de una clase en `app/Rules`: `tests/Unit/Rules/<Regla>Test.php` con `AssertsValidationRule`. Un caso que pasa (`assertRulePasses`) y uno que falla con el mensaje exacto (`assertRuleFails`). No hace falta un feature test HTTP. Test de un correo inline en el FormRequest: la regla está en `rules()`, la clave (`email.email`, `email.unique`) está en `messages()`, y `Validator::make` afirma el texto.

## 8. Dropbox y backup (HARD)

Referencia: `mrpobox-core`. `ValidateDropboxToken::check` es el mismo en mrpobox y amartinez. Lo que la copia vieja no tiene, y aquí se exige:

- `AutoRefreshingTokenProvider` comprueba credenciales, formatea el error de Dropbox y manda `DropboxBackupFailed`. `Cache::add` con TTL de una hora: un refresh roto avisa una vez, no en cada intento. Un provider que solo tiene `getToken` y `refresh` es la variante delgada.
- `BackupDisks::usable()`: si faltan `DROPBOX_APP_KEY`, `DROPBOX_APP_SECRET` o `DROPBOX_REFRESH_TOKEN`, ese disco se omite con un aviso y el respaldo sigue a los otros. No se aborta el respaldo porque Dropbox no está configurado.
- `DatabaseBackupRunner` guarda la config que va a pisar, arma el plan con esos discos, devuelve `false` si no hay destino, restaura la config, y vuelve a registrar el comando de Spatie (`Config::rebind()`, olvidar `BackupCommand`, `registerCommand`) para que el comando use los discos recién calculados.
- `BackupRunResultCache::recordCentralSkipped`: un central omitido no cuenta como éxito ni como fallo.

Al tocar cualquiera de estas clases, se compara contra mrpobox y el delta se reporta. Las copias anteriores quedan como PROP. No se reescriben en una tarea que no pidió alinearlas.

Tests que viajan con la pieza: `AutoRefreshingTokenProviderTest`, `ValidateDropboxTokenTest`, `DatabaseBackupRunnerTest`, `BackupDisksTest`, y el del comando `backup:all` si el repo tiene ese comando. `MoneyHelper` no tiene molde propio: solo entra en la lista de §6.

## 9. Exports XLSX/CSV y PDFs con Blade (HARD)

### Exports (`openspout/openspout`)

- Contrato base en `app/Exports/ExportContract.php` (`filename(): string`, `headings(): array`, `rows(): iterable`) y extensión opcional `app/Exports/FormattedExport.php` (`columnWidths(): array`, `columnFormats(): array`).
- Cada export (`app/Exports/<Entity>Export.php`) reutiliza la **`BaseQuery`** del módulo (`<Entity>Query::make($queryRequest)->getBuilder()->lazy(500)`) y produce filas con `yield $this->mapRow($model)` sobre el `Model` ya cargado.
- Prohibido duplicar filtros o scope territorial dentro de un `ReportService` o cargar tablas completas con `->get()` en memoria antes de escribir el archivo (`27`).
- Un solo escritor compartido: `app/Exports/XlsxWriter.php` (o `ExportWriter`) recibe un `ExportContract` y escribe con OpenSpout; un enum `ExportModule` mapea el módulo a su clase (`exportClass()`). Prohibido repetir el bucle `Writer`/`Row::fromValues` en cada Controller o Service.
- El streaming HTTP usa `OpenSpout` escribiendo en `php://output` (o un almacenamiento temporal si un reporte pesado corre en un Job). Cambiar de descarga directa a Job no cambia el contrato `ExportContract`.

```php
interface ExportContract {
    public function filename(): string;

    public function headings(): array;

    public function rows(): iterable;
}
```

### Imports (`openspout/openspout` Reader)

- Leer XLSX/CSV con el Reader de OpenSpout. Prohibido un lector a mano con `ZipArchive` + `XMLReader` sobre `xl/worksheets` (`hand-rolled-xlsx`, Media).
- Parse y persistencia separados: un parser en `app/Services/<Formato>/` (integración con el archivo) hace `yield` de filas normalizadas; una Action `Import<Entity>` valida y persiste por bloques (`chunk` de 500 con una transacción por bloque, nunca una sola transacción para todo el archivo).
- El archivo se valida en el FormRequest (`mimes`, `max`). Un import de más de unos cientos de filas corre en un Job (`28`) que recibe la ruta del archivo guardado, y deja un resumen (filas creadas, actualizadas, rechazadas con motivo) que el usuario puede ver.
- Auditoría: Service de import que parsea y escribe en BD dentro del request (Media).

### PDFs (`barryvdh/laravel-dompdf` + Blade)

- Todo PDF se renderiza desde una vista **Blade** en `resources/views/pdf/<nombre>.blade.php` usando `barryvdh/laravel-dompdf` (`Pdf::loadView('pdf.<nombre>', $data)`).
- Prohibido instanciar `new Dompdf(...)` directamente en `app/` o construir HTML concatenando strings en PHP (`raw-dompdf-new` en `self-check-backend.py`).
- Si el PDF se adjunta a un correo o consume datos pesados externos, la generación corre dentro de un Job (`28`), nunca bloqueando el request HTTP.
- El PDF se genera en una Action (`app/Http/Actions/<Contexto>/Generate<Doc>Pdf.php`) que arma los datos y llama a `Pdf::loadView`. Solo un renderer externo (Gotenberg u otro por HTTP) es Service en `app/Services/<Proveedor>/`. Un `<X>PdfRenderer` Service que solo llama a dompdf es un Service de dominio (`05` §Migración).

## 10. Correos en cola, plantillas Blade y colas Horizon (HARD)

- **Configuración de entorno:** `.env.example` declara siempre `MAIL_MAILER=log` (local) / `smtp` (producción), `MAIL_SCHEME`, `MAIL_HOST`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM_ADDRESS`, `MAIL_FROM_NAME="${APP_NAME}"`, junto con `QUEUE_CONNECTION` y `REDIS_*`. En `phpunit.xml`: `MAIL_MAILER=array` y `QUEUE_CONNECTION=sync`.
- **Plantillas Blade:** componentes base reutilizables en `resources/views/emails/components/layout.blade.php` y `button.blade.php`; vistas por dominio en `resources/views/emails/<contexto>/`. Sin HTML de correo escrito dentro de clases PHP.
- **Envío asíncrono y trazabilidad:** los Mailables viven en `app/Mail/<Contexto>/` y **nunca** se envían síncronos por SMTP dentro del request HTTP. Se encolan en la cola dedicada `emails` con `->afterCommit()`, `$tries` y `backoff()` (`28`): un Mailable `ShouldQueue` con `$queue = 'emails'`, `$tries`, `backoff()` y `afterCommit()` cumple; el Job envoltorio (`Send<X>MailJob` + `DeliverMail`) solo se exige cuando el transporte cambia por tenant o por cuenta (SMTP por tenant). El envío y los fallos relevantes se trazan en `spatie/laravel-activitylog` (`ActivityLogName::Mail`), sin guardar secretos ni PII sensible (`29`).
- **Supervisor vacío:** un supervisor de Horizon al que ningún Job despacha (por ejemplo `webhooks` mientras el webhook se procesa en el request) es hallazgo Media; o se mueve el trabajo al Job o se quita el supervisor.
- **Colas Horizon (`config/horizon.php`):** separar supervisores por criticidad (por ejemplo `emails`, `webhooks`/integraciones, `default`) con `tries`, `backoff` y `timeout` explícitos (con `timeout` menor que `retry_after`, `28`). No dejar todos los trabajos mezclados en una sola cola `default` cuando conviven correos, webhooks y procesos pesados.

## 11. Query de listado vs. Query agregada (HARD)

- **Listado** (tabla paginada, select, export): extiende `BaseQuery` (`05`), con allowlists de filtros/sorts/includes y orden determinista. Un listado que arma su `QueryBuilder` a mano o pagina con `perPage` fijo es hallazgo.
- **Agregada** (dashboard, reporte, KPI, mapa): `final class <X>Query` en `app/Queries/<Contexto>/` con un único `handle(...): array` (o DTO) que recibe los filtros ya validados (rango de fechas, scope). Cuando crece, se parte en secciones (`<X>Section` o métodos privados por bloque), no en un Service.
- Prohibido `DashboardService`, `ReportService` o `<X>AnalyticsService` de dominio: la lectura es Query (`05` §Migración).
- Ambas aplican el scope territorial/tenant en un solo lugar (trait de la Query o `BaseQuery`), nunca repetido por método.

Auditoría (§9, §10 y §11): `new Dompdf(` directo (Media), `->get()` sin `lazy`/`chunkById` en export masivo (Media), envío de `Mail::send()` síncrono dentro de un controller o transacción (Media), `.env.example` sin claves `MAIL_*` en un proyecto que envía correos (Baja).
