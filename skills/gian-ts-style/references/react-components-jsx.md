# React components and JSX

Solo React. En Vue, Angular y Node no aplica.

## Component explicit return (HARD)

`react-component-explicit-return`. Identificador **PascalCase** (o anotado `FC`): block body + `return` explícito, incluso si solo retorna JSX.

```tsx
export const EmptyState: FC = () => {
  return (
    <Stack>
      <Typography>Sin registros</Typography>
    </Stack>
  );
};
```

No:

```tsx
export const EmptyState: FC = () => (
  <Stack>
    <Typography>Sin registros</Typography>
  </Stack>
);
```

WRITE/FIX: implicit JSX de componente PascalCase → block + `return`.

No aplica a:

- helpers camelCase `renderFoo` / `renderTitle` → `arrow-implicit-return`
- `Cell`, `Header`, `queryFn` que retornan JSX → `arrow-implicit-return`
- factories no PascalCase

## Component props (HARD)

`react-component-fc-props`. Las props van en una interface que se llama como el componente más `Props`: `HomePage` → `HomePageProps`, `InvoiceDrawer` → `InvoiceDrawerProps`. El componente se anota con `FC<HomePageProps>` y destructura las props en la firma. Sin props: `FC`.

```tsx
import type { FC, ReactNode } from 'react';

interface InvoiceDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

export const InvoiceDrawer: FC<InvoiceDrawerProps> = ({ isOpen, onClose, children }) => {
  return (
    <Drawer open={isOpen} onClose={onClose}>
      {children}
    </Drawer>
  );
};
```

Props derivadas de otro componente:

```tsx
interface StatusChipProps extends ComponentProps<typeof Chip> {
  status: InvoiceStatus;
}
```

Prohibido:

```tsx
interface Props { … }
export const InvoiceDrawer: FC<Props> = …;

interface DrawerProps { … }
export const InvoiceDrawer: FC<DrawerProps> = …;

export const InvoiceDrawer = ({ isOpen, onClose }: InvoiceDrawerProps) => { … };
export const InvoiceDrawer = ({ isOpen }: { isOpen: boolean }) => { … };
export const InvoiceDrawer: FC<InvoiceDrawerProps> = ({ isOpen }): JSX.Element => { … };
export function InvoiceDrawer({ isOpen }: InvoiceDrawerProps) { … }
type InvoiceDrawerProps = { isOpen: boolean };
type StatusChipProps = ComponentProps<typeof Chip> & { status: InvoiceStatus };
export const InvoiceDrawer: React.FC<InvoiceDrawerProps> = …;
export const InvoiceDrawer: FunctionComponent<InvoiceDrawerProps> = …;
export const InvoiceDrawer: VFC<InvoiceDrawerProps> = …;
export const InvoiceDrawer: FC<PropsWithChildren<InvoiceDrawerProps>> = …;
```

- El nombre es exacto: `<NombreDelComponente>Props`. `Props` a secas, una abreviatura o el nombre de otro componente es error.
- Cada componente del archivo tiene la suya: `HomePage` usa `HomePageProps` y `HomePageHeader` usa `HomePageHeaderProps`.
- Los componentes no exportados del archivo usan la misma forma.
- La interface es local. Se exporta solo si otro archivo la necesita, con el mismo nombre.
- `FC` con `import type { FC } from 'react'`. Prohibidos `React.FC`, `FunctionComponent`, `VFC` y `PropsWithChildren`.
- `children` se declara en la interface como `ReactNode`. `FC` no lo agrega.
- El retorno no se anota (`): JSX.Element`, `): ReactElement`, `): ReactNode`).
- `export default`: `export const X: FC = …;` y luego `export default X;`. Ningún router obliga a otra forma.
- Los archivos generados (`*.gen.ts`, `*.gen.tsx`) quedan fuera de alcance.
- WRITE: componente nuevo y componente tocado. FIX: el mismo cambio en ese alcance, incluido renombrar `Props` → `<Componente>Props` y sus usos. El otro componente del archivo no se migra.
- Gate: el typecheck del repo (`gian-how-i-code` `17`). Si falla por la firma (retorna `string` o `undefined` con tipos viejos), revertir y reportar `GAP react-component-fc-props archivo:línea — typecheck falla por la firma`.

GAP, se conserva la forma actual (`principles.md` § NEVER AUTOFIX):

- componente genérico (`<T,>(props: SelectProps<T>)`)
- `forwardRef`
- `memo(...)`, con o sin comparador
- `Cell`, `Header` y render props de librería
- el repo tiene activa una regla de ESLint que prohíbe `FC`: gana el lint

## className con cn() (HARD)

`classname-cn`. En el alcance, todo `className` o prop `*ClassName` (`inputClassName`, `paperClassName`) que no es un string literal estático se escribe con el `cn` del repo:

- template literal → `cn(...)`
- concatenación con `+` → `cn(...)`
- ternario de strings o de variables → `cn(base, cond && extra)`
- `[...].join(' ')` o `filter(Boolean).join(' ')` → `cn(...)`
- `className` recibido por props → `cn(base, className)`
- `clsx(...)`, `classnames(...)`, `twMerge(...)` → `cn(...)`
- variable intermedia construida con ternario o template (`const classes = …; className={classes}`) → se inlinea en `cn(...)`
- `cva`: `className={cn(buttonVariants({ size }), className)}`

```tsx
BAD:  <span className={`mr-1 text-muted ${isOpen ? 'rotate-180' : ''}`} />
GOOD: <span className={cn('mr-1 text-muted', isOpen && 'rotate-180')} />

BAD:  <article className={prominent ? cardClass : innerClass}>
GOOD: <article className={cn('rounded-lg border p-3', prominent && 'rounded-xl bg-white p-4')}>

BAD:  <Input inputClassName={clsx('h-9', hasError && 'border-destructive')} />
GOOD: <Input inputClassName={cn('h-9', hasError && 'border-destructive')} />
```

Un string estático sigue sin `cn()`: `className="flex gap-2"`.

Antes de escribir, localizar el `cn` existente: `rg "export (const|function) cn\b"`. No crear otro. No importar `clsx`, `classnames` ni `twMerge` directo.

Antes de cerrar, sobre los `.tsx` tocados corre `node <ruta de gian-ts-style>/assets/self-check.mjs`. El script cubre `classname-cn`, pero no detecta `clsx`/`classnames`/`twMerge` directo ni `const xClass = '…'`. Esos dos `rg` se siguen corriendo a mano. Equivale a:

```bash
rg -nU '[A-Za-z]*[cC]lassName=\{\s*(`|[^}]*\+|[^}]*\?|[^}]*join\()' <archivos tocados>
rg -n '\b(clsx|classnames|twMerge)\(' <archivos tocados>
rg -n "const [A-Za-z_]*(Class|CLASS|Classes|CLASSES)[A-Za-z_]* = ['\`]" <archivos tocados>
```

Cada coincidencia dentro del alcance se corrige. Un string de clases local (`const cardClass = '…'`) se inlinea en el componente tocado (`gian-how-i-code` `04`/`23`).

GAP: el repo no tiene `cn`. No se crea (`gian-how-i-code` `19`). Qué va en Tailwind y qué en `sx` lo decide `gian-how-i-code` `04`.

## Conditional `&&` (HARD)

`conditional-and-render`. Condición de tipo `boolean` (comparación, `!x`, `!!x`, `Boolean(x)`, variable tipada `boolean`) y rama falsa `null` → `&&`.

```tsx
{isEnabled && <Panel />}
```

No:

```tsx
{isEnabled ? <Panel /> : null}
```

Condición `number`, `string` o array → se conserva el ternario. `{count && <Badge />}` renderiza `0`. No es FAIL.

## Simple JSX ternary (HARD)

`simple-jsx-ternary`. Un ternario de dos ramas que se usa una sola vez queda inline en el JSX. Prohibido extraerlo a una variable o a una IIFE.

```tsx
{isActive ? <ActiveState /> : <InactiveState />}
```

No:

```tsx
const statusNode = isActive ? <ActiveState /> : <InactiveState />;

return <Card>{statusNode}</Card>;
```

## Boolean props (HARD)

`boolean-prop-shorthand`. SAFE FIX:

```tsx
<Button disabled />
```

No: `<Button disabled={true} />`.

`={false}` se conserva. Omitirlo cambia el default de la prop. No es FAIL.

## Fragments (HARD)

`fragment-shorthand`. `<Fragment>` y `<React.Fragment>` sin `key` → `<>…</>`. Con `key`: `<Fragment key={id}>`.

SAFE FIX. Un fragment con un solo hijo se conserva; esta regla no lo quita.

## Self-closing (HARD)

`self-closing-jsx`. Sin children: `<LoadingIndicator />`. No `<LoadingIndicator></LoadingIndicator>`.

SAFE FIX. Si ESLint `react/self-closing-comp` ya cubre la línea, no FAIL duplicado.

## Prop spread (HARD en WRITE)

`intentional-prop-spread`. WRITE solo hace spread de:

- un objeto tipado `<X>Props` o `ComponentProps<typeof Y>`;
- el `...rest` de las props del propio componente.

```tsx
<UserCard {...userCardProps} />

export const SearchInput: FC<SearchInputProps> = ({ label, ...rest }) => {
  return <TextField label={label} {...rest} />;
};
```

Prohibido: spread de una entity, un DTO o una fila de query. Se pasan las props explícitas.

```tsx
BAD:  <UserCard {...user} />
GOOD: <UserCard name={user.name} email={user.email} />
```

Código existente con spread de entity/DTO: `GAP intentional-prop-spread archivo:línea — spread de entity/DTO`.
