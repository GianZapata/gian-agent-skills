# Lentes

Cada lente lee solo el diff y el código necesario para entenderlo. Ninguna edita.

## L1 Seguridad y dependencias

- Autorización: cada endpoint, acción o job nuevo verifica quién puede ejecutarlo (policy, gate, middleware, scope de tenant `gian-how-i-code` `16`).
- Entrada: validación en el borde (`10`), mass assignment, SQL crudo con interpolación, rutas de archivo desde input, deserialización, SSRF en URLs de usuario.
- Secretos: credenciales en código, logs con datos sensibles (`29`), tokens en query string.
- Salida: XSS (`v-html`, `dangerouslySetInnerHTML`, `{!! !!}`), datos de otro tenant en Resources.
- Webhooks: firma validada, idempotencia por ID de evento (`28`).
- Dependencias: solo si cambió `composer.json`/`composer.lock`/`package.json`/lockfile JS. Correr el audit del gestor del repo (`composer audit`, `npm audit --omit=dev`, `pnpm audit --prod`). Cada paquete nuevo necesita justificación (`19` regla 11): mantenimiento, licencia, alternativa nativa.

## L2 Bugs y regresiones

- Caminos nulos, vacíos y límites; off-by-one; zonas horarias y redondeo de dinero.
- Ramas que cambian comportamiento existente que nadie pidió cambiar (regresión).
- Errores tragados, `catch` vacío, promesas sin manejar.
- Si hay spec: cada requisito tiene código y test que lo cubre; marcar los que no.
- Tests: ¿el test falla sin el cambio? ¿Asserta el efecto observable (`17`)?

## L3 Transacciones e integridad

- Escrituras múltiples relacionadas dentro de una transacción; efectos externos (mail, cola, API) después del commit (`afterCommit`, `28`).
- Concurrencia: lock (`lockForUpdate`, unique index) donde dos requests pueden pisar el mismo registro.
- Idempotencia de jobs y webhooks; reintentos que duplican cobros o envíos.
- Migraciones: reversibles, sin bloquear tablas grandes, backfill separado (`27`).
- Máquinas de estado: transiciones validadas, no `update(['status' => ...])` suelto.

## L4 Diseño

Criterio de `gian-how-i-code` `22`: responsabilidad única operacional, dependencias inyectadas, sin abstracciones especulativas, nombres que dicen intención, funciones cortas con un nivel de abstracción. Señalar duplicación con código existente que ya resuelve lo mismo (citar el helper).

## L5 Prácticas actuales de librerías

Por cada librería externa cuya API usa el diff: resolver la versión del lockfile, consultar Context7 y comparar. Hallazgo solo con fuente: API deprecada, opción renombrada, patrón desaconsejado en la versión instalada. Si Context7 no está disponible: la lente queda `no evaluable` y se dice; no se responde de memoria.

## L6 Conformidad con gian-how-i-code

Aplicar la matriz de routing de `gian-how-i-code` a lo tocado y revisar solo esas references. Citar número de reference y regla en cada hallazgo. Convenciones del repo guardadas en Engram (`project/conventions`) mandan sobre la reference cuando el repo diverge a propósito.

## L7 Docs desactualizadas

Si el diff cambia comando, opción, endpoint, variable de entorno, config o contrato: buscar con `rg` el nombre viejo en README, `docs/`, `.env.example`, help de comandos, colecciones de API y comentarios de uso. Cada mención vieja es un hallazgo MINOR con `path:line`.
