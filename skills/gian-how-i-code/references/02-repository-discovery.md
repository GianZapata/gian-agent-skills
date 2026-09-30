# 02 — Descubrimiento de repositorio

Cargar cuando: cualquier Implementar / Auditar / Aplicar sobre un repo.

## Principio

Antes de inventar wrappers o proponer installs: **contrastar el repo contra el inventario FE/BE esperado**. Ausente o subutilizado → Hallazgo y/o PROP (`19`), no recrear en silencio.

## Checklist Fase 0

1. Raíz monorepo vs app única; apps/packages reales del repositorio.
2. Leer `AGENTS.md` / `CLAUDE.md` / docs de convenciones si existen (contexto; esta skill manda cuando el usuario pide su estándar).
3. Detectar el stack real, no asumir React:
   - package manager (`bun` preferido si está)
   - framework de vista (React, Vue, Angular, ninguno) y su versión
   - Laravel + Spatie QueryBuilder + state machines, si hay backend
   - i18n del stack
   - tenancy (`stancl/tenancy`, fetchers por scope)
   - router, si aplica — detectar, no imponer
4. **Inventario por capacidad** (marcar presente / ausente / subutilizado). Buscar el equivalente del stack. En React, el adaptador esperado es el de la segunda columna. En otro stack, la ausencia de esa librería no es hallazgo ni PROP de instalarla.

   | Capacidad | Adaptador React |
   |-----------|-----------------|
   | Fechas | `dayjs` + módulo configurado (plugins/locale) |
   | HTTP | `apiFetcher` (o equivalente) + `SharedService` |
   | Errores | `CustomError` + `ErrorMapper` |
   | Server state | `QueryClient` central + store `queries` / query-key-factory |
   | Forms | RHF + Zod |
   | i18n y clases | i18n + `cn()` |
   | Multipart | `FormDataHelper` en `shared/helpers`, solo si hay uploads |
   | Scope / overlays / realtime | fetchers por scope, drawer store, Echo/Reverb, solo si aplica |
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

- `package.json` / `composer.json` + lockfiles
- Abstracciones existentes (`SharedService`, `CustomTable`, `ErrorMapper`, Query classes, query-key-factory, módulo dayjs)
- No sugerir TanStack Query / Zod / QueryBuilder / dayjs si ya hay equivalente instalado o wrapper local
