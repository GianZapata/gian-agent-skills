# React components and JSX

Solo React. En Vue, Angular y Node no aplica.

## Component explicit return (HARD)

`react-component-explicit-return`. Identificador **PascalCase** (o anotado `FC` / `React.FC`): block body + `return` explícito, incluso si solo retorna JSX.

```tsx
export const EmptyState: FC = () => {
  return (
    <Stack>
      <Typography>Sin registros</Typography>
    </Stack>
  );
};
```

No convertir automáticamente a:

```tsx
export const EmptyState: FC = () => (
  <Stack>
    <Typography>Sin registros</Typography>
  </Stack>
);
```

WRITE/FIX: implicit JSX de componente PascalCase → block + `return`.

No aplicar a:

- camelCase `renderFoo` / `renderTitle` → GAP (ambiguo)
- `Cell`, `Header`, `queryFn` que retornan JSX → `arrow-implicit-return`
- factories no PascalCase

## Component props (HARD)

`react-component-fc-props`. Las props van en una `interface Props` local al archivo. El componente se anota con `FC<Props>` y destructura las props en la firma. Sin props: `FC`.

```tsx
import type { FC, ReactNode } from 'react';

interface Props {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}

export const InvoiceDrawer: FC<Props> = ({ open, onClose, children }) => {
  return (
    <Drawer open={open} onClose={onClose}>
      {children}
    </Drawer>
  );
};
```

No:

```tsx
export const InvoiceDrawer = ({ open, onClose }: Props) => { … };
export const InvoiceDrawer = ({ open, onClose }: { open: boolean; onClose: () => void }) => { … };
type Props = { open: boolean };
export const InvoiceDrawer: React.FC<Props> = …;
```

- `FC` con `import type { FC } from 'react'`, no `React.FC`.
- `children` se declara en `Props` como `ReactNode`. `FC` no lo agrega.
- Si otro archivo necesita el tipo: `export interface InvoiceDrawerProps`.
- WRITE: componente nuevo y componente tocado. FIX: el mismo cambio en ese alcance. El otro componente del archivo no se migra.
- Si el typecheck falla por la firma (retorna `string` o `undefined` con tipos viejos), revertir y registrar GAP.

GAP, se conserva la forma actual:

- componente genérico (`<T,>(props: Props<T>)`)
- `forwardRef`, y `memo(...)` con comparador
- `Cell`, `Header` y render props de librería
- componente cuya forma impone el generador del router
- el repo tiene activa una regla de ESLint que prohíbe `FC`: gana el lint

## className con cn() (HARD)

`classname-cn`. En el hunk tocado, un `className` que no es un string literal estático se escribe con el `cn` del repo:

- template literal → `cn(...)`
- concatenación con `+` → `cn(...)`
- ternario de strings o de variables → `cn(base, cond && extra)`
- `[...].join(' ')` o `filter(Boolean).join(' ')` → `cn(...)`
- `className` recibido por props → `cn(base, className)`

```tsx
BAD:  <span className={`mr-1 text-muted ${isOpen ? 'rotate-180' : ''}`} />
GOOD: <span className={cn('mr-1 text-muted', isOpen && 'rotate-180')} />

BAD:  <article className={prominent ? cardClass : innerClass}>
GOOD: <article className={cn('rounded-lg border p-3', prominent && 'rounded-xl bg-white p-4')}>
```

Un string estático sigue sin `cn()`: `className="flex gap-2"`.

Antes de escribir, localizar el `cn` existente: `rg "export (const|function) cn\b"`. No crear otro. No importar `clsx` ni `twMerge` directo si `cn` existe.

Antes de cerrar, sobre los `.tsx` tocados:

```bash
rg -n 'className=\{(`|[^}]*\+|[^}]*\?|[^}]*join\()' <archivos tocados>
rg -n "const [A-Za-z_]*(Class|CLASS|Classes|CLASSES)[A-Za-z_]* = ['\`]" <archivos tocados>
```

Cada coincidencia dentro del hunk se corrige. Un string de clases local (`const cardClass = '…'`) se inlinea en el componente tocado (`gian-how-i-code` `04`/`23`).

GAP: el repo no tiene `cn`, o no es React. No se crea (`gian-how-i-code` `19`). Qué va en Tailwind y qué en `sx` lo decide `gian-how-i-code` `04`.

## Conditional `&&` (PREFERENCE)

`conditional-and-render`. Mostrar algo solo si es true:

```tsx
{isEnabled && <Panel />}
```

No `{isEnabled ? <Panel /> : null}` cuando son equivalentes.

AST-SENSITIVE. Condición **boolean-safe** (`boolean`, ya `!!x`). NEVER AUTOFIX:

```tsx
{count && <Badge />}
```

si `count` puede ser `0` / `""`.

## Simple JSX ternary (PREFERENCE)

`simple-jsx-ternary`. Dos alternativas reales:

```tsx
{isActive ? <ActiveState /> : <InactiveState />}
```

No extraer a variable/IIFE solo por el ternario. Anti-fixture KEEP. No FAIL.

## Boolean props (HARD)

`boolean-prop-shorthand`. SAFE FIX:

```tsx
<Button disabled />
```

No: `<Button disabled={true} />`.

`={false}`: GAP. No omitir ni forzar simetría (cambia el default).

## Fragments (HARD)

`fragment-shorthand`. Sin `key`/ref/props: `<>…</>`. Con `key` u otras props: `<Fragment key={id}>`.

SAFE FIX solo en el caso sin props.

## Self-closing (HARD)

`self-closing-jsx`. Sin children: `<LoadingIndicator />`. No `<LoadingIndicator></LoadingIndicator>`.

SAFE FIX. Si ESLint `react/self-closing-comp` ya cubre la línea, no FAIL duplicado.

## Prop spread (PREFERENCE)

`intentional-prop-spread`. OK cuando el objeto **ya es** props:

```tsx
<UserCard {...userCardProps} />
```

No HARD. NEVER AUTOFIX conversión a spread. Spread de entity/DTO/query row → no fomentar; GAP si se pide convertir.
