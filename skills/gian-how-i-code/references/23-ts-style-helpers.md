# 23 — Memoización, cn, dayjs, utils y helpers

Cargar cuando: Implementar FE, crear util/helper, fechas en frontend, consultar memoización/`cn`/dayjs, constantes `*_SX` / concat de `className`.

**Formato visual TS/TSX** (arrows, braces, JSX, imports type, comments): skill `gian-react-ts-style`. Esta reference no duplica esas reglas. **Autoridad de styling** (Tailwind vs `sx` vs theme): `04`. Forma de `export const` utils: la style skill; **cuándo** crear util vs helper: aquí.

## Memoización React (regla)

No usar `useMemo`, `useCallback` o `memo` por costumbre de performance.

| Caso | Qué hacer |
|---|---|
| A. expresión derivada sencilla | cálculo directo; no `useMemo` |
| B. 2 ramas | ternario, o `&&` boolean-safe en JSX (`gian-react-ts-style`) |
| C. valor derivado multi-rama (evitaría nested ternary) | `useMemo` + `if` + early return — STYLE_GIAN de claridad, **no** claim de performance (`derived-multi-branch`) |
| D. JSX multi-rama en render | `if` / early return en el componente (`08`); no `useMemo` |
| E. performance / identidad referencial | frontera ya memoizada (p. ej. `columns` MRT, `11`) o evidencia real |

```ts
// A — no
const fullName = useMemo(
  () => `${firstName} ${lastName}`,
  [firstName, lastName],
);

// A — sí
const fullName = `${firstName} ${lastName}`;

// C — sí (claridad; ver gian-react-ts-style)
const statusLabel = useMemo(() => {
  if (isLoading) return t('…');
  if (hasError) return t('…');
  return t('…');
}, [hasError, isLoading, t]);
```

No crear helpers de display (`08` es autoridad). **No** está prohibido `useMemo` en C o E.

## `cn()` y styling local

`04` decide qué va en Tailwind vs `sx` y es la autoridad de styling. Esta sección solo define la mecánica de clases.

| Forma de las clases | Mecánica |
|---|---|
| Completamente estáticas | `className` directo; no `cn()` ceremonial |
| Condicionales, compuestas o variables por estado/props runtime | `cn()` |
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
```

Preferir Tailwind + `cn()` directamente en JSX cuando el gate de `04` lo permita.

Excepciones (igual que `04`): mapping semántico reutilizable de variantes; primitive/shared real; valor dinámico que requiere `theme`; API MUI que sólo expone razonablemente `sx`.

## Renombres explícitos (default)

Alias claros frente a nombres opacos (`d`, `o`, `x`). Geometría de destructuring: `gian-react-ts-style` (`query-data-alias`, `direct-property-access`). MRT `Cell: ({ row: { original } })` se queda en `11`.

```ts
const { data: entities } = useEntitiesQuery(…);
```

## Fechas — dayjs (regla)

- Stack FE canónico incluye **dayjs** en todos los proyectos.
- No usar `new Date` / Date nativo para parseo, formato o aritmética de negocio en FE.
- Si el repo tiene un **módulo configurado** (`lib/dayjs`, plugins utc/timezone/locale, etc.): importar **desde ese módulo**, no `import dayjs from 'dayjs'` crudo.
- Preferir `DateHelper` (u helper de área) que envuelva ese dayjs; o `dayjs(value).format(…)` puntual vía el mismo módulo.

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
| `utils/` | Cosas **pequeñas** y genéricas (pocas líneas, sin dominio rico) | `export const … = () =>` (sintaxis: `gian-react-ts-style`) | `.util.ts` |
| `helpers/` | Agrupan un **área** (fechas, números, usuario, formatos humanos, reglas de dominio, **Record de meta de enum**) | `export class XxxHelper` | `.helper.ts` |

Ejemplos de helpers de área: `DateHelper`, `HumanFormatsHelper`, `NumberHelper`, `UserHelper`.

```ts
export const clamp = (n: number, min: number, max: number) =>
  Math.min(max, Math.max(min, n));

export class DateHelper {
  static format(value: string | Date, pattern = 'YYYY-MM-DD') {
    return dayjs(value).format(pattern);
  }
}
```

**Prohibido:** `*.display.config.ts`, inyectar `TFunction`, `labelKey` diferido, clase *solo* de UI (`ColorHelper.statusColor`, `FooDisplayHelper`). El Record de enum **sí** vive en el entity helper con `i18n.t()` — `08` / `15`.

`*Helper` **cohesivo** (un solo eje) está permitido. Clase cajón multi-dominio (`FooHelper` con fechas + user + money + UI) = hallazgo (`22`).

## Antes de crear helper/util (checklist)

1. Buscar en la feature (`helpers/`, `utils/`) y en `shared/helpers`, `shared/utils`.
2. Si existe el área → **reutilizar o extender** la clase/función.
3. Si no existe → elegir `util` (pequeño) o `helper` clase (área).
4. Mapping exhaustivo de enum → Record en el entity helper con `i18n.t()` (`08`). If-chain ad-hoc → inline con `t()`. No `*.display.config.ts`. `useMemo` según A–E de esta reference.

## Duplicación vs helper/util existente (Auditar + Implementar)

Si ya existe un helper/util de área (`DateHelper`, `NumberHelper`, util compartido) y otro archivo define una función local / dayjs wrapper que hace **lo mismo** → **Hallazgo** (no PROP de librería).

| Caso | Severidad | Corrección |
|------|-----------|------------|
| Reimplementa capacidad de `*Helper`/util **compartido** (p. ej. `formatOrderDate` ≈ `DateHelper.format`) | Media | Llamar o extender el helper; eliminar la función local |
| Util local mínimo casi idéntico **solo** dentro del mismo feature, sin shared | Baja | Consolidar en el helper/util de la feature o shared si ya aplica |
| Labels/colores de UI duplicados entre componentes | — | **Permitido** (`08`); no es este hallazgo |
| Una sola coincidencia accidental trivial **sin** abstracción previa | — | No forzar extracción (`22`); omitir o Baja |

Tooling: Serena/codegraph para localizar `DateHelper` / `NumberHelper`; ast-grep para `dayjs($X).format` u wrappers `format*Date` locales.

## Severidades (auditoría)

| Observado | Severidad |
|-----------|-----------|
| Falta dayjs en deps FE / uso sistemático de `new Date` para negocio | Alta |
| dayjs crudo pese a módulo configurado del proyecto | Media |
| Función/util local que duplica `DateHelper` / `NumberHelper` / helper compartido | Media |
| Helper de display suelto / `*.display.config.ts` / `t: TFunction` en helper o schema | Media |
| `*Helper` cajón multi-dominio | Media |
| `useMemo` / `useCallback` / `memo` ceremonial (caso A; no C ni E) | Media |
| Concatenación/template de clases condicionales en vez de `cn()` | Media |
| Ternario completo de `className` cuando las clases varían (base duplicada) | Media |
| Constante/function local de styling sustituible por Tailwind + `cn()` | Media |
| `sx` usado para layout/spacing/sizing ordinario pudiendo usar Tailwind | Media |
| `useTheme()` solo para alimentar `sx` (preferir `sx={theme => …}`) | Media |
| Clase estática sin `cn()` | — permitido |
| Util que debería ser helper de área (o al revés) | Baja |
| Duplicación mínima solo dentro del mismo feature | Baja |
| Nombre opaco en alias frecuente | Baja |

Arrows, `{ return }`, braces de `if`, JSX props: **no** esta tabla — `gian-react-ts-style`.
