# 03 — Molde de feature (frontend)

Cargar cuando: crear/limpiar feature FE.

## Estructura canónica

```text
features/<feature>/
  components/   <Entity>Table, Form, FormContainer, Page, Show, Dialogs
  hooks/        <entity>.queries.ts, <entity>.mutations.ts, useThing.ts
  interfaces/   <entity>.interface.ts
  schemas/      <entity>.schema.ts
  services/     <entity>.service.ts
  helpers/      <entity>.helper.ts   # clases de área (DateHelper, reglas, Record de enum)
  utils/        <entity>.util.ts     # funciones pequeñas genéricas
```

Custom 1:1: `useThing.ts` (nunca `use-thing.ts`). Barrels no se renombran a `useEntitiesQuery.ts`. Naming: `04`.

Ver `23-ts-style-helpers` para estilo TS, dayjs, `cn()`, y cuándo utils vs helpers.

Query keys: store central del proyecto (p. ej. `lib/query-keys.ts`), no `*.keys.ts` sueltos por feature salvo variante documentada.

## Capas

| Pieza | Rol |
|-------|-----|
| interface | Resource JSON de respuesta (+ params de listado si aplica) |
| schema Zod | Input/Output mutación (Form Request); tipos con `z.infer` — no `interface Input` paralela |
| service | Extiende SharedService (default); static + ErrorMapper |
| queries | `*QueryProps` = `Omit<UseQueryOptions…, 'queryKey' \| 'queryFn'>` |
| mutations | `Use*MutationOptions` extends `UseMutationOptions<…>`; hook solo `mutationFn` + `...options` |
| FormContainer | Datos (queries) |
| Form | Presentational + RHF |
| Table | Wrapper tipo CustomTable |
| Page | Header + Table / rutas |

## Checklist implementar feature FE

- [ ] Carpetas y sufijos correctos; hooks custom `useThing.ts` (`04`)
- [ ] Service + ErrorMapper en mutaciones
- [ ] Query keys vía store central (`13`); invalidar:
      - listas: `queries.entities.list._def`
      - detalle: `queries.entities.detail(id).queryKey`
      - todos los detalles: `queries.entities.detail._def`
- [ ] Enums de dominio alineados al backend
- [ ] Form RHF+Zod (`z.infer` DTO; sin interface Input); i18n es+en
- [ ] 422 user-facing: mapear errores por campo con el mensaje del backend (`05`/`10`/`14`); no genérico
- [ ] Queries `*QueryProps` + mutations solo `mutationFn` + options (`13`)
- [ ] Diálogos §09: `{isOpen && user && (`; props `isOpen` + tipo (no `open`/`entity`/`data`); caller pasa onSuccess/onError
- [ ] Display §08: Record de enum en el helper con `i18n.t()`; if-chain ad-hoc con `t()`; sin `*.display.config.ts` ni `TFunction` inyectado
- [ ] Estilo TS / dayjs / utils|helpers §23
- [ ] Sin `any` en contratos

Ver templates en `assets/frontend/`.
