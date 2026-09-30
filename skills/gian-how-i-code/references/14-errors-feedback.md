# 14 — Errores, HTTP client y feedback

Cargar cuando: ErrorMapper, CustomError, apiFetcher, HttpClient/interceptor, toasts, 422, mensajes API.

## Alcance

- **Núcleo:** un cliente compartido, un mapper de errores, 401 → clear session si el producto lo requiere, 422 por campo con el mensaje del backend, toasts humanos.
- **Adaptador:** React usa `apiFetcher` (axios) + `CustomError` / `ErrorMapper`. Angular usa `HttpClient` + interceptor (`LIBRARY_OWNED`); no se pide axios (`19`). La cancelación es `AbortSignal` o `takeUntilDestroyed`.

## Cliente HTTP (regla)

- Un **cliente compartido** (`apiFetcher` o equivalente): baseURL API, credentials, headers comunes.
- Interceptor de auth (p. ej. Bearer desde store) y **401 → clear session** cuando el producto lo requiera.
- Services / `SharedService` usan ese cliente; **no** un cliente ad-hoc por feature (`axios.create` en React).

Si falta el cliente o hay varios clientes sueltos → Hallazgo + PROP de abstracción interna (`19`).

## CustomError + ErrorMapper (regla)

Contrato FE esperado:

| Pieza | Rol |
|-------|-----|
| `CustomError` | Error de dominio FE: `message`, `errors` (campos), `statusCode`, `code`, `params` |
| `ErrorMapper.mapErrorToApiResponse` | Normaliza Axios / Error / unknown |
| `ErrorMapper.getTranslatedMessage` | Mensaje i18n (`api_errors:<code>` + params; fallback default) |
| `ErrorMapper.throwMappedError` | En services de mutación tras catch |
| `ErrorMapper.throwCustomError` | Errores construidos a mano |

Mutaciones (caller): `onError` → `ErrorMapper.getTranslatedMessage(error)` — no raw `.message` si el mapper existe.

## Feedback UI

- Toasts humanos (qué pasó / a dónde); sin jerga interna
- 422: mapear a campos según el patrón del repo; conservar captura; **mostrar el mensaje human-facing del backend** (`05`). No sustituirlo por un genérico. Definir mensajes en BE y no mostrarlos en FE no cuenta como integración completa. No crear ErrorMapper ni arquitectura nueva si el repo ya tiene patrón.
- Lecturas: empty/error states claros (no spinner eterno sin copy)

## Backend

- Mensajes de mutación en idioma de política del proyecto
- No mezclar shape de lectura con mutación solo para toast

## Anti-patrones

- Toast con `error.message` crudo cuando existe `getTranslatedMessage`
- Duplicar lógica de parseo Axios en cada service
- Crear un segundo cliente HTTP “porque es más fácil”
- Toast o copy genérico en lugar del 422 por campo cuando el patrón del repo ya mapea campos
