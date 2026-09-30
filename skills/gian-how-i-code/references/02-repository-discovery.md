# 02 — Descubrimiento de repositorio

Cargar cuando: cualquier Implementar / Auditar / Aplicar sobre un repo.

## Principio

Antes de inventar wrappers o proponer installs: **contrastar el repo contra el inventario FE/BE esperado**. Ausente o subutilizado → Hallazgo y/o PROP (`19`), no recrear en silencio.

## Checklist Fase 0

1. Raíz monorepo vs app única; apps/packages reales del repositorio.
2. Leer `AGENTS.md` / `CLAUDE.md` / docs de convenciones si existen (contexto; esta skill manda cuando el usuario pide su estándar).
3. Detectar el stack real, no asumir React:
   - package manager (`bun` preferido si está; `uv` en Python si hay `uv.lock`)
   - framework de vista y su versión (React, Vue, Angular o ninguno). Angular también se detecta por `angular.json` o `nx.json`.
   - backend: Laravel (`composer.json`; Spatie QueryBuilder, state machines), Python (`pyproject.toml`, `requirements*.txt`, `uv.lock`) o Node (Nest o Express en `package.json`)
   - tooling del repo: ruff, mypy o pyrefly, pytest, ng/nx
   - i18n del stack
   - tenancy (`stancl/tenancy`, fetchers por scope)
   - router, si aplica — detectar, no imponer
4. **Inventario por capacidad** (marcar presente / ausente / subutilizado). Buscar el equivalente del stack. En React, el adaptador esperado es el de la segunda columna. En otro stack, la ausencia de esa librería no es hallazgo ni PROP de instalarla.

   | Capacidad | Adaptador React | Equivalente / detectar |
   |-----------|-----------------|------------------------|
   | Fechas | `dayjs` + módulo configurado (plugins/locale) | Otro cliente TS: el mismo módulo dayjs. Python: un módulo con datetimes aware (`01`) |
   | HTTP | `apiFetcher` (o equivalente) + `SharedService` | Angular: `HttpClient` + interceptor. Otro stack: el cliente compartido del repo (`14`) |
   | Errores | `CustomError` + `ErrorMapper` | El mapper de errores del cliente (`14`) |
   | Server state | `QueryClient` central + store `queries` / query-key-factory | Vue: el cliente de datos del repo (`25`). Angular: services con RxJS o signals |
   | Forms | RHF + Zod | El form del stack con un schema nombrado (`10`). Python: body model de Pydantic |
   | i18n y clases | i18n + `cn()` | Vue: `vue-i18n`. Angular: `$localize` o ngx-translate (`15`). `class` sin `cn()` |
   | Multipart | `FormDataHelper` en `shared/helpers`, solo si hay uploads | El serializador equivalente, en el service (`23`) |
   | Scope / overlays / realtime | fetchers por scope, drawer store, Echo/Reverb, solo si aplica | Pinia o `provide`/`inject` si ya existen (`12`) |
5. Abrir ≥2 features de referencia en el repo.
6. Clasificar:
   - **Compatible con el estándar** — cliente HTTP compartido (o equivalente), server state con keys centrales si el stack las usa, Form+Container
   - **Variante reconocida** — p. ej. drawers con Zustand store
   - **Legacy para migración** — keys sueltas, ternarios anidados, helpers de display
   - **Patrón desconocido** — documentar y proponer alineación gradual
7. Solo entonces cargar references de dominio.

## Cómo buscar (tooling; no obligatorio)

Preferir, si están disponibles:

| Herramienta | Uso |
|-------------|-----|
| Serena / codegraph | Localizar por símbolo: `ErrorMapper`, `CustomError`, `apiFetcher`, `getQueryClient`, `DateHelper`, `queries` |
| ast-grep | Anti-patrones: `new Date(…)`, `import dayjs from 'dayjs'` (si hay wrapper), `axios.create` fuera de config, `useMutation` con `onSuccess` fijo, `invalidateQueries()` sin filtro, `new FormData(` en dialogs/components |

Si no hay MCP: Grep / lectura manual. **No** fallar la skill por ausencia de tooling.

Ejemplos de intención ast-grep (no ruleset formal):

- `new Date($X)` en TS/TSX de features
- `axios.create($_)` fuera de `config/` / `lib/`
- `import dayjs from 'dayjs'` cuando existe `@/lib/dayjs`

## Evidencia mínima antes de proponer una lib

- `package.json` / `composer.json` / `pyproject.toml` + lockfiles (`uv.lock` incluido)
- Abstracciones existentes (`SharedService`, `CustomTable`, `ErrorMapper`, Query classes, query-key-factory, módulo dayjs)
- No sugerir TanStack Query / Zod / QueryBuilder / dayjs si ya hay equivalente instalado o wrapper local
