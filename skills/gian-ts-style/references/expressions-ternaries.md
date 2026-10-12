# Expressions and ternaries

## No nested ternary (HARD: WRITE, FIX y AUDIT)

`no-nested-ternary`. Más de un `? :` en la misma expresión → prohibido. Aplica a expresiones de valor y a JSX. Los conditional types (`T extends U ? X : Y`) quedan fuera.

El rewrite depende del **resultado**:

- **JSX en render** → if / early return en el componente, o un subcomponente por rama (`gian-how-i-code` `08`).
- **Valor derivado** (string, objeto, número) → `derived-multi-branch`.

El rewrite a if/return se hace siempre. GAP solo si el ternario está en un default param, en un decorator o en una posición de tipo: `GAP no-nested-ternary archivo:línea — <caso>`.

## Derived multi-branch (HARD)

`derived-multi-branch`. Entra aquí un valor derivado que cumple una de estas:

- tiene 3 o más ramas;
- es un ternario cuya condición junta 3 o más partes con `&&` / `||`, aunque solo tenga dos resultados.

Dentro de un componente o hook React: `useMemo` con `if` y early return (`gian-how-i-code` `23` caso C). En Vue: `computed`. Es claridad, no performance.

```tsx
const orderMessage = useMemo(() => {
  if (fromMessage !== null || toMessage !== null) return null;
  if (localFrom === null || localTo === null) return null;
  if (!localTo.startOf('day').isBefore(localFrom.startOf('day'))) return null;

  return DashboardHelper.periodMessages.order;
}, [fromMessage, toMessage, localFrom, localTo]);
```

Los guards siguen el orden de `26`: invalidez, ausencia, conflicto, precondición. El valor del camino feliz va al final.

Fuera de un componente o hook (función plana, helper): `if` con `return` en la propia función, o una función con nombre en el módulo.

```ts
const statusLabel = (status: Status | null): string => {
  if (status === null) return 'Sin estado';
  if (status === Status.Failed) return 'Error';

  return 'Listo';
};
```

Prohibido: IIFE, ternario anidado y ternario con una condición de 3+ partes.

No:

```tsx
const orderMessage =
  fromMessage === null &&
  toMessage === null &&
  localTo !== null &&
  localFrom !== null &&
  localTo.startOf('day').isBefore(localFrom.startOf('day'))
    ? DashboardHelper.periodMessages.order
    : null;

const statusLabel = isLoading
  ? 'Cargando'
  : hasError
    ? 'Error'
    : 'Listo';

const statusLabel = (() => {
  if (isLoading) return 'Cargando';
  return 'Listo';
})();
```

Dos resultados con una condición de 1 o 2 partes → ternario simple (`simple-jsx-ternary` o ternario de valor). Un boolean puro (`const canPay = a && b && c`) no es ternario: se queda como expresión.

## Memoización

Cuándo usar o quitar `useMemo` / `computed` lo decide `gian-how-i-code` `23`. `assets/self-check.mjs` marca FAIL `derived-multi-branch` y `no-nested-ternary`, y GAP `memo-ceremonial` para un `useMemo` de una sola expresión sin ramas.
