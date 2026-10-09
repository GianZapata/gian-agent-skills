# 04 — Arquitectura frontend

Cargar cuando: estructura FE, MUI+Tailwind, organización de componentes, styling (`className` / `cn()` / `sx` / theme).

## Alcance

- **Adaptador React:** stack canónico y styling MUI/Tailwind de este archivo.
- **Núcleo:** §Naming. Vale en cualquier stack. En Vue la carpeta es `composables/` (`25`); el archivo sigue `useThing.ts`.

## Stack canónico

- React + TypeScript
- MUI v7 + Tailwind + `cn()`
- React Query v5+
- RHF + Zod
- i18n react-i18next (JSON flat)
- **dayjs** (fechas; ver `23`)

Este stack es el adaptador React. Otro stack no hereda MUI, RHF ni React Query. El núcleo sigue (`01`); el delta de vista, si existe, se suma (`25` en Vue).

Sintaxis TS/TSX: `gian-ts-style` (no decide Tailwind/MUI/`sx`). Mecánica de `cn()` y anti-patrones: `23`. Contratos de props de librería (MUI/RHF/TanStack): tipo oficial, no shadow — `07`. Labels/colores de **display de estado**: `08` (metadata del enum en el entity helper; ad-hoc inline). Tokens MUI: `theme.palette` aquí.

## Styling ownership — MUI + Tailwind

### Regla

En componentes React/MUI:

1. Tailwind es el default para CSS visual:
   - layout
   - flex / grid de CSS
   - spacing
   - width / height
   - min/max sizes
   - border radius
   - borders
   - typography puramente CSS
   - responsive
   - hover/focus simples
   - visibility/display

2. Usar `className` directamente cuando las clases son completamente estáticas.

```tsx
<div className="flex items-center gap-2" />
```

No: `className={cn('flex items-center gap-2')}` sin condición (ceremonia).

3. **Gate de `cn()` según clases runtime.** Usar `cn()` cuando:
   - existen clases condicionales o compuestas;
   - se combinan clases base + estado;
   - existe `className` recibido por props;
   - las clases varían por `selected`, `active`, `checked`, `disabled` custom, `status`, `mode` o cualquier estado/prop runtime.

```tsx
<Button
  className={cn(
    'h-[30px] rounded-lg px-2',
    !isSelected && 'text-text-secondary hover:bg-white'
  )}
/>
```

No repetir el string base en un ternario completo de `className` cuando `cn()` expresa la composición:

```tsx
className={
  isSelected
    ? 'h-[30px] rounded-lg px-2'
    : 'h-[30px] rounded-lg px-2 text-text-secondary hover:bg-white'
}
```

Tampoco duplicar dos árboles JSX solo para evitar `cn()`.

El gate observa si **las clases varían**, no si el componente tiene estado. Si el estado visual se resuelve por completo con props oficiales de MUI y `className` es idéntico, conservarlo estático:

```tsx
<Button
  variant={isSelected ? 'contained' : 'text'}
  color={isSelected ? 'primary' : 'inherit'}
  className="h-[30px] rounded-lg px-2"
/>
```

Mecánica y anti-patrones de composición: `23`.

4. **`no-local-style-constants` (HARD).** No extraer objetos/functions de styling locales por organización visual.

No:

```ts
const CONTROL_SX: SxProps<Theme> = { height: 38, minHeight: 38 };

const toggleButtonSx = (isSelected: boolean): SxProps<Theme> => ({ … });

const getButtonSx = (selected: boolean) => ({ … });
```

Si representan styling ordinario, expresarlos con Tailwind y `cn()` en el punto de uso.

Lo mismo con un string de clases. No:

```tsx
const cardClass = 'rounded-xl border border-divider bg-white p-4';
const innerClass = 'rounded-lg border border-divider p-3';

<article className={prominent ? cardClass : innerClass}>
<div className={`${cardClass} mt-4`}>
```

Sí:

```tsx
<article
  className={cn(
    'rounded-lg border border-divider p-3',
    prominent && 'rounded-xl bg-white p-4'
  )}
>
```

Si el mismo bloque se repite, se extrae un componente (`<SummaryCard prominent>`), no un string. Al tocar un componente que usa la constante, se inlinea en ese componente; el resto del archivo no se migra. Un primitive compartido entre archivos que ya existe en el repo, o un mapa de variantes, se conserva y se compone con `cn()`, nunca con template literal.

Una constante de styling sólo se justifica si representa una abstracción **semántica reutilizable** y no una agrupación de CSS. Excepciones: mapping de variantes compartido; primitive/shared real; valor dinámico que exige theme; API MUI que sólo expone razonablemente `sx`.

5. `sx` es escape hatch, no styling default. Sigue siendo válido cuando:
   - el token del theme no tiene una utility Tailwind equivalente;
   - el valor es dinámico y depende realmente del theme;
   - una API MUI requiere razonablemente `sx`;
   - Tailwind o `slotProps` degradan claridad o correctness.

### Gate de resolución de tokens visuales

Cuando un estilo necesita un color/token, resolver en este orden:

1. **Utility Tailwind verificada.** Si la configuración real del repo expone una utility respaldada por el MUI theme o por su bridge, preferir `className` / `cn()`.

   Infraestructura válida del repo:

   ```css
   --color-success-light: var(--mui-palette-success-light);
   --color-success-dark: var(--mui-palette-success-dark);
   --color-divider: var(--mui-palette-divider);
   --color-text-secondary: var(--mui-palette-text-secondary);
   ```

   Uso:

   ```tsx
   className={cn(
     'rounded-full font-bold',
     isActive && 'bg-success-light text-success-dark',
     !isActive && 'bg-divider text-text-secondary'
   )}
   ```

   El source of truth sigue siendo MUI theme: Tailwind consume el bridge generado/configurado desde él. Esos aliases de bridge no son una duplicación independiente de tokens.

2. **`slotProps.className` cuando aplica a un slot interno.** Usarlo solo si la API pública del componente documenta y expone ese slot. Esto no significa que `slotProps` preceda a `sx` para cualquier propiedad; el paso solo aplica cuando el objetivo es estilizar ese slot.

3. **`sx={(theme) => …}`.** Conservarlo cuando no existe una equivalencia limpia y demostrable o cuando la API MUI lo requiere.

Tailwind-first no convierte automáticamente cada `theme.palette` a utilities. Primero verificar la configuración real del repo. No inventar utilities, colores arbitrarios (`bg-[#…]`, `text-[#…]`, `border-[#…]`), aliases aproximados ni editar theme/Tailwind CSS silenciosamente.

### Theme dentro de styling

Si el theme sólo se necesita para `sx`, NO crear `const theme = useTheme()`.

Preferir:

```tsx
sx={(theme) => ({
  color: theme.palette.text.secondary,
  backgroundColor: theme.palette.background.paper,
})}
```

`useTheme()` únicamente cuando el theme también sea necesario fuera de `sx` o participe en lógica JS.

No crear constantes de colores paralelas ni importar `Color.*` cuando el valor ya pertenece al MUI theme.

6. No duplicar el mismo token entre Tailwind, `Color.ts`, constantes locales, `sx` y `theme.palette`. El MUI theme del proyecto es la fuente de verdad; un alias del bridge que lo referencia no constituye un token independiente.

### Slots MUI vs selectores internos

Antes de usar selector interno con `sx`:

```ts
'& .MuiOutlinedInput-root': { … }
```

revisar si el componente permite la API pública:

```tsx
slotProps={{
  input: {
    className: 'h-9',
  },
}}
```

Selectores `'& .Mui…'` son fallback, no default. No inventar nombres de slot: usar solo los que documenta **ese** componente.

### Grid MUI

`size={{ xs: 12, md: 6 }}` (no props legacy `item` / `xs`).

## Skeleton de carga

Si la espera ocupa el lugar de una tarjeta, lista, ficha o gráfica, el placeholder es un skeleton con el alto de lo que va a llegar. No un párrafo visible.

- La pantalla ya está en Tailwind: bloques `animate-pulse`.
- La superficie ya es MUI (tabla, diálogo): `Skeleton` de MUI.

No se agrega una librería. El texto de error y el vacío no se sustituyen.

## Organización

- Container / presentational en forms
- Diálogos como componentes aparte
- Shared solo para transversal real (`shared/helpers`, `shared/utils`)
- No meter dialogs compartidos solo dentro de `Form/**` si la tabla también los usa

## Naming

**Núcleo.** No depende del framework.

- Componentes PascalCase
- Callbacks `on*` / verbos; **prohibido `handle*`**
- Archivos `use*` y composables (**HARD**): archivo, directorio 1:1, export `use*` e import specifier en camelCase. `use-`/`use_` + segmentos → `use` + PascalCase (`use-dashboard` → `useDashboard`). Nunca kebab/snake. Implementar: rename en alcance (archivo/dir + imports); no barrer el repo. Auditar: Hallazgo. **No** aplica a barrels del molde (`<entity>.queries.ts`, `<entity>.mutations.ts`) ni a `.interface` / `.schema` / `.service` / `.helper` / `.util`.

## Orden dentro del composable, hook o componente (HARD)

Aplica a composables Vue, hooks React, services Angular con estado y al cuerpo de un componente React. La línea en blanco entre grupos es formato: `gian-ts-style`. Sin comentarios de sección (`// State`, `// Effects`).

1. Dependencias que no leen estado local: router, route, stores, `inject()`, clientes.
2. Estado: `ref` / `useState` / `useRef` / `signal`.
3. Hooks que leen ese estado: query, mutation, debounce, otro composable. Van arriba de cualquier `return`.
4. Variables derivadas: `const` desde esos datos, `computed` / `useMemo`, según A–E de `23`.
5. Funciones: helpers internos y handlers.
6. Efectos, al final: `watch` / `useEffect` / `effect`, y el ciclo de vida (`onMounted`) si existe.
7. `return`, o el JSX en un componente.

Un `return` temprano no queda antes de un hook. Si hoy está arriba, baja.

Si el edit entra en ese cuerpo, esa función queda en este orden antes de cerrar el cambio. Se mueven los bloques de primer nivel. No se agrega un guard dentro de un efecto para compensar el movimiento.

Un archivo con dos componentes: solo el cuerpo que se editó. Imports, la interface de props o un tipo al lado no disparan el reorden si el cuerpo no se tocó. No se recorre el archivo ni el repo.

Los casos dentro de cada slot (dependencias, estado, queries, derivadas, handlers, efectos y returns tempranos) están en `26`. Esta sección no los repite.

```tsx
export const InboxPage: FC = () => {
  const navigate = useNavigate();

  const [search, setSearch] = useState('');

  const inbox = useInboxQuery({ search });

  const rows = inbox.data?.data ?? [];

  const openRow = (id: string) => {
    navigate(`/inbox/${id}`);
  };

  useEffect(() => {
    document.title = rows[0]?.title ?? 'Bandeja';
  }, [rows]);

  return <List rows={rows} onOpen={openRow} />;
};
```
