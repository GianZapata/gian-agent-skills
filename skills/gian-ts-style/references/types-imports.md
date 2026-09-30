# Types and imports

## Type-only import (HARD)

`type-only-import`. Si el specifier existe solo en type position:

```ts
import type { ChipProps } from '@mui/material/Chip';
```

SAFE FIX de runtime import innecesario → `import type`.

Mixed type+value: seguir ESLint `import/order` del repo si existe; si no, `import { Foo, type Bar }` o split. Decorators/metadata runtime oculto → GAP.

Unused imports: owner ESLint (`unused-imports`). No reimplementar. WRITE no deja unused.

Import **order/groups**: owner ESLint del repo. Esta skill no inventa grupos.

## Interface for own object shapes (PREFERENCE)

`interface-object-shape`.

```ts
interface StatusChipProps {
  label: string;
  disabled?: boolean;
}
```

No (object shape propio):

```ts
type StatusChipProps = {
  label: string;
  disabled?: boolean;
};
```

No contradice `gian-how-i-code` `07`:

- conjuntos cerrados APP_OWNED → enum
- unions legítimas → `type`
- derived/library → tipo oficial / `type`
- mapped/conditional/intersection → `type`
- `z.infer` → `type`
- props/object shapes propios → `interface` default

AST-SENSITIVE. WRITE emite `interface`. AUDIT FAIL `type` de object shape propio en hunk tocado. No migrar unions ni `z.infer`.
