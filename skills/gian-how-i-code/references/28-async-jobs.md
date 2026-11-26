# 28 — Jobs, colas y tareas programadas

Cargar cuando: Job nuevo o editado, `dispatch`, listener en cola, notificación o mail en cola, comando programado (`schedule`), webhook entrante o saliente, integración externa.

## Alcance

- **Núcleo:** un trabajo asíncrono puede correr dos veces, tarde, en desorden o nunca. El código lo asume.
- **Adaptador Laravel:** este archivo. En Python (Celery, RQ, arq) o Node (BullMQ), las mismas reglas con su API.
- Transacción, idempotencia y efectos externos del caso de uso: `05` §Transacciones (líneas de idempotencia y `afterCommit`). Esta reference agrega lo específico de la cola y no lo repite.

## Reglas

1. **El Job no tiene lógica de negocio.** Recibe IDs, carga el modelo y llama a la Action (`05`). La lógica se prueba en la Action sin cola.
2. **Payload chico:** IDs o modelos (`SerializesModels` los re-hidrata). Nunca colecciones grandes, archivos ni arrays con datos personales.
3. **Despachar después del commit.** Un dispatch dentro de `DB::transaction` usa `->afterCommit()` (o `after_commit` en la conexión de cola). Si no, el worker puede leer datos que todavía no existen o que se revirtieron.
4. **Idempotente.** Correr el job dos veces deja el mismo resultado. Revisar el estado antes de actuar (`if ($order->isPaid()) return;`) o usar una clave de idempotencia (`05`).
5. **Reintentos declarados.** Todo Job define `$tries` (o `retryUntil()`) y `backoff()`. Un error permanente (validación, registro borrado) no se reintenta: `$this->fail($e)` o `deleteWhenMissingModels = true`.
6. `failed(Throwable $e)` cuando el usuario o un operador tiene que enterarse (estado `failed` en el modelo, notificación). Si no, el job falla en silencio en `failed_jobs`.
7. **Exclusión:** si dos ejecuciones simultáneas sobre el mismo recurso rompen algo, usar `ShouldBeUnique` (no encolar duplicados) o el middleware `WithoutOverlapping($id)` (no correr a la vez). Elegir según el caso y decirlo.
8. **Timeout:** `$timeout` menor que el `retry_after` de la conexión. Si no, el mismo job corre dos veces en paralelo.
9. **Llamadas externas:** timeout explícito en el cliente HTTP (`Http::timeout()->retry()`), y para un 429 o 5xx `release($delay)` en vez de fallar.
10. **Comandos programados:** `withoutOverlapping()` y `onOneServer()` cuando hay más de un servidor. Un comando que procesa muchos registros despacha jobs por lote (`28` + `27` §procesos masivos).
11. **Tenancy:** el job conoce su tenant: `QueueTenancyBootstrapper` activo, o `tenantId` escalar + `TenantHelper::run` que restaura en `finally` (`32` §5). Nunca `tenancy()->initialize()` sin restaurar. Verificarlo en `16`.
12. **Webhook entrante:** validar la firma, responder 2xx rápido y procesar en un job. Deduplicar por el ID del evento del proveedor.

```php
// Mal: lógica en el job, dispatch dentro de la transacción, sin reintentos
public function handle(): void
{
    $this->order->update(['status' => 'paid']);
    Mail::to($this->order->user)->send(new Paid($this->order));
}

// Bien
public int $tries = 5;

public function backoff(): array
{
    return [10, 60, 300];
}

public function handle(MarkOrderPaid $action): void
{
    if ($this->order->isPaid()) {
        return;
    }

    $action->execute($this->order);
}
```

## Verificación

- Test de la Action sin cola. Test del dispatch con `Queue::fake()` y `assertPushed` (con los argumentos).
- Un test que corra el job dos veces y verifique el mismo estado final, cuando la regla 4 aplica.
- En el cierre (`21`), declarar reintentos, unicidad y qué pasa si el job falla definitivamente.
