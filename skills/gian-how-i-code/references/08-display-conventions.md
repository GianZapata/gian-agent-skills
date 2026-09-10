# 08 — Convenciones de display

Cargar cuando: labels, colores, textos por estado, copy visible, mappings de chip/filtro.

## Gate

| Situación | Dónde | i18n |
|-----------|--------|------|
| Metadata exhaustiva de un enum `APP_OWNED` (tabla + filtros + drawer) | `Record<Enum, Meta>` en `<entity>.helper.ts` (`07`) | `i18n.t()` dentro del helper (`15`) |
| Display ad-hoc de **un** componente (stock vs production, loading vs error) | Cadena de `if` + early return **inline** | `t()` de `useTranslation` |
| Schema / util / `.ts` no React | No mapping de UI | `i18n.t()` (`10`/`15`) |

Nested ternary: `gian-react-ts-style` (`no-nested-ternary`). Valor multi-rama **ad-hoc** en componente: `useMemo`+if (`23` caso C). JSX multi-rama: if/early return aquí, sin `useMemo` (`23` D).

## Enum metadata — entity helper (HARD)

El `<entity>.helper.ts` **es** el hogar del `Record`. Un solo Record (color / icon / label juntos). Labels **ya resueltos** al leer: método o getter que **llama** `i18n.t` — no `const` de módulo que congela el locale al import.

```ts
import i18n from '@/lib/i18n';

export class WarehouseHelper {
  static typeConfig(): Record<WarehouseType, { color: ChipColor; label: string }> {
    return {
      [WarehouseType.Main]: {
        color: 'primary',
        label: i18n.t('warehouses:type.main'),
      },
    };
  }
}
```

Chip color: tipo `LIBRARY_OWNED` (`ChipProps['color']` / `ChipColor` del theme) — `07`.

## Display ad-hoc — inline (HARD)

```tsx
if (isStockOnly) return t('…');
if (isProductionOnly) return t('…');
return t('…');
```

Se acepta duplicar if-chains **ad-hoc** entre componentes. No extraer eso a helper ni a `display.config`.

## Prohibido

- `*.display.config.ts` / `*-display.ts` / `FooDisplayHelper` / clase *solo* de UI
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

Al tocar un componente o helper: si el mapping de enum está en `*.display.config.ts` o recibe `TFunction`, moverlo al entity helper con `i18n.t()`. Si es if-chain ad-hoc, dejarlo inline con `t()`. No añadir `useMemo` ceremonial (`23` A). Caso C (valor multi-rama ad-hoc) sí.
