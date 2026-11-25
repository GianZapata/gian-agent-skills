# 31 — Control de formulario y ayudas ágiles

El tipo correcto (`10`) no basta: el campo tiene que sentirse ágil. Esta reference elige **qué control** usar y **qué ayuda dentro del control** pone, según tres ejes: qué dato es, cuántas opciones hay y dónde se muestra. Aplica en Implementar (formulario nuevo o campo tocado), en Auditar (`24`) y en la auditoría de pantalla (`30`).

`10` sigue siendo dueño del tipo, la validación, la paridad con el backend y las reglas de las ayudas (icono sin texto, nada de "Disponible", debounce, la consulta vigente). Esta reference no las repite: decide el control y cuál ayuda corresponde.

## Matriz: dato × opciones × contexto

| Dato / opciones | Formulario de página | Dialog / drawer | Barra de filtros de tabla | Edición inline en tabla |
|---|---|---|---|---|
| 2 exclusivas | radio | radio en línea o switch si es sí/no | chips toggle o segmented | switch / select compacto |
| 2 a 4 con datos que comparar (precio, límite, plan) | radio cards con el default ya marcado | radio cards solo si son 2–3; si no, radio con el dato en la etiqueta | select o chips (el dato no cabe) | select compacto |
| 3 a 7 fijas, sin datos que comparar | select del repo; radio si hay que verlas juntas | select | select o chips | select compacto |
| Muchas o catálogo dinámico (clientes, ciudades, productos) | autocomplete/combobox; búsqueda en servidor si el catálogo es grande | autocomplete | autocomplete compacto | autocomplete en popover |
| Varias a la vez, pocas | grupo de checkbox visible | grupo de checkbox | multi-select o chips | — (se edita fuera de la celda) |
| Varias a la vez, muchas | autocomplete múltiple con chips | autocomplete múltiple | multi-select con contador | — |
| Booleano | switch si aplica al instante; checkbox si se confirma con Guardar | igual | chip toggle o select Todos/Sí/No | switch |
| Fecha | DatePicker del repo | DatePicker | date range compacto con presets | DatePicker en popover |
| Rango de fechas | DateRangePicker con presets y min/max | igual | date range compacto con presets | — |
| Hora | TimePicker del repo con intervalo de negocio | igual | — | TimePicker en popover |
| Dinero / cantidad con unidad | input con adornment (ver §Ayudas) | igual | rango min–max | input con adornment |

Reglas de la matriz:

- **El espacio manda.** El mismo campo cambia de control según el contexto: los 3 planes con precio son radio cards en el alta y chips o select en el filtro. Que difieran entre contextos no es inconsistencia.
- **Las opciones se ven sin abrir nada** cuando son pocas y hay que compararlas o hay un default. Un select que esconde 3 opciones con precio obliga a abrir para decidir.
- **El catálogo grande no se carga entero.** Búsqueda en servidor con el endpoint que ya existe (`10` §Fuente del combobox).
- **El input de fecha nativo pierde** contra el picker que el repo ya tiene (MUI `@mui/x-date-pickers`, shadcn `Calendar` + `Popover`, o el wrapper local). El payload sigue siendo ISO / `HH:mm` (`10`).

## Ayudas ágiles

Cada ayuda tiene la condición que la dispara. No se ponen en todos los campos. Las reglas de cómo se señala el estado (icono, sin texto de éxito, fallo de red) son las de `10` §Ayudas de captura.

| Ayuda | Cuándo | Qué hace |
|---|---|---|
| **Slug** | El registro tiene un identificador público derivado de un nombre | Se genera del nombre (`Str::slug` o el helper del repo) mientras el usuario no lo edite a mano; si lo toca, deja de sincronizar. Un registro existente no cambia de slug porque cambió el nombre. Unicidad en vivo con debounce contra un endpoint que **ya exista**; sin endpoint es PROP al back, nunca se inventa. Si está ocupado, sugiere alternativas (`torre-norte-2`, `torre-norte-fortezza`). El prefijo de la URL va como `startAdornment` de solo lectura. |
| **Dominio / URL** | El valor arma una URL o un subdominio | `startAdornment` / `endAdornment` que construye el valor (`https://`, `.fortezza.mx`) y preview en vivo dentro del control mientras se escribe (`fortezza.mx/torre-norte`). Es la consecuencia que la persona va a usar, no una frase explicativa. |
| **Dinero / unidades** | Monto, superficie, porcentaje, cantidad con unidad | Adornment con `$`, `MXN`, `m²`, `%`. Formato con separadores mientras se escribe; el payload es el número limpio (decimal con 2 decimales en dinero, `10`). La máscara sale del componente del repo, no de un parser casero. |
| **Default visible** | Pocas opciones y existe un valor por defecto | Cards o radio con el default ya seleccionado; no hay que desplegar nada. El default se busca en este orden: `->default()` de la migración, `$attributes` del modelo o el FormRequest, el seeder. Si ninguno lo tiene, el agente decide y lo marca como **supuesto** en el PROP. |
| **Formato con máscara** | Teléfono, RFC, CURP, código postal | Máscara y contador de caracteres. El CP autocompleta estado y municipio si el endpoint existe, y deja elegir si hay varias colonias (`10` §Ejemplos abiertos). |
| **Fecha con atajos** | Rango de fechas, sobre todo en filtros y reportes | Presets (hoy, últimos 7 días, este mes, mes anterior) y `min`/`max` desde la regla de negocio (no se agenda en el pasado, no se factura a futuro). |

## Aplicar o proponer

- **Formulario nuevo:** se eligen el control y las ayudas de esta reference directamente. Van en la línea por campo de `10` (control y ayuda).
- **Formulario existente que se toca:** un control que no encaja con la matriz, o una ayuda que falta, se reporta como **PROP**: actual → propuesto → por qué → componente del repo que lo resuelve. No se cambia sin preguntar, porque cambia la UX que los usuarios ya conocen. No se recorre el formulario convirtiendo widgets de campos no tocados.
- **Auditoría:** es hallazgo según §Severidad.

## Componente ausente

Si el control ideal no está en el repo (no hay `@mui/x-date-pickers`, shadcn sin `Calendar`, no hay autocomplete), se usa lo que existe y la falta se reporta como propuesta de stack (`19`): el paquete, el porqué y el costo. **Nunca se instala durante la tarea.** En ese caso el input de fecha nativo no es hallazgo: el hallazgo, si aplica, es la propuesta de stack.

## Severidad (auditoría)

| Caso | Severidad |
|---|---|
| Fecha nativa con un picker disponible en el repo | Media |
| Select con un catálogo grande o dinámico, sin búsqueda | Media |
| Slug o dominio sin autogenerado, sin prefijo o sin preview | Media |
| Pocas opciones con datos que comparar, escondidas en un select (formulario de página) | Baja |
| Default existente que el control no muestra seleccionado | Baja |
| Adornment de unidad o máscara que falta | Baja |
| El mismo campo con controles distintos en contextos distintos | No es hallazgo |
| Control ideal sin dependencia en el repo | Propuesta `19`, no Media |

## Ejemplos

**Fecha (repo con MUI y x-date-pickers instalado)**

```tsx
// Antes
<TextField type="date" label="Fecha de entrega" {...register('deliveredAt')} />

// Después
<Controller
  name="deliveredAt"
  control={control}
  render={({ field }) => (
    <DatePicker label="Fecha de entrega" value={field.value} onChange={field.onChange} minDate={today} />
  )}
/>
```

**Catálogo grande (300 clientes)**: `Select` con todos los `MenuItem` → `Autocomplete` con búsqueda en servidor contra el endpoint de listado que ya existe.

**Planes en alta**: `Select` con «Básico $499 / Pro $999 / Empresa $1,999» → radio cards con precio y límite visibles y el default de la migración (`->default('basic')`) ya marcado. En la barra de filtros de la tabla de suscripciones el mismo campo queda como select o chips.

**Slug**

```tsx
// Antes
<TextField label="Slug" {...register('slug')} />

// Después: autogenerado hasta la edición manual, prefijo de solo lectura, check en vivo
<TextField
  label="Slug"
  value={slug}
  onChange={(event) => {
    setSlugTouched(true)
    setValue('slug', event.target.value)
  }}
  slotProps={{
    input: {
      startAdornment: <InputAdornment position="start">fortezza.mx/</InputAdornment>,
      endAdornment: <SlugStatusIcon status={slugQuery.status} />,
    },
  }}
/>
```

**Dinero**: `type="number"` libre → input con `startAdornment="$"` y `endAdornment="MXN"`, separadores al escribir y número limpio en el payload.

## Qué no hacer

- Instalar un picker o una librería de máscaras durante la tarea.
- Inventar un endpoint de disponibilidad o de catálogo.
- Cambiar sin preguntar un control que ya existe en un formulario que solo se tocó.
- Meter radio cards en una barra de filtros o en una celda.
- Escribir "Disponible" o una frase que explique la ayuda (`10`).
