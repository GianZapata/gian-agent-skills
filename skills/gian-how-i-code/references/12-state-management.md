# 12 — State management

Cargar cuando: estado cliente, drawers store, filters locales.

## Separación de responsabilidades

| Tipo | Dónde vive |
|------|------------|
| Server state (remoto) | TanStack React Query |
| Estado de formulario | React Hook Form |
| UI local (isOpen, tab, selección de fila) | `useState` / URL params |
| Store de overlays (variante) | Zustand / store tipado del repo |
| Estado derivado | Calcular durante render / `select` de Query; `useMemo` según `23` A–E; no copiar a otro store |

## Default

- No `useEffect` para fetch de API
- Forms: RHF (no estado paralelo del mismo formulario)

## Drawers / overlays

- **Default:** `useState` `isOpen` + entidad por tipo en el padre de la tabla (`09`)
- **Variante:** store de drawers — ver `09` y `20`

## Prohibido

- Duplicar server state en Zustand/Context/Redux “porque sí”
- Hoistear estado de form de diálogo al padre
