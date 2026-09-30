# 12 — State management

Cargar cuando: estado cliente, drawers store, filters locales.

## Alcance

- **Núcleo:** el server state no se duplica en un store de UI; el estado del form no se hoistea al padre; lo derivado se calcula, no se copia.
- **Adaptador React:** TanStack Query, RHF, `useState`, Zustand. En otro stack, el cliente de datos y el primitivo de estado de ese stack.

## Separación de responsabilidades

| Tipo | Adaptador React | Equivalente |
|------|-----------------|-------------|
| Server state (remoto) | TanStack React Query | El cliente de datos del stack (`13`) |
| Estado de formulario | React Hook Form | El form del stack (`10`) |
| UI local (isOpen, tab, selección de fila) | `useState` / URL params | El primitivo del framework (`ref` en Vue, signal o campo en Angular) / URL params |
| Store de overlays (variante) | Zustand / store tipado del repo | Pinia o `provide`/`inject` si ya existen. No introducir el otro |
| Estado derivado | Calcular durante render / `select` de Query; `useMemo` según `23` A–E | `computed` según `23` A–E (`25`). No copiar a otro store |

## Default

- No `useEffect` para fetch de API
- Forms: RHF (no estado paralelo del mismo formulario)

## Drawers / overlays

- **Default:** `useState` `isOpen` + entidad por tipo en el padre de la tabla (`09`)
- **Variante:** store de drawers — ver `09` y `20`

## Prohibido

- Duplicar server state en Zustand/Context/Redux/Pinia “porque sí”
- Hoistear estado de form de diálogo al padre
