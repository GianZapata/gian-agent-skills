# Types and imports

## Type-only import (HARD)

`type-only-import`. Todos los specifiers de la sentencia se usan solo en posición de tipo → `import type { … }`, también si venían como `{ type A, type B }`.

```ts
import type { ChipProps } from '@mui/material/Chip';
import type { Invoice, InvoiceStatus } from '../interfaces/invoice.interface';
```

Mixto (valor + tipo) → una sola sentencia con `type` inline. Sin split en dos sentencias.

```ts
import { Chip, type ChipProps } from '@mui/material';
```

Re-export de tipos → `export type { … }`.

```ts
export type { Invoice, InvoiceStatus } from './invoice.interface';
```

No:

```ts
import { ChipProps } from '@mui/material/Chip';
import { type Invoice, type InvoiceStatus } from '../interfaces/invoice.interface';
import { Chip } from '@mui/material';
import type { ChipProps } from '@mui/material';
export { Invoice } from './invoice.interface';
```

SAFE FIX. Decorators o metadata de runtime (`emitDecoratorMetadata`) → `GAP type-only-import archivo:línea — metadata de runtime`.

Unused imports: owner ESLint (`unused-imports`). No reimplementar. WRITE no deja imports sin uso.

Import **order/groups**: owner ESLint del repo. Esta skill no inventa grupos.

## Interface for own object shapes (HARD)

`interface-object-shape`. `type X = { … }` cuyo lado derecho es un object literal → `interface X { … }`.

```ts
interface StatusChipProps {
  label: string;
  disabled?: boolean;
}
```

No:

```ts
type StatusChipProps = {
  label: string;
  disabled?: boolean;
};
```

Se conserva `type`, no FAIL, cuando el lado derecho es (no contradice `gian-how-i-code` `07`):

- union (`|`) o intersection (`&`)
- mapped o conditional type
- `z.infer<…>` u otro tipo derivado de librería
- alias de otro tipo (`type InvoiceId = string`)

Conjuntos cerrados APP_OWNED → enum (`gian-how-i-code` `07`).

WRITE emite `interface`. FIX/AUDIT: aplicar en el alcance. Gate: el typecheck del repo (`gian-how-i-code` `17`). Si falla por el cambio (por ejemplo, un index signature implícito que la interface no da), revertir y reportar `GAP interface-object-shape archivo:línea — typecheck falla`.

## Named interface (HARD)

`named-interface`. Un tipo de objeto inline con 2+ campos se nombra con `interface`, también dentro de un genérico o de otra interface.

```ts
interface ChartTick {
  top: string;
  label: string;
}

interface IncomeChartProps {
  ticks: ChartTick[];
}
```

No:

```ts
ticks: Array<{ top: string; label: string }>;
const ARREARS_EMPTY: Record<ArrearsTone, { heading: string; detail: string }> = { … };
```

Un campo suelto (`isValidElement<{ className?: string }>`) puede quedarse inline.

## Library and enum types (HARD)

`library-shadow-type`. Una unión de colores, variants, sizes o severities de MUI se escribe con el tipo del componente que la recibe: `NonNullable<ButtonProps['color']>`, `ChipProps['color']`, `AlertProps['severity']`.

`enum-ownership`. Una unión de strings propia de la app es un string enum de la feature. Si la feature ya tiene un enum con esos valores, se usa ese (`gian-how-i-code` `07` §Checklist al declarar).

WRITE los aplica en el alcance. `assets/self-check.mjs` los marca FAIL; generado, externo o discriminated → GAP en el cierre.
