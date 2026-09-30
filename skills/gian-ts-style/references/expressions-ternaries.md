# Expressions and ternaries

## No nested ternary (HARD AUDIT)

`no-nested-ternary`. Más de un nivel de `? :` → FAIL.

El FIX depende del **resultado**:

- **JSX en render** → if / early return en el componente (`gian-how-i-code` `08`).
- **Valor derivado** (string/objeto/número) → `derived-multi-branch`.

AST-SENSITIVE. Si el rewrite no es 1:1 → GAP.

## Derived multi-branch (PREFERENCE, STYLE_GIAN)

`derived-multi-branch`. Un valor con varias ramas que sería un ternario anidado se escribe como una cadena de `if` con `return`. Si se envuelve en `useMemo` (React) o `computed` (Vue) lo decide `gian-how-i-code` `23`.

```ts
const getStatusLabel = (): string => {
  if (isLoading) return 'Cargando';
  if (hasError) return 'Error';
  if (isEmpty) return 'Sin registros';

  return 'Listo';
};
```

Esto es **claridad estructural**, no requisito de performance ni de React Compiler.

No:

```ts
const statusLabel = isLoading
  ? 'Cargando'
  : hasError
    ? 'Error'
    : isEmpty
      ? 'Sin registros'
      : 'Listo';
```

Dos ramas → ternario simple (`simple-jsx-ternary` o ternario de valor). No extraer.

## Memoización

Cuándo usar o quitar `useMemo` / `computed` (incluido el ceremonial) lo decide `gian-how-i-code` `23`.
