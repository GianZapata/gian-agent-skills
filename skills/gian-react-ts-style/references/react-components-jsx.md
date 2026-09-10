# React components and JSX

## Component explicit return (HARD)

`react-component-explicit-return`. Identificador **PascalCase** (o anotado `FC` / `React.FC`): block body + `return` explícito, incluso si solo retorna JSX.

```tsx
const EmptyState = () => {
  return (
    <Stack>
      <Typography>Sin registros</Typography>
    </Stack>
  );
};
```

No convertir automáticamente a:

```tsx
const EmptyState = () => (
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

`React.FC` vs props explícitas: GAP; match-file. No migrar.

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
