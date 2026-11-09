# 02 — Descubrimiento de repositorio

Cargar cuando: cualquier Implementar / Auditar / Aplicar sobre un repo.

## Principio

Antes de inventar wrappers o proponer installs: **contrastar el repo contra el inventario FE/BE esperado**. No se recrea en silencio:

- **Ausente** → hallazgo y PROP (`19`).
- **Subutilizado** → hallazgo con `archivo:línea` del uso que lo esquiva.

## Checklist Fase 0

1. Raíz monorepo vs app única; apps/packages reales del repositorio.
2. Leer `AGENTS.md` / `CLAUDE.md` / docs de convenciones si existen. Son contexto. Esta skill manda en toda tarea de desarrollo que el workflow carga (SKILL.md §Autoridad). Sus divergencias son hallazgos.
3. Detectar el stack real, no asumir React:
   - package manager: el del lockfile presente (`bun.lock` / `bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm, `yarn.lock` → yarn, `uv.lock` → uv). Nunca cambiar de manager. Lo instalado en la máquina no cuenta.
   - framework de vista y su versión (React, Vue, Angular o ninguno). Angular también se detecta por `angular.json` o `nx.json`.
   - backend: Laravel (`composer.json`; Spatie QueryBuilder, state machines), Python (`pyproject.toml`, `requirements*.txt`, `uv.lock`) o Node (Nest o Express en `package.json`)
   - tooling del repo: ruff, mypy o pyrefly, pytest, ng/nx
   - i18n del stack
   - tenancy (`stancl/tenancy`, fetchers por scope)
   - router: detectar el del repo, no imponer uno
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
   | Scope / overlays / realtime | fetchers por scope, drawer store, Echo/Reverb, solo si el repo los usa | Pinia o `provide`/`inject` si ya existen (`12`) |
5. Abrir ≥2 features de referencia en el repo. Si hay menos de 2 equivalentes, usar los templates de `assets/` como segunda referencia y declararlo en el reporte.
6. Clasificar:
   - **Compatible con el estándar** — cliente HTTP compartido (o equivalente), server state con keys centrales si el stack las usa, Form+Container
   - **Variante reconocida** — p. ej. drawers con Zustand store
   - **Legacy para migración** — keys sueltas, ternarios anidados, helpers de display
   - **Patrón desconocido** — hallazgo con `archivo:línea`, regla de núcleo afectada y PROP de migración por lotes (`20`)
7. Solo entonces cargar references de dominio.

## Barrido de anti-patrones (obligatorio)

El barrido MUST ejecutarse siempre en Fase 0. La herramienta es opcional; el barrido no.

- Con ast-grep si está instalado. Si no, con `rg`.
- No instalar tooling para hacerlo. No fallar la skill por ausencia de tooling.

Patrones mínimos:

| Patrón | Dónde es hallazgo |
|--------|-------------------|
| `new Date(` | TS/TSX de features |
| `import dayjs from 'dayjs'` | Fuera del módulo dayjs del repo (p. ej. `@/lib/dayjs`) |
| `axios.create(` | Fuera de `config/` / `lib/` |
| `useMutation` con `onSuccess` fijo en el hook | `hooks/*.mutations.ts` |
| `invalidateQueries()` sin filtro | Cualquier archivo |
| `new FormData(` | Dialogs y componentes |

Cada coincidencia fuera de su lugar permitido es hallazgo con `archivo:línea`.

Para localizar símbolos (`ErrorMapper`, `CustomError`, `apiFetcher`, `getQueryClient`, `DateHelper`, `queries`): Serena o CodeGraph si existen; si no, `rg` o lectura directa.

## Evidencia mínima antes de proponer una lib

- `package.json` / `composer.json` / `pyproject.toml` + lockfiles (`uv.lock` incluido)
- Abstracciones existentes (`SharedService`, `CustomTable`, `ErrorMapper`, Query classes, query-key-factory, módulo dayjs)
- No sugerir TanStack Query / Zod / QueryBuilder / dayjs si ya hay equivalente instalado o wrapper local
