# 14 — Errores, HTTP client y feedback

Cargar cuando: ErrorMapper, CustomError, apiFetcher, HttpClient/interceptor, toasts, 422, mensajes API.

## Alcance

- **Núcleo:** un cliente compartido, un mapper de errores, 401 → limpiar sesión y redirigir, 422 por campo con el mensaje del backend, toasts humanos.
- **Adaptador:** React usa `apiFetcher` (axios) + `CustomError` / `ErrorMapper`. Angular usa `HttpClient` + interceptor (`LIBRARY_OWNED`); no se pide axios (`19`). La cancelación es `AbortSignal` o `takeUntilDestroyed`.

## Cliente HTTP (regla)

- Un **cliente compartido** (`apiFetcher` o equivalente): baseURL API, credentials, headers comunes.
- Interceptor de auth (p. ej. Bearer desde store).
- **401:** si el repo tiene sesión o store de auth, el interceptor limpia la sesión y redirige al login. Si el repo no tiene sesión, registrar `GAP 401 sin sesión` en el cierre.
- Services / `SharedService` usan ese cliente; **no** un cliente ad-hoc por feature (`axios.create` en React).

Si falta el cliente o hay varios clientes sueltos:

- **Auditar:** Hallazgo + PROP de abstracción interna (`19`).
- **Implementar:** prohibido crear un cliente ad-hoc (`axios.create`, `fetch` suelto, un cliente por feature). Usar el cliente existente más cercano y abrir la PROP de abstracción interna en el cierre.

## CustomError + ErrorMapper (regla)

Contrato FE esperado:

| Pieza | Rol |
|-------|-----|
| `CustomError` | Error de dominio FE: `message`, `errors` (campos), `statusCode`, `code`, `params` |
| `ErrorMapper.mapErrorToApiResponse` | Normaliza Axios / Error / unknown |
| `ErrorMapper.getTranslatedMessage` | Mensaje i18n (`api_errors:<code>` + params; fallback default) |
| `ErrorMapper.throwMappedError` | En services de mutación tras catch |
| `ErrorMapper.throwCustomError` | Errores construidos a mano |

Todo error visible al usuario pasa por `ErrorMapper.getTranslatedMessage(error)` o su equivalente en el repo. Aplica a mutaciones (`onError` en el caller), queries con estado de error, submits fuera de React Query y subscriptions, en cualquier stack (React, Vue, Angular).

Prohibido mostrar `error.message` crudo. Si el repo no tiene mapper: Hallazgo en el cierre; el `error.message` crudo sigue prohibido.

## Feedback UI

- Toasts humanos (qué pasó / a dónde); sin jerga interna.
- Toda mutación iniciada por el usuario muestra un toast de error traducido (mapper). Es obligatorio.
- 422: mapear a campos según el patrón del repo. Sin patrón en el repo: cada clave de `errors` va al campo del form con el mismo nombre, con su mensaje tal cual. Una clave sin campo va al toast o a la alerta del form. Conservar captura; **mostrar el mensaje human-facing del backend** (`05`). No sustituirlo por un genérico. Definir mensajes en BE y no mostrarlos en FE no cuenta como integración completa. No crear ErrorMapper ni arquitectura nueva si el repo ya tiene patrón.
- Ayuda de captura (`10`): el icono de estado va solo en un campo con comprobación asíncrona del valor completo (unicidad o existencia contra el backend). En cualquier otro campo no va. Es un icono, no una frase: carga mientras consulta, verde si está libre, rojo si no. Nunca lleva texto de éxito. Mismo criterio en `15`. Un fallo de red no se muestra como inválido. El mensaje aparece solo cuando hay que corregir algo. El 422 final sigue siendo el del backend.
- Lecturas: carga con skeleton que tiene la forma de la pantalla (`15`); prohibido spinner o «Cargando…» cuando la pantalla tiene forma. Error: texto con qué pasó y qué hacer. Vacío: texto. El copy sigue `15`: audiencia y función, no una palabra prohibida. Un término de dominio se conserva. Copy de operador, o una instrucción que el lector no puede cumplir, se corrige directo y después se informa. Si el usuario pidió solo analizar, se propone y no se edita.

## Backend

- Mensajes visibles, incluidos los errores por campo, usan el idioma soportado del usuario y el fallback del proyecto. `code`, status y claves de campo quedan estables. Se traduce el mensaje, no la clave. Si ese recorrido no existe, se identifica y se propone (`05`). No se inventa un sistema de i18n en el mismo corte.
- No mezclar shape de lectura con mutación solo para toast

## Anti-patrones

- Toast o texto con `error.message` crudo, exista o no el mapper
- Duplicar lógica de parseo Axios en cada service
- Crear un segundo cliente HTTP “porque es más fácil”, también al implementar sin cliente compartido
- Toast o copy genérico en lugar del 422 por campo cuando el patrón del repo ya mapea campos
