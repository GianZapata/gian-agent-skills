---
name: gian-how-i-code
description: "Estándar oficial de Gian para implementar, auditar, migrar y consultar features. El núcleo vale en cualquier stack. Usar para contratos API, forms, tables, dialogs, SFC Vue, enums y evaluación guiada de mejoras de stack."
license: Apache-2.0
metadata:
  author: gian
  version: "1.3.2"
---

# gian-how-i-code

Estándar oficial, autocontenido y ejecutable de cómo programa Gian. El núcleo vale en cualquier stack; Laravel, React y Vue son adaptadores documentados. Funciona como manual humano y contrato de agente.

## Activation Contract

Usar en toda tarea de desarrollo que el workflow carga: crear, editar, alinear, auditar o migrar features; consultar el estándar; contratos API + molde; forms/tables/dialogs; SFC Vue; evaluar mejoras de stack. No queda opcional por no haber dicho “mi estilo”.

No usar como única skill para: explicación genérica de React/Vue/Angular/Laravel/Node sin aplicar el estándar; infra Docker/CI pura; CV/LinkedIn u otros dominios ajenos.

## Hard Rules

- Idioma de hallazgos, propuestas y reportes: **español**.
- No leer todas las `references/` por defecto; usar la matriz de routing.
- No migrar el repo entero en silencio; solo alcance aprobado.
- No instalar deps ni tocar lockfiles/manifests sin OK explícito.
- Auditoría no modifica código ni manifests.
- El conocimiento vive en esta skill; no depender de skills externas como autoridad, **excepto** formato visual PHP → `gian-php-style` y formato visual TS/TSX → `gian-react-ts-style`.
- El lenguaje no apaga el estándar. Núcleo (nombres, helpers, enums, contratos, errores, display) vale en cualquier stack. Un capítulo de stack solo documenta el adaptador. Ver `01`.
- Vue: SFC con lógica → `<script setup lang="ts" src="./Nombre.ts">`; `defineProps` / `defineEmits` con `interface Props` / `interface Emits` locales. Sin `defineComponent`. `25` es el delta; no reemplaza el núcleo.
- Tests/contratos ejecutables del repo no se rompen para imponer estilo.
- String enum (TS) para conjuntos cerrados; PHP: backed Enum por default, o constantes `public const` en State Machine string-based (`asantibanez`) como fuente única — ver `07`. `Record<Enum, V>` en mappings FE exhaustivos. Membresía 2+: `.includes()` / `in_array(..., true)`, no `=== || ===` — ver `07`.
- Ownership **antes** de declarar `type`/union/enum/mapping: `APP_OWNED` \| `LIBRARY_OWNED` \| `EXTERNAL_GENERATED` \| `UNION LEGÍTIMA` — ver `07`.
- `APP_OWNED` cerrado y nombrado (incl. modos/estados de UI de feature) → string enum por default. `LIBRARY_OWNED` → tipo oficial de la lib; no shadow types.
- Memoización React según `23` (A–E): no ceremonial (A); STYLE_GIAN multi-rama (C) y MRT/`11` (E) sí.
- Styling FE: Tailwind-first cuando existe una utility o un token bridge real equivalente; `cn()` cuando las clases se componen o varían por estado/props runtime; no constantes locales `*_SX` / `get*Sx`; `sx={(theme) => ({ … theme.palette })}` queda como escape hatch sin equivalencia limpia; `useTheme()` solo si el theme sale de `sx` — ver `04`/`23`.
- Comentarios `ADAPTAR` solo en templates de `assets/`; eliminarlos al materializar código productivo. Template-only `ADAPTAR` MUST resolverse o quitarse al instanciar; MUST NOT sobrevivir en código de producto.
- Validación user-facing: no dar por terminado un FormRequest solo con `rules()`; revisar `messages()` y, si hace falta, `attributes()`; copy de dominio; cobertura semántica regla→mensaje; 422→campos en la UI existente — ver `05`/`10`/`14`.
- Display FE: metadata exhaustiva en una propiedad pública `static readonly Record<Enum, Meta>` de `<entity>.helper.ts`; getter de `label` con `i18n.t()` para resolver el locale al leer; `getXMeta(Enum | null | undefined)` como API preferida cuando el consumidor puede recibir ausencia, con `unknownMeta` y resolver privados. El acceso directo al Record queda para enums garantizados o iteración. No ampliar a `string`, usar casts ni fallbacks para ocultar drift. If-chain ad-hoc en el componente con `t()`. Prohibido `*.display.config.ts`, inyectar `TFunction`, `labelKey` diferido — ver `07`/`08`/`15`.
- Resource: `new XResource($this->whenLoaded('rel'))` / `::collection($this->whenLoaded('rels'))`; no callback `fn() => new X($this->rel)` salvo lógica extra — ver `06`.
- Mutaciones: IDs de ruta nunca se mezclan con el DTO del body. 1 ID: `(id, data: TDto)`; 2+: `(params, data: TDto)`. El DTO sale de un schema nombrado; en TypeScript ese schema es Zod. El envelope `*Variables` es del adaptador React Query o Vue Query (`13`). UI no arma FormData — ver `13`/`10`/`23`.

## Autoridad y precedencia

1. Instrucción explícita del usuario en el hilo.
2. Contratos ejecutables del repo (tests, tipos, schemas, HTTP, migraciones, versiones).
3. Esta skill como estándar objetivo en toda tarea de desarrollo que el workflow carga. No solo cuando el usuario dice “mi estilo”.
4. Convenciones locales del repo (contexto; divergencias = hallazgos).
5. Buenas prácticas genéricas solo como Propuesta.

El molde canónico define la estructura objetivo FE/BE. Multi-tenant solo si aplica.

## Modos

| Modo | Señales | Edita código |
|------|---------|--------------|
| Implementar | crear feature, seguí mi estilo | Sí (alcance nuevo) |
| Auditar (feature) | audita esta feature / este módulo | No |
| Auditar (repositorio completo) | audita todo / el proyecto / el repo / full audit | No |
| Auditar + aplicar | audita y migra / aplica H-00x | Sí (lotes aprobados) |
| Consultar estándar | ¿cómo suelo…?, ¿enum o union? | No |

Alcance **repositorio completo** → protocolo `24` (coverage ledger + gate). Prohibido muestreo como cierre.
## Decision Gates

| Situación | Acción |
|-----------|--------|
| Toca repo | Fase 0 discovery → clasificar → cargar references |
| Repo Vue, Angular, Node u otro stack | Núcleo (`01`) + el delta del stack si existe (`25` en Vue). No heredar la API React/MUI que el repo no usa. No saltarse nombres, helpers, enums ni contratos |
| Gap u oportunidad de mejorar stack, tipado, linting o abstracción | Aplicar **Evaluación de mejoras de stack** (`19`); comparar solución actual, mejora interna y librería externa; no instalar sin aprobación |
| Divergencia vs molde | Hallazgo en `18-migrate-audit.md` |
| Hook custom o archivo `use-*` / `use_*` | `04` Naming: camelCase `useX`; rename en alcance; no barrels `<entity>.queries.ts` |
| Variante con store de UI / drawers / fetchers por scope | `20-variants.md` + `09` |
| Tenancy central/tenant | `16-multi-tenant.md` |
| Solo pregunta de estándar | Modo Consultar; citar `references/…` |

## Execution Steps

### Fase 0 — Descubrimiento (antes de diseñar/auditar/editar)

1. Identificar raíz y alcance del repo.
2. Leer AGENTS.md / docs locales relevantes (contexto).
3. Detectar framework, versiones, package manager, deps, estructura, patrones equivalentes, comandos de validación.
4. **Inventario por capacidad** (`02`): fechas, HTTP, errores, server state, forms, i18n. En React, contrastar con QueryClient, RHF y `cn()`. En otro stack, buscar el equivalente; no marcar “ausente” la librería React ni proponer instalarla.
5. Ejemplos de feature:
   - **Implementar** o **Auditar feature:** ≥2 features de referencia equivalentes.
   - **Auditar repositorio completo:** inventario total de features/archivos (`24`) — **no** bastan 2 ejemplos como cierre.
6. Clasificar: Compatible con el estándar | Variante reconocida | Legacy para migración | Patrón desconocido.
7. Cargar solo references necesarias (matriz abajo).

### Por modo

**Implementar:** aplicar molde en alcance nuevo; reportar bloqueos; checklist `03`/`05`/`17`; Evaluación de mejoras de stack si hay evidencia.  
**Auditar (feature):** escanear vs molde; un solo `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` (ES); Hallazgos / Propuestas.  
**Auditar (repositorio completo):** `18` + **`24`** (inventario, barridos, gate, disposición); mismo path de reporte; ledger auxiliar solo si hace falta; sin “alineado” sin gate.  
**Auditar + aplicar:** igual + checklist/registro **en el mismo archivo**; solo ítems aprobados; sin installs no aprobados.  
**Consultar:** responder desde references; distinguir Regla / Default / Variante / Excepción / Propuesta; citar ruta.

## Routing de references

| Situación | Leer |
|-----------|------|
| Arranque / índice humano | `00-index`, `01-principles` |
| Toca repo | `02-repository-discovery` (inventario + tooling) |
| Feature FE | `03-feature-mold`, `04-frontend-architecture`, `13-data-fetching`, `23-ts-style-helpers` |
| Repo Vue / `.vue` / script hermano | Núcleo (`01`, `03`, `04` Naming, `07`, `08`, `14`, `23`) + `25-vue-sfc` |
| Otro stack sin capítulo | Núcleo (`01`). El adaptador es la API del framework; no saltar el núcleo |
| Styling MUI/Tailwind / `sx` / `cn()` | `04-frontend-architecture`, `23-ts-style-helpers` |
| Display / labels / estados UI | `07-types-enums-statuses`, `08-display-conventions`, `15-i18n-copy` |
| Ownership / enum vs union / shadow MUI / membresía includes | `07-types-enums-statuses` |
| cn / dayjs / utils vs helpers / memoización | `23-ts-style-helpers` |
| Memoización React (`useMemo` / `useCallback` / `memo`) | `23-ts-style-helpers` (A–E) |
| Formato visual TS/TSX (arrows, braces, JSX) | **no esta skill** — cargar `gian-react-ts-style` |
| Modal / drawer | `09-dialogs-drawers` |
| Forms / RHF / Zod | `10-forms-validation` |
| Mutations / ruta vs DTO / multipart | `13-data-fetching`, `10-forms-validation`, `23-ts-style-helpers` |
| Validación user-facing / FormRequest `messages` / 422 por campo | `05-backend-mold`, `10-forms-validation`, `14-errors-feedback` |
| Tablas / filtros | `11-tables-filters` |
| State UI (Zustand etc.) | `12-state-management` |
| Laravel Action/Query/Resource/Request | `05-backend-mold`, `06-api-contracts` |
| Joins / Query Builder / SQL table aliases | `05-backend-mold` (t1/t2, st1 por nivel) |
| Formato visual PHP (indent, braces, guards, arrays) | **no esta skill** — cargar `gian-php-style` |
| Contratos HTTP / envelopes / whenLoaded Resource | `06-api-contracts` |
| Errores / toasts / apiFetcher | `14-errors-feedback` |
| i18n / copy / `t()` vs `i18n.t()` | `15-i18n-copy`, `08-display-conventions`, `10-forms-validation` |
| Central/tenant | `16-multi-tenant` |
| Validación comandos | `17-testing-validation` |
| Auditar / migrar (feature) | `18-migrate-audit`, `21-output-contracts` |
| Auditar repositorio completo | `18-migrate-audit`, `24-full-repo-audit`, `21-output-contracts`, `02`, `19` |
| Gap u mejora de stack | `19-propuestas-stack` |
| Repo con patrón dominante distinto del default | `20-variants` |
| Calidad de diseño / traits / límites / refactor cohesión | `22-design-quality` |

## Output Contract

- Implementar: archivos tocados + checklist + propuestas pendientes.
- Auditar (feature): un solo `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` (Hallazgos + Propuestas).  
- Auditar (repo completo): igual + gate/cobertura `24`; sin muestreo; sin “alineado” prematuro.  
- Aplicar: actualizar el mismo archivo (checklist + registro) + validación del repo.  
- Consultar: respuesta con cita `references/<file>.md` §sección.

## References
Ver `references/00-index.md`. Templates en `assets/`. Evals en `evals/`.
