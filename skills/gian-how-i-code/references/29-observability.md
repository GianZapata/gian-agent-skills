# 29 — Logging, auditoría, cache y rate limiting

Cargar cuando: `Log::` o logger, `catch` que traga o re-lanza, integración externa, acción sensible (dinero, permisos, borrado, datos personales), cache, endpoint público o de autenticación.

## Alcance

- **Núcleo:** cuando algo falla en producción, el log dice qué, a quién y con qué ID, sin exponer datos personales. Lo que se cachea se invalida en el mismo cambio.
- **Adaptador Laravel:** este archivo. En Python (`logging`, structlog) o Node (pino), las mismas reglas.
- Errores hacia el usuario (toasts, 422, mensajes): `14`. Esta reference cubre lo que ve el operador, no el usuario.

## Logging

1. **Mensaje fijo + contexto en array.** `Log::warning('Payment declined', [ 'order_id' => $order->id, 'gateway_code' => $code ])`. Nunca datos interpolados en el mensaje: no se pueden agrupar ni buscar.
2. Contexto común (request ID, tenant, usuario) una vez por request o job con `Context::add()` (Laravel 11+) o `Log::withContext()`. No repetirlo en cada línea.
3. **Nivel correcto:** `error` = alguien tiene que actuar; `warning` = degradado pero recuperado; `info` = evento de negocio relevante; `debug` = desarrollo. Un error esperado de validación no es `error`.
4. **Nunca loguear:** contraseñas, tokens, headers `Authorization`, números de tarjeta, documento de identidad completo, payloads completos de request o de un proveedor. Loguear el ID y los campos necesarios.
5. **`catch` que no re-lanza, loguea** con la excepción en el contexto (`'exception' => $e`). Un `catch` vacío es hallazgo. Si re-lanza, no loguea (el handler ya lo hace, si no queda duplicado).
6. Integración externa: loguear request ID del proveedor, status y duración. No el body.

## Auditoría

1. Acción sensible (cambio de rol o permiso, dinero, borrado, exportación de datos personales) deja rastro de quién, cuándo, qué y valor anterior. Usar el mecanismo del repo (activity log, state machine `recordHistory` en `05`, tabla de auditoría). Si el repo no tiene ninguno, es PROP (`19`), no se instala sin OK.
2. El log de aplicación no es auditoría: rota y no se consulta desde el producto.

## Cache

1. **Cachear solo con una razón medida** (query cara, API externa con límite). No por defecto.
2. Clave con todo lo que cambia el resultado: tenant, usuario o rol si aplica, filtros, versión. `"reports:{$tenantId}:{$month}"`.
3. **La invalidación va en el mismo cambio que escribe el dato** (`Cache::forget` en la Action, o tags si el driver los soporta). Un cache sin invalidación declarada es hallazgo.
4. TTL siempre explícito. `rememberForever` solo para datos que cambian con un deploy.
5. Nunca cachear respuestas con datos de otro usuario bajo una clave compartida.

## Rate limiting

1. Login, registro, recuperación de contraseña, OTP, endpoints públicos y endpoints que disparan correos, SMS o cobros llevan `throttle`. Si el repo los tiene sin límite, es hallazgo de seguridad.
2. Límite con nombre en `RateLimiter::for(...)`, por usuario autenticado o por IP si no hay usuario. No un número suelto en cada ruta.
3. La respuesta 429 usa el envelope de error del repo (`06`, `14`).

## Verificación

- Test del `catch` que loguea: `Log::spy()` o `Log::shouldReceive` con el mensaje y las claves de contexto, sin datos sensibles.
- Cache: test que escribe, lee, invalida y vuelve a leer el valor nuevo.
- Throttle: test que excede el límite y recibe 429.
