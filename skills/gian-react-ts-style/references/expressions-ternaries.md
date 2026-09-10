# Expressions and ternaries

## No nested ternary (HARD AUDIT)

`no-nested-ternary`. Más de un nivel de `? :` → FAIL.

El FIX depende del **resultado**:

- **JSX en render** → if / early return en el componente (`gian-how-i-code` `08`). **No** envolver en `useMemo`.
- **Valor derivado** (string/objeto/número) → `derived-multi-branch`.

AST-SENSITIVE. Si el rewrite no es 1:1 → GAP.

## Derived multi-branch (PREFERENCE, STYLE_GIAN)

`derived-multi-branch`. Valor con varias ramas que produciría nested ternary:

```ts
const statusLabel = useMemo(() => {
  if (isLoading) return 'Cargando';
  if (hasError) return 'Error';
  if (isEmpty) return 'Sin registros';

  return 'Listo';
}, [hasError, isEmpty, isLoading]);
```

Esto es **claridad estructural**, no requisito de performance ni de React Compiler. Ver `gian-how-i-code` `23` (A–E).

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

## Ceremonial useMemo (prohibido aquí y en `23`)

No:

```ts
const fullName = useMemo(
  () => `${firstName} ${lastName}`,
  [firstName, lastName],
);
```

Una expresión trivial → cálculo directo. `useMemo` de performance (MRT `columns`, identidad referencial) sigue en `23`/`11`.
