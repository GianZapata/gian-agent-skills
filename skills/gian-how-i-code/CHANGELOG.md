# Changelog

## 1.4.13 — 2026-10-01

- Copy visible (`15`, `14`): título, descripción, vacío, error, toast y ayuda le hablan a quien usa el producto. No nombran API, servidor ni piden operarlo. Al tocarlo, se reescribe.

## 1.4.12 — 2026-10-01

- Ayudas de captura (`10`): evaluar es obligatorio; implementar no. Local y asíncrona se separan. Cada ayuda declara solo lo que necesita. La corrección manual gana, y se señala si dejó de ser coherente. El dominio del email puede ir en minúsculas; la parte local es decisión de producto.
- `05`: no se borra una clase solo porque declara constructor. Adaptador si la integración la exige, no solo si hay `new`. `Support` es convención, no Alta automático (`18`).
- Transacción y error (`05`): dueño de la operación, savepoint en la misma conexión, `throw` para revertir, `CustomException` se lanza, reintento de deadlock se conserva hasta agotarlo, idempotencia operable, colisión al guardar, efectos externos por flujo.

## 1.4.11 — 2026-10-01

- Laravel (`05`): antes de crear el archivo se decide el lugar. No se agrega a `Support` porque la carpeta ya existe. Config, modelo, enum, helper estático, adaptador de paquete, método privado o fixture. Prohibida una clase cuyo único miembro es el constructor.

## 1.4.10 — 2026-10-01

- Laravel (`05`): si el repo ya tiene `Support`, no es el molde y una feature nueva no agrega archivos ahí. La forma a copiar es Action `handle`, método privado en la Query, y helper estático en `Helpers`. Prohibido un `readonly` cuyo cuerpo es solo el constructor. No migrar el `Support` existente en silencio.

## 1.4.9 — 2026-10-01

- Laravel (`05`): prohibido `Support` y prohibida una clase cuyo único miembro es el constructor. Un valor o un arreglo va a un método privado del dueño; `private static` si no usa `$this`. Un helper nuevo solo si ese eje se reutiliza o ya existe. Al tocarla, se borra.

## 1.4.8 — 2026-10-01

- Campo de formulario (`10`): la tabla es ejemplo, no el universo. Cualquier campo se trata por lo que representa. Se aplica la normalización sin pérdida; lo que rechaza datos guardados o cambia el contrato se propone. El control sigue a la elección: dos opciones exclusivas son un radio, no cards; muchas opciones usan el autocomplete del repo, o se propone.

## 1.4.7 — 2026-10-01

- Entorno ≠ producto (`01`, `08`, `15`, `17`). `npm run dev` y el test runner no son un modo. Prohibido chip, banner o copy "Test mode" / "Testing mode", y prohibido ramificar validaciones por el runtime. Al tocar ese código, se borra; si el archivo existe solo para anunciarlo, se borra el archivo. Excepción solo si el contrato ya trae el flag y el requisito pide mostrarlo.

## 1.4.6 — 2026-10-01

- Campo de formulario (`10`): el tipo y la validación siguen lo que el campo representa. Se aplica `type`, `inputmode`, `autocomplete` y la normalización sin pérdida. Nombre sin dígitos, rangos y topes que puedan rechazar datos guardados se proponen. La misma regla va en el schema del form y en el borde.
- Campo complejo (`10`, `19`): moneda, decimal por locale, fecha con rangos o zona, hora con intervalos. Se usa el componente del repo. Si no existe, se propone una librería del framework. No se escribe la máscara a mano ni se instala sin OK.

## 1.4.5 — 2026-10-01

- Tests (`17`): siguen al requisito, no al borrado. Si el requisito desaparece, se borran el código y sus tests exclusivos, sin un test de "ya no existe". Si sigue, se conservan o adaptan. Si la eliminación crea una garantía vigente, se prueba esa garantía. La limpieza incluye fixtures, mocks y factories sin uso.

## 1.4.4 — 2026-09-30

- Orden dentro de un composable, hook o componente (`04`): dependencias, estado, derivados, funciones, efectos, ciclo de vida, return. Dependencias y estado van separados.
- El formato visual TypeScript pasa a llamarse `gian-ts-style`. La línea en blanco entre secciones vive ahí.

## 1.4.3 — 2026-09-30

- Auditoría: el reporte vive en `docs/pattern-audit/` de la raíz git del repo auditado. Si esa carpeta no está en el `.gitignore` de esa raíz, se agrega. No se ignora `docs/` entero.

## 1.4.2 — 2026-09-30

- Vue (`25`): si hay computed, handler, `watch` o llamada al service, vive en `composables/useThing.ts`. El script inline solo declara macros, imports y la llamada. El `.vue` no acumula esa lógica.

## 1.4.1 — 2026-09-30

- Vue (`25`): `<script setup lang="ts">` inline en el `.vue`. Sin `src`. Las macros no se mueven a un `.ts`. La lógica extraída va a `composables/useThing.ts`. La extracción pasa a ser obligatoria en 1.4.2.
- Supersede el SFC partido `<script setup lang="ts" src="./Nombre.ts">` de 1.3.0.

## 1.4.0 — 2026-09-30

- Hard rules del núcleo partidas: styling, validación user-facing y contrato de lectura son adaptadores. El schema nombrado es el núcleo; Zod lo es solo en TypeScript.
- `01`: filas de Python sin capítulo (body de Pydantic ≠ path, 422 por campo, `StrEnum`, `in`, datetimes aware, PEP 8 snake_case).
- Equivalentes Angular y Vue: MatDialog, `v-if`, Pinia, HttpClient, tabla de i18n, `defineModel`, `computed` A–E.
- `05` y `06` quedan declarados como adaptadores de Laravel.

## 1.3.2 — 2026-09-30

- `25`: ejemplos genéricos (`EntityPage`, `entityId`, `confirm` / `cancel`). Tailwind solo si el repo lo usa.
- `20`: adaptador (otra tecnología, misma capacidad) distinto de legacy (rompe el núcleo). Alineado con `24` §3.
- `01`: filas de backend sin capítulo nuevo. El DTO sale de un schema nombrado; Zod es ese schema en TypeScript. El nombre de archivo que impone el framework es `LIBRARY_OWNED`.
- `19`: cliente HTTP por capacidad. En Angular, `HttpClient` + interceptor; no pedir axios.
- `13` y la hard rule de mutaciones: el envelope `*Variables` queda en el adaptador de React Query o Vue Query. El DTO sale de un schema nombrado.

## 1.3.1 — 2026-09-30

- El lenguaje no apaga el estándar (`01`). Núcleo (nombres, helpers de área, enums, contratos, errores, display) vale en cualquier stack. Un capítulo de stack solo documenta el adaptador. Lo que el framework impone es `LIBRARY_OWNED`.
- “No aplica” no cierra la responsabilidad: se cumple con el equivalente del stack, en todo modo, no solo en la auditoría de repo (`24` §3).
- Fase 0 y `19` inventarían capacidades. En un repo que no es React, no se propone instalar TanStack Query, RHF ni MUI.
- `20`: solo se sigue una variante de la lista. Un patrón local no reconocido es legacy, no molde.
- `01` #4 y `04` quedan alineados con `08`: metadata del enum en el entity helper; ad-hoc inline.
- `25` es delta. Se quita `formatMoney` como ejemplo. Un archivo por función no es un helper de área.

## 1.3.0 — 2026-09-30

- Vue (`25`): SFC con lógica en `<script setup lang="ts" src="./Nombre.ts">`; `interface Props` / `interface Emits` locales; `composables/` en lugar de `hooks/`. Prohibido `defineComponent` y el genérico anónimo de `defineProps`. Reemplazado en 1.4.1: el script setup va inline, sin `src`.
- El stack React de `04`/`13` no se hereda. Naming sigue en esta skill; el formato del `.ts` hermano sigue en `gian-react-ts-style`.

## 1.2.14 — 2026-09-17

- Mutaciones (`13`): HARD ruta ≠ body. Service `(id, data)` o `(params, data)`; `TVariables` DTO / `{ id, data }` / `{ params, data }` / `EntityId`.
- DTOs (`10`): schema Zod nombrado = body HTTP; prohibido anónimo e IDs de ruta en el schema.
- UI (`09`) no serializa multipart; `FormDataHelper` shared (`23`) solo si el endpoint es multipart (Laravel `null` → `""`).
- Templates de service/mutation/schema + helper/tests. Evals `impl-mutation-route-vs-dto`, `impl-mutation-bind-id-at-hook`, `impl-named-dto-not-anonymous`, `audit-hybrid-mutation-vars`.

## 1.2.13 — 2026-09-15

- Metadata nullable (`07`/`08`/`15`): `getXMeta(Enum | null | undefined)` es el resolver canónico para componentes; `unknownMeta` y `getMeta` son privados.
- Supersede el consumo directo `Helper.statusMeta[status]` de 1.2.12 cuando el valor puede llegar ausente: ahí manda `getXMeta`.
- El `Record<Enum, Meta>` público se conserva para valores garantizados e iteración; los resolvers no aceptan `string`, casts ni fallbacks para ocultar drift.
- `unknownMeta.label` usa getter cuando el copy es dinámico para no congelar el locale.

## 1.2.12 — 2026-09-15

- Metadata de enums (`07`/`08`): un único mapa público `static readonly Record<Enum, Meta>` en el entity helper; no métodos que reconstruyen el Record.
- i18n (`15`): getters de `label` ejecutan `i18n.t()` al leer para que el cambio de locale no deje traducciones congeladas.
- Consumo normal directo `Helper.statusMeta[status]` o spread al componente, sin método, `?.`, `??` ni fallback para enums cerrados.
- Nullable, contratos externos y legacy se validan, normalizan o ramifican por separado sin debilitar el Record canónico.
- Checklists `03`/`23` y evals de implementación/auditoría alineados con exhaustividad, locale dinámico, consumo directo y fronteras desconocidas.

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
