# 03 — Molde de feature (frontend)

Cargar cuando: crear/limpiar feature FE.

## Alcance

- **Núcleo:** carpetas y sufijos, las capas interface / schema / service / helper y el checklist núcleo. Vale en cualquier stack. Vue remite a `25`.
- **Adaptador React:** RHF, `UseQueryOptions`, `UseMutationOptions`, query keys y el montaje `{isOpen && user && (`. En otro stack, el equivalente (`01`).

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

Vue: `composables/` reemplaza `hooks/`. SFC, `Props` / `Emits` y lo que no se copia de un repo de referencia: `25`.

Ver `23-ts-style-helpers` para estilo TS, dayjs, `cn()`, y cuándo utils vs helpers.

Query keys (adaptador React): store central del proyecto (p. ej. `lib/query-keys.ts`), no `*.keys.ts` sueltos por feature salvo variante documentada.

## Capas

| Pieza | Rol |
|-------|-----|
| interface | Resource JSON de respuesta (+ params de listado si aplica) |
| schema | Input/Output mutación (Form Request / body HTTP), nombrado; en TS es Zod y el tipo sale de `z.infer` — no `interface Input` paralela; IDs de ruta fuera (`13`) |
| service | Extiende SharedService (default); static + ErrorMapper |
| queries (adaptador React) | `*QueryProps` = `Omit<UseQueryOptions…, 'queryKey' \| 'queryFn'>` |
| mutations (adaptador React) | `Use*MutationOptions` extends `UseMutationOptions<…>`; hook solo `mutationFn` + `...options`; ruta ≠ body (`13`) |
| FormContainer | Datos (queries) |
| Form | Presentational + el form del stack (RHF en React) |
| Table | Wrapper tipo CustomTable |
| Page | Header + Table / rutas |

## Checklist implementar feature FE

### Núcleo (cualquier stack)

- [ ] Carpetas y sufijos correctos; archivos `useThing.ts`, o `composables/` en Vue (`04`, `25`)
- [ ] Service + mapper de errores en mutaciones (`14`)
- [ ] DTO desde un schema nombrado, sin interface Input paralela; ruta ≠ body (`13`)
- [ ] 422 user-facing: errores por campo con el mensaje del backend (`05`/`10`/`14`); no genérico
- [ ] Overlay dueño de su mutación; props `isOpen` + el tipo (no `open`/`entity`/`data`) (`09`)
- [ ] Display en el helper de la entidad (`08`): propiedad pública `static readonly Record<Enum, Meta>`; getters de label con `i18n.t()`; `getXMeta(Enum | null | undefined)` preferido cuando el consumidor recibe ausencia; acceso directo solo para enum garantizado/iteración; sin `string`, casts ni fallbacks silenciosos; if-chain ad-hoc con `t()`; sin `*.display.config.ts` ni `TFunction` inyectado
- [ ] La UI no arma FormData; multipart vía `FormDataHelper` en el service (`23`)
- [ ] Enums de dominio alineados al backend (`07`); i18n es+en (`15`)
- [ ] Estilo TS / dayjs / utils|helpers (`23`)
- [ ] Sin `any` en contratos

### Adaptador React

- [ ] Form RHF + Zod (`z.infer` como DTO)
- [ ] Queries `*QueryProps` + mutations `Use*MutationOptions` con solo `mutationFn` + options (`13`)
- [ ] `useMutation<TData, CustomError, TVariables>`; TVariables DTO o envelope `*Variables` (`13` §4)
- [ ] Montaje `{isOpen && user && (`; el caller pasa onSuccess/onError (`09`)
- [ ] Query keys vía store central (`13`); invalidar:
      - listas: `queries.entities.list._def`
      - detalle: `queries.entities.detail(id).queryKey`
      - todos los detalles: `queries.entities.detail._def`

Ver templates en `assets/frontend/`.
