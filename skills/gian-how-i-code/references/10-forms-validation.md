# 10 — Forms y validación

Cargar cuando: formularios, RHF, Zod, DTOs de mutation (body HTTP), campos condicionales, UX de captura (patrón, no audit A/B+/C legacy).

## Alcance

- **Núcleo:** el body sale de un schema nombrado. Prohibido un `interface *Input` paralelo y el payload anónimo. Los IDs de ruta no entran al schema. Fuera del componente, `i18n.t()`. 422 por campo con el mensaje del backend.
- **Tipo de campo:** al crear o editar un campo, nombrar qué representa. El tipo, la validación y el control siguen eso. La tabla de abajo es ejemplo, no el universo. Un campo que no está en ella sigue la misma regla.
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

## Tipo de campo y validación semántica

Al crear o editar un campo, nombrar qué representa. El tipo, la validación y el control siguen eso. No hace falta que el campo esté en la tabla. Email, nombre o teléfono son ejemplos de la misma regla, no la lista cerrada.

El alcance es ese campo. Un hermano del mismo form con el mismo problema se reporta como propuesta; no se recorre el formulario ni el repo cambiando widgets.

Qué se cambia ahora y qué se propone está en «Aplicar y proponer». Los atributos HTML (`type`, `inputmode`, `autocomplete`) son del cliente web. La regla semántica es la misma en el schema del form y en el borde.

### Ejemplos

La tabla no limita la regla. Si el campo no aparece, se identifica qué representa y se aplica el gate de abajo.

| Campo | Objetivo |
|-------|----------|
| Email | `type="email"`, `autocomplete="email"`. `trim` y minúsculas al escribir o al salir. Schema: email válido. En el borde, la regla de email del stack, normalizando antes de validar. |
| Nombre / apellidos | Letras con acentos, espacios, apóstrofo y guion. Sin dígitos. `trim` y espacios colapsados. `autocomplete="given-name"` / `"family-name"`. |
| Teléfono | `type="tel"`, `inputmode="tel"`, `autocomplete="tel"`. Se normaliza a dígitos y un `+` inicial antes de enviar. Un número con guiones o espacios se normaliza; no se rechaza el pegado. |
| Fecha | Date input nativo o el DatePicker del repo. ISO en el payload. Texto libre no es el tipo. |
| Hora | `type="time"` o el picker del repo. `HH:mm` en el payload. |
| Entero | `inputmode="numeric"` y entero. `min` / `max` cuando el dominio ya los tiene. |
| Decimal / dinero | `inputmode="decimal"`. Dinero: 2 decimales, sin redondeo por float. Si el repo tiene schema de dinero o decimal, se usa. |
| URL / contraseña | `type="url"`. `type="password"` con `autocomplete="new-password"` o `"current-password"`. |

### Aplicar y proponer

- **Se aplica** en el campo tocado lo que no rechaza un valor que hoy pasa: el `type` que le corresponde, `inputmode`, `autocomplete` y normalización sin pérdida. Los ejemplos de la tabla (`trim`, minúsculas en email, teléfono a dígitos y `+`) no agotan la lista. Un monto `type="number"` libre pasa a decimal con 2 decimales, usando el schema de dinero o decimal del repo, sin parseo por float.
- **Se propone (PROP)** lo que puede rechazar datos ya guardados o cambiar el contrato. Los ejemplos (nombre o apellidos sin dígitos, reescribir un identificador ya guardado, rangos de negocio, un tope nuevo, una longitud máxima nueva) no agotan la lista. No se aplica en silencio.
- **El control sigue a la elección, no al gusto.** Dos opciones exclusivas son un radio. No se cambian a cards. Muchas opciones usan el autocomplete que el repo ya tiene; si no hay, se propone. No se recorre el formulario cambiando widgets.
- **La misma regla** va en el schema del form y en el borde (FormRequest, body model de Pydantic, schema del handler), con mensaje de dominio y 422 por campo (`05`, `15`).
- **No se bloquea el pegado ni la escritura.** Si se puede normalizar sin perder el dato, se normaliza.

### Campo complejo

El input nativo no alcanza cuando el campo pide:

- moneda con máscara y separadores por locale;
- decimales con coma o punto según el idioma;
- fechas con rangos o zonas horarias;
- horas con intervalos.

Ahí no se escribe una máscara, un parser ni un picker. El orden es el Decision Gate de `19`:

1. Usar lo que el repo ya tiene: el DatePicker, el campo de moneda de su librería de UI, o un wrapper local.
2. Si no hay, proponer una librería del framework del repo. Se consulta la documentación y se explican costo y riesgo. La librería es la de ese stack.
3. No instalar sin OK. Mientras tanto, el campo queda con el tipo y la validación de la tabla, sin máscara casera.

Señal: la tarea pide formateo, parseo o máscara propios para un dato que una librería madura ya cubre.

## Qué no hacer aquí

No abrir workflow completo de `ui-audit/` con modos A/B+/C de densidad/layout vivacidad. Si el usuario pide auditoría UX visual profunda, aplicar patrones de esta reference + `08`/`09`/`15`; reportar en `docs/pattern-audit` o, si pide pasada visual Playwright densa, hacerlo como extensión de Auditar bajo este estándar (no reactivar skill shim).
