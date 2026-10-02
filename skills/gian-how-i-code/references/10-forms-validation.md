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
| Email | `type="email"`, `autocomplete="email"`. `trim`. El dominio puede ir en minúsculas. La parte antes de `@` no se fuerza a minúsculas: es decisión de producto. Schema: email válido. En el borde, la regla de email del stack. |
| Nombre / apellidos | Letras con acentos, espacios, apóstrofo y guion. Sin dígitos. `trim` y espacios colapsados. `autocomplete="given-name"` / `"family-name"`. |
| Teléfono | `type="tel"`, `inputmode="tel"`, `autocomplete="tel"`. Se normaliza a dígitos y un `+` inicial antes de enviar. Un número con guiones o espacios se normaliza; no se rechaza el pegado. |
| Fecha | Date input nativo o el DatePicker del repo. ISO en el payload. Texto libre no es el tipo. |
| Hora | `type="time"` o el picker del repo. `HH:mm` en el payload. |
| Entero | `inputmode="numeric"` y entero. `min` / `max` cuando el dominio ya los tiene. |
| Decimal / dinero | `inputmode="decimal"`. Dinero: 2 decimales, sin redondeo por float. Si el repo tiene schema de dinero o decimal, se usa. |
| URL / contraseña | `type="url"`. `type="password"` con `autocomplete="new-password"` o `"current-password"`. |

### Aplicar y proponer

- **Se aplica** en el campo tocado lo que no rechaza un valor que hoy pasa: el `type` que le corresponde, `inputmode`, `autocomplete` y normalización sin pérdida. Los ejemplos de la tabla (`trim`, teléfono a dígitos y `+`) no agotan la lista. Minúsculas en todo el email no son ese default. Un monto `type="number"` libre pasa a decimal con 2 decimales, usando el schema de dinero o decimal del repo, sin parseo por float.
- **Se propone (PROP)** lo que puede rechazar datos ya guardados o cambiar el contrato. Los ejemplos (nombre o apellidos sin dígitos, reescribir un identificador ya guardado, rangos de negocio, un tope nuevo, una longitud máxima nueva) no agotan la lista. No se aplica en silencio.
- **El control sigue a la elección, no al gusto.** Dos opciones exclusivas son un radio. No se cambian a cards. Muchas opciones usan el autocomplete que el repo ya tiene; si no hay, se propone. No se recorre el formulario cambiando widgets.
- **La misma regla** va en el schema del form y en el borde (FormRequest, body model de Pydantic, schema del handler), con mensaje de dominio y 422 por campo (`05`, `15`).
- **No se bloquea el pegado ni la escritura.** Si se puede normalizar sin perder el dato, se normaliza.

## Ayudas de captura

Al crear o editar un campo, evaluar si se puede ahorrar captura, anticipar un problema o mostrar la consecuencia. Evaluar es obligatorio. Implementar no. Pintar el resultado tampoco. Se aplica solo si el repo ya tiene lo que esa ayuda necesita, el alcance lo autoriza y no pisa un valor guardado ni una corrección manual. Si falta capacidad, es propuesta (`19`). No se exigen a la vez catálogo, endpoint y debounce: cada ayuda declara solo lo suyo. Los ejemplos orientan. Un campo que no está en ellos pasa por el mismo gate. No se recorre el formulario implementando ayudas en campos no tocados.

Que el sistema lo haga no autoriza mostrarlo. Una comprobación correcta, un ejemplo o un límite pueden quedarse en el sistema. Pintar el resultado no es el default.

Si el estado se entiende sin texto, no se escribe. Si hace falta señalarlo, es un icono y nada más: carga mientras consulta, verde si está libre, rojo si no. El icono no se pone siempre. En reposo, con el valor incompleto, o cuando el valor ya guardado sigue siendo el normal, no se pone nada. El éxito no se anuncia. Prohibido "Disponible", "Encontrado", "Libre" y un check gris. El fallo que hay que corregir sí lleva el mensaje de qué corregir. El icono puede acompañarlo. Un fallo de red no invalida el campo.

La consecuencia que esa persona va a usar vive en el control, como el dominio al final del input. No se escribe una frase para explicar el control. No se agrega un botón de comprobar si el campo ya consulta al escribir o al salir. No se agrega un segundo envío al lado de Guardar, salvo que el usuario pidió esa acción. El título de una sección no repite la etiqueta de su único campo. Si el grupo tiene un solo campo, basta la etiqueta.

La ayuda dice el formato, un ejemplo que sirva para capturar, o qué corregir. No dice qué no hace Guardar, ni "solo presentación", ni un límite interno del sistema.

Al tocar un archivo que ya lo publica, se quita ese adorno. No se reemplaza "Disponible" por otro texto, ni se obliga un icono donde el silencio basta. Si el usuario pidió solo analizar, se propone y no se edita.

Una corrección manual gana frente a un valor generado. No se conserva en silencio si dejó de ser coherente. Si cambia el padre y la selección hija ya no corresponde, se señala o se pide revisión. No se borra sola y no se deja como válida.

Cada propuesta dice qué trabajo ahorra, de dónde salen los datos, cuándo se activa, y qué pasa ante ambigüedad o fallo.

### Locales

No consultan. Generar un derivado con la utilidad del repo (`Str::slug` o el helper que ya exista). Filtrar un catálogo ya cargado. Proponer un valor. La URL, el total o el nombre público, si se muestran, viven en el control. No son una frase que explique el sistema. Un registro existente no cambia de slug porque cambió el nombre. La unicidad se comprueba aparte, al guardar.

### Asíncronas

Consultan. Formato mínimo primero. Debounce del proyecto, o se proponen 300–500 ms. No se instala una librería para eso. Solo se aplica la respuesta de la consulta vigente para el valor y su contexto: el mismo código postal con otro país descarta la respuesta anterior. Si hace falta señalar el estado, es un icono, no las palabras "comprobando", "encontrado" o "no encontrado". Carga mientras consulta. Verde si está libre y señalarlo aporta. Rojo si no, con el mensaje de qué corregir. Un fallo de red no invalida el campo. Al guardar, el servidor vuelve a comprobar.

“Formato válido”, “ya existe en esta base” y “el usuario controla ese correo” son tres comprobaciones. La tercera es un flujo de confirmación, no una ayuda de campo. En un formulario público no se dice “esta cuenta existe”. Al editar, la unicidad excluye el propio registro y nombra tenant, empresa y borrados. Sugerir un subdominio de la plataforma necesita formato y ocupación interna. DNS y propiedad son otro flujo.

La comprobación previa orienta al sistema. No se publica como "Disponible". Guardar resuelve la colisión: índice único, operación atómica o bloqueo, junto con la escritura. Una comprobación previa, aunque sea de backend, puede quedar vieja (`05`).

La validación mientras se escribe no es obligatoria en todos los inputs. Se usa si aporta: disponibilidad cuando el valor ya alcanza, no marcar un formato incompleto mientras se sigue escribiendo, quitar el mensaje cuando el error se corrige.

### Ejemplos abiertos

Valor derivado. Dato ya conocido. Valor inicial del contexto. Búsqueda que distinga opciones parecidas. Posible duplicado, sin tratar un nombre igual como duplicado seguro. Consecuencia que esa persona va a usar, en el control. Campos que aparecen según la elección. Conservar lo escrito ante un error. Crear un faltante y volver. Repetir una fila sin copiar identificadores. Archivo: vista previa, requisitos, progreso, reintento. Código postal que completa lo inequívoco y deja elegir si hay varias colonias. Campo dependiente cuya selección se revisa cuando cambia el padre.

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
