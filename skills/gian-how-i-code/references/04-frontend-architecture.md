# 04 — Arquitectura frontend

Cargar cuando: estructura FE, MUI+Tailwind, organización de componentes, styling (`className` / `cn()` / `sx` / theme).

## Stack canónico

- React + TypeScript
- MUI v7 + Tailwind + `cn()`
- React Query v5+
- RHF + Zod
- i18n react-i18next (JSON flat)
- **dayjs** (fechas; ver `23`)

Sintaxis TS/TSX: `gian-react-ts-style` (no decide Tailwind/MUI/`sx`). Mecánica de `cn()` y anti-patrones: `23`. Contratos de props de librería (MUI/RHF/TanStack): tipo oficial, no shadow — `07`. Labels/colores de **display de estado**: `08` (no helpers); tokens MUI: `theme.palette` aquí.

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

## Organización

- Container / presentational en forms
- Diálogos como componentes aparte
- Shared solo para transversal real (`shared/helpers`, `shared/utils`)
- No meter dialogs compartidos solo dentro de `Form/**` si la tabla también los usa

## Naming

- Componentes PascalCase
- Callbacks `on*` / verbos; **prohibido `handle*`**
- Hooks custom (**HARD**): archivo, directorio 1:1, export `use*` e import specifier en camelCase. `use-`/`use_` + segmentos → `use` + PascalCase (`use-dashboard` → `useDashboard`). Nunca kebab/snake. Implementar: rename en alcance (archivo/dir + imports); no barrer el repo. Auditar: Hallazgo. **No** aplica a barrels del molde (`<entity>.queries.ts`, `<entity>.mutations.ts`) ni a `.interface` / `.schema` / `.service` / `.helper` / `.util`.
- Sin comentarios en código productivo — `gian-react-ts-style` `comments-noise` (conservar directives)
