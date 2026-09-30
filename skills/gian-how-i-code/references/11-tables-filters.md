# 11 — Tablas y filtros

Cargar cuando: listados, MRT/CustomTable, exports, filtros.

## Alcance

- **Núcleo:** la tabla usa el wrapper compartido del repo; filtros y sorts alineados al backend, en la URL o en params tipados; defaults de disponibilidad.
- **Adaptador React:** MRT / `CustomTable`, `useMemo` de columns (`23` caso E), `Cell`, `useExport`, `useAuth().permissions`. En otro stack, la tabla y los hooks equivalentes.

## Default

- Tabla sobre wrapper compartido del proyecto (`CustomTable` o equivalente), no MRT crudo si existe wrapper
- Columnas `useMemo` + `Cell: ({ row: { original } }) => …` (estabilidad MRT; `23` caso E, no display ceremonial). Sintaxis del callback: `gian-ts-style`
- Celdas compartidas: DateTime, StatusChip, etc.
- Export: hook tipo `useExport`
- Fechas: `useDateRangeFilter` o equivalente
- Permisos: `useAuth().permissions`

## Availability defaults (catálogos)

Queries operativas: inyectar default usable (`active` / `is_active` / `status`) si el filter no lo trae.  
Queries admin CRUD: skip default.  
Un solo campo canónico por módulo.  
No aplicar a status de flujo de órdenes.

## Filtros / sorts

Alineados a AllowedFilters/Sorts del Query backend. Conteos ordenables = `withCount` forzado en BE.
