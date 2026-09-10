# 10 — Forms y validación

Cargar cuando: formularios, RHF, Zod, campos condicionales, UX de captura (patrón, no audit A/B+/C legacy).

## Stack

RHF + Zod + zodResolver. Schemas fuera del componente. Tipos con `z.infer` / `z.input` / `z.output`. No form state solo con `useState` (salvo micro-forms locales justificados).

## Input / DTO (regla)

- El shape de form y de `TVariables` de mutation sale del **schema Zod** (`schemas/`).
- Exportar el tipo: `export type EntityDto = z.infer<typeof entitySchema>` (o `z.input` / `z.output` según el caso).
- Ese tipo alimenta `UseMutationOptions<…, EntityDto>` (`13`).
- **Prohibido** crear `interface EntityCreateInput` / `interface XxxDto` a mano que duplique el schema.
- `interfaces/` = Resource/JSON de **respuesta** (y params de listado si aplica), no input de form.

## Patrones

| Tema | Regla |
|------|-------|
| MUI controlados | `Controller` (Autocomplete, DatePicker, Select…) |
| useFieldArray | `field.id` como key; errores por fila |
| Condicionales | Limpiar / conservar / unregister explícito; oculto no bloquea submit invisible |
| Cross-field | `.refine`/`.superRefine` con `path` al campo |
| Edit async | `reset(data)` cuando llega; skeleton hasta reset |
| Submit inválido | Scroll/focus primer error; no disable Guardar solo por inválido |
| 422 | Conservar datos; comprobar el camino real del 422; `setError` (o el patrón del repo) por campo cuando esa sea la arquitectura; mostrar el mensaje human-facing del backend — ver `05`/`14` |

## Container / Form

- Container: queries + props
- Form: RHF + UI

## i18n en schemas (HARD)

Fuera de componente: `i18n.t()` del módulo i18n del repo (`15`). No `useTranslation`. No inyectar `TFunction`. No `createXSchema(t)` / `entitySchema(t)`.

Hallazgo típico: `export function createInventoryManualMovementSchema(t: TFunction<…>)` — el schema debe llamar `i18n.t('ns:key')` directo.

## User-facing 422 (HARD)

Si hay UI que consume la validación del FormRequest (`05`):

- MUST comprobar cómo llegan los errores.
- MUST asignar 422 por campo a los inputs cuando esa sea la arquitectura existente.
- MUST preferir el mensaje human-facing del backend; no sustituirlo por un error genérico.
- Definir buenos mensajes en BE y no mostrarlos en FE **no** es integración completa.
- No introducir una arquitectura nueva de errores; seguir ErrorMapper/`setError`/toasts del repo.

Una tarea de formulario/validación no está terminada sin el completion gate de `05`.

## Qué no hacer aquí

No abrir workflow completo de `ui-audit/` con modos A/B+/C de densidad/layout vivacidad. Si el usuario pide auditoría UX visual profunda, aplicar patrones de esta reference + `08`/`09`/`15`; reportar en `pattern-audit` o, si pide pasada visual Playwright densa, hacerlo como extensión de Auditar bajo este estándar (no reactivar skill shim).
