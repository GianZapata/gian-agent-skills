# Changelog

## 1.2.11 — 2026-09-10

- Resources (`06`): `new XResource($this->whenLoaded('rel'))` y `::collection($this->whenLoaded('rels'))`. Prohibido callback `whenLoaded(..., fn() => new X($this->rel))` salvo lógica extra.
- `05` apunta a `06`. Evals: `impl-whenloaded-resource-ctor`, `audit-whenloaded-callback`.

## 1.2.10 — 2026-09-09

- Membresía HARD (`07`): 2+ `===`/`!==` del mismo identificador contra un conjunto cerrado → `.includes()` (TS) / `in_array(..., true)` (PHP). Una sola comparación sigue `===`.
- `05` SM apunta a `07`. Evals: `impl-status-membership-includes`, `impl-php-status-in-array`, `audit-status-or-chain`.

## 1.2.9 — 2026-09-08

- Diálogos (`09`): montaje canónico `{isOpen && user && (`; props `isOpen` + entidad por tipo (`user={user}`). Prohibido `open`, `entity=`, `data=`.
- Varios overlays: un boolean por diálogo; el JSX sigue el mismo molde. `03` checklist alineado.
- Evals: `impl-dialog-mount-typed-props`, `audit-dialog-entity-open`.

## 1.2.8 — 2026-09-08

- Display / i18n HARD (`08`/`15`/`07`/`10`): Record de enum en `<entity>.helper.ts` con `i18n.t()` al leer; if-chain ad-hoc en el componente con `t()`.
- Prohibido `*.display.config.ts`, inyectar `TFunction` (`getXConfig(t)`, `createXSchema(t)`), `labelKey` diferido, mappings de color/icon/key en paralelo.
- Audits locales del repo no ganan al molde. `03`/`23`: el entity helper puede exponer el Record; no hay archivo display extra.
- Evals: `impl-reject-display-config-t-inject`, `impl-enum-meta-in-helper`, `audit-display-config-tfunction`, `audit-labelkey-indirection`.

## 1.2.7 — 2026-08-25

- HARD naming de hooks custom (`04`): archivo, directorio 1:1, export e import camelCase `useDashboard`; nunca `use-dashboard` / `use_dashboard`. Implementar: rename en alcance. Auditar: Hallazgo.
- No aplica a barrels `<entity>.queries.ts` / `<entity>.mutations.ts`.
- Evals: `impl-hook-file-camelcase`, `impl-hook-kebab-rename`, `impl-keep-query-barrel`, `audit-hook-kebab-file`.

## 1.2.6 — 2026-08-14

- HARD User-Facing Validation Contracts (`05` autoridad; `10`/`14` consumen 422): no terminar un FormRequest solo con `rules()`.
- Cobertura semántica regla→mensaje (no `count(rules) === count(messages)`). `attributes()` solo si `:attribute` o el copy lo necesita.
- UI: mapear 422 por campo según el patrón del repo; preservar el mensaje human-facing del backend; no sustituir por genérico ni crear ErrorMapper nuevo.
- Evals: `impl-formrequest-user-facing`, `impl-422-show-backend-messages`, `audit-formrequest-rules-only`.

## 1.2.5 — 2026-08-14

- `04`: Tailwind-first no autoriza `bg-[#…]` / `text-[#…]` si el token vive en `theme.palette`; no inventar nombres de `slotProps`.
- Evals negativos: conservar `sx` theme-aware, `useTheme()` en lógica JS, y `slotProps.className` frente a `'& .Mui…'` de layout.
- `04`/`23`: `cn()` depende de la composición real de clases; estado/props runtime con clases variables usa `cn()`, mientras un `className` idéntico permanece estático aunque MUI cambie `variant`/`color`.
- `04`: gate de tokens verificados; si el bridge MUI→Tailwind ya expone una equivalencia real, Tailwind-first también aplica a colores/tokens. `sx(theme)` queda como hatch cuando no existe equivalencia limpia o la API MUI lo requiere.
- `18`: auditorías focalizadas distinguen FAIL/GAP de “Fuera de alcance” y no convierten deuda lateral en PROP automáticamente.
- Evals positivos/negativos contra sobre-aplicación y sub-aplicación de `cn()`, bridges Tailwind, `sx(theme)`, `useTheme()` y scope de auditoría.

## 1.2.4 — 2026-08-14

- Styling FE (`04` HARD `no-local-style-constants`): Tailwind-first; `className` estático sin `cn()`; `cn()` solo composición; `sx` escape hatch; `sx={(theme) => theme.palette.*}` en vez de `useTheme()` ceremonial; `slotProps.className` antes de `'& .Mui…'`.
- `23`: mecánica de `cn()` alineada; concatenación, `*_SX` locales, `sx` de layout y `useTheme()` huérfano = Media. Clase estática sin `cn()` permitida.
- No vive en `gian-react-ts-style`.

## 1.2.3 — 2026-08-13

- Formato visual TS/TSX sale de esta skill: `gian-react-ts-style` (WRITE/FIX corrigen hunk; AUDIT no edita).
- `23` ya no gobierna arrows/expresión corta; conserva `cn()`, dayjs, utils vs helpers y memoización **A–E** (ceremonial A prohibido; multi-rama C STYLE_GIAN; MRT E).
- `08`/`04`/`01`/`00`: nested ternary y comments apuntan a la style skill.

## 1.2.2 — 2026-08-13

- Ownership de contratos TS (`07`): `APP_OWNED` \| `LIBRARY_OWNED` \| `EXTERNAL_GENERATED` \| `UNION LEGÍTIMA` antes de enum/union/mapping. No duplica la regla de string enum; la acota.
- `LIBRARY_OWNED`: tipo oficial (`ChipProps['color']`, etc.); el shadow (`StatusTone`/`tone`) desaparece — no se reemplaza por enum shadow.
- `APP_OWNED` incluye modos/estados de UI nombrados; `null` de ausencia no es miembro del enum.
- Mappings: un `Record<Enum, Meta>`; `satisfies` en arrays runtime de la lib.
- Memoización React no ceremonial (`23`); `08` deja de exigir `useMemo` en todo display.

## 1.2.1 — 2026-08-13

- Queries SQL/Query Builder: alias de tabla `t1`/`t2` en el raíz; `st1`/`sst1` según profundidad de subquery. No `users u` / `orders o`.

## 1.2.0 — 2026-08-05

- Alcance **Auditar repositorio completo** (`24-full-repo-audit`): inventario, coverage ledger, categorías sin hallazgos con evidencia, gate de cobertura, disposición; prohibido muestreo como cierre.
- `18`/`21`/`SKILL` distinguen Auditar feature vs repo completo; Fase 0 ya no usa “≥2 features” como cierre de full-repo.
- PROP (`19`): costos/riesgos reales; no “garantiza CI” sin evidencia de lint + pipeline.

## 1.1.5 — 2026-08-05

- Auditoría: duplicación vs helper/util de área existente (p. ej. función local ≈ `DateHelper`) es Hallazgo Media; display duplicable (`08`) y “no extraer por una sola dup accidental” (`22`) quedan matizados.

## 1.1.4 — 2026-08-05

- Inventario FE en Fase 0 (`02`): dayjs módulo, apiFetcher, ErrorMapper/CustomError, QueryClient, query-keys; tooling Serena/ast-grep opcional.
- Contratos explícitos en `14` (HTTP/errores), `13` (QueryClient defaults), `23` (import dayjs del módulo del proyecto); canónicos en `19`; variantes profile/realtime en `20`.

## 1.1.3 — 2026-08-05

- Query/Mutation: `*QueryProps` y `Use*MutationOptions` con genéricos; hook de mutation solo `mutationFn` + `...options` (toast/invalidate en el caller).
- Input/DTO de form y mutación vía Zod `z.infer`; sin `interface Input` paralela.

## 1.1.2 — 2026-08-05

- Reference `23-ts-style-helpers`: arrows, expresión corta, `cn()`, renombres, dayjs como regla FE, utils pequeños vs helpers clase de área.
- Ajuste de `08`/`22`/`19`/`04` y severidades de auditoría alineadas.

## 1.1.1 — 2026-08-05

- Auditoría: un solo archivo `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` (hallazgos, propuestas, lotes; checklist/registro si aplicar). Sin carpetas multi-archivo por feature.

## 1.1 — 2026-08-05 (ready)

- Cierre minor fixes: invalidación alineada (`list._def` / `detail(id).queryKey` / `detail._def`).
- AbortSignal punta a punta en service + docs; `EntityId` tipado (default `number`).
- PHP: backed Enum por default; State Machine string-based con `public const` como fuente única.
- Evaluación de mejoras de stack (gap u oportunidad) consolidada.
- Referencia `22-design-quality` (traits, SOLID operacional, Clean Code).
- Description semántica; evals de aprobación (aplicar vs revisar PROP).
- Terminología neutral; regla ADAPTAR solo en templates.

## 1.0 — 2026-08-05

- Creación del estándar canónico.
- Incorporación del molde frontend y backend.
- Definición de contratos API, forms, dialogs y display.
- Modos Implementar, Auditar, Aplicar y Consultar.
- String enums canónicos y mappings exhaustivos.
- Evals iniciales de activación y calidad.
