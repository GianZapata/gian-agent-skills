# 08 — Convenciones de display

Cargar cuando: labels, colores, textos por estado, copy visible, mappings de chip/filtro.

## Alcance

- **Núcleo:** metadata del enum en el entity helper; ad-hoc inline; sin `*.display.config.ts`, sin `TFunction`, sin `labelKey`.
- **Adaptador React:** `t()` de `useTranslation`, `useMemo`, JSX y `Chip`/`ChipProps`. En otro stack se lee la misma metadata con el componente de estado de ese stack.

## Gate

| Situación | Dónde | i18n |
|-----------|--------|------|
| Metadata exhaustiva de un enum `APP_OWNED` (tabla + filtros + drawer) | Propiedad pública `static readonly Record<Enum, Meta>` y `getXMeta(Enum | null | undefined)` en `<entity>.helper.ts` (`07`) | Getter de `label` y `unknownMeta.label` con `i18n.t()` (`15`) |
| Display ad-hoc de **un** componente (stock vs production, loading vs error) | Cadena de `if` + early return **inline** | `t()` de la vista (`15`) |
| Schema / util / `.ts` no React | No mapping de UI | `i18n.t()` (`10`/`15`) |

Nested ternary: `gian-react-ts-style` (`no-nested-ternary`). Valor multi-rama **ad-hoc** en componente: `useMemo`+if (`23` caso C). JSX multi-rama: if/early return aquí, sin `useMemo` (`23` D).

## Enum metadata — entity helper (HARD)

El `<entity>.helper.ts` **es** el hogar del `Record`. Exponer un solo mapa público `static readonly` (color / icon / label juntos), construido una vez. Cada `label` usa un getter que llama `i18n.t()` al leer; no método que reconstruya el mapa ni traducción evaluada durante la inicialización de la clase.

```ts
import i18n from '@/lib/i18n';

export class WarehouseHelper {
  static readonly typeMeta: Record<
    WarehouseType,
    { tone: ChipTone; label: string }
  > = {
    [WarehouseType.Main]: {
      tone: 'primary',
      get label() {
        return i18n.t('warehouses:type.main');
      },
    },
  };
}
```

`ChipTone` es el tipo `LIBRARY_OWNED` del chip del stack, no una union propia (`07`). Adaptador React/MUI: el campo es `color: NonNullable<ChipProps['color']>` (o el `ChipColor` del theme), para el spread en `<Chip>`.

Consumo preferido en componentes: `WarehouseHelper.getTypeMeta(type)`; en React/MUI, `<Chip {...WarehouseHelper.getTypeMeta(type)} />`. El acceso directo `WarehouseHelper.typeMeta[type]` queda para un enum garantizado o para iterar el catálogo. El resolver acepta solo `WarehouseType | null | undefined`, devuelve `unknownMeta` únicamente para ausencia legítima y no usa `string`, casts ni fallback por consumidor. Valores externos y legacy se validan o normalizan en la frontera.

## Display ad-hoc — inline (HARD)

```tsx
if (isStockOnly) return t('…');
if (isProductionOnly) return t('…');
return t('…');
```

Se acepta duplicar if-chains **ad-hoc** entre componentes. No extraer eso a helper ni a `display.config`.

## Prohibido

- `*.display.config.ts` / `*-display.ts` / `FooDisplayHelper` / clase *solo* de UI
- Método `typeMeta()` que crea un nuevo `Record` por llamada; `getTypeMeta()` sí es canónico cuando resuelve `null | undefined` mediante el mapa estático
- `label: i18n.t('…')` evaluado al inicializar la clase; debe ser getter
- Lookup normal `Helper.typeMeta?.[type]` o `Helper.typeMeta[type] ?? fallback` para enum cerrado; usar `getTypeMeta(type)` cuando el valor sea opcional
- Resolver que acepta `string`, usa casts o devuelve `unknownMeta` ante una key desconocida para ocultar drift del contrato
- Inyectar `t: TFunction` (`getXConfig(t)`, `createXSchema(t)`, `formatX(display, t)`)
- `labelKey` + `t(config.labelKey)` en render; `humanStatusesKeys` + `statusChipColors` + `statusIcons` en paralelo (`07`)
- `Helper.getPrimaryLabel` / `ColorHelper.statusColor` como helper de display suelto
- Ternario anidado (>1 nivel) — forma: `gian-react-ts-style`
- Title Case forzado; siglas internas del dominio en copy visible, salvo que el usuario final las conozca y formen parte del lenguaje oficial del producto

Audits locales del repo **no** ganan a esta reference. No “relocate to feature-level display configs”.

## helpers/ vs utils/

| Carpeta | Uso | Forma | Sufijo |
|---------|-----|-------|--------|
| `helpers/` | Área cohesiva: fechas, números, usuario, formatos humanos, reglas de dominio, **Record de meta de enum** | `export class XxxHelper` | `.helper.ts` |
| `utils/` | Funciones **pequeñas** y genéricas | `export const …` | `.util.ts` |

Fechas de negocio → **dayjs** vía `DateHelper` (u helper de área) — detalle en `23`.

No hay carpeta ni archivo extra para labels/colores. El Record vive en el entity helper, no al lado del Table.

## Migración oportunista

Al tocar un componente o helper: si el mapping de enum está en `*.display.config.ts`, recibe `TFunction` o se reconstruye mediante un método, moverlo a la propiedad pública `static readonly` del entity helper con getters de label. Si es if-chain ad-hoc, dejarlo inline con `t()`. No añadir `useMemo` ceremonial (`23` A). Caso C (valor multi-rama ad-hoc) sí.
