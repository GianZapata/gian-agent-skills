# 10 — Forms y validación

Cargar cuando: formularios, RHF, Zod, DTOs de mutation (body HTTP), campos condicionales, UX de captura (patrón, no audit A/B+/C legacy).

## Alcance

- **Núcleo:** el body sale de un schema nombrado. Prohibido un `interface *Input` paralelo y el payload anónimo. Los IDs de ruta no entran al schema. Fuera del componente, `i18n.t()`. 422 por campo con el mensaje del backend.
- **Adaptador:** en TypeScript, ese schema es Zod y el tipo sale de `z.infer`. En Python, es un body model de Pydantic. En React: RHF, `Controller`, `useFieldArray`, `zodResolver`, Container/Form. En otro stack, el form de ese stack enlaza el mismo schema.

## Stack (adaptador React)

RHF + Zod + zodResolver. Schemas fuera del componente. Tipos con `z.infer` / `z.input` / `z.output`. No form state solo con `useState` (salvo micro-forms locales justificados).

## Input / DTO (regla)

- El shape de form y el **body HTTP** salen del **schema nombrado** (`schemas/`; Zod en TypeScript).
- Exportar: `export type EntityDto = z.infer<typeof entitySchema>` (o `z.input` / `z.output`).
- Ese tipo es `data` en el service y, cuando aplica, `TVariables` o `TVariables['data']` (`13`).
- **Prohibido** `interface EntityCreateInput` / `interface XxxDto` a mano que duplique el schema.
- **Prohibido** payloads anónimos (`{ body: string }`, `{ contract_template_id: number }`) como contrato de mutation. Aunque sea un campo: schema + `type XxxDto`.
- El schema **no** incluye IDs de ruta (`contractId`, `documentId`, `id` de URL). Esos van en la firma / envelope (`13`).
- `interfaces/` = Resource/JSON de **respuesta** (y params de listado si aplica), no input de form.

```ts
export const updateNestedSchema = z.object({
  body: z.string().min(1, i18n.t('…')),
});

export type UpdateNestedDto = z.infer<typeof updateNestedSchema>;

export const prepareChildSchema = z.object({
  template_id: z.number().int().positive(i18n.t('…')),
});

export type PrepareChildDto = z.infer<typeof prepareChildSchema>;
```

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
