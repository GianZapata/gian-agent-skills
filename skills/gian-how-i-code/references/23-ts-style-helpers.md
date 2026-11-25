# 23 — Memoización, cn, dayjs, utils y helpers

Cargar cuando: Implementar FE, crear util/helper, fechas en frontend, multipart/`FormDataHelper`, consultar memoización/`cn`/dayjs, constantes `*_SX` / concat de `className`, constantes o literales de negocio repetidos (timezone, moneda, límites), enums de dominio, lógica derivada en JSX.

## Alcance

- **Núcleo:** renombres explícitos, dayjs, utils vs helpers, `FormDataHelper` y la sección de duplicación. Un área es `export class XxxHelper`. Una función suelta de área (fecha, número, etiqueta, dinero) es hallazgo.
- **Adaptador React:** memoización A–E y `cn()` / `className`. En Vue, los mismos casos A–E deciden `computed` (`25`). Sin `cn()`, las clases condicionales no se resuelven inventando la utilidad: se componen en el mecanismo del stack. Vue: `:class` con array u objeto (`:class="['base', { 'font-semibold': isActive }]"`, `25`). Angular: `[class.x]` o `[ngClass]`. Prohibido interpolar o concatenar clases en todos los stacks, y prohibido construir nombres Tailwind dinámicos.

**Formato visual TS/TSX** (arrows, braces, JSX, imports type, comments): skill `gian-ts-style`. Esta reference no duplica esas reglas. **Autoridad de styling** (Tailwind vs `sx` vs theme): `04`. Forma de `export const` utils: la style skill; **cuándo** crear util vs helper: aquí.

## Memoización React (regla)

No usar `useMemo`, `useCallback` o `memo` por costumbre de performance.

| Caso | Qué hacer |
|---|---|
| A. expresión derivada sencilla | cálculo directo; no `useMemo` |
| B. 2 ramas con una condición de 1 o 2 partes | ternario, o `&&` boolean-safe en JSX (`gian-ts-style`) |
| C. valor derivado con 3+ ramas, o ternario cuya condición junta 3+ partes con `&&` / `||` | `useMemo` + `if` + early return, obligatorio en componente y hook (Vue: `computed`) — claridad, **no** claim de performance (`derived-multi-branch`) |
| D. JSX multi-rama en render | `if` / early return en el componente (`08`); no `useMemo` |
| E. performance / identidad referencial | `useMemo` / `useCallback` / `memo` solo con una de estas evidencias, citada en el cierre: el valor es prop de un componente memoizado (p. ej. `columns` MRT, `11`); el valor es dependencia de un efecto o de una query key; hay una medición del profiler citada. Sin evidencia, es caso A |

```ts
// A — no
const fullName = useMemo(
  () => `${firstName} ${lastName}`,
  [firstName, lastName],
);

// A — sí
const fullName = `${firstName} ${lastName}`;

// C — sí (claridad; ver gian-ts-style)
const statusLabel = useMemo(() => {
  if (isLoading) return t('…');
  if (hasError) return t('…');
  return t('…');
}, [hasError, isLoading, t]);
```

No crear helpers de display (`08` es autoridad). En C, `useMemo` es obligatorio aunque el valor tenga solo dos resultados. En E, solo con la evidencia de la tabla.

```ts
// C — sí: dos resultados, pero la condición junta 5 partes
const orderMessage = useMemo(() => {
  if (fromMessage !== null || toMessage !== null) return null;
  if (localFrom === null || localTo === null) return null;
  if (!localTo.startOf('day').isBefore(localFrom.startOf('day'))) return null;

  return DashboardHelper.periodMessages.order;
}, [fromMessage, toMessage, localFrom, localTo]);
```

Lo verifica `gian-ts-style` `assets/self-check.mjs` (`derived-multi-branch`, `no-nested-ternary`; `memo-ceremonial` como GAP).

### Lógica en JSX (Auditar + Implementar)

`useMemo` no sirve para concatenar. Lo que decide es la forma de la lógica:

| Forma | Qué hacer |
|---|---|
| La misma derivación se repite 2+ veces (p. ej. `ready ? Helper.format(x) : '—'` en cuatro KPIs) | Método del helper de la feature (`Helper.metricValue(metric)`). Media |
| Expresión larga en una prop o en el JSX: template con 2+ llamadas, o ternario + `??` | `const` con nombre antes del `return`, sin `useMemo` (caso A/B) |
| Un booleano de 3+ partes (`!readOnly && (a || b || (!c && d))`) | Partir en `const` con nombre por parte y componer: `const showClear = !readOnly && (hasPendingChange || hasSavedLogo)`. Sin `useMemo` (A/B). Media |
| 3+ ramas (el resultado es uno de varios estados), sobre todo si se repite en varios bloques del JSX | `useMemo` + `if` (caso C). El JSX hace `if` / early return o un `switch` sobre el resultado (caso D) |

```tsx
// Mal — la condición se repite en dos bloques y junta 4 partes
{!(tablePending && !tableRows) && !tableError && (tableRows ?? []).length === 0 ? <Empty /> : null}
{!(tablePending && !tableRows) && !tableError && (tableRows ?? []).length > 0 ? <Table /> : null}

// Bien — se deriva una vez (C)
const tableState = useMemo(() => {
  if (tablePending && !tableRows) return TableState.Loading;
  if (tableError) return TableState.Error;
  if (!tableRows?.length) return TableState.Empty;

  return TableState.Ready;
}, [tablePending, tableRows, tableError]);

// Mal — template largo dentro de la prop
footnote={row ? `Cobrado ${DashboardHelper.money(row.collected, row.currency)} de ${DashboardHelper.money(row.expected, row.currency)}` : (reason ?? 'Sin datos')}

// Bien — const con nombre (A/B) o método del helper si se repite
const cohortFootnote = CentralDashboardHelper.cohortFootnote(data.cohort);
```

```tsx
// Mal — booleano de 4 partes sin nombre
const showClearLogo =
  !readOnly && (Boolean(logoFile) || removeLogo || (!deferred && Boolean(settings.logo?.url)));

// Bien — cada parte con nombre
const hasPendingLogoChange = Boolean(logoFile) || removeLogo;
const hasSavedLogo = !deferred && Boolean(settings.logo?.url);
const showClearLogo = !readOnly && (hasPendingLogoChange || hasSavedLogo);
```

El estado derivado de UI (`TableState`) es `APP_OWNED` cerrado: string enum (`07`).

## `cn()` y styling local

`04` decide qué va en Tailwind vs `sx` y es la autoridad de styling. Esta sección solo define la mecánica de clases.

| Forma de las clases | Mecánica |
|---|---|
| Completamente estáticas | `className` directo; no `cn()` ceremonial |
| Condicionales, compuestas o variables por estado/props runtime | `cn()` |
| Ternario entre strings de clase | `cn(base, cond && extra)` inline |
| Estado resuelto solo por props MUI y `className` idéntico | `className` estático permitido |

Selected:

```tsx
<Button
  className={cn(
    'h-[30px] rounded-lg px-2',
    !isSelected && 'text-text-secondary hover:bg-white'
  )}
/>
```

Active:

```tsx
<div
  className={cn(
    'flex items-center gap-2',
    isActive && 'font-semibold',
    className
  )}
/>
```

No usar un ternario completo de strings cuando `cn()` puede expresar una base única más la variación:

```tsx
className={
  isSelected
    ? 'h-[30px] rounded-lg px-2'
    : 'h-[30px] rounded-lg px-2 text-text-secondary hover:bg-white'
}
```

Tampoco concatenar, interpolar una condición en template strings ni construir nombres Tailwind dinámicos:

```tsx
className={'flex ' + (isActive ? 'font-semibold' : '')}

className={`flex ${isActive ? 'font-semibold' : ''}`}

className={`bg-${color}-600`}
```

Las clases Tailwind deben existir completas y ser detectables estáticamente por el scanner. No duplicar árboles JSX solo para evitar `cn()`.

**HARD — `no-local-style-constants`.** No crear constantes/functions locales cuya única responsabilidad sea almacenar styling ordinario (`04`):

```ts
const CONTROL_SX = { … };
const selectedToggleSx = { … };
const toggleButtonSx = (selected: boolean) => ({ … });
const cardClass = 'rounded-xl border border-divider bg-white p-4';
```

Un string de clases tampoco: va inline. Si el bloque se repite, componente (`04`).

Tailwind + `cn()` inline en el JSX es obligatorio (MUST) cuando el gate de `04` lo permite.

Excepciones cerradas (las de `04` puntos 4 y 5). El cierre cita cuál aplica:

1. mapping de variantes que ya existe y se usa en 2+ archivos;
2. primitive que ya existe en `shared/`;
3. valor que depende del `theme` en runtime;
4. prop que la API documentada del componente solo acepta en `sx`;
5. token sin utility Tailwind ni bridge verificado (`04` 5a).

Crear un mapping o un primitive nuevo para styling ordinario está prohibido (`04`).

## Renombres explícitos (HARD)

Prohibidos los alias opacos (`d`, `o`, `x`). Usar alias con nombre de dominio. Geometría de destructuring: `gian-ts-style` (`query-data-alias`, `direct-property-access`). MRT `Cell: ({ row: { original } })` se queda en `11`.

```ts
const { data: entities } = useEntitiesQuery(…);
```

## Fechas — dayjs (regla)

- Stack FE canónico incluye **dayjs** en todos los proyectos.
- No usar `new Date` / Date nativo para parseo, formato o aritmética de negocio en FE.
- Si el repo tiene un **módulo configurado** (`lib/dayjs`, plugins utc/timezone/locale, etc.): importar **desde ese módulo**, no `import dayjs from 'dayjs'` crudo.
- Si existe `DateHelper` (u helper de área de fechas), usarlo es obligatorio. Si al helper le falta el método, agregarlo al helper; no llamar `dayjs(value).format(…)` suelto en el consumidor.
- Sin `DateHelper` en el repo: `dayjs(value).format(…)` vía el módulo configurado.

Plugins típicos del módulo (orientativos): `utc`, `timezone`, `customParseFormat`, `isSameOrAfter` / `isSameOrBefore`, `relativeTime`, locale del producto (p. ej. `es-mx`).

```ts
// Mal
const label = new Date(iso).toLocaleDateString();
import dayjs from 'dayjs'; // si existe @/lib/dayjs configurado

// Bien
import { dayjs } from '@/lib/dayjs'; // o el path del repo
DateHelper.format(iso, 'DD/MM/YYYY');
```

Si `dayjs` falta en `package.json` → hallazgo **Alto** + PROP de stack (librería faltante).  
Si hay deps pero no módulo configurado y se repiten `extend`/locale por archivo → PROP de **abstracción interna** (`19`).  
No instalar sin OK (`19`).

Excepción: APIs del runtime que exigen `Date` (p. ej. firma de librería externa) — convertir en el borde con dayjs.

## utils vs helpers

| Carpeta | Cuándo | Forma | Sufijo |
|---------|--------|-------|--------|
| `utils/` | Cosas **pequeñas** y genéricas (pocas líneas, sin dominio rico) | `export const … = () =>` (sintaxis: `gian-ts-style`) | `.util.ts` |
| `helpers/` | Agrupan un **área** (fechas, números, usuario, formatos humanos, reglas de dominio, **Record de meta de enum**) | `export class XxxHelper` | `.helper.ts` |

Ejemplos de helpers de área: `DateHelper`, `HumanFormatsHelper`, `NumberHelper`, `UserHelper`, `FormDataHelper`.

Un helper puro es clase estática en cualquier TS. En Angular, se usa un service solo si necesita DI.

```ts
export const clamp = (n: number, min: number, max: number) =>
  Math.min(max, Math.max(min, n));

export class DateHelper {
  static format(value: string | Date, pattern = 'YYYY-MM-DD') {
    return dayjs(value).format(pattern);
  }
}
```

### FormDataHelper (multipart)

Área: serializar un DTO plano/anidado a `FormData` para Laravel.

- Crear **una vez** en `shared/helpers/form-data.helper.ts` (materializar `assets/frontend/helpers/form-data.helper.ts.template`). No un helper por feature.
- Usar **solo** si el endpoint es multipart (`File` / `Blob` / `FileList` / evidencia). JSON: pasar el DTO.
- UI no llama a `toFormData`. Solo el service.
- `undefined` → omitir. `null` → `""` (`ConvertEmptyStringsToNull`).
- Booleanos `'1'` / `'0'`. Dayjs fecha-calendario (`00:00:00.000`) → `YYYY-MM-DD`; con hora → ISO. `Date` nativo solo en este borde (el resto del FE sigue dayjs, esta misma reference).
- Throw `TypeError` en raíz no-objeto, número no finito, Date/Dayjs inválido, ciclo, `Map`/`Set`/clase no soportada.
- Tests: materializar `form-data.helper.test.ts.template` junto al helper.

Si el repo ya tiene un serializador equivalente y cubre estas convenciones → reutilizar (`Antes de crear helper/util`). Si serializa mal `null`/fechas/files → Hallazgo Media: extender o reemplazar por este helper.

**Prohibido:** `*.display.config.ts`, inyectar `TFunction`, `labelKey` diferido, clase *solo* de UI (`ColorHelper.statusColor`, `FooDisplayHelper`). La metadata de enum **sí** vive en el entity helper como propiedad pública `static readonly Record<Enum, Meta>`, con getters de label que llaman `i18n.t()`. Si el consumidor recibe ausencia, el helper expone `getXMeta(Enum | null | undefined)` con resolver privado y `unknownMeta` — `08` / `15`.

`*Helper` **cohesivo** (un solo eje) está permitido. Clase cajón multi-dominio (`FooHelper` con fechas + user + money + UI) = hallazgo (`22`).

## Antes de crear helper/util (checklist)

1. Buscar en la feature (`helpers/`, `utils/`) y en `shared/helpers`, `shared/utils`.
2. Si existe el área → **reutilizar o extender** la clase/función.
3. Si no existe → elegir `util` (pequeño) o `helper` clase (área).
4. Mapping exhaustivo de enum → propiedad pública `static readonly Record<Enum, Meta>` en el entity helper, getter de label con `i18n.t()` y `getXMeta()` cuando el valor sea nullable (`08`). Acceso directo para enum garantizado o iteración. No aceptar `string`, casts ni fallback por consumidor; no método que reconstruya el mapa ni `*.display.config.ts`. `useMemo` según A–E de esta reference.

## Duplicación vs helper/util existente (Auditar + Implementar)

Si ya existe un helper/util de área (`DateHelper`, `NumberHelper`, util compartido) y otro archivo define una función local / dayjs wrapper que hace **lo mismo** → **Hallazgo** (no PROP de librería).

| Caso | Severidad | Corrección |
|------|-----------|------------|
| Reimplementa capacidad de `*Helper`/util **compartido** (p. ej. `formatOrderDate` ≈ `DateHelper.format`) | Media | Llamar o extender el helper; eliminar la función local |
| Util local mínimo casi idéntico **solo** dentro del mismo feature, sin shared | Baja | Consolidar en el helper/util de la feature o shared si ya aplica |
| Labels/colores de UI duplicados entre componentes | — | **Permitido** (`08`); no es este hallazgo |
| Una sola coincidencia accidental trivial **sin** abstracción previa | Baja | Baja; se reporta con propuesta genérica (`22`) |
| Misma función local (mismo nombre o mismo propósito) en 2+ archivos **sin** helper previo (p. ej. `emptyDraft` / `draftToPatch` en 6 filtros, `getEditDefaultValues` en 5 forms) | Media | Un hallazgo por grupo, con todos los archivos. Mismo cuerpo → helper de la feature o `shared/helpers`. Cuerpo con la misma forma y distinto tipo → helper genérico o hook. Cuerpo distinto con el mismo nombre → se reporta y se deja local |

Para encontrar estas funciones, el inventario de funciones locales y la comparación de cuerpos están en `24` §4.1. Aunque no sea una auditoría de repo completo, antes de escribir una función local se busca su nombre y su propósito en otros archivos.

### Formato inline (sin función local)

También es hallazgo cuando el formato se escribe **directo** en el componente o en el JSX, sin envolverlo en una función: `toFixed`, `toLocaleString`, `Intl.NumberFormat`, `Intl.DateTimeFormat`, cálculo de bytes a KB/MB, porcentaje (`${(x * 100).toFixed(1)}%`), dinero con `$` concatenado o fecha con `dayjs().format()`.

- Si existe el helper del eje (`NumberHelper`, `HumanFormatsHelper`, `DateHelper`), se usa. Si le falta el método, se agrega al helper (`HumanFormatsHelper.fileSize(bytes)`, `NumberHelper.percent(rate)`), aunque hoy se use una sola vez.
- Si no existe el helper del eje, se crea uno en `shared/helpers/` solo cuando el mismo formato aparece en 2+ archivos. Con un solo uso, Baja con propuesta.
- El locale (`'es-MX'`) y la moneda no se escriben en el call site; salen del helper o de §Valores.

```tsx
// Mal
{`${(bytes / (1024 * 1024)).toFixed(1)} MB`}
{total.toLocaleString('es-MX')}
{(amountWithTax - amount).toFixed(2)}

// Bien
{HumanFormatsHelper.fileSize(bytes)}
{NumberHelper.integer(total)}
{NumberHelper.decimal(amountWithTax - amount)}
```

Búsqueda: `rg "toFixed\(|toLocaleString\(|Intl\.(Number|DateTime)Format|1024 \* 1024" -g '*.tsx'`.

Tooling: Serena/codegraph para localizar `DateHelper` / `NumberHelper`; ast-grep para `dayjs($X).format` u wrappers `format*Date` locales.

## Valores: constantes, enums y helpers (Auditar + Implementar)

Núcleo. Complementa §Duplicación, que mira funciones; esta sección mira **valores**: literales, constantes locales y textos que repiten configuración.

### Buscar antes de declarar

Antes de escribir `const X = '<literal>'` o un literal de negocio, buscar si ya existe: `rg "'<literal>'" src/`, codegraph para `*_TIMEZONE`, `*_MAX_*`, `DEFAULT_*`, y los `static readonly` de los helpers de área. Si existe, se importa. Una cuarta fuente del mismo valor es hallazgo.

### Cuándo un valor sale del archivo

Sale si cumple **una** de estas condiciones:

1. Ya existe una constante global o un `static readonly` de helper equivalente.
2. Se usa en 2+ archivos (p. ej. schema y form de la misma feature).
3. Es valor de negocio o configuración: timezone, moneda, límites de archivo, MIME aceptados, tamaño de página, debounce.

Una constante de un solo archivo que es detalle de UI se queda local, arriba del archivo. No se arma un `constants` cajón.

### Drift: se corrige a un solo valor

Cuando dos fuentes del mismo concepto tienen valores distintos (`'America/Monterrey'` contra `APP_TIMEZONE = 'America/Mexico_City'`):

- La corrección deja **un solo valor**, que normalmente es el de la fuente de eje o global. No se legitiman los dos valores creando una segunda constante con nombre propio. Eso solo se hace si el usuario confirma que son dos conceptos de negocio distintos.
- Cuál valor es el correcto es una decisión del usuario. El hallazgo la pide, con la evidencia de los dos valores, y no la da por resuelta.
- Si el otro repo (API) tiene el mismo drift, se reporta como follow-up cruzado. Si solo se corrige un lado, el drift queda entre los dos repos.
- Los valores que ya están guardados (por ejemplo, la timezone de las torres que ya existen) no se migran como parte de la corrección. Solo cambia el valor por defecto. Migrarlos es una decisión aparte y de riesgo alto.

### Constante sin consumidores

Una constante o un `static readonly` que nadie usa (`rg -w <NOMBRE>` solo encuentra su declaración) se borra. Por ejemplo, `DEBOUNCE_FILTER_TIME` junto a `SEARCH_DEBOUNCE_MS`. Si su valor contradice el de la constante que sí se usa, no se reporta como drift: es código muerto. Severidad Baja.

### Dónde va (en orden)

1. Si el valor es del eje de un helper (timezone → `DateHelper.DEFAULT_BUSINESS_TIMEZONE`), se consume desde ahí. No se crea otra fuente.
2. Si lo usan varias features, va al archivo de constantes global que encuentre el discovery (`02`), p. ej. `config/constants/app.constants.ts`.
3. Si lo usa una sola feature, va a `features/<f>/constants/<f>.constants.ts`.

### Constante o enum

- Un literal de dominio de un **conjunto cerrado** (`'MXN'`, un estado, un tipo) → string enum (`07`). El default va como constante tipada: `DEFAULT_CURRENCY = Currency.MXN`. Prohibido `const MXN = 'MXN'`.
- Un valor de configuración (número, string, objeto de MIME) → constante `SCREAMING_SNAKE_CASE`.

### Copy que repite un valor

- El copy puro (`'Ej. Torre Santa Catarina'`) se queda inline o en i18n (`15`). No va a `constants`.
- El copy que **repite** un valor de configuración se interpola desde la constante: `` `Ej. ${DateHelper.DEFAULT_BUSINESS_TIMEZONE}` ``, `` `no puede exceder ${LOGO_MAX_MB} MB` ``. Si se escribe a mano, el texto y la validación terminan diciendo cosas distintas.

### Contraste con el backend (HARD, Auditar + Implementar)

Todo valor que la UI muestra o valida y que codifica una regla del servidor se corrobora contra el backend: límites de tamaño, MIME, dimensiones, rangos, longitudes, required/nullable, enums y estados, defaults (timezone, moneda, `per_page`, estado inicial).

**Siempre, no solo en auditoría.** Al implementar o tocar un form, un schema, un enum o un label, un copy con límites o un default, se corrobora en ese mismo cambio, aunque nadie lo pida. Un desfase que se encuentra después ya es un 422 o un label roto en producción.

Cómo:

1. **Buscar la fuente del backend:** FormRequest o `rules()`, `config/*.php`, enum, Resource o Action. Si el repo de la API está en el workspace (hermano, monorepo), se lee y se cita `archivo:línea`. Si no está, la fila queda «sin verificar». Eso no es un OK y se dice en la salida.
2. **Paridad campo a campo:** por cada campo del form o schema tocado se compara con su regla del backend: required o nullable, tipo, max de longitud, min/max numérico, MIME, tamaño y dimensiones. En auditoría se entrega una tabla:

   | Campo | Front | Backend (archivo:línea) | Estado |
   |---|---|---|---|
   | `logo` | MIME jpeg/png/webp · ≤ 2 MB · sin dimensiones | `UpdateGeneralSettingsRequest.php:67` `mimes:jpeg,png,webp` `max:2048` `dimensions:max_width=4096,max_height=4096` | Falta dimensiones |

3. **Enums exhaustivos:** cada caso del enum o estado del backend tiene su caso en el front y su label o meta en un `Record<Enum, …>` exhaustivo, nunca en un `Record<string, …>` (`07`). Si falta un caso (`rescinded`) o existe uno que el backend no tiene (`operator`), es Alta.
4. **Defaults iguales:** los valores iniciales del form y los fallbacks son iguales al default del backend o vienen de la respuesta. Si difieren, es Alta (p. ej. `America/Monterrey` en el front contra `America/Mexico_City` en la API).
5. **Una sola fuente en el front:** la constante se declara una vez, se exporta, y de ella salen el schema, `accept`, el hint y el mensaje de error. `accept` y la lista de formatos se derivan de `*_MIME_TYPES`, y los MB de `*_MAX_BYTES` (con `NumberHelper` o `HumanFormatsHelper`, §Formato inline). La constante lleva un comentario de una línea con la fuente: `// fortezza-api UpdateGeneralSettingsRequest: max:2048`.
6. **Si el backend expone el valor** (config o meta en la respuesta), el front lo consume y no lo duplica. Exponerlo cuando hoy no lo expone es **PROP**: no se cambia la API en silencio.

Ante un desfase:

- Se alinea el lado que se está editando con el **dueño** del valor. El dueño es el backend, salvo evidencia contraria.
- Alinear el front a una regla que el backend **ya** aplica se aplica directo: no es un tope nuevo ni PROP (`10` §Aplicar y proponer), porque esos datos ya los rechaza la API.
- Si el que está mal es el backend y la tarea no lo incluye, se reporta como follow-up cruzado y no se edita la API.

```tsx
// Mal — límite y formatos escritos a mano en tres lugares
const LOGO_MAX_BYTES = 2 * 1024 * 1024; // privada en settings.schema.ts
return 'PNG, JPEG o WebP · Máx. 2 MB';
<input accept='image/png,image/jpeg,image/webp' />

// Bien — una fuente exportada y corroborada
// fortezza-api UpdateGeneralSettingsRequest:67 — mimes:jpeg,png,webp · max:2048 · dimensions 4096
export const LOGO_MAX_BYTES = 2 * 1024 * 1024;
export const LOGO_MAX_DIMENSION = 4096;
export const IMAGE_MIME_TYPES = [ImageMime.Png, ImageMime.Jpeg, ImageMime.Webp];

return `${FileHelper.formatList(IMAGE_MIME_TYPES)} · Máx. ${HumanFormatsHelper.bytes(LOGO_MAX_BYTES)}`;
<input accept={IMAGE_MIME_TYPES.join(',')} />
```

### Funciones locales

- Una función del eje de un helper existente (fecha, número, teléfono, invalidación de queries, formato) se agrega como método a ese helper, aunque hoy se use una sola vez. Ver §Duplicación y §Fechas.
- Un mapper propio del componente (`toFormValues(entity)`) se queda local. Pasa al entity helper cuando otro archivo lo reutiliza.
- Si el repo no tiene un helper de ese eje, no se crea uno nuevo por una sola función (`22`).
- Si la función la usa solo un árbol de componentes, se queda privada en el padre (`04` §Funciones de un árbol de componentes).

```ts
// Mal — tres fuentes distintas del mismo valor
const DEFAULT_TIMEZONE = 'America/Monterrey';          // GeneralForm.tsx
static readonly fallbackTimezone = 'America/Monterrey'; // DashboardHelper
export const APP_TIMEZONE = 'America/Mexico_City';     // app.constants.ts

const LOGO_MAX_BYTES = 2 * 1024 * 1024; // form, y otra vez en el schema
setLogoError('El logo no puede exceder 2 MB');
currency: 'MXN',
const timezoneExample = (zone: string) => dayjs().tz(zone).format('D [de] MMMM');

// Bien
timezone: settings.timezone || DateHelper.DEFAULT_BUSINESS_TIMEZONE,
maxSize: SETTINGS_LOGO_MAX_BYTES, // features/settings/constants/settings.constants.ts, también lo importa el schema
setLogoError(`El logo no puede exceder ${SETTINGS_LOGO_MAX_MB} MB`);
currency: DEFAULT_CURRENCY,
const example = DateHelper.formatZoneExample(zone);
```

| Caso | Severidad | Corrección |
|------|-----------|------------|
| Constante local o `static readonly` con **valor distinto** a otra fuente del mismo concepto (drift) | Alta | Elegir una sola fuente, borrar las demás y revisar qué valor es el correcto |
| Constante local con el mismo valor que una global o de helper existente | Media | Importar la existente |
| Valor de configuración repetido en 2+ archivos sin fuente común (schema + UI) | Media | Constante de feature o global |
| Literal de dominio de un conjunto cerrado repetido en 2+ archivos | Media | String enum (`07`) + default tipado |
| Copy que escribe a mano un valor de configuración (límite, timezone, moneda) | Media | Interpolar desde la constante |
| El front permite lo que el backend rechaza, o el valor difiere del backend (límite, MIME, default, caso de enum) | Alta | Alinear al dueño (§Contraste con el backend) |
| Regla del backend que el front no refleja (p. ej. `dimensions`), o el front es más estricto sin motivo | Media | Agregar validación y hint, o alinear |
| Valor de regla del servidor sin corroborar ni marcar «sin verificar» | Media | Corroborar y citar `archivo:línea` |
| Función local del eje de un helper existente | Media | Método en el helper (§Duplicación) |
| Constante de UI de un solo archivo | — | Permitido, arriba del archivo |
| Placeholder o copy puro | — | Permitido (`15`) |
| Constante de styling | — | No es esta sección: `no-local-style-constants` (`04`) |

## URLs blob (HARD, Auditar + Implementar)

`URL.createObjectURL` / `revokeObjectURL` no se escriben a mano en componentes ni helpers de feature. Hay dos piezas compartidas; si no existen, se crean en `shared/` al primer uso:

| Caso | Pieza | Qué hace |
|------|-------|----------|
| Descargar un `Blob` | `FileHelper.download(blob, fileName)` (`shared/helpers`) | Crea la URL, dispara el `<a download>`, la revoca en el mismo tick |
| Preview de un `File`/`Blob` | `useObjectUrl(file)` (`shared/hooks`) → `string \| null` | Crea la URL cuando cambia `file`, la revoca en el cleanup (cambio de archivo y unmount) |

- Abrir en otra pestaña usa la misma pieza de descarga (variante `FileHelper.open(blob)`), no otra copia.
- Un preview con varios archivos llama al hook por ítem desde un componente de fila (`04` §Composición), no un array de URLs en `useState`.
- Prohibido guardar la URL en `useState` + efecto propio de create/revoke: es justo lo que encapsula el hook (`12` §Efectos).
- Auditoría: `rg -n 'URL\.(createObjectURL|revokeObjectURL)' src` — todo hit fuera de las dos piezas es hallazgo.

## Casts que apagan el tipado (HARD, Auditar + Implementar)

- Prohibidos `as any`, `as unknown as X` y `as never`. Los tres apagan el chequeo de tipos igual.
- La corrección va en el origen: tipar la fuente, alinear el schema o usar el genérico de la librería.
- Forms (RHF + Zod): si el resolver no encaja, el form usa `useForm<z.input<typeof schema>, unknown, z.output<typeof schema>>({ resolver: zodResolver(schema) })` o se alinea el schema (`.default`, `coerce`) con los valores del form (`10` §Stack). Prohibido `resolver: zodResolver(schema) as unknown as Resolver<…>`.
- Única excepción: la librería no deja otra salida. Entonces el cast va en una sola línea con un comentario que dice por qué.
- rg: `rg -n 'as unknown as|as never\b|as any\b' src`.

## Severidades (auditoría)

| Observado | Severidad |
|-----------|-----------|
| Falta dayjs en deps FE / uso sistemático de `new Date` para negocio | Alta |
| dayjs crudo pese a módulo configurado del proyecto | Media |
| Función/util local que duplica `DateHelper` / `NumberHelper` / helper compartido | Media |
| Formato inline (`toFixed`, `toLocaleString`, `Intl.*Format`, bytes→MB, `%`) con helper del eje existente | Media |
| Formato inline sin helper del eje y en 2+ archivos | Media (crear helper en `shared/helpers`) |
| Helper de display suelto / `*.display.config.ts` / `t: TFunction` en helper o schema | Media |
| `*Helper` cajón multi-dominio | Media |
| `useMemo` / `useCallback` / `memo` ceremonial (caso A; no C ni E) | Media |
| Concatenación/template de clases condicionales en vez de `cn()` | Media |
| Ternario completo de `className` cuando las clases varían (base duplicada) | Media |
| Constante/function local de styling sustituible por Tailwind + `cn()` | Media |
| String de clases local (`const cardClass = '…'`) en vez de inline + `cn()` | Media |
| Template literal que compone una constante de clases | Media |
| `sx` usado para layout/spacing/sizing ordinario pudiendo usar Tailwind | Media |
| `useTheme()` solo para alimentar `sx` (usar `sx={theme => …}`) | Media |
| `URL.createObjectURL`/`revokeObjectURL` a mano fuera de `FileHelper` / `useObjectUrl` | Media |
| Constante/`static readonly` con valor distinto a otra fuente del mismo concepto (drift) | Alta (corrección a un solo valor) |
| `as unknown as` / `as never` / `as any` sin comentario de excepción | Media |
| Misma función local en 2+ archivos sin helper previo | Media |
| Constante / `static readonly` sin consumidores | Baja |
| Constante local que duplica una global o de helper | Media |
| Valor de configuración o literal de dominio repetido en 2+ archivos | Media |
| Copy que escribe a mano un valor de configuración | Media |
| Front permite lo que el backend rechaza / default o caso de enum distinto al backend | Alta |
| Regla del backend no reflejada en el front | Media |
| Derivación repetida 2+ veces en JSX en vez de método del helper | Media |
| 3+ ramas repetidas en JSX en vez de estado derivado (C) | Media |
| Booleano de 3+ partes sin `const` con nombre por parte | Media |
| Clase estática sin `cn()` | — permitido |
| UI construye `FormData` / formatea fechas para el payload | Media |
| Multipart a mano en el service pese a existir `FormDataHelper` | Media |
| Falta `FormDataHelper` y la feature **necesita** multipart | Media (crear shared; no PROP de lib) |
| Util que debería ser helper de área (o al revés) | Baja |
| Duplicación mínima solo dentro del mismo feature | Baja |
| Alias opaco (`d`, `o`, `x`) | Baja en auditoría; en Implementar se corrige en la función tocada |

Arrows, `{ return }`, braces de `if`, JSX props: **no** esta tabla — `gian-ts-style`.
