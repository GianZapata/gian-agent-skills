# 07 — Tipos, enums y statuses

Cargar cuando: estados, tipos cerrados, exhaustividad de mappings, state machines, ownership de contratos TS, shadow types de librería.

## Ownership (antes de declarar el contrato)

Antes de crear un `type`, union, enum o mapping para un conjunto de valores, identificar **quién posee** el concepto.

| Gate | Criterio | Representación |
|---|---|---|
| `APP_OWNED` | Conjunto cerrado, nombrado y controlado por la app (dominio persistido **o** UI/feature con identidad clara) | **string enum** por default |
| `LIBRARY_OWNED` | El concepto ya lo define MUI, TanStack, RHF, Zod u otra dep, y la semántica es la misma | Tipo oficial / derivado (`ComponentProps['prop']`). Sin union, enum ni alias shadow |
| `EXTERNAL_GENERATED` | OpenAPI, schemas generados, APIs externas, legacy no normalizado | Respetar el contrato; normalizar en la frontera si aplica. No imponer enum por estética |
| `UNION LEGÍTIMA` | Discriminated unions con shapes distintas; unions estructurales; el literal es narrowing estructural, no un catálogo nominal | Conservar esa representación |

Criterio:

```text
¿Es un conjunto cerrado propio y nombrado?
→ enum por default

¿Ya pertenece a una librería?
→ tipo oficial de la librería

¿Es discriminated / structural / external?
→ conservar la representación apropiada
```

No convertir mecánicamente toda union a enum.

## APP_OWNED

Incluye statuses, types, modes, roles, scopes, categories, actions, **y** estados/modos cerrados de componente o feature (`normal | loading | empty | error`, `default | selected | uploading | success | error | disabled`).

```ts
export enum DesignSystemTableMode {
  Normal = 'normal',
  Loading = 'loading',
  Empty = 'empty',
  Error = 'error',
}

export enum UploadDemoState {
  Default = 'default',
  Selected = 'selected',
  Uploading = 'uploading',
  Success = 'success',
  Error = 'error',
  Disabled = 'disabled',
}
```

`null` / `undefined` que representan **ausencia** no son miembros del enum:

```ts
export enum DialogKind {
  Normal = 'normal',
  Form = 'form',
  Confirm = 'confirm',
  Destructive = 'destructive',
}

useState<DialogKind | null>(null);
```

## LIBRARY_OWNED

Si solo alimenta una prop de librería, **no recrear el contrato**.

Preferir (adaptador React/MUI; en otro stack, el tipo que exporta su librería):

```ts
ChipProps['color']
ButtonProps['color']
ButtonProps['variant']
AlertProps['severity']
AlertProps['variant']
```

`NonNullable<…>` cuando el valor es requerido y la prop de la lib es opcional.

Incorrecto (shadow; desaparece entero; **no** sustituir por `enum StatusTone`):

```ts
type StatusTone = 'success' | 'warning' | 'error' | 'info' | 'neutral';
```

si únicamente termina en `<Chip color={…}>`.

Un wrapper puede existir si agrega semántica real (p. ej. `StatusChip` = pill de estado vs Chip de filtro). Reutiliza el contrato base:

```ts
interface StatusChipProps {
  label: ChipProps['label'];
  color?: ChipProps['color'];
  disabled?: ChipProps['disabled'];
}
```

Estilos de identidad del wrapper (p. ej. `borderRadius: 999`) sí. No `StatusTone`, `TONE_SX`, ni una prop `tone` con union propia que duplique `Chip.color`. Estilos globales → theme / componente fuente.

## Regla canónica (TypeScript)

Usar **`string enum`** para conjuntos cerrados `APP_OWNED`: estados, tipos, modos, scopes, roles, categorías, acciones.

```ts
export enum OrderStatus {
  Pending = 'pending',
  InProcess = 'in_process',
  Completed = 'completed',
  Cancelled = 'cancelled',
}
```

Mappings UI/comportamiento con una propiedad pública `static readonly Record<Enum, Value>` obligatoria (exhaustividad y una sola construcción). Labels/colores fuera del enum de dominio.

## Membresía (HARD) — TS, PHP y Python

Si el **mismo** identificador se compara con **2 o más** miembros de un conjunto cerrado (`APP_OWNED`: status, type, mode, similares; constantes de SM), unidos por `||` (`===`) o `&&` (`!==`): membresía, no cadena.

TS:

```ts
[OrderStatus.Pending, OrderStatus.Cancelled].includes(status)
```

```ts
![OrderStatus.Pending, OrderStatus.Cancelled].includes(status)
```

No:

```ts
status === OrderStatus.Pending || status === OrderStatus.Cancelled
```

PHP (strict):

```php
in_array($status, [
    OrderStatusStateMachine::PENDING,
    OrderStatusStateMachine::CANCELLED,
], true)
```

Python:

```python
if status in (OrderStatus.PENDING, OrderStatus.CANCELLED):
```

Una sola comparación sigue `===` (`==` en Python). Array inline; extraer helper solo si el mismo set se repite (`22`).

KEEP / no FAIL: un `===`; identificadores distintos; `LIBRARY_OWNED` / valores abiertos; `switch` exhaustivo; `Rule::in(SM::values())`.

AUDIT: FAIL. WRITE/FIX: SAFE en el hunk tocado; no barrer el repo.

## Mappings exhaustivos (FE)

Metadata derivada de un enum propio → **una** fuente en `<entity>.helper.ts` (`08`). No `*-display.config.ts`. No duplicar el Record inline en cada tabla.

```ts
import i18n from '@/lib/i18n';

interface StatusMeta {
  label: string;
  tone: ChipTone;
}

export class OrderHelper {
  static readonly statusMeta: Record<OrderStatus, StatusMeta> = {
    [OrderStatus.Pending]: {
      get label() {
        return i18n.t('orders:status.pending');
      },
      tone: 'warning',
    },
    // … todos los miembros
  };
}
```

`ChipTone` es el tipo `LIBRARY_OWNED` del chip del stack (§LIBRARY_OWNED), no una union propia. Adaptador React/MUI: el campo es `color: NonNullable<ChipProps['color']>`, para esparcir el meta en `<Chip>`.

La propiedad es pública por default: no usar `private`/`protected` ni envolverla en un método. `Record<OrderStatus, StatusMeta>` hace que agregar un miembro al enum rompa el chequeo hasta completar la metadata. Unir en este mapa todos los campos relacionados (label, tone, icon, etc.).

El getter de cada `label` ejecuta `i18n.t()` al leer y evita congelar el locale al inicializar la clase (`15`). No inyectar `TFunction`, no usar `labelKey` diferido y no asignar `label: i18n.t(...)` directamente durante la inicialización.

Consumo de metadata:

```ts
const meta = OrderHelper.getStatusMeta(status);
```

Adaptador React/MUI:

```tsx
<Chip {...OrderHelper.getStatusMeta(status)} />
```

Cuando el valor ya está garantizado como `OrderStatus` o se necesita iterar el catálogo, se permite el acceso directo:

```ts
const meta = OrderHelper.statusMeta[status];
```

El resolver canónico para ausencia legítima vive en el mismo helper:

```ts
private static readonly unknownMeta: StatusMeta = {
  tone: 'default',
  get label() {
    return i18n.t('common:unknown');
  },
};

private static getMeta<T extends PropertyKey>(
  meta: Record<T, StatusMeta>,
  value: T | null | undefined
): StatusMeta {
  if (value == null) {
    return this.unknownMeta;
  }

  return meta[value];
}

static getStatusMeta(status: OrderStatus | null | undefined): StatusMeta {
  return this.getMeta(this.statusMeta, status);
}
```

`getXMeta()` es la API preferida en componentes que reciben valores opcionales. Para `EXTERNAL_GENERATED` o legacy no normalizado, validar/normalizar primero o definir el resolver explícito de esa frontera; no debilitar el Record canónico.

Prohibido: métodos que reconstruyen el `Record`; `Record<string, …>` cuando las keys son un enum/conjunto cerrado conocido; índices abiertos; `string` o casts para ampliar/ocultar el contrato; `?? unknownMeta` en cada consumidor; traducciones congeladas al inicializar la clase; partir metadata fuertemente relacionada en `STATUS_COLOR` + `STATUS_LABEL` / `humanStatusesKeys` + `statusChipColors` + `statusIcons` paralelos.

Los campos de meta reutilizan tipos `LIBRARY_OWNED` cuando corresponda (el tipo del chip del stack; en MUI `ChipProps['color']`), no una union de tonos.

## Runtime arrays `LIBRARY_OWNED`

Arrays para `.map()` / render **no** son la fuente del contrato. Validarlos contra el tipo de la lib; no derivar `type ButtonVariant = typeof BUTTON_VARIANTS[number]`.

```ts
const BUTTON_VARIANTS = [
  'contained',
  'outlined',
  'text',
] satisfies readonly NonNullable<ButtonProps['variant']>[];
```

Igual para colors/variants de Button, Chip, Alert, y props equivalentes.

## Valores cerrados en PHP

### Default — backed Enum

Usar backed Enum cuando:

- el valor se castea desde Eloquent;
- se usa en varias capas fuera de una State Machine string-based;
- necesita métodos/`from()`/`tryFrom()`/`cases()`;
- la librería consumidora soporta enums correctamente.

```php
enum OrderType: string
{
    case Standard = 'standard';
    case Express = 'express';
}
```

### Excepción canónica — State Machine basada en strings

Con `asantibanez/laravel-eloquent-state-machines` (API de strings: `transitions()`, `defaultState()`, `transitionTo`, `is`, `canBe`):

- la **State Machine es la fuente única** de los valores de estado;
- declarar estados como `public const` UPPER_SNAKE en la SM;
- usar constantes en transitions, defaultState, hooks, validators, factories, Actions y tests;
- exponer `values()` para `Rule::in` / enumeración;
- **no** crear un backed Enum paralelo con los mismos valores salvo necesidad concreta, testeada y documentada;
- no repetir strings literales fuera de la SM.

```php
final class OrderStatusStateMachine extends StateMachine
{
    public const PENDING = 'pending';
    public const APPROVED = 'approved';
    public const CANCELLED = 'cancelled';

    public static function values(): array
    {
        return [self::PENDING, self::APPROVED, self::CANCELLED];
    }

    public function transitions(): array
    {
        return [
            self::PENDING => [self::APPROVED, self::CANCELLED],
            self::APPROVED => [self::CANCELLED],
        ];
    }

    public function defaultState(): ?string
    {
        return self::PENDING;
    }
}
```

### Regla de no duplicación

No mantener a la vez: constantes SM + backed Enum + strings literales para los **mismos** estados, salvo integración explícita.

## Excepciones (no forzar enum/const)

- Texto libre, IDs dinámicos, keys i18n abiertas
- `EXTERNAL_GENERATED` / legacy no normalizado
- `UNION LEGÍTIMA` (discriminated / estructural)
- Tipos generados desde OpenAPI/schema

`as const` + tipo derivado: solo interop JS o valor no compartido entre capas. **No es el default** TS para conjuntos `APP_OWNED`. En arrays runtime `LIBRARY_OWNED`, `satisfies` el tipo de la lib (no `as const` como fuente de un tipo propio).

## Hallazgos típicos

| Observado | Tipo |
|-----------|------|
| `type Status = 'a' \| 'b'` `APP_OWNED` | Mejora / Mala práctica |
| Shadow `StatusTone` (union propia) alimentando `Chip.color` | Mejora / Mala práctica |
| `enum StatusTone` sustituyendo el shadow | Mala práctica (el shadow debe desaparecer) |
| `Record<string, …>` con keys de enum conocido | Medio |
| Método que reconstruye el `Record` / propiedad no `static readonly` | Medio |
| `label: i18n.t(...)` inicializado una vez (locale congelado) | Medio |
| Lookup normal con `?.` / `??` para enum cerrado | Medio |
| `STATUS_COLOR` + `STATUS_LABEL` / `labelKey` paralelos | Mejora |
| `*.display.config.ts` o `getXConfig(t: TFunction)` | Medio |
| Array MUI sin `satisfies` el tipo de la lib | Baja / Mejora |
| `status: string` abierto para SM | Alto |
| Enum PHP + constantes SM duplicadas | Mala práctica |
| Mapping incompleto sin Record | Medio |
| Strings literales fuera de la SM | Medio |
| `status === A \|\| status === B` (conjunto cerrado, 2+) | Medio |
| Discriminated union convertida a enum | Mala práctica (sobre-aplicación) |
